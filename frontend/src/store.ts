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
}));


export const fetchAccountInfo = async () => {
  const { setLoadingAccount, setErrorAccount, setAccount } = useStore.getState();
  setLoadingAccount(true);
  try {
    const response = await apiClient.get('/account');
    setAccount(response.data);
    setErrorAccount(null);
  } catch (error) {
    setErrorAccount('Failed to fetch account information.');
    console.error('Failed to fetch account information:', error);
  } finally {
    setLoadingAccount(false);
  }
};

export const fetchMarketStatus = async () => {
  const { setLoadingMarketStatus, setErrorMarketStatus, setMarketStatus } = useStore.getState();
  setLoadingMarketStatus(true);
  try {
    const response = await apiClient.get('/market/status');
    setMarketStatus(response.data);
    setErrorMarketStatus(null);
  } catch (error) {
    setErrorMarketStatus('Failed to fetch market status.');
    console.error('Failed to fetch market status:', error);
  } finally {
    setLoadingMarketStatus(false);
  }
}

export const fetchTrades = async () => {
  const { setLoadingTrades, setErrorTrades, setTrades } = useStore.getState();
  setLoadingTrades(true);
  try {
    const response = await apiClient.get('/trades');
    setTrades(response.data);
    setErrorTrades(null);
  } catch (error) {
    setErrorTrades('Failed to fetch trades.');
    console.error('Failed to fetch trades:', error);
  } finally {
    setLoadingTrades(false);
  }
};

export const fetchPositions = async () => {
  const { setLoadingPositions, setErrorPositions, setPositions } = useStore.getState();
  setLoadingPositions(true);
  try {
    const response = await apiClient.get('/positions');
    setPositions(response.data);
    setErrorPositions(null);
  } catch (error) {
    setErrorPositions('Failed to fetch positions.');
    console.error('Failed to fetch positions:', error);
  } finally {
    setLoadingPositions(false);
  }
};

export const fetchOrders = async () => {
  const { setLoadingOrders, setErrorOrders, setOrders } = useStore.getState();
  setLoadingOrders(true);
  try {
    const response = await apiClient.get('/orders');
    setOrders(response.data);
    setErrorOrders(null);
  } catch (error) {
    setErrorOrders('Failed to fetch orders.');
    console.error('Failed to fetch orders:', error);
  } finally {
    setLoadingOrders(false);
  }
};

export const connectWebSocket = () => {
  const { addMessage } = useStore.getState();
  const ws = new WebSocket('ws://localhost:8000/ws');
  ws.onmessage = (event) => {
    addMessage(event.data);
  };
  ws.onopen = () => {
    addMessage('WebSocket connected');
  };
  ws.onclose = () => {
    addMessage('WebSocket disconnected');
  };
  ws.onerror = (error) => {
    addMessage(`WebSocket error: ${error}`);
  };
};
