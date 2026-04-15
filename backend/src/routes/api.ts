import { Router, Request, Response } from 'express';
import { stockService } from '../services/stockService';
import { analysisService } from '../services/analysisService';
import { halalScreeningService } from '../services/halalScreening';

const router = Router();

// Get stock analysis with technical and fundamental indicators
router.get('/stocks/:symbol', async (req: Request, res: Response) => {
  try {
    const { symbol } = req.params;
    const upperSymbol = symbol.toUpperCase();

    // Get stock data and historical data in parallel
    const [stockData, historicalData] = await Promise.all([
      stockService.getStockData(upperSymbol),
      stockService.getHistoricalData(upperSymbol),
    ]);

    // Analyze technical indicators
    const technical = analysisService.analyzeTechnical(historicalData, stockData.price);

    // Analyze fundamental metrics
    const fundamental = analysisService.analyzeFundamental({
      pe: stockData.pe,
      eps: stockData.eps,
      debtToEquity: 0.5, // Default value - would come from financial API
      roe: 15, // Default value
      profitMargin: 10, // Default value
    });

    // Get recommendation
    const { recommendation, confidence } = analysisService.getRecommendation(
      technical.technicalScore,
      fundamental.fundamentalScore
    );

    // Screen for halal compliance
    const halalScreening = halalScreeningService.screenStock(upperSymbol, {
      name: stockData.name,
      sector: '', // Would come from detailed company data
      industry: '', // Would come from detailed company data
      debtToEquity: 0.5,
      dividendYield: stockData.dividend / stockData.price,
    });

    res.json({
      symbol: upperSymbol,
      name: stockData.name,
      price: stockData.price,
      change: stockData.change,
      changePercent: stockData.changePercent,
      marketCap: stockData.marketCap,
      volume: stockData.volume,
      high52week: stockData.high52week,
      low52week: stockData.low52week,
      technical,
      fundamental,
      recommendation,
      confidence,
      halal: halalScreening,
      historical: historicalData.slice(-100), // Last 100 days for chart
    });
  } catch (error) {
    console.error('Error fetching stock analysis:', error);
    res.status(500).json({ error: 'Failed to fetch stock analysis' });
  }
});

// Search for stocks
router.get('/search/:query', async (req: Request, res: Response) => {
  try {
    const { query } = req.params;
    const results = await stockService.searchStocks(query);
    res.json(results);
  } catch (error) {
    console.error('Error searching stocks:', error);
    res.status(500).json({ error: 'Failed to search stocks' });
  }
});

// Get halal stocks list
router.get('/halal-stocks', async (req: Request, res: Response) => {
  try {
    const halalStocks = halalScreeningService.getHalalStocksList();

    // Get data for top 15 halal stocks
    const topStocks = halalStocks.slice(0, 15);
    const stocksData = await Promise.all(
      topStocks.map(async symbol => {
        try {
          const data = await stockService.getStockData(symbol);
          return {
            symbol,
            name: data.name,
            price: data.price,
            changePercent: data.changePercent,
          };
        } catch {
          return null;
        }
      })
    );

    res.json({
      total: halalStocks.length,
      featured: stocksData.filter(s => s !== null),
      allSymbols: halalStocks,
    });
  } catch (error) {
    console.error('Error fetching halal stocks:', error);
    res.status(500).json({ error: 'Failed to fetch halal stocks' });
  }
});

// Batch get multiple stocks (for dashboard)
router.post('/batch', async (req: Request, res: Response) => {
  try {
    const { symbols } = req.body;

    if (!Array.isArray(symbols) || symbols.length === 0) {
      return res.status(400).json({ error: 'Please provide array of symbols' });
    }

    const results = await Promise.all(
      symbols.slice(0, 20).map(async symbol => {
        try {
          const data = await stockService.getStockData(symbol.toUpperCase());
          return {
            symbol: symbol.toUpperCase(),
            name: data.name,
            price: data.price,
            changePercent: data.changePercent,
            marketCap: data.marketCap,
          };
        } catch {
          return null;
        }
      })
    );

    res.json(results.filter(s => s !== null));
  } catch (error) {
    console.error('Error fetching batch stocks:', error);
    res.status(500).json({ error: 'Failed to fetch stocks' });
  }
});

export default router;
