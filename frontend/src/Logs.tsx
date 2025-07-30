import React from 'react';
import { Typography, Box, List, ListItem, ListItemText } from '@mui/material';
import { useStore } from './store';

const Logs: React.FC = () => {
    const { messages } = useStore();

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
            <Typography variant="h6" gutterBottom>Logs</Typography>
            <Box sx={{ flexGrow: 1, overflow: 'auto', pr: 2 }}>
                <List dense>
                    {messages.map((msg, index) => (
                        <ListItem key={index}>
                            <ListItemText primary={msg} />
                        </ListItem>
                    ))}
                </List>
            </Box>
        </Box>
    );
};

export default Logs;
