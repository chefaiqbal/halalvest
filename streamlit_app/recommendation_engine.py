"""
Recommendation Engine
Combines technical and fundamental analysis for Buy/Sell/Hold recommendations
"""

from technical_analysis import technical_signal_score, technical_analysis
from fundamental_analysis import fundamental_signal_score, fundamental_analysis
from typing import Dict


def get_recommendation(symbol: str) -> Dict:
    """
    Generate comprehensive buy/sell/hold recommendation
    Combines technical (50%) and fundamental (50%) analysis
    """
    try:
        # Get technical analysis
        tech_analysis = technical_analysis(symbol)
        if 'error' in tech_analysis:
            return {'error': tech_analysis['error']}

        tech_score, tech_interp = technical_signal_score(tech_analysis)

        # Get fundamental analysis
        fund_analysis = fundamental_analysis(symbol)
        fund_score, fund_interp = fundamental_signal_score(fund_analysis)

        # Combine scores (50% technical, 50% fundamental)
        combined_score = (tech_score * 0.5) + (fund_score * 0.5)

        # Determine recommendation based on score
        if combined_score > 65:
            recommendation = '🟢 BUY'
            explanation = 'Strong buy signals from both technical and fundamental analysis'
        elif combined_score > 55:
            recommendation = '💹 STRONG HOLD'
            explanation = 'Positive outlook with good fundamentals or technical trends'
        elif combined_score > 45:
            recommendation = '〰️ HOLD'
            explanation = 'Mixed signals - wait for more clarity'
        elif combined_score > 35:
            recommendation = '⚠️ WEAK HOLD'
            explanation = 'Negative outlook but not yet a clear sell'
        else:
            recommendation = '🔴 SELL'
            explanation = 'Weak signals from both technical and fundamental analysis'

        # Calculate confidence
        confidence = min(100, abs(combined_score - 50) * 2)

        return {
            'symbol': symbol,
            'recommendation': recommendation,
            'combined_score': combined_score,
            'confidence': confidence,
            'explanation': explanation,
            'technical_score': tech_score,
            'technical_interpretation': tech_interp,
            'fundamental_score': fund_score,
            'fundamental_interpretation': fund_interp,
            'technical_analysis': tech_analysis,
            'fundamental_analysis': fund_analysis,
        }
    except Exception as e:
        return {'error': f'Could not generate recommendation: {str(e)}'}

