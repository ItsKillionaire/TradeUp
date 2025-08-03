import { create } from 'zustand';
import axios from 'axios';

export const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
});

interface StoreState {
  account: any;
  messages: string[];
  trades: any[];
  positions: any[];
  orders: any[];
  loadingAccount: boolean;
  errorAccount: string | null;
  loadingTrades: boolean;
  errorTrades: string | null;
  loadingPositions: boolean;
  errorPositions: string | null;
  loadingOrders: boolean;
  errorOrders: string | null;
  loggedIn: boolean;
  setAccount: (account: any) => void;
  addMessage: (message: string) => void;
  setTrades: (trades: any[]) => void;
  setPositions: (positions: any[]) => void;
  setOrders: (orders: any[]) => void;
  setLoadingAccount: (loading: boolean) => void;
  setErrorAccount: (error: string | null) => void;
  setLoadingTrades: (loading: boolean) => void;
  setErrorTrades: (error: string | null) => void;
  setLoadingPositions: (loading: boolean) => void;
  setErrorPositions: (error: string | null) => void;
  setLoadingOrders: (loading: boolean) => void;
  setErrorOrders: (error: string | null) => void;
  login: (username: string, password: string) => Promise<void>;
}

export const useStore = create<StoreState>((set) => ({
  account: null,
  messages: [],
  trades: [],
  positions: [],
  orders: [],
  loadingAccount: true,
  errorAccount: null,
  loadingTrades: true,
  errorTrades: null,
  loadingPositions: true,
  errorPositions: null,
  loadingOrders: true,
  errorOrders: null,
  loggedIn: false,
  setAccount: (account) => set({ account }),
  addMessage: (message) => set((state) => ({ messages: [...state.messages, message] })),
  setTrades: (trades) => set({ trades }),
  setPositions: (positions) => set({ positions }),
  setOrders: (orders) => set({ orders }),
  setLoadingAccount: (loading) => set({ loadingAccount: loading }),
  setErrorAccount: (error) => set({ errorAccount: error }),
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
}));
