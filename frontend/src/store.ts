

import { create } from 'zustand';
import axios from 'axios';

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
  account: any;
  marketStatus: MarketStatus | null;
  messages: string[];
  trades: any[];
  positions: any[];
  orders: any[];
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
  loggedIn: boolean;
  setAccount: (account: any) => void;
  setMarketStatus: (marketStatus: MarketStatus) => void;
  addMessage: (message: string) => void;
  setTrades: (trades: any[]) => void;
  setPositions: (positions: any[]) => void;
  setOrders: (orders: any[]) => void;
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
  login: (username: string, password: string) => Promise<void>;
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
  loggedIn: false,
  setAccount: (account) => set({ account }),
  setMarketStatus: (marketStatus) => set({ marketStatus }),
  addMessage: (message) => set((state) => ({ messages: [...state.messages, message] })),
  setTrades: (trades) => set({ trades }),
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
  login: async (username, password) => {
    try {
      // In a real application, you would make an API call here
      // For now, we'll simulate a successful login
      if (username === 'user' && password === 'password') {
        set({ loggedIn: true });
        console.log('Login successful');
      } else {
        throw new Error('Invalid credentials');
      }
    } catch (error) {
      console.error('Login failed:', error);
      throw error;
    }
  },
  fetchMarketStatus: async () => {
    set({ loadingMarketStatus: true });
    try {
      const response = await apiClient.get('/market/status');
      set({ marketStatus: response.data, errorMarketStatus: null });
    } catch (error) {
      set({ errorMarketStatus: 'Failed to fetch market status.' });
      console.error('Failed to fetch market status:', error);
    } finally {
      set({ loadingMarketStatus: false });
    }
  },
}));
