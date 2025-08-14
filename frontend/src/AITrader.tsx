import React, { useState, useEffect } from 'react';
import {
  trainAIModel,
  TrainParams,
  TrainResult,
} from './services/aiTraderService';
import {
  Container,
  TextField,
  Button,
  Typography,
  Paper,
  Grid,
  CircularProgress,
  Alert,
  LinearProgress,
  Box
} from '@mui/material';

const AITrader: React.FC = () => {
  const [params, setParams] = useState<TrainParams>({
    symbol: 'SPY',
    start_date: '2020-01-01',
    end_date: '2023-01-01',
  });
  const [result, setResult] = useState<TrainResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [trainingStatus, setTrainingStatus] = useState<string | null>(null);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws');

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      if (message.type === 'training_status') {
        setTrainingStatus(message.data.status);
        if (message.data.error) {
          setError(message.data.status);
          setLoading(false);
        }
        if (message.data.status === 'Training complete!') {
          setLoading(false);
          setResult({
            message: message.data.status,
            accuracy: message.data.accuracy,
            error: undefined,
          });
        }
      }
    };

    return () => {
      ws.close();
    };
  }, []);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setParams({
      ...params,
      [event.target.name]: event.target.value,
    });
  };

  const handleTrainModel = () => {
    setLoading(true);
    setError(null);
    setResult(null);
    setTrainingStatus("Starting training...");
    trainAIModel(params).catch((err) => {
      setError(err.message || 'An unknown error occurred.');
      setLoading(false);
    });
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h5" gutterBottom>
        AI Trader Model Management
      </Typography>
      <Paper sx={{ p: 2, mb: 4 }}>
        <Grid container spacing={3} alignItems="center">
          <Grid item xs={12} sm={4}>
            <TextField
              name="symbol"
              label="Symbol for Training"
              value={params.symbol}
              onChange={handleChange}
              fullWidth
              disabled={loading}
            />
          </Grid>
          <Grid item xs={12} sm={3}>
            <TextField
              name="start_date"
              label="Start Date"
              type="date"
              value={params.start_date}
              onChange={handleChange}
              InputLabelProps={{ shrink: true }}
              fullWidth
              disabled={loading}
            />
          </Grid>
          <Grid item xs={12} sm={3}>
            <TextField
              name="end_date"
              label="End Date"
              type="date"
              value={params.end_date}
              onChange={handleChange}
              InputLabelProps={{ shrink: true }}
              fullWidth
              disabled={loading}
            />
          </Grid>
          <Grid item xs={12} sm={2}>
            <Button
              variant="contained"
              color="primary"
              onClick={handleTrainModel}
              disabled={loading}
              fullWidth
            >
              {loading ? <CircularProgress size={24} /> : 'Train Model'}
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {loading && (
        <Paper sx={{ p: 2, mb: 2 }}>
          <Typography variant="h6" gutterBottom>
            Training in Progress...
          </Typography>
          <Box sx={{ width: '100%' }}>
            <LinearProgress />
          </Box>
          <Typography sx={{ mt: 1 }}>{trainingStatus}</Typography>
        </Paper>
      )}

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
      {result && (
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Training Result
          </Typography>
          {result.error ? (
            <Alert severity="warning">{result.error}</Alert>
          ) : (
            <Alert severity="success">
              {result.message}. Accuracy: {result.accuracy.toFixed(4)}
            </Alert>
          )}
        </Paper>
      )}
    </Container>
  );
};

export default AITrader;
