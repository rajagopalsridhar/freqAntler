'use client';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { SpectrumData } from '../types/spectrum';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface Props {
  data: SpectrumData[];
}

export default function SpectrumChart({ data }: Props) {
  const chartData = {
    labels: data.map(d => d.frequency_range),
    datasets: [
      {
        label: 'Signal Strength',
        data: data.map(d => d.strength),
        borderColor: '#3498db',
        backgroundColor: 'rgba(52, 152, 219, 0.2)',
        borderWidth: 2,
        pointBackgroundColor: '#3498db',
        tension: 0.1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
        labels: {
          color: '#fff'
        }
      },
      title: {
        display: true,
        text: 'Frequency Spectrum Analysis',
        color: '#fff'
      },
    },
    scales: {
      y: {
        title: {
          display: true,
          text: 'Signal Strength (dB)',
          color: '#fff'
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)'
        },
        ticks: {
          color: '#fff'
        }
      },
      x: {
        title: {
          display: true,
          text: 'Frequency Range',
          color: '#fff'
        },
        grid: {
          color: 'rgba(255, 255, 255, 0.1)'
        },
        ticks: {
          color: '#fff'
        }
      },
    },
  };

  return <Line data={chartData} options={options} />;
} 