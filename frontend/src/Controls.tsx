import React, { useState, useEffect } from 'react';
import {
  Button,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Box,
  Typography,
  Grid,
  IconButton,
  Tooltip,
} from '@mui/material';
import InfoIcon from '@mui/icons-material/Info';
import axios from 'axios';

interface Strategy {
  name: string;
  display_name: string;
  description: string;
}

interface StartStopResponse {
  message: string;
}

interface AvailableStrategiesResponse {
  data: {
    strategies: Strategy[];
  };
}

const Controls: React.FC = () => {
  const [symbol, setSymbol] = useState('SPY');
  const [strategy, setStrategy] = useState('');
  const [botStatus, setBotStatus] = useState('idle');
  const [availableStrategies, setAvailableStrategies] = useState<Strategy[]>(
    []
  );

  useEffect(() => {
    axios
      .get<AvailableStrategiesResponse>('/api/strategy/available')
      .then((response) => {
        setAvailableStrategies(response.data.data.strategies);
        if (response.data.data.strategies.length > 0) {
          setStrategy(response.data.data.strategies[0].name);
        }
      })
      .catch((error) => {
        console.error('Error fetching available strategies:', error);
      });
  }, []);

  const handleStart = () => {
    axios
      .post<StartStopResponse>(`/api/strategy/start/${strategy}/${symbol}`)
      .then((response) => {
        console.log(response.data.message);
        setBotStatus('online');
      })
      .catch((error: any) => {
        console.error('Error starting strategy:', error);
      });
  };

  const handleStop = () => {
    axios
      .post<StartStopResponse>(`/api/strategy/stop/${strategy}/${symbol}`)
      .then((response) => {
        console.log(response.data.message);
        setBotStatus('offline');
      })
      .catch((error) => {});
  };

  const selectedStrategy = availableStrategies.find((s) => s.name === strategy);

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Typography variant="h6" gutterBottom>
        Controls
      </Typography>
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
        <Grid item xs={12} sm={6} md={4}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <FormControl variant="outlined" fullWidth>
              <InputLabel>Strategy</InputLabel>
              <Select
                value={strategy}
                onChange={(e) => setStrategy(e.target.value as string)}
                label="Strategy"
              >
                {availableStrategies.map((strat) => (
                  <MenuItem key={strat.name} value={strat.name}>
                    {strat.display_name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            {selectedStrategy && (
              <Tooltip title={selectedStrategy.description} arrow>
                <IconButton color="primary" sx={{ ml: 1 }}>
                  <InfoIcon />
                </IconButton>
              </Tooltip>
            )}
          </Box>
        </Grid>
        <Grid item xs={12} sm={6} md={2}>
          <Button
            variant="contained"
            color="primary"
            onClick={handleStart}
            disabled={botStatus === 'online' || !strategy}
            fullWidth
          >
            Start Bot
          </Button>
        </Grid>
        <Grid item xs={12} sm={6} md={2}>
          <Button
            variant="contained"
            color="secondary"
            onClick={handleStop}
            disabled={botStatus !== 'online' || !strategy}
            fullWidth
          >
            Stop Bot
          </Button>
        </Grid>
        <Grid item xs={12} sm={12} md={1}>
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              height: '100%',
            }}
          >
            <Box
              sx={{
                width: 10,
                height: 10,
                borderRadius: '50%',
                bgcolor:
                  botStatus === 'online'
                    ? 'success.main'
                    : botStatus === 'offline'
                      ? 'error.main'
                      : 'grey.500',
                mr: 1,
              }}
            />
            <Typography variant="subtitle1">{botStatus}</Typography>
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Controls;
