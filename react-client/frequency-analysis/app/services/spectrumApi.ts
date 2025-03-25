import { SpectrumData } from '../types/spectrum';

export const fetchSpectrumData = (): Promise<SpectrumData[]> => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve([
        {
          "provider": "Local AM stations",
          "strength": 0.34,
          "technology": "Analog AM",
          "service": "AM Radio Broadcasting",
          "frequency_range": "1 MHz"
        },
        // ... paste the rest of your data here ...
      ]);
    }, 2000); // 2 second delay
  });
}; 