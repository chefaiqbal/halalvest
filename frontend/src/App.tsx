import React, { useState } from 'react';
import './index.css';
import { Header } from './components/Header';
import { Dashboard } from './pages/Dashboard';
import { StockDetail } from './pages/StockDetail';

type PageType = 'dashboard' | 'detail';

function App() {
  const [currentPage, setCurrentPage] = useState<PageType>('dashboard');
  const [selectedSymbol, setSelectedSymbol] = useState<string>('');
  const [searchQuery, setSearchQuery] = useState<string>('');

  const handleSearch = (query: string) => {
    setSearchQuery(query);
    setSelectedSymbol(query.toUpperCase());
    setCurrentPage('detail');
  };

  const handleSelectStock = (symbol: string) => {
    setSelectedSymbol(symbol);
    setCurrentPage('detail');
  };

  const handleNavigate = (page: PageType) => {
    setCurrentPage(page);
    setSearchQuery('');
  };

  const handleBack = () => {
    setCurrentPage('dashboard');
    setSelectedSymbol('');
    setSearchQuery('');
  };

  return (
    <>
      <Header onSearch={handleSearch} onNavigate={handleNavigate} />

      {currentPage === 'dashboard' ? (
        <Dashboard onSelectStock={handleSelectStock} searchQuery={searchQuery} />
      ) : (
        <StockDetail symbol={selectedSymbol} onBack={handleBack} />
      )}

      <footer style={styles.footer}>
        <div className="container">
          <p style={styles.disclaimer}>
            ⚠️ <strong>Disclaimer:</strong> HalalVest is for educational purposes only. Not financial advice.
            Always consult a financial advisor and conduct your own research. Stock market involves risk.
          </p>
          <p style={styles.credit}>
            Built with ❤️ | Data from Yahoo Finance | Open Source Project
          </p>
        </div>
      </footer>
    </>
  );
}

const styles = {
  footer: {
    backgroundColor: 'var(--gray-900)',
    borderTop: '1px solid var(--gray-700)',
    padding: '2rem 0',
    marginTop: '4rem',
  },
  disclaimer: {
    fontSize: '0.875rem',
    color: 'var(--text-muted)',
    marginBottom: '0.5rem',
  },
  credit: {
    fontSize: '0.75rem',
    color: 'var(--gray-500)',
    marginBottom: '0',
  },
};

export default App;
