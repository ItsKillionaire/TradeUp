import React, { useState } from 'react';
import { trainAIModel, TrainParams, TrainResult } from './services/aiTraderService';
import {
  Container, TextField, Button, Typography, Paper, Grid, CircularProgress, Alert
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

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setParams({
      ...params,
      [event.target.name]: event.target.value,
    });
  };

  const handleTrainModel = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await trainAIModel(params);
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'An unknown error occurred.');
    }
    setLoading(false);
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

      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      {result && (
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>Training Result</Typography>
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
