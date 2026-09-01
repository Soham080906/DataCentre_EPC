'use client';

import { useState, useEffect, useCallback } from 'react';
import { HealthResponse } from '@/types';
import { fetchHealth } from '@/lib/api';

export function useHealth() {
  const [data, setData] = useState<HealthResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [latencyMs, setLatencyMs] = useState<number | null>(null);
  const [lastChecked, setLastChecked] = useState<Date | null>(null);

  const checkHealth = useCallback(async () => {
    setIsLoading(true);
    const start = performance.now();
    try {
      const response = await fetchHealth();
      const end = performance.now();
      setLatencyMs(Math.round(end - start));
      setData(response);
      setError(null);
      setLastChecked(new Date());
    } catch (err: any) {
      const end = performance.now();
      setLatencyMs(Math.round(end - start));
      setError(err?.response?.data?.message || err?.message || 'Failed to connect to backend server');
      setData(null);
      setLastChecked(new Date());
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    checkHealth();
    const interval = setInterval(checkHealth, 15000);
    return () => clearInterval(interval);
  }, [checkHealth]);

  return {
    data,
    isLoading,
    error,
    latencyMs,
    lastChecked,
    refresh: checkHealth,
  };
}
