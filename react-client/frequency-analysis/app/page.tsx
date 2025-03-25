'use client';
import { useState } from 'react';
import styles from './page.module.css';
import LoadingSpinner from './components/LoadingSpinner';
import SpectrumChart from './components/SpectrumChart';
import SpectrumSummary from './components/SpectrumSummary';
import { fetchSpectrumData } from './services/spectrumApi';
import { ApiResponse } from './types/spectrum';

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<ApiResponse | null>(null);

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const spectrumData = await fetchSpectrumData();
      setData(spectrumData);
    } catch (error) {
      console.error('Failed to fetch spectrum data:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.page}>
      <div className={`${styles.gradientBg} ${(loading || data) ? styles.active : ''}`} />
      <main className={styles.main}>
        {!loading && !data && (
          <button className={styles.analyzeButton} onClick={handleAnalyze}>
            Analyze
          </button>
        )}
        
        {loading && <LoadingSpinner />}
        
        {data && (
          <>
            <div className={styles.chartContainer}>
              <SpectrumChart 
                frequencies={data.frequency}
                signalStrengths={data.signal_strengths}
              />
            </div>
            <SpectrumSummary data={data.frequency_report.frequencyReports} />
          </>
        )}
      </main>
    </div>
  );
}
