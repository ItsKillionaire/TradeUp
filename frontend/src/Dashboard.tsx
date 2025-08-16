import React, { useEffect } from 'react';
import { Typography, Box, Grid, Paper, styled } from '@mui/material';

import Controls from './Controls';
import { useStore, apiClient } from './store';
import AccountInfo from './AccountInfo';
import Logs from './Logs';
import TradeHistory from './TradeHistory';
import OpenPositions from './OpenPositions';
import RecentOrders from './RecentOrders';
import MarketStatus from './MarketStatus';
import AITrader from './AITrader';
import Backtester from './Backtester';
import packageJson from '../package.json';

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  display: 'flex',
  flexDirection: 'column',
  height: '100%',
  boxShadow: theme.shadows[3],
}));

const Dashboard: React.FC = () => {
  const {
    setAccount,
    setTrades,
    setPositions,
    setOrders,
    setLoadingAccount,
    setErrorAccount,
    setLoadingTrades,
    setErrorTrades,
    setLoadingPositions,
    setErrorPositions,
    setLoadingOrders,
    setErrorOrders,
  } = useStore();

  useEffect(() => {
    const fetchAccountData = async () => {
      setLoadingAccount(true);
      try {
        const response = await apiClient.get('/account');
        setAccount(response.data);
      } catch (error) {
        setErrorAccount('Failed to fetch account information.');
      } finally {
        setLoadingAccount(false);
      }
    };

    const fetchPositionsData = async () => {
      setLoadingPositions(true);
      try {
        const response = await apiClient.get('/positions');
        setPositions(response.data);
      } catch (error) {
        setErrorPositions('Failed to fetch positions.');
      } finally {
        setLoadingPositions(false);
      }
    };

    const fetchOrdersData = async () => {
      setLoadingOrders(true);
      try {
        const response = await apiClient.get('/orders');
        setOrders(response.data);
      } catch (error) {
        setErrorOrders('Failed to fetch orders.');
      } finally {
        setLoadingOrders(false);
      }
    };

    const fetchTradesData = async () => {
      setLoadingTrades(true);
      try {
        const response = await apiClient.get('/trades');
        setTrades(response.data);
      } catch (error) {
        setErrorTrades('Failed to fetch trade history.');
      } finally {
        setLoadingTrades(false);
      }
    };

    fetchAccountData();
    fetchPositionsData();
    fetchOrdersData();
    fetchTradesData();
  }, [
    setAccount,
    setLoadingAccount,
    setErrorAccount,
    setPositions,
    setLoadingPositions,
    setErrorPositions,
    setOrders,
    setLoadingOrders,
    setErrorOrders,
    setTrades,
    setLoadingTrades,
    setErrorTrades,
  ]);

  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      <Typography
        variant="h4"
        gutterBottom
        sx={{
          mb: 4,
          background: 'linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          animation: 'fadeIn 2s ease-in-out',
          '@keyframes fadeIn': {
            '0%': {
              opacity: 0,
              transform: 'translateY(-20px)',
            },
            '100%': {
              opacity: 1,
              transform: 'translateY(0)',
            },
          },
        }}
      >
        TradeUp
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <StyledPaper>
            <MarketStatus />
          </StyledPaper>
        </Grid>
        <Grid item xs={12}>
          <StyledPaper>
            <AccountInfo />
          </StyledPaper>
        </Grid>
        <Grid item xs={12}>
          <StyledPaper>
            <Controls />
          </StyledPaper>
        </Grid>
        <Grid item xs={12} md={8}>
          <StyledPaper>
            <OpenPositions />
          </StyledPaper>
        </Grid>
        <Grid item xs={12} md={4}>
          <StyledPaper>
            <Logs />
          </StyledPaper>
        </Grid>
        <Grid item xs={12}>
          <StyledPaper>
            <RecentOrders />
          </StyledPaper>
        </Grid>
        <Grid item xs={12}>
          <StyledPaper>
            <TradeHistory />
          </StyledPaper>
        </Grid>
        <Grid item xs={12}>
          <StyledPaper>
            <AITrader />
          </StyledPaper>
        </Grid>
        <Grid item xs={12}>
          <StyledPaper>
            <Backtester />
          </StyledPaper>
        </Grid>
      </Grid>
      <Box sx={{ pt: 4, textAlign: 'center', color: 'text.secondary' }}>
        <Typography variant="body2">Version: {packageJson.version}</Typography>
      </Box>
    </Box>
  );
};

export default Dashboard;
