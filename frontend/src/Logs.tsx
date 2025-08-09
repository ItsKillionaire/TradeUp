import React from 'react';
import { Typography, Box, List, ListItem, ListItemText, Button } from '@mui/material';
import { useStore } from './store';

const Logs: React.FC = () => {
    const { messages, clearMessages } = useStore();

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="h6" gutterBottom>Logs</Typography>
                <Button variant="outlined" size="small" onClick={clearMessages}>Clear Logs</Button>
            </Box>
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
