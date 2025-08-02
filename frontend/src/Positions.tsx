import React, { useEffect, useState } from 'react';
import { apiClient } from './store';

import { Typography, Box, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, CircularProgress } from '@mui/material';

interface Position {
    asset_class: string;
    side: string;
    symbol: string;
    current_price: string;
    qty: string;
    market_value: string;
    unrealized_pl: string;
}

const Positions: React.FC = () => {
    const [positions, setPositions] = useState<Position[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        apiClient.get('/positions')
            .then((response: any) => {
                setPositions(response.data);
                setLoading(false);
            })
            .catch((error: any) => {
                console.error('Error fetching positions:', error);
                setError('Failed to fetch positions.');
                setLoading(false);
            });
    }, []);

    if (loading) {
        return <CircularProgress />;
    }

    if (error) {
        return <Typography color="error">{error}</Typography>;
    }

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
            <Typography variant="h6" gutterBottom>Top Positions</Typography>
            <TableContainer component={Paper} sx={{ flexGrow: 1 }}>
                <Table stickyHeader size="small">
                    <TableHead>
                        <TableRow>
                            <TableCell>Asset Class</TableCell>
                            <TableCell>Side</TableCell>
                            <TableCell>Asset</TableCell>
                            <TableCell align="right">Price</TableCell>
                            <TableCell align="right">Qty</TableCell>
                            <TableCell align="right">Market Value</TableCell>
                            <TableCell align="right">Total P/L ($)</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {positions.map((position) => (
                            <TableRow key={position.symbol}>
                                <TableCell>{position.asset_class}</TableCell>
                                <TableCell>{position.side}</TableCell>
                                <TableCell>{position.symbol}</TableCell>
                                <TableCell align="right">${parseFloat(position.current_price).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</TableCell>
                                <TableCell align="right">{parseFloat(position.qty).toLocaleString('en-US')}</TableCell>
                                <TableCell align="right">${parseFloat(position.market_value).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</TableCell>
                                <TableCell align="right">{parseFloat(position.unrealized_pl).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </Box>
    );
};

export default Positions;
