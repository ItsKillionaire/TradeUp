import React from 'react';
import { Typography, Box, CircularProgress, Grid, Paper } from '@mui/material';
import {
  AccountBalanceWallet,
  BarChart,
  Power,
  TrendingUp,
  TrendingDown,
} from '@mui/icons-material';
import { useStore } from './store';

const AccountInfo: React.FC = () => {
  const { account, loadingAccount, errorAccount } = useStore();

  if (loadingAccount) {
    return <CircularProgress />;
  }

  if (errorAccount) {
    return <Typography color="error">{errorAccount}</Typography>;
  }

  if (!account) {
    return null;
  }

  const dailyChange =
    parseFloat(account.equity) - parseFloat(account.last_equity);
  const isProfit = dailyChange >= 0;

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Typography variant="h6" gutterBottom>
        Account Overview
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <Paper elevation={3} sx={{ p: 2, height: '100%' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
              <AccountBalanceWallet sx={{ mr: 1, color: 'primary.main' }} />
              <Typography variant="subtitle1">Portfolio Value</Typography>
            </Box>
            <Typography variant="h5">
              $
              {parseFloat(account.portfolio_value).toLocaleString('en-US', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2,
              })}
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper elevation={3} sx={{ p: 2, height: '100%' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
              <BarChart sx={{ mr: 1, color: 'primary.main' }} />
              <Typography variant="subtitle1">Buying Power</Typography>
            </Box>
            <Typography variant="h5">
              $
              {parseFloat(account.buying_power).toLocaleString('en-US', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2,
              })}
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper elevation={3} sx={{ p: 2, height: '100%' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
              {isProfit ? (
                <TrendingUp sx={{ mr: 1, color: 'success.main' }} />
              ) : (
                <TrendingDown sx={{ mr: 1, color: 'error.main' }} />
              )}
              <Typography variant="subtitle1">Today's P/L</Typography>
            </Box>
            <Typography
              variant="h5"
              color={isProfit ? 'success.main' : 'error.main'}
            >
              $
              {dailyChange.toLocaleString('en-US', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2,
              })}
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper elevation={3} sx={{ p: 2, height: '100%' }}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
              <Power
                sx={{
                  mr: 1,
                  color:
                    account.status === 'ACTIVE' ? 'success.main' : 'error.main',
                }}
              />
              <Typography variant="subtitle1">Status</Typography>
            </Box>
            <Typography variant="h5">{account.status}</Typography>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default AccountInfo;
