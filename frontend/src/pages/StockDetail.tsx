import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { apiService, StockAnalysis } from '../services/api';
import { RecommendationBadge, HalalBadge } from '../components/RecommendationBadge';

interface StockDetailProps {
  symbol: string;
  onBack: () => void;
}

export const StockDetail: React.FC<StockDetailProps> = ({ symbol, onBack }) => {
  const [stock, setStock] = useState<StockAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadStockDetail();
  }, [symbol]);

  const loadStockDetail = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await apiService.getStockAnalysis(symbol);
      setStock(data);
    } catch (err) {
      setError(`Failed to load stock data for ${symbol}`);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="container" style={styles.container}>
        <button className="button button-secondary" onClick={onBack} style={styles.backBtn}>
          ← Back
        </button>
        <div className="flex-center" style={{ minHeight: '400px' }}>
          <div className="loading"></div>
          <p style={{ marginLeft: '1rem' }}>Loading stock data...</p>
        </div>
      </div>
    );
  }

  if (error || !stock) {
    return (
      <div className="container" style={styles.container}>
        <button className="button button-secondary" onClick={onBack} style={styles.backBtn}>
          ← Back
        </button>
        <div style={styles.error}>
          <p>{error || 'Stock not found'}</p>
          <button className="button button-secondary" onClick={loadStockDetail}>
            Retry
          </button>
        </div>
      </div>
    );
  }

  const isPositive = stock.changePercent >= 0;
  const chartData = stock.historical.map(h => ({
    date: h.date.substring(5), // MM-DD format
    price: h.close,
  }));

  return (
    <div style={styles.container}>
      <div className="container">
        <button className="button button-secondary" onClick={onBack} style={styles.backBtn}>
          ← Back to Stocks
        </button>
      </div>

      {/* Header */}
      <div style={styles.headerBg}>
        <div className="container">
          <div style={styles.headerContent}>
            <div>
              <h1 style={styles.title}>{stock.symbol}</h1>
              <p style={styles.name}>{stock.name}</p>
            </div>

            <div style={styles.priceBox}>
              <div style={styles.priceValue}>${stock.price.toFixed(2)}</div>
              <div
                style={{
                  ...styles.change,
                  color: isPositive ? 'var(--success)' : 'var(--danger)',
                }}
              >
                {isPositive ? '▲' : '▼'} ${Math.abs(stock.change).toFixed(2)} ({stock.changePercent.toFixed(2)}%)
              </div>
            </div>
          </div>

          <div style={styles.badges}>
            <RecommendationBadge
              recommendation={stock.recommendation}
              confidence={stock.confidence}
              size="lg"
            />
            {stock.halal && <HalalBadge isHalal={stock.halal.isHalal} score={stock.halal.score} />}
          </div>
        </div>
      </div>

      <div className="container" style={styles.contentContainer}>
        {/* Chart */}
        <div style={styles.chartSection}>
          <h3>Price Chart (Last 100 days)</h3>
          <div style={styles.chart}>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--gray-700)" />
                <XAxis dataKey="date" stroke="var(--text-muted)" />
                <YAxis stroke="var(--text-muted)" domain="dataMin - 10" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'var(--gray-800)',
                    border: '1px solid var(--gray-700)',
                    color: 'var(--text-light)',
                  }}
                />
                <Line type="monotone" dataKey="price" stroke="var(--primary)" dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Analysis Grid */}
        <div className="grid grid-2">
          {/* Technical Analysis */}
          <div className="card">
            <h3>📈 Technical Analysis</h3>
            <div style={styles.analysisGrid}>
              <div>
                <p className="text-muted text-sm">SMA 20</p>
                <p style={styles.value}>${stock.technical.sma20.toFixed(2)}</p>
              </div>
              <div>
                <p className="text-muted text-sm">SMA 50</p>
                <p style={styles.value}>${stock.technical.sma50.toFixed(2)}</p>
              </div>
              <div>
                <p className="text-muted text-sm">SMA 200</p>
                <p style={styles.value}>${stock.technical.sma200.toFixed(2)}</p>
              </div>
              <div>
                <p className="text-muted text-sm">RSI (14)</p>
                <p style={styles.value}>{stock.technical.rsi14.toFixed(1)}</p>
              </div>
              <div>
                <p className="text-muted text-sm">MACD</p>
                <p style={styles.value}>{stock.technical.macd.line.toFixed(4)}</p>
              </div>
              <div>
                <p className="text-muted text-sm">Volume Trend</p>
                <p style={styles.value}>{stock.technical.volumeTrend}</p>
              </div>
            </div>
            <div style={styles.score}>
              <p className="text-muted text-sm">Technical Score</p>
              <div style={styles.progressBar}>
                <div
                  style={{
                    ...styles.progressFill,
                    width: `${stock.technical.technicalScore}%`,
                  }}
                ></div>
              </div>
              <p style={styles.scoreValue}>{stock.technical.technicalScore.toFixed(1)}/100</p>
            </div>
          </div>

          {/* Fundamental Analysis */}
          <div className="card">
            <h3>💼 Fundamental Analysis</h3>
            <div style={styles.analysisGrid}>
              <div>
                <p className="text-muted text-sm">P/E Ratio</p>
                <p style={styles.value}>{stock.fundamental.pe.toFixed(2)}</p>
              </div>
              <div>
                <p className="text-muted text-sm">EPS</p>
                <p style={styles.value}>${stock.fundamental.eps.toFixed(2)}</p>
              </div>
              <div>
                <p className="text-muted text-sm">Debt/Equity</p>
                <p style={styles.value}>{stock.fundamental.debtToEquity.toFixed(2)}</p>
              </div>
              <div>
                <p className="text-muted text-sm">ROE</p>
                <p style={styles.value}>{stock.fundamental.roe.toFixed(2)}%</p>
              </div>
              <div>
                <p className="text-muted text-sm">Profit Margin</p>
                <p style={styles.value}>{stock.fundamental.profitMargin.toFixed(2)}%</p>
              </div>
            </div>
            <div style={styles.score}>
              <p className="text-muted text-sm">Fundamental Score</p>
              <div style={styles.progressBar}>
                <div
                  style={{
                    ...styles.progressFill,
                    width: `${stock.fundamental.fundamentalScore}%`,
                  }}
                ></div>
              </div>
              <p style={styles.scoreValue}>{stock.fundamental.fundamentalScore.toFixed(1)}/100</p>
            </div>
          </div>
        </div>

        {/* Market Data */}
        <div className="card">
          <h3>📊 Market Data</h3>
          <div className="grid grid-3">
            <div>
              <p className="text-muted text-sm">Market Cap</p>
              <p style={styles.value}>${(stock.marketCap / 1e9).toFixed(2)}B</p>
            </div>
            <div>
              <p className="text-muted text-sm">Volume</p>
              <p style={styles.value}>{(stock.volume / 1e6).toFixed(2)}M</p>
            </div>
            <div>
              <p className="text-muted text-sm">52 Week High</p>
              <p style={styles.value}>${stock.high52week.toFixed(2)}</p>
            </div>
            <div>
              <p className="text-muted text-sm">52 Week Low</p>
              <p style={styles.value}>${stock.low52week.toFixed(2)}</p>
            </div>
          </div>
        </div>

        {/* Halal Screening */}
        {stock.halal && (
          <div className="card">
            <h3>🕌 Halal Compliance</h3>
            <p>
              <strong>Status:</strong>{' '}
              <span style={{ color: stock.halal.isHalal ? 'var(--success)' : 'var(--warning)' }}>
                {stock.halal.isHalal ? '✅ Approved' : '⚠️ Review Recommended'}
              </span>
            </p>
            <p>
              <strong>Score:</strong> {stock.halal.score.toFixed(1)}/100
            </p>
            {stock.halal.reasons.length > 0 && (
              <>
                <p>
                  <strong>Details:</strong>
                </p>
                <ul style={styles.list}>
                  {stock.halal.reasons.map((reason, i) => (
                    <li key={i}>{reason}</li>
                  ))}
                </ul>
              </>
            )}
            {stock.halal.prohibitedSectors.length > 0 && (
              <>
                <p>
                  <strong>Prohibited Elements:</strong>
                </p>
                <ul style={styles.list}>
                  {stock.halal.prohibitedSectors.map((sector, i) => (
                    <li key={i}>{sector}</li>
                  ))}
                </ul>
              </>
            )}
          </div>
        )}

        {/* Disclaimer */}
        <div style={styles.disclaimer}>
          <p>
            <strong>⚠️ Disclaimer:</strong> This analysis is for educational purposes only and should not be considered
            financial advice. Always consult with a financial advisor and conduct your own research before making investment
            decisions. Past performance does not guarantee future results.
          </p>
        </div>
      </div>
    </div>
  );
};

