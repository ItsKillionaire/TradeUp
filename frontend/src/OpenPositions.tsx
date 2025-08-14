import React from 'react';
import { useStore } from './store';
import {
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from '@mui/material';

const OpenPositions: React.FC = () => {
  const { positions, loadingPositions, errorPositions } = useStore();

  if (loadingPositions) return <Typography>Loading positions...</Typography>;
  if (errorPositions)
    return <Typography color="error">{errorPositions}</Typography>;

  return (
    <>
      <Typography variant="h6" gutterBottom>
        Open Positions
      </Typography>
      <TableContainer component={Paper} sx={{ maxHeight: 400 }}>
        <Table stickyHeader sx={{ minWidth: 650 }} aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>Symbol</TableCell>
              <TableCell align="right">Qty</TableCell>
              <TableCell align="right">Entry Price</TableCell>
              <TableCell align="right">Market Value</TableCell>
              <TableCell align="right">Unrealized P/L</TableCell>
              <TableCell align="right">Take Profit</TableCell>
              <TableCell align="right">Stop Loss</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {positions.map((position: any) => {
              const entryPrice = parseFloat(position.avg_entry_price);
              const takeProfitPrice = position.take_profit_price
                ? parseFloat(position.take_profit_price)
                : null;
              const stopLossPrice = position.stop_loss_price
                ? parseFloat(position.stop_loss_price)
                : null;
              const qty = parseFloat(position.qty);

              const potentialGain = takeProfitPrice
                ? (takeProfitPrice - entryPrice) * qty
                : null;
              const potentialLoss = stopLossPrice
                ? (stopLossPrice - entryPrice) * qty
                : null;

              return (
                <TableRow key={position.asset_id}>
                  <TableCell component="th" scope="row">
                    {position.symbol}
                  </TableCell>
                  <TableCell align="right">{position.qty}</TableCell>
                  <TableCell align="right">
                    {entryPrice.toLocaleString('en-US', {
                      minimumFractionDigits: 2,
                      maximumFractionDigits: 2,
                    })}
                  </TableCell>
                  <TableCell align="right">
                    {parseFloat(position.market_value).toLocaleString('en-US', {
                      minimumFractionDigits: 2,
                      maximumFractionDigits: 2,
                    })}
                  </TableCell>
                  <TableCell
                    align="right"
                    style={{
                      color: position.unrealized_pl >= 0 ? 'green' : 'red',
                    }}
                  >
                    {parseFloat(position.unrealized_pl).toLocaleString(
                      'en-US',
                      { minimumFractionDigits: 2, maximumFractionDigits: 2 }
                    )}
                  </TableCell>
                  <TableCell align="right">
                    {takeProfitPrice
                      ? `${takeProfitPrice.toFixed(2)} (${potentialGain?.toFixed(2)})`
                      : 'N/A'}
                  </TableCell>
                  <TableCell align="right">
                    {stopLossPrice
                      ? `${stopLossPrice.toFixed(2)} (${potentialLoss?.toFixed(2)})`
                      : 'N/A'}
                  </TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>
    </>
  );
};

export default OpenPositions;
