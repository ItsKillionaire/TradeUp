import React, { useState, useEffect } from 'react';
import { Button, TextField, Select, MenuItem, FormControl, InputLabel, Box, Typography } from '@mui/material';

import axios from 'axios';

const Controls: React.FC = () => {
    const [symbol, setSymbol] = useState('SPY');
    const [strategy, setStrategy] = useState('');
    const [botStatus, setBotStatus] = useState('offline');
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

        axios.get('/api/strategy/status')
            .then(response => {
                setBotStatus(response.data.status);
            })
            .catch(error => {
                console.error('Error getting bot status:', error);
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
        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2, alignItems: 'center' }}>
            <Box sx={{ width: { xs: '100%', sm: '50%', md: '25%' } }}>
                <TextField 
                    label="Symbol" 
                    variant="outlined" 
                    value={symbol} 
                    onChange={(e) => setSymbol(e.target.value)} 
                    fullWidth
                />
            </Box>
            <Box sx={{ width: { xs: '100%', sm: '50%', md: '25%' } }}>
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
            </Box>
            <Box sx={{ width: { xs: '100%', sm: '50%', md: '15%' } }}>
                <Button variant="contained" color="primary" onClick={handleStart} disabled={botStatus === 'online'} fullWidth>
                    Start Bot
                </Button>
            </Box>
            <Box sx={{ width: { xs: '100%', sm: '50%', md: '15%' } }}>
                <Button variant="contained" color="secondary" onClick={handleStop} disabled={botStatus === 'offline'} fullWidth>
                    Stop Bot
                </Button>
            </Box>
            <Box sx={{ width: { xs: '100%', sm: '100%', md: '20%' } }}>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <Box sx={{ width: 10, height: 10, borderRadius: '50%', bgcolor: botStatus === 'online' ? 'green' : 'red', mr: 1 }} />
                    <Typography>{botStatus}</Typography>
                </Box>
            </Box>
        </Box>
    );
};

export default Controls;
