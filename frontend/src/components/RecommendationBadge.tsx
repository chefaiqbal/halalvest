import React from 'react';

interface RecommendationBadgeProps {
  recommendation: 'BUY' | 'SELL' | 'HOLD';
  confidence: number;
  size?: 'sm' | 'md' | 'lg';
}

export const RecommendationBadge: React.FC<RecommendationBadgeProps> = ({
  recommendation,
  confidence,
  size = 'md',
}) => {
  const getBadgeClass = () => {
    switch (recommendation) {
      case 'BUY':
        return 'badge-buy';
      case 'SELL':
        return 'badge-sell';
      case 'HOLD':
        return 'badge-hold';
    }
  };

  const getSizeStyle = () => {
    switch (size) {
      case 'sm':
        return { fontSize: '0.75rem', padding: '0.25rem 0.5rem' };
      case 'lg':
        return { fontSize: '1rem', padding: '0.375rem 1rem' };
      default:
        return {};
    }
  };

  return (
    <span className={`badge ${getBadgeClass()}`} style={getSizeStyle()}>
      {recommendation} ({Math.round(confidence)}%)
    </span>
  );
};

export const HalalBadge: React.FC<{ isHalal: boolean; score: number }> = ({ isHalal, score }) => {
  return (
    <span className="badge badge-halal">
      {isHalal ? '✅ Halal' : '⚠️ Review'} ({Math.round(score)}%)
    </span>
  );
};
