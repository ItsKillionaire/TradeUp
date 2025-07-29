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
        <Grid container spacing={3} sx={{ mt: 2 }}>
            <Grid xs={12} sm={6} md={4}>
                <Card>
                    <CardContent>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                            <ShowChart sx={{ mr: 1 }} />
                            <Typography variant="h6">Portfolio Value</Typography>
                        </Box>
                        <Typography variant="h4">${account.portfolio_value}</Typography>
                    </CardContent>
                </Card>
            </Grid>
            <Grid xs={12} sm={6} md={4}>
                <Card>
                    <CardContent>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                            <AttachMoney sx={{ mr: 1 }} />
                            <Typography variant="h6">Buying Power</Typography>
                        </Box>
                        <Typography variant="h4">${parseFloat(account.buying_power).toFixed(2)}</Typography>
                    </CardContent>
                </Card>
            </Grid>
            <Grid xs={12} sm={6} md={4}>
                <Card>
                    <CardContent>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                            <PowerSettingsNew sx={{ mr: 1 }} />
                            <Typography variant="h6">Status</Typography>
                        </Box>
                        <Typography variant="h4">{account.status}</Typography>
                    </CardContent>
                </Card>
            </Grid>
        </Grid>
    );
};

export default AccountInfo;
