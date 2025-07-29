import React from 'react';
import { Card, CardContent, Typography, Paper } from '@mui/material';
import { useStore } from './store';

const Logs: React.FC = () => {
    const { messages } = useStore();

    return (
        <Card>
            <CardContent>
                <Typography variant="h6">Logs</Typography>
                <Paper sx={{ maxHeight: 300, overflow: 'auto', p: 2 }}>
                    {messages.map((msg, index) => (
                        <Typography key={index}>{msg}</Typography>
                    ))}
                </Paper>
            </CardContent>
        </Card>
    );
};

export default Logs;
