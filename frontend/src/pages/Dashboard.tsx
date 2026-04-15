import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import { StockCard } from './StockCard';
import { HalalBadge } from './RecommendationBadge';

interface DashboardProps {
  onSelectStock: (symbol: string) => void;
  searchQuery?: string;
}

export const Dashboard: React.FC<DashboardProps> = ({ onSelectStock, searchQuery }) => {
  const [halalStocks, setHalalStocks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [watchlist, setWatchlist] = useState<string[]>([]);

  useEffect(() => {
    // Load watchlist from localStorage
    const saved = localStorage.getItem('halalvest_watchlist');
    if (saved) {
      setWatchlist(JSON.parse(saved));
    }
  }, []);

  useEffect(() => {
    loadHalalStocks();
  }, []);

  const loadHalalStocks = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiService.getHalalStocks();

      // Load full data for featured stocks
      const featured = await Promise.all(
        data.featured.map(async (stock: any) => {
          try {
            const fullData = await apiService.getStockAnalysis(stock.symbol);
            return {
              ...stock,
              recommendation: fullData.recommendation,
              confidence: fullData.confidence,
              halal: fullData.halal,
            };
          } catch {
            return stock;
          }
        })
      );

      setHalalStocks(featured);
    } catch (err) {
      setError('Failed to load halal stocks');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const toggleWatchlist = (symbol: string, e: React.MouseEvent) => {
    e.stopPropagation();
    const updated = watchlist.includes(symbol)
      ? watchlist.filter(s => s !== symbol)
      : [...watchlist, symbol];
    setWatchlist(updated);
    localStorage.setItem('halalvest_watchlist', JSON.stringify(updated));
  };

  if (loading) {
    return (
      <div className="container" style={styles.container}>
        <div className="flex-center" style={{ minHeight: '400px' }}>
          <div className="loading"></div>
          <p style={{ marginLeft: '1rem' }}>Loading halal stocks...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container" style={styles.container}>
      <div style={styles.header}>
        <div>
          <h2>Featured Halal Stocks</h2>
          <p className="text-muted">
            Curated Islamic-compliant stocks from S&P 500. Click any stock for detailed analysis.
          </p>
        </div>
      </div>

      {error && (
        <div style={styles.error}>
          <p>{error}</p>
          <button className="button button-secondary" onClick={loadHalalStocks}>
            Retry
          </button>
        </div>
      )}

      {watchlist.length > 0 && (
        <div style={styles.section}>
          <h3>📌 Your Watchlist ({watchlist.length})</h3>
          <div className="grid grid-2">
            {halalStocks
              .filter(s => watchlist.includes(s.symbol))
              .map(stock => (
                <div key={stock.symbol} style={styles.cardWrapper}>
                  <StockCard
                    {...stock}
                    onClick={onSelectStock}
                  />
                  <button
                    style={styles.watchlistBtn}
                    onClick={e => toggleWatchlist(stock.symbol, e)}
                    title="Remove from watchlist"
                  >
                    ★
                  </button>
                </div>
              ))}
          </div>
        </div>
      )}

      <div style={styles.section}>
        <h3>All Halal Stocks</h3>
        <div className="grid grid-2">
          {halalStocks.map(stock => (
            <div key={stock.symbol} style={styles.cardWrapper}>
              <StockCard
                {...stock}
                onClick={onSelectStock}
              />
              <button
                style={styles.watchlistBtn}
                onClick={e => toggleWatchlist(stock.symbol, e)}
                title={watchlist.includes(stock.symbol) ? 'Remove from watchlist' : 'Add to watchlist'}
              >
                {watchlist.includes(stock.symbol) ? '★' : '☆'}
              </button>
              {stock.halal && <HalalBadge isHalal={stock.halal.isHalal} score={stock.halal.score} />}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

const styles = {
  container: {
    padding: '2rem 0',
    minHeight: '100vh',
  },
  header: {
    marginBottom: '2rem',
  },
  section: {
    marginTop: '2rem',
  },
  error: {
    backgroundColor: 'rgba(239, 68, 68, 0.1)',
    border: '1px solid rgba(239, 68, 68, 0.3)',
    borderRadius: '0.5rem',
    padding: '1rem',
    marginBottom: '2rem',
    color: 'var(--danger)',
  },
  cardWrapper: {
    position: 'relative' as const,
  },
  watchlistBtn: {
    position: 'absolute' as const,
    top: '0.75rem',
    right: '0.75rem',
    background: 'var(--primary)',
    border: 'none',
    borderRadius: '50%',
    width: '2rem',
    height: '2rem',
    fontSize: '1.25rem',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    transition: 'background-color 0.2s',
  } as React.CSSProperties,
};
