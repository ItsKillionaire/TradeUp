import React, { useEffect } from 'react';
import axios from 'axios';
import { Typography, Box, Grid } from '@mui/material';

import Controls from './Controls';
import { useStore } from './store';
import AccountInfo from './AccountInfo';
import Logs from './Logs';
import TradeHistory from './TradeHistory';

const Dashboard: React.FC = () => {
    const {
        setAccount,
        addMessage,
        setTrades,
        setLoadingAccount,
        setErrorAccount,
        setLoadingTrades,
        setErrorTrades,
    } = useStore();

    useEffect(() => {
        axios.get('/api/account')
            .then(response => {
                setAccount(response.data._raw);
                setLoadingAccount(false);
            })
            .catch(error => {
                console.error('Error fetching account data:', error);
                setErrorAccount('Failed to fetch account data.');
                setLoadingAccount(false);
            });

        axios.get('/api/trades')
            .then(response => {
                setTrades(response.data);
                setLoadingTrades(false);
            })
            .catch(error => {
                console.error('Error fetching trades data:', error);
                setErrorTrades('Failed to fetch trades data.');
                setLoadingTrades(false);
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
    }, [setAccount, addMessage, setTrades, setLoadingAccount, setErrorAccount, setLoadingTrades, setErrorTrades]);

    return (
        <Box sx={{ flexGrow: 1, p: 3 }}>
            <Typography variant="h4" gutterBottom>
                Dashboard
            </Typography>
            <Controls />
            <AccountInfo />
            <Grid container spacing={3} sx={{ mt: 2 }}>
                <Grid xs={12} md={6}>
                    <Logs />
                </Grid>
                <Grid xs={12} md={6}>
                    <TradeHistory />
                </Grid>
            </Grid>
        </Box>
    );
};

export default Dashboard;