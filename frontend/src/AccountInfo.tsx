import React from 'react';
import { Card, CardContent, Typography, Box, CircularProgress, Grid } from '@mui/material';
import { AttachMoney, ShowChart, PowerSettingsNew } from '@mui/icons-material';
import { useStore } from './store';

const AccountInfo: React.FC = () => {
    const { account, loadingAccount, errorAccount } = useStore();

    if (loadingAccount) {
        return <CircularProgress />;
    }

    if (errorAccount) {
        return <Typography color="error">{errorAccount}</Typography>;
    }

    if (!account) {
        return null;
    }

    return (
        <Box sx={{ flexGrow: 1 }}>
            <Typography variant="h6" gutterBottom>Account Information</Typography>
            <Grid container spacing={3}>
                <Grid item xs={12} sm={6} md={4}>
                    <Card sx={{ height: '100%' }}>
                        <CardContent>
                            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                                <ShowChart sx={{ mr: 1, color: 'primary.main' }} />
                                <Typography variant="subtitle1">Portfolio Value</Typography>
                            </Box>
                            <Typography variant="h5">${parseFloat(account.portfolio_value).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</Typography>
                        </CardContent>
                    </Card>
                </Grid>
                <Grid item xs={12} sm={6} md={4}>
                    <Card sx={{ height: '100%' }}>
                        <CardContent>
                            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                                <AttachMoney sx={{ mr: 1, color: 'primary.main' }} />
                                <Typography variant="subtitle1">Buying Power</Typography>
                            </Box>
                            <Typography variant="h5">${parseFloat(account.buying_power).toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</Typography>
                        </CardContent>
                    </Card>
                </Grid>
                <Grid item xs={12} sm={6} md={4}>
                    <Card sx={{ height: '100%' }}>
                        <CardContent>
                            <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                                <PowerSettingsNew sx={{ mr: 1, color: account.status === 'ACTIVE' ? 'success.main' : 'error.main' }} />
                                <Typography variant="subtitle1">Status</Typography>
                            </Box>
                            <Typography variant="h5">{account.status}</Typography>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>
        </Box>
    );
};

export default AccountInfo;
