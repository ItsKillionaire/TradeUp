const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export interface BacktestParams {
  symbol: string;
  strategy_name: string;
  start_date: string;
  end_date: string;
}

export interface BacktestTrade {
  date: string;
  symbol: string;
  side: 'buy' | 'sell';
  qty: number;
  price: number;
}

export interface BacktestResult {
  initial_capital: number;
  final_portfolio_value: number;
  net_profit: number;
  return_pct: number;
  total_trades: number;
  trades: BacktestTrade[];
  error?: string;
}

export const runBacktest = async (
  params: BacktestParams
): Promise<BacktestResult> => {
  const response = await fetch(`${API_URL}/api/backtest`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(params),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to run backtest');
  }

  return response.json();
};
