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
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Frequency Spectrum Analysis',
      },
    },
    scales: {
      y: {
        title: {
          display: true,
          text: 'Signal Strength (dB)',
        },
      },
      x: {
        title: {
          display: true,
          text: 'Frequency Range',
        },
      },
    },
  };

  return <Line data={chartData} options={options} />;
} 