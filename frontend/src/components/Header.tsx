import React, { useState } from 'react';

interface HeaderProps {
  onSearch: (query: string) => void;
  onNavigate: (page: 'dashboard' | 'detail') => void;
}

export const Header: React.FC<HeaderProps> = ({ onSearch, onNavigate }) => {
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      onSearch(searchQuery);
      setSearchQuery('');
    }
  };

  const handleLogoClick = () => {
    setSearchQuery('');
    onNavigate('dashboard');
  };

  return (
    <header style={styles.header}>
      <div className="container">
        <div className="flex-between">
          <div style={styles.logo} onClick={handleLogoClick}>
            <h1 style={styles.title}>🕌 HalalVest</h1>
            <p style={styles.subtitle}>Halal Stock Tracker</p>
          </div>

          <form onSubmit={handleSearch} style={styles.searchForm}>
            <input
              type="text"
              className="input"
              placeholder="Search stocks (e.g., AAPL, MSFT)"
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              style={styles.searchInput}
            />
            <button type="submit" className="button" style={styles.searchButton}>
              Search
            </button>
          </form>
        </div>
      </div>
    </header>
  );
};

const styles = {
  header: {
    backgroundColor: 'var(--gray-900)',
    borderBottom: '1px solid var(--gray-700)',
    padding: '1rem 0',
    position: 'sticky' as const,
    top: 0,
    zIndex: 100,
  },
  logo: {
    cursor: 'pointer',
    transition: 'opacity 0.2s',
  },
  title: {
    fontSize: '1.5rem',
    marginBottom: '0rem',
    color: 'var(--primary)',
  },
  subtitle: {
    fontSize: '0.75rem',
    color: 'var(--text-muted)',
    marginBottom: '0',
  },
  searchForm: {
    display: 'flex',
    gap: '0.5rem',
    maxWidth: '400px',
  } as React.CSSProperties,
  searchInput: {
    flex: 1,
  },
  searchButton: {
    whiteSpace: 'nowrap' as const,
  },
};
