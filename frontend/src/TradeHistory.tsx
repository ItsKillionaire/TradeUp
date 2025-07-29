import React from 'react';
import { Card, CardContent, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, CircularProgress } from '@mui/material';
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
        <Card>
            <CardContent>
                <Typography variant="h6">Trade History</Typography>
                <TableContainer component={Paper} sx={{ maxHeight: 300, overflow: 'auto' }}>
                    <Table stickyHeader>
                        <TableHead>
                            <TableRow>
                                <TableCell>ID</TableCell>
                                <TableCell>Symbol</TableCell>
                                <TableCell>Quantity</TableCell>
                                <TableCell>Price</TableCell>
                                <TableCell>Side</TableCell>
                                <TableCell>Timestamp</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {trades.map((trade) => (
                                <TableRow key={trade.id}>
                                    <TableCell>{trade.id}</TableCell>
                                    <TableCell>{trade.symbol}</TableCell>
                                    <TableCell>{trade.qty}</TableCell>
                                    <TableCell>{trade.price}</TableCell>
                                    <TableCell>{trade.side}</TableCell>
                                    <TableCell>{new Date(trade.timestamp).toLocaleString()}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </CardContent>
        </Card>
    );
};

export default TradeHistory;
