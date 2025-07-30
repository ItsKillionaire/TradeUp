import React from 'react';
import { Typography, Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, CircularProgress } from '@mui/material';
import { useStore } from './store';

const TradeHistory: React.FC = () => {
    const { trades, loadingTrades, errorTrades } = useStore();

    if (loadingTrades) {
        return <CircularProgress />;
    }

    if (errorTrades) {
        return <Typography color="error">{errorTrades}</Typography>;
    }

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
            <Typography variant="h6" gutterBottom>Trade History</Typography>
            <TableContainer component={Paper} sx={{ flexGrow: 1 }}>
                <Table stickyHeader size="small">
                    <TableHead>
                        <TableRow>
                            <TableCell>Symbol</TableCell>
                            <TableCell align="right">Quantity</TableCell>
                            <TableCell align="right">Price</TableCell>
                            <TableCell>Side</TableCell>
                            <TableCell>Timestamp</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {trades.map((trade) => (
                            <TableRow key={trade.id}>
                                <TableCell>{trade.symbol}</TableCell>
                                <TableCell align="right">{parseFloat(trade.qty).toLocaleString('en-US')}</TableCell>
                                <TableCell align="right">${parseFloat(trade.price).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</TableCell>
                                <TableCell>{trade.side}</TableCell>
                                <TableCell>{new Date(trade.timestamp).toLocaleString()}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </Box>
    );
};

export default TradeHistory;
