import React, { useState, useEffect } from 'react';
import { useStore, fetchMarketStatus } from './store';

const MarketStatus: React.FC = () => {
  const { marketStatus, loadingMarketStatus, errorMarketStatus } = useStore();
  const [countdown, setCountdown] = useState<string>('');

  useEffect(() => {
    fetchMarketStatus();
  }, []);

  useEffect(() => {
    if (!marketStatus) return;

    const calculateCountdown = () => {
      const targetTime = new Date(marketStatus.is_open ? marketStatus.next_close : marketStatus.next_open).getTime();
      const now = new Date().getTime();
      const distance = targetTime - now;

      if (distance < 0) {
        setCountdown('Now');
        return;
      }

      const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((distance % (1000 * 60)) / 1000);

      setCountdown(`${hours}h ${minutes}m ${seconds}s`);
    };

    const interval = setInterval(calculateCountdown, 1000);
    return () => clearInterval(interval);
  }, [marketStatus]);

  if (loadingMarketStatus) {
    return <div>Loading market status...</div>;
  }

  if (errorMarketStatus) {
    return <div>Error: {errorMarketStatus}</div>;
  }

  if (!marketStatus) {
    return <div>No market status available.</div>;
  }

  return (
    <div>
      <h2>Market Status</h2>
      <p>Status: {marketStatus.is_open ? 'Open' : 'Closed'}</p>
      <p>{marketStatus.is_open ? 'Closes in' : 'Opens in'}: {countdown}</p>
    </div>
  );
};

export default MarketStatus;
