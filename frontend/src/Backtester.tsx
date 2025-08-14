import React, { useState } from 'react';
import {
  runBacktest,
  BacktestParams,
  BacktestResult,
} from './services/backtesterService';
import {
  Container,
  TextField,
  Button,
  Typography,
  Paper,
  Grid,
  CircularProgress,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';

const Backtester: React.FC = () => {
  const [params, setParams] = useState<BacktestParams>({
    symbol: 'SPY',
    strategy_name: 'SMA Crossover',
    start_date: '2022-01-01',
    end_date: '2023-01-01',
  });
  const [result, setResult] = useState<BacktestResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setParams({
      ...params,
      [event.target.name]: event.target.value,
    });
  };

  const handleRunBacktest = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await runBacktest(params);
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'An unknown error occurred.');
    }
    setLoading(false);
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Strategy Backtester
      </Typography>
      <Paper sx={{ p: 2, mb: 4 }}>
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6} md={2}>
            <TextField
              name="symbol"
              label="Symbol"
              value={params.symbol}
              onChange={handleChange}
              fullWidth
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <TextField
              name="strategy_name"
              label="Strategy"
              value={params.strategy_name}
              onChange={handleChange}
              fullWidth
            />
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
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
          <Grid item xs={12} sm={6} md={3}>
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
          <Grid
            item
            xs={12}
            md={1}
            sx={{ display: 'flex', alignItems: 'center' }}
          >
            <Button
              variant="contained"
              onClick={handleRunBacktest}
              disabled={loading}
              fullWidth
            >
              {loading ? <CircularProgress size={24} /> : 'Run'}
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
      {result && (
        <Paper sx={{ p: 2 }}>
          <Typography variant="h5" gutterBottom>
            Backtest Results
          </Typography>
          {result.error ? (
            <Alert severity="warning">{result.error}</Alert>
          ) : (
            <Grid container spacing={3}>
              <Grid item xs={6} md={3}>
                <Typography>
                  Initial Capital: ${result.initial_capital.toLocaleString()}
                </Typography>
              </Grid>
              <Grid item xs={6} md={3}>
                <Typography>
                  Final Value: ${result.final_portfolio_value.toLocaleString()}
                </Typography>
              </Grid>
              <Grid item xs={6} md={3}>
                <Typography>
                  Net Profit: ${result.net_profit.toLocaleString()}
                </Typography>
              </Grid>
              <Grid item xs={6} md={3}>
                <Typography>Return: {result.return_pct.toFixed(2)}%</Typography>
              </Grid>
              <Grid item xs={6} md={3}>
                <Typography>Total Trades: {result.total_trades}</Typography>
              </Grid>
            </Grid>
          )}
          {result.trades && result.trades.length > 0 && (
            <TableContainer sx={{ mt: 4 }}>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Date</TableCell>
                    <TableCell>Symbol</TableCell>
                    <TableCell>Side</TableCell>
                    <TableCell align="right">Quantity</TableCell>
                    <TableCell align="right">Price</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {result.trades.map((trade, index) => (
                    <TableRow key={index}>
                      <TableCell>
                        {new Date(trade.date).toLocaleDateString()}
                      </TableCell>
                      <TableCell>{trade.symbol}</TableCell>
                      <TableCell>{trade.side}</TableCell>
                      <TableCell align="right">
                        {trade.qty.toFixed(4)}
                      </TableCell>
                      <TableCell align="right">
                        ${trade.price.toFixed(2)}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </Paper>
      )}
    </Container>
  );
};

export default Backtester;