const styles = {
  container: {
    minHeight: '100vh',
    backgroundColor: 'var(--bg-darker)',
    paddingBottom: '2rem',
  },
  backBtn: {
    marginTop: '1rem',
    marginBottom: '1rem',
  },
  headerBg: {
    backgroundColor: 'var(--gray-800)',
    borderBottom: '1px solid var(--gray-700)',
    padding: '2rem 0',
    marginBottom: '2rem',
  },
  headerContent: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: '1.5rem',
  } as React.CSSProperties,
  title: {
    fontSize: '2.5rem',
    color: 'var(--primary)',
    marginBottom: '0.25rem',
  },
  name: {
    fontSize: '1.125rem',
    color: 'var(--text-muted)',
    marginBottom: '0',
  },
  priceBox: {
    textAlign: 'right' as const,
  },
  priceValue: {
    fontSize: '2rem',
    fontWeight: '700',
    marginBottom: '0.5rem',
  },
  change: {
    fontSize: '1.125rem',
    fontWeight: '600',
  },
  badges: {
    display: 'flex',
    gap: '0.5rem',
    flexWrap: 'wrap' as const,
  },
  contentContainer: {
    paddingBottom: '2rem',
  },
  chartSection: {
    marginBottom: '2rem',
  },
  chart: {
    backgroundColor: 'var(--gray-800)',
    borderRadius: '0.5rem',
    padding: '1rem',
    marginTop: '1rem',
  },
  analysisGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(2, 1fr)',
    gap: '1rem',
    marginBottom: '1.5rem',
  } as React.CSSProperties,
  value: {
    fontSize: '1.25rem',
    fontWeight: '700',
    color: 'var(--primary)',
    marginBottom: '0',
  },
  score: {
    paddingTop: '0.75rem',
    borderTop: '1px solid var(--gray-700)',
  },
  progressBar: {
    width: '100%',
    height: '0.5rem',
    backgroundColor: 'var(--gray-700)',
    borderRadius: '9999px',
    overflow: 'hidden',
    marginTop: '0.5rem',
    marginBottom: '0.5rem',
  },
  progressFill: {
    height: '100%',
    backgroundColor: 'var(--primary)',
    transition: 'width 0.3s ease',
  },
  scoreValue: {
    fontSize: '0.875rem',
    color: 'var(--text-muted)',
    marginBottom: '0',
  },
  disclaimer: {
    backgroundColor: 'rgba(245, 158, 11, 0.1)',
    border: '1px solid rgba(245, 158, 11, 0.3)',
    borderRadius: '0.5rem',
    padding: '1rem',
    marginTop: '2rem',
    fontSize: '0.875rem',
    lineHeight: '1.6',
  },
  list: {
    paddingLeft: '1.5rem',
    marginTop: '0.5rem',
  },
};
