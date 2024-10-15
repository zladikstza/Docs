/**
 * main - React Component
 */

import React, { useState, useEffect, useCallback, useMemo } from 'react';
import PropTypes from 'prop-types';
import './main.css';

const useApi = (url, options = {}) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        },
        ...options
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${await response.text()}`);
      }

      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err.message);
      console.error('API Error:', err);
    } finally {
      setLoading(false);
    }
  }, [url, JSON.stringify(options)]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
};

const Component = ({ initialCount = 0, onCountChange, className = '' }) => {
  const [count, setCount] = useState(initialCount);
  const [items, setItems] = useState([]);
  const { data: apiData, loading, error } = useApi('https://api.example.com/data');

  const increment = useCallback(() => {
    const newCount = count + 1;
    setCount(newCount);
    onCountChange?.(newCount);
  }, [count, onCountChange]);

  const decrement = useCallback(() => {
    const newCount = Math.max(0, count - 1);
    setCount(newCount);
    onCountChange?.(newCount);
  }, [count, onCountChange]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className={className}>
      <h2>main</h2>
      <div>
        <button onClick={decrement}>-</button>
        <span>{count}</span>
        <button onClick={increment}>+</button>
      </div>
    </div>
  );
};

Component.propTypes = {
  initialCount: PropTypes.number,
  onCountChange: PropTypes.func,
  className: PropTypes.string
};

export default Component;
