import React from 'react';
import { useStore } from './store';
import { Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Box } from '@mui/material';

const OpenPositions: React.FC = () => {
    const { positions, loadingPositions, errorPositions } = useStore();

    if (loadingPositions) return <Typography>Loading positions...</Typography>;
    if (errorPositions) return <Typography color="error">{errorPositions}</Typography>;

    return (
        <>
            <Typography variant="h6" gutterBottom>Open Positions</Typography>
            <TableContainer component={Paper} sx={{ maxHeight: 400 }}>
                <Table stickyHeader sx={{ minWidth: 650 }} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell>Symbol</TableCell>
                            <TableCell align="right">Qty</TableCell>
                            <TableCell align="right">Side</TableCell>
                            <TableCell align="right">Avg. Entry Price</TableCell>
                            <TableCell align="right">Market Value</TableCell>
                            <TableCell align="right">Unrealized P/L</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {positions.map((position: any) => (
                            <TableRow key={position.asset_id}>
                                <TableCell component="th" scope="row">{position.symbol}</TableCell>
                                <TableCell align="right">{position.qty}</TableCell>
                                <TableCell align="right">{position.side}</TableCell>
                                <TableCell align="right">{position.avg_entry_price}</TableCell>
                                <TableCell align="right">{position.market_value}</TableCell>
                                <TableCell align="right">{position.unrealized_pl}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </>
    );
};

export default OpenPositions;
