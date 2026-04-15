import React from 'react';
import { RecommendationBadge } from './RecommendationBadge';

interface StockCardProps {
  symbol: string;
  name: string;
  price: number;
  changePercent: number;
  recommendation?: 'BUY' | 'SELL' | 'HOLD';
  confidence?: number;
  onClick: (symbol: string) => void;
}

export const StockCard: React.FC<StockCardProps> = ({
  symbol,
  name,
  price,
  changePercent,
  recommendation,
  confidence,
  onClick,
}) => {
  const isPositive = changePercent >= 0;

  return (
    <div className="card" style={styles.card} onClick={() => onClick(symbol)}>
      <div style={styles.header}>
        <div>
          <h3 style={styles.symbol}>{symbol}</h3>
          <p className="text-muted text-sm" style={styles.name}>
            {name}
          </p>
        </div>
        {recommendation && confidence !== undefined && (
          <RecommendationBadge recommendation={recommendation} confidence={confidence} size="sm" />
        )}
      </div>

      <div style={styles.priceSection}>
        <div style={styles.price}>
          <span style={styles.priceValue}>${price.toFixed(2)}</span>
          <span
            style={{
              ...styles.change,
              color: isPositive ? 'var(--success)' : 'var(--danger)',
            }}
          >
            {isPositive ? '▲' : '▼'} {Math.abs(changePercent).toFixed(2)}%
          </span>
        </div>
      </div>
    </div>
  );
};

const styles = {
  card: {
    cursor: 'pointer',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: '1rem',
    gap: '1rem',
  } as React.CSSProperties,
  symbol: {
    fontSize: '1.25rem',
    marginBottom: '0.25rem',
    color: 'var(--primary)',
  },
  name: {
    marginBottom: '0',
  },
  priceSection: {
    marginTop: '1rem',
  },
  price: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  } as React.CSSProperties,
  priceValue: {
    fontSize: '1.5rem',
    fontWeight: '700',
  },
  change: {
    fontSize: '1rem',
    fontWeight: '600',
  },
};
