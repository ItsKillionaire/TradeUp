import { create } from 'zustand';

interface StoreState {
  account: any;
  messages: string[];
  trades: any[];
  loadingAccount: boolean;
  errorAccount: string | null;
  loadingTrades: boolean;
  errorTrades: string | null;
  setAccount: (account: any) => void;
  addMessage: (message: string) => void;
  setTrades: (trades: any[]) => void;
  setLoadingAccount: (loading: boolean) => void;
  setErrorAccount: (error: string | null) => void;
  setLoadingTrades: (loading: boolean) => void;
  setErrorTrades: (error: string | null) => void;
}

export const useStore = create<StoreState>((set) => ({
  account: null,
  messages: [],
  trades: [],
  loadingAccount: true,
  errorAccount: null,
  loadingTrades: true,
  errorTrades: null,
  setAccount: (account) => set({ account }),
  addMessage: (message) => set((state) => ({ messages: [...state.messages, message] })),
  setTrades: (trades) => set({ trades }),
  setLoadingAccount: (loading) => set({ loadingAccount: loading }),
  setErrorAccount: (error) => set({ errorAccount: error }),
  setLoadingTrades: (loading) => set({ loadingTrades: loading }),
  setErrorTrades: (error) => set({ errorTrades: error }),
}));
