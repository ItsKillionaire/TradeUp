import React from 'react';
import { useStore } from './store';
import { Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

const RecentOrders: React.FC = () => {
    const { orders, loadingOrders, errorOrders } = useStore();

    if (loadingOrders) return <Typography>Loading orders...</Typography>;
    if (errorOrders) return <Typography color="error">{errorOrders}</Typography>;

    return (
        <>
            <Typography variant="h6" gutterBottom>Recent Orders</Typography>
            <TableContainer component={Paper} sx={{ maxHeight: 400 }}>
                <Table stickyHeader sx={{ minWidth: 650 }} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell>Symbol</TableCell>
                            <TableCell align="right">Qty</TableCell>
                            <TableCell align="right">Side</TableCell>
                            <TableCell align="right">Type</TableCell>
                            <TableCell align="right">Status</TableCell>
                            <TableCell align="right">Filled</TableCell>
                            <TableCell align="right">Price</TableCell>
                            <TableCell align="right">Created At</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {orders.slice(0, 20).map((order: any) => (
                            <TableRow key={order.id}>
                                <TableCell component="th" scope="row">{order.symbol}</TableCell>
                                <TableCell align="right">{order.qty}</TableCell>
                                <TableCell align="right">{order.side}</TableCell>
                                <TableCell align="right">{order.type}</TableCell>
                                <TableCell align="right">{order.status}</TableCell>
                                <TableCell align="right">{order.filled_qty} / {order.qty}</TableCell>
                                <TableCell align="right">{order.filled_avg_price || 'N/A'}</TableCell>
                                <TableCell align="right">{new Date(order.created_at).toLocaleString()}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </>
    );
};

export default RecentOrders;
