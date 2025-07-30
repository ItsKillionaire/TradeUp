import React, { useState, useEffect } from 'react';
import { Button, TextField, Select, MenuItem, FormControl, InputLabel, Box, Typography, Grid } from '@mui/material';
import axios from 'axios';

const Controls: React.FC = () => {
    const [symbol, setSymbol] = useState('SPY');
    const [strategy, setStrategy] = useState('');
    const [botStatus, setBotStatus] = useState('idle');
    const [availableStrategies, setAvailableStrategies] = useState<string[]>([]);

    useEffect(() => {
        axios.get('/api/strategy/available')
            .then(response => {
                setAvailableStrategies(response.data.strategies);
                if (response.data.strategies.length > 0) {
                    setStrategy(response.data.strategies[0]);
                }
            })
            .catch(error => {
                console.error('Error fetching available strategies:', error);
            });
    }, []);

    const handleStart = () => {
        axios.post(`/api/strategy/start/${strategy}/${symbol}`)
            .then(response => {
                console.log(response.data.message);
                setBotStatus('online');
            })
            .catch(error => {
                console.error('Error starting strategy:', error);
            });
    };

    const handleStop = () => {
        axios.post(`/api/strategy/stop/${strategy}/${symbol}`)
            .then(response => {
                console.log(response.data.message);
                setBotStatus('offline');
            })
            .catch(error => {
                console.error('Error stopping strategy:', error);
            });
    };

    return (
        <Box sx={{ flexGrow: 1 }}>
            <Typography variant="h6" gutterBottom>Controls</Typography>
            <Grid container spacing={2} alignItems="center">
                <Grid item xs={12} sm={6} md={3}>
                    <TextField
                        label="Symbol"
                        variant="outlined"
                        value={symbol}
                        onChange={(e) => setSymbol(e.target.value)}
                        fullWidth
                    />
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                    <FormControl variant="outlined" fullWidth>
                        <InputLabel>Strategy</InputLabel>
                        <Select
                            value={strategy}
                            onChange={(e) => setStrategy(e.target.value as string)}
                            label="Strategy"
                        >
                            {availableStrategies.map((strat) => (
                                <MenuItem key={strat} value={strat}>{strat}</MenuItem>
                            ))}
                        </Select>
                    </FormControl>
                </Grid>
                <Grid item xs={12} sm={6} md={2}>
                    <Button variant="contained" color="primary" onClick={handleStart} disabled={botStatus === 'online'} fullWidth>
                        Start Bot
                    </Button>
                </Grid>
                <Grid item xs={12} sm={6} md={2}>
                    <Button variant="contained" color="secondary" onClick={handleStop} disabled={botStatus !== 'online'} fullWidth>
                        Stop Bot
                    </Button>
                </Grid>
                <Grid item xs={12} sm={12} md={2}>
                    <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
                        <Box sx={{ width: 10, height: 10, borderRadius: '50%', bgcolor: botStatus === 'online' ? 'success.main' : botStatus === 'offline' ? 'error.main' : 'grey.500', mr: 1 }} />
                        <Typography variant="subtitle1">{botStatus}</Typography>
                    </Box>
                </Grid>
            </Grid>
        </Box>
    );
};

export default Controls;
