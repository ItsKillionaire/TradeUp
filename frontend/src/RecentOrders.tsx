import { Order } from './types';
import { useStore } from './store';
import {
  Typography,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from '@mui/material';

const RecentOrders: React.FC = () => {
  const { orders, loadingOrders, errorOrders } = useStore();

  if (loadingOrders) return <Typography>Loading orders...</Typography>;
  if (errorOrders) return <Typography color="error">{errorOrders}</Typography>;

  const getStatusChip = (status: string) => {
    let color: 'success' | 'primary' | 'warning' | 'error' | 'default' =
      'default';
    switch (status) {
      case 'filled':
        color = 'success';
        break;
      case 'new':
        color = 'primary';
        break;
      case 'partially_filled':
        color = 'warning';
        break;
      case 'canceled':
      case 'expired':
        color = 'error';
        break;
    }
    return (
      <Chip
        label={status}
        color={color}
        size="small"
        sx={{ textTransform: 'capitalize' }}
      />
    );
  };

  const formatDate = (dateString: string | null) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <>
      <Typography variant="h6" gutterBottom sx={{ mb: 2 }}>
        Recent Orders
      </Typography>
      <Paper
        sx={{
          width: '100%',
          overflow: 'hidden',
          borderRadius: 2,
          boxShadow: '0 2px 10px rgba(0,0,0,0.05)',
        }}
      >
        <TableContainer sx={{ maxHeight: 440 }}>
          <Table stickyHeader aria-label="recent orders table">
            <TableHead>
              <TableRow>
                <TableCell sx={{ fontWeight: 'bold' }}>Asset</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Side/Type</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }} align="right">
                  Quantity
                </TableCell>
                <TableCell sx={{ fontWeight: 'bold' }} align="right">
                  Avg. Fill Price
                </TableCell>
                <TableCell sx={{ fontWeight: 'bold' }} align="center">
                  Status
                </TableCell>
                <TableCell sx={{ fontWeight: 'bold', minWidth: 170 }}>
                  Submitted At
                </TableCell>
                <TableCell sx={{ fontWeight: 'bold', minWidth: 170 }}>
                  Filled At
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {orders.slice(0, 20).map((order: Order, index: number) => (
                <TableRow
                  key={order.id}
                  hover
                  sx={{
                    '&:last-child td, &:last-child th': { border: 0 },
                    backgroundColor:
                      index % 2 === 0 ? 'action.hover' : 'background.paper',
                  }}
                >
                  <TableCell component="th" scope="row" sx={{ py: 1 }}>
                    <Typography variant="body2" fontWeight="bold">
                      {order.symbol}
                    </Typography>
                  </TableCell>
                  <TableCell sx={{ py: 1 }}>
                    <Typography
                      variant="body2"
                      sx={{
                        color:
                          order.side === 'buy' ? 'success.main' : 'error.main',
                        textTransform: 'capitalize',
                      }}
                    >
                      {order.side} {order.order_type}
                    </Typography>
                  </TableCell>
                  <TableCell align="right" sx={{ py: 1 }}>
                    {order.filled_qty} / {order.qty}
                  </TableCell>
                  <TableCell align="right" sx={{ py: 1 }}>
                    {order.filled_avg_price
                      ? `${parseFloat(order.filled_avg_price).toFixed(2)}`
                      : 'N/A'}
                  </TableCell>
                  <TableCell align="center" sx={{ py: 1 }}>
                    {getStatusChip(order.status)}
                  </TableCell>
                  <TableCell sx={{ py: 1 }}>
                    {formatDate(order.submitted_at)}
                  </TableCell>
                  <TableCell sx={{ py: 1 }}>
                    {formatDate(order.filled_at)}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </>
  );
};

export default RecentOrders;
