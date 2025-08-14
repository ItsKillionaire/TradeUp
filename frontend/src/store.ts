import { create } from 'zustand';
import axios from 'axios';
import { Account, Position, Order, Trade } from './types';

export const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
});

interface MarketStatus {
  is_open: boolean;
  next_open: string;
  next_close: string;
  timestamp: string;
}

interface StoreState {
  account: Account | null;
  marketStatus: MarketStatus | null;
  messages: string[];
  trades: Trade[];
  positions: Position[];
  orders: Order[];
  loadingAccount: boolean;
  errorAccount: string | null;
  loadingMarketStatus: boolean;
  errorMarketStatus: string | null;
  loadingTrades: boolean;
  errorTrades: string | null;
  loadingPositions: boolean;
  errorPositions: string | null;
  loadingOrders: boolean;
  errorOrders: string | null;
  setAccount: (account: Account | null) => void;
  setMarketStatus: (marketStatus: MarketStatus) => void;
  addMessage: (message: string) => void;
  clearMessages: () => void;
  setTrades: (trades: Trade[]) => void;
  addTrade: (trade: Trade) => void;
  setPositions: (positions: Position[]) => void;
  setOrders: (orders: Order[]) => void;
  setLoadingAccount: (loading: boolean) => void;
  setErrorAccount: (error: string | null) => void;
  setLoadingMarketStatus: (loading: boolean) => void;
  setErrorMarketStatus: (error: string | null) => void;
  setLoadingTrades: (loading: boolean) => void;
  setErrorTrades: (error: string | null) => void;
  setLoadingPositions: (loading: boolean) => void;
  setErrorPositions: (error: string | null) => void;
  setLoadingOrders: (loading: boolean) => void;
  setErrorOrders: (error: string | null) => void;
  fetchMarketStatus: () => Promise<void>;
}

export const useStore = create<StoreState>((set) => ({
  account: null,
  marketStatus: null,
  messages: [],
  trades: [],
  positions: [],
  orders: [],
  loadingAccount: true,
  errorAccount: null,
  loadingMarketStatus: true,
  errorMarketStatus: null,
  loadingTrades: true,
  errorTrades: null,
  loadingPositions: true,
  errorPositions: null,
  loadingOrders: true,
  errorOrders: null,
  setAccount: (account) => set({ account }),
  setMarketStatus: (marketStatus) => set({ marketStatus }),
  addMessage: (message) =>
    set((state) => ({ messages: [...state.messages, message] })),
  clearMessages: () => set({ messages: [] }),
  setTrades: (trades) => set({ trades }),
  addTrade: (trade) => set((state) => ({ trades: [...state.trades, trade] })),
  setPositions: (positions) => set({ positions }),
  setOrders: (orders) => set({ orders }),
  setLoadingAccount: (loading) => set({ loadingAccount: loading }),
  setErrorAccount: (error) => set({ errorAccount: error }),
  setLoadingMarketStatus: (loading) => set({ loadingMarketStatus: loading }),
  setErrorMarketStatus: (error) => set({ errorMarketStatus: error }),
  setLoadingTrades: (loading) => set({ loadingTrades: loading }),
  setErrorTrades: (error) => set({ errorTrades: error }),
  setLoadingPositions: (loading) => set({ loadingPositions: loading }),
  setErrorPositions: (error) => set({ errorPositions: error }),
  setLoadingOrders: (loading) => set({ loadingOrders: loading }),
  setErrorOrders: (error) => set({ errorOrders: error }),
  fetchMarketStatus: async () => {
    set({ loadingMarketStatus: true });
    try {
      const response = await apiClient.get('/market/status');
      set({ marketStatus: response.data, errorMarketStatus: null });
    } catch (error) {
      set({ errorMarketStatus: 'Failed to fetch market status.' });
    } finally {
      set({ loadingMarketStatus: false });
    }
  },
}));

const socket = new WebSocket('ws://localhost:8000/ws');

socket.onmessage = (event) => {
  const message = JSON.parse(event.data);
  const {
    addMessage,
    setPositions,
    setOrders,
    addTrade,
    setAccount,
    setMarketStatus,
  } = useStore.getState();

  if (message.type === 'log') {
    addMessage(message.message);
  } else if (message.type === 'positions_update') {
    setPositions(message.data);
  } else if (message.type === 'orders_update') {
    setOrders(message.data);
  } else if (message.type === 'trade_update') {
    addTrade(message.data);
  } else if (message.type === 'account_update') {
    setAccount(message.data);
  } else if (message.type === 'market_status_update') {
    setMarketStatus(message.data);
  }
};
