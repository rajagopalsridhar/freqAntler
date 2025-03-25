export interface SpectrumData {
  provider: string;
  strength: number;
  technology: string;
  service: string;
  frequency_range: string;
}

export interface ApiResponse {
  signal_strengths: number[];
  frequency: number[];
  frequency_report: {
    frequencyReports: SpectrumData[];
  };
} 