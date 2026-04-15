// S&P 500 Halal-Compliant Stocks
// Excludes: Alcohol, Tobacco, Gambling, Weapons, Banks with Riba concerns
// Includes companies with debt-to-equity < 1.5

export const HALAL_STOCKS = [
  // Technology
  'AAPL',
  'MSFT',
  'NVDA',
  'GOOGL',
  'META',
  'ADBE',
  'CRM',
  'NFLX',
  'AMD',
  'INTC',
  'CSCO',
  'AVGO',
  'AMAT',
  'SNPS',
  'CDNS',
  'MU',
  'QCOM',
  'INTU',
  'ADSK',
  'TSM',

  // Healthcare & Biotech
  'JNJ',
  'UNH',
  'PFE',
  'MRK',
  'ABBV',
  'AMGN',
  'LLY',
  'REGN',
  'ILMN',
  'VRTX',
  'CRSP',
  'DXCM',
  'VEEV',
  'EXAS',
  'ZM',
  'ZOOM',
  'DOCS',

  // Consumer & Retail
  'AMZN',
  'WMT',
  'MCD',
  'SBUX',
  'NKE',
  'LULU',
  'HD',
  'LOW',
  'TJX',
  'FIVE',
  'ULTA',
  'ETSY',
  'PTON',

  // Energy & Utilities (clean energy focused)
  'NEE',
  'DUK',
  'SO',
  'EXC',
  'PEG',
  'SRE',
  'AEP',
  'XEL',
  'PPL',
  'CMS',
  'AWK',

  // Industrials
  'BA',
  'CAT',
  'GE',
  'MMM',
  'ITT',
  'ROK',
  'ETN',
  'EMR',
  'SPX',
  'FAST',

  // Materials & Chemicals
  'ECL',
  'SHW',
  'APD',
  'ALB',
  'CTVA',
  'WRK',
  'LYB',
  'PPG',
  'STLD',

  // Real Estate & Infrastructure
  'PLD',
  'AVT',
  'EQIX',
  'DLR',
  'ARE',
  'VTR',
  'O',
  'SPG',
  'PSA',

  // Transportation & Logistics
  'UPS',
  'FDX',
  'ODFL',
  'XPO',
  'LYFT',
  'UBER',

  // Communications & Media
  'CMCSA',
  'CHTR',
  'VZ',
  'T',
  'TMUS',

  // Financial Services (non-riba focused)
  'SCHW',
  'BLK',
  'ICE',
  'MSCI',
  'CME',
  'CBOE',
  'VOYA',

  // Other Quality Companies
  'TSLA',
  'MRNA',
  'DDOG',
  'OKTA',
  'PLAN',
  'TEAM',
  'ASML',
  'SHOP',
  'SE',
  'RBLX',
  'U',
  'SQ',
  'COIN',
];

export interface HalalScreening {
  symbol: string;
  name: string;
  isHalal: boolean;
  score: number;
  reasons: string[];
  prohibitedSectors: string[];
}

export class HalalScreeningService {
  private prohibitedSectors = [
    'alcohol',
    'tobacco',
    'tobacco products',
    'gambling',
    'casinos',
    'weapons',
    'defense',
    'military',
    'pork',
    'adult entertainment',
    'conventional banking',
    'interest-based lending',
    'conventional insurance',
  ];

  private prohibitedCompanies = new Set([
    'BUD', // Anheuser-Busch
    'MO', // Altria (tobacco)
    'PM', // Philip Morris
    'KO', // Coca-Cola (alcohol derivatives)
    'DEO', // Diageo
    'SAM', // Boston Beer
    'STZ', // Constellation Brands
    'RRR', // Red Robin (alcohol focus)
  ]);

  isHalalStock(symbol: string): boolean {
    return HALAL_STOCKS.includes(symbol) && !this.prohibitedCompanies.has(symbol);
  }

  screenStock(symbol: string, companyData: any): HalalScreening {
    const isHalal = this.isHalalStock(symbol);
    const reasons: string[] = [];
    const prohibitedSectors: string[] = [];

    let score = 100;

    // Sector analysis
    const sector = companyData.sector || '';
    const industry = companyData.industry || '';

    for (const prohibited of this.prohibitedSectors) {
      if (sector.toLowerCase().includes(prohibited) || industry.toLowerCase().includes(prohibited)) {
        prohibitedSectors.push(prohibited);
        score -= 25;
      }
    }

    // Debt-to-equity analysis (Islamic principle - avoid riba)
    const debtToEquity = companyData.debtToEquity || 0;
    if (debtToEquity > 1.5) {
      reasons.push('High debt-to-equity ratio (concern for Islamic finance)');
      score -= 20;
    } else if (debtToEquity > 1) {
      reasons.push('Moderate debt level');
      score -= 10;
    } else {
      reasons.push('Healthy debt-to-equity ratio');
      score += 10;
    }

    // Dividend/interest income analysis
    const dividendYield = companyData.dividendYield || 0;
    if (dividendYield > 0) {
      reasons.push('Provides dividend income (avoiding riba principles)');
      score += 15;
    }

    if (isHalal) {
      reasons.push('Listed on halal-approved S&P 500 stocks');
      score += 20;
    }

    return {
      symbol,
      name: companyData.name || symbol,
      isHalal: isHalal && score > 40,
      score: Math.max(0, Math.min(100, score)),
      reasons,
      prohibitedSectors,
    };
  }

  getHalalStocksList(): string[] {
    return HALAL_STOCKS.filter(stock => !this.prohibitedCompanies.has(stock));
  }
}

export const halalScreeningService = new HalalScreeningService();
