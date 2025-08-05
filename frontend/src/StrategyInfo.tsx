import React from 'react';
import { Typography, Box } from '@mui/material';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

interface StrategyInfoProps {
    strategy: {
        name: string;
        display_name: string;
        description: string;
        chartData?: any;
        chartOptions?: any;
    };
}

const StrategyInfo: React.FC<StrategyInfoProps> = ({ strategy }) => {
    return (
        <Box>
            <Typography variant="h6">{strategy.display_name}</Typography>
            <Typography>{strategy.description}</Typography>
            {strategy.chartData && (
                <Box sx={{ mt: 3 }}>
                    <Line data={strategy.chartData} options={strategy.chartOptions} />
                </Box>
            )}
        </Box>
    );
};

export default StrategyInfo;
