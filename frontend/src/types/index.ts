export interface Position {
  asset_id: string;
  symbol: string;
  qty: string;
  avg_entry_price: string;
  market_value: string;
  unrealized_pl: string;
  take_profit_price?: string;
  stop_loss_price?: string;
}

export interface Account {
  portfolio_value: string;
  buying_power: string;
  equity: string;
  last_equity: string;
  status: string;
}

export interface Order {
  id: string;
  symbol: string;
  side: 'buy' | 'sell';
  order_type: string;
  filled_qty: string;
  qty: string;
  filled_avg_price: string | null;
  status: string;
  submitted_at: string | null;
  filled_at: string | null;
}

export interface Trade {
  id: string;
  symbol: string;
  qty: string;
  price: string;
  side: string;
  timestamp: string;
}