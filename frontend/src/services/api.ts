import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001/api';

const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
});

export interface StockAnalysis {
  symbol: string;
  name: string;
  price: number;
  change: number;
  changePercent: number;
  marketCap: number;
  volume: number;
  high52week: number;
  low52week: number;
  technical: any;
  fundamental: any;
  recommendation: 'BUY' | 'SELL' | 'HOLD';
  confidence: number;
  halal: any;
  historical: any[];
}

export interface StockQuote {
  symbol: string;
  name: string;
  price: number;
  changePercent: number;
  marketCap?: number;
}

export const apiService = {
  async getStockAnalysis(symbol: string): Promise<StockAnalysis> {
    const response = await api.get(`/stocks/${symbol}`);
    return response.data;
  },

  async searchStocks(query: string): Promise<any[]> {
    const response = await api.get(`/search/${query}`);
    return response.data;
  },

  async getHalalStocks(): Promise<any> {
    const response = await api.get('/halal-stocks');
    return response.data;
  },

  async getBatchStocks(symbols: string[]): Promise<StockQuote[]> {
    const response = await api.post('/batch', { symbols });
    return response.data;
  },
};
