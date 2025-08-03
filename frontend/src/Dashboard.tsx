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

const Dashboard: React.FC = () => {
    const {
        setAccount,
        addMessage,
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

        const ws = new WebSocket(`ws://localhost:8000/ws`);
        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                if (data.type === 'account_update') {
                    setAccount(data.data._raw);
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
            <Typography variant="h4" gutterBottom sx={{ mb: 4 }}>
                Alpaca Trading Bot
            </Typography>
            <Grid container spacing={3}>
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
                <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
                        <Logs />
                    </Paper>
                </Grid>
                <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
                        <TradeHistory />
                    </Paper>
                </Grid>
                <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
                        <OpenPositions />
                    </Paper>
                </Grid>
                <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
                        <RecentOrders />
                    </Paper>
                </Grid>
            </Grid>
        </Box>
    );
};

export default Dashboard;