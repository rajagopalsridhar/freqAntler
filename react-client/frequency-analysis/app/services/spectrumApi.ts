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
        {
          "provider": "Local FM stations (e.g., NPR, iHeart)",
          "strength": -61.53,
          "technology": "Analog FM, HD Radio",
          "service": "FM Radio Broadcasting",
          "frequency_range": "89–107 MHz"
        },
        {
          "provider": "Government, Businesses",
          "strength": -66.43,
          "technology": "Analog FM, P25, DMR",
          "service": "Land Mobile Radio (LMR)",
          "frequency_range": "175–179 MHz"
        },
        {
          "provider": "Businesses, Public Safety",
          "strength": -77.07,
          "technology": "Analog FM, DMR, P25",
          "service": "Land Mobile Radio (LMR)",
          "frequency_range": "451–475 MHz"
        },
        {
          "provider": "T-Mobile",
          "strength": -65.70,
          "technology": "4G LTE, 5G NR",
          "service": "Cellular (600 MHz, Band 71)",
          "frequency_range": "505–645 MHz"
        },
        {
          "provider": "Verizon",
          "strength": -62.40,
          "technology": "4G LTE, 5G NR",
          "service": "Cellular (700 MHz, Band 13)",
          "frequency_range": "729–756 MHz"
        },
        {
          "provider": "AT&T (FirstNet)",
          "strength": -74.73,
          "technology": "4G LTE, 5G NR",
          "service": "Cellular/Public Safety (700 MHz, Band 14)",
          "frequency_range": "757–767 MHz"
        },
        {
          "provider": "Verizon, AT&T",
          "strength": -74.95,
          "technology": "4G LTE",
          "service": "Cellular (800 MHz, Band 5)",
          "frequency_range": "851–894 MHz"
        },
        {
          "provider": "T-Mobile, AT&T",
          "strength": -68.32,
          "technology": "4G LTE, 5G NR",
          "service": "Cellular (AWS-1, Band 4)",
          "frequency_range": "2110–2155 MHz"
        },
        {
          "provider": "WiFi Networks",
          "strength": -55.21,
          "technology": "WiFi 4/5/6",
          "service": "Wireless LAN",
          "frequency_range": "2400–2483 MHz"
        },
        {
          "provider": "Verizon, AT&T, T-Mobile",
          "strength": -71.89,
          "technology": "5G NR",
          "service": "Cellular (C-Band)",
          "frequency_range": "3700–3980 MHz"
        },
        {
          "provider": "WiFi 6E Networks",
          "strength": -82.45,
          "technology": "WiFi 6E",
          "service": "Wireless LAN",
          "frequency_range": "5925–7125 MHz"
        },
        {
          "provider": "Satellite Internet",
          "strength": -89.67,
          "technology": "Starlink",
          "service": "Satellite Communications",
          "frequency_range": "10700–12700 MHz"
        },
        {
          "provider": "Military Radar",
          "strength": -95.12,
          "technology": "Pulse-Doppler Radar",
          "service": "Air Traffic Control",
          "frequency_range": "15700–17700 MHz"
        }
      ]);
    }, 2000);
  });
}; 