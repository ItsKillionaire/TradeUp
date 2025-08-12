import React, { useEffect } from 'react';
import axios from 'axios';
import { Typography, Box, Grid, Paper } from '@mui/material';

import Controls from './Controls';
import { useStore } from './store';
import AccountInfo from './AccountInfo';
import Logs from './Logs';
import TradeHistory from './TradeHistory';
import OpenPositions from './OpenPositions';
import RecentOrders from './RecentOrders';
import MarketStatus from './MarketStatus';
import AITrader from './AITrader';
import Backtester from './Backtester';
import packageJson from '../package.json';

const Dashboard: React.FC = () => {
    const {
        setAccount,
        addMessage,
        setTrades,
        addTrade,
        setPositions,
        setOrders,
        setMarketStatus,
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
        const ws = new WebSocket(`ws://localhost:8000/ws`);

        ws.onopen = () => {
            axios.get('/api/account')
                .then((response: any) => {
                    setAccount(response.data._raw);
                    setLoadingAccount(false);
                })
                .catch((error: any) => {
                    console.error('Error fetching account data:', error);
                    setErrorAccount('Failed to fetch account data.');
                    setLoadingAccount(false);
                });

            axios.get('/api/trades')
                .then((response: any) => {
                    setTrades(response.data);
                    setLoadingTrades(false);
                })
                .catch((error: any) => {
                    console.error('Error fetching trades data:', error);
                    setErrorTrades('Failed to fetch trades data.');
                    setLoadingTrades(false);
                });

            axios.get('/api/positions')
                .then((response: any) => {
                    setPositions(response.data);
                    setLoadingPositions(false);
                })
                .catch((error: any) => {
                    console.error('Error fetching positions data:', error);
                    setErrorPositions('Failed to fetch positions data.');
                    setLoadingPositions(false);
                });

            axios.get('/api/orders')
                .then((response: any) => {
                    setOrders(response.data);
                    setLoadingOrders(false);
                })
                .catch((error: any) => {
                    console.error('Error fetching orders data:', error);
                    setErrorOrders('Failed to fetch orders data.');
                    setLoadingOrders(false);
                });
        };

        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                if (data.type === 'account_update') {
                    setAccount(data.data._raw);
                } else if (data.type === 'positions_update') {
                    setPositions(data.data);
                } else if (data.type === 'orders_update') {
                    setOrders(data.data);
                } else if (data.type === 'trades_update') {
                    addTrade(data.data);
                } else if (data.type === 'market_status_update') {
                    setMarketStatus(data.data);
                } else if (data.type === 'chat' || data.type === 'log' || data.type === 'error') {
                    addMessage(data.message);
                } else {
                    addMessage(JSON.stringify(data));
                }
            } catch (error) {
                console.log("Raw WebSocket data:", event.data);
                addMessage(event.data);
            }
        };

        return () => {
            ws.close();
        };
    }, [setAccount, addMessage, setTrades, setLoadingAccount, setErrorAccount, setLoadingTrades, setErrorTrades, setPositions, setOrders, setLoadingPositions, setErrorPositions, setLoadingOrders, setErrorOrders]);

    return (
        <Box sx={{ flexGrow: 1, p: 3 }}>
            <Typography variant="h4" gutterBottom sx={{
                mb: 4,
                background: 'linear-gradient(45deg, #FE6B8B 30%, #FF8E53 90%)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                animation: 'fadeIn 2s ease-in-out',
                '@keyframes fadeIn': {
                    '0%': {
                        opacity: 0,
                        transform: 'translateY(-20px)'
                    },
                    '100%': {
                        opacity: 1,
                        transform: 'translateY(0)'
                    }
                }
            }}>
                TradeUp
            </Typography>
            <Grid container spacing={3}>
                <Grid item xs={12}>
                    <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
                        <MarketStatus />
                    </Paper>
                </Grid>
                <Grid item xs={12}>
                    <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
                        <AccountInfo />
                    </Paper>
                </Grid>
                <Grid item xs={12}>
                    <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
                        <Controls />
                    </Paper>
                </Grid>
                <Grid item xs={12} md={8}>
                    <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: '100%' }}>
                        <OpenPositions />
                    </Paper>
                </Grid>
                <Grid item xs={12} md={4}>
                    <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: '100%' }}>
                        <Logs />
                    </Paper>
                </Grid>
                <Grid item xs={12}>
                    <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
                        <RecentOrders />
                    </Paper>
                </Grid>
                <Grid item xs={12}>
                    <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
                        <TradeHistory />
                    </Paper>
                </Grid>
                <Grid item xs={12}>
                    <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
                        <AITrader />
                    </Paper>
                </Grid>
                <Grid item xs={12}>
                    <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
                        <Backtester />
                    </Paper>
                </Grid>
            </Grid>
            <Box sx={{ pt: 4, textAlign: 'center', color: 'text.secondary' }}>
                <Typography variant="body2">
                    Version: {packageJson.version}
                </Typography>
            </Box>
        </Box>
    );
};

export default Dashboard;