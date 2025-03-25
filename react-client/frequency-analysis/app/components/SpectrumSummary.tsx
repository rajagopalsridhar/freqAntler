import { SpectrumData } from '../types/spectrum';
import styles from './SpectrumSummary.module.css';

interface Props {
  data: SpectrumData[];
}

export default function SpectrumSummary({ data }: Props) {
  return (
    <div className={styles.summary}>
      {data.map((item, index) => (
        <div key={index} className={styles.card}>
          <h3>{item.provider}</h3>
          <p><strong>Strength:</strong> {item.strength} dB</p>
          <p><strong>Technology:</strong> {item.technology}</p>
          <p><strong>Service:</strong> {item.service}</p>
          <p><strong>Frequency Range:</strong> {item.frequency_range}</p>
        </div>
      ))}
    </div>
  );
} 