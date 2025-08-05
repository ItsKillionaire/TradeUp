import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Typography, Box, Paper } from '@mui/material';
import { styled } from '@mui/material/styles';

const StatusIndicator = styled(Box)<{ open: boolean }>(({ theme, open }) => ({
  width: 20,
  height: 20,
  borderRadius: '50%',
  backgroundColor: open ? theme.palette.success.main : theme.palette.error.main,
  boxShadow: `0 0 10px ${open ? theme.palette.success.main : theme.palette.error.main}`,
  marginRight: theme.spacing(2),
}));

const MarketStatus: React.FC = () => {
  const [marketStatus, setMarketStatus] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    axios.get('/api/market/status')
      .then(response => {
        setMarketStatus(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching market status:', error);
        setError('Failed to fetch market status.');
        setLoading(false);
      });
  }, []);

  const renderStatus = () => {
    if (loading) {
      return <Typography>Loading market status...</Typography>;
    }

    if (error) {
      return <Typography color="error">{error}</Typography>;
    }

    if (marketStatus) {
      const nextEventTime = marketStatus.is_open ? marketStatus.next_close : marketStatus.next_open;
      const nextEventLabel = marketStatus.is_open ? 'closes' : 'opens';
      
      return (
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <StatusIndicator open={marketStatus.is_open} />
          <Box>
            <Typography variant="h6">
              Market is {marketStatus.is_open ? 'Open' : 'Closed'}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Next market event: {nextEventLabel} at {new Date(nextEventTime).toLocaleString()}
            </Typography>
          </Box>
        </Box>
      );
    }

    return null;
  };

  return (
    <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
      {renderStatus()}
    </Paper>
  );
};

export default MarketStatus;