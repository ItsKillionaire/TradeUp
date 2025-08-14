const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export interface TrainParams {
  symbol: string;
  start_date?: string;
  end_date?: string;
}

export interface TrainResult {
  message: string;
  accuracy: number;
  error?: string;
}

export const trainAIModel = async (params: TrainParams): Promise<TrainResult> => {
  const queryString = new URLSearchParams();
  queryString.append('symbol', params.symbol);
  if (params.start_date) queryString.append('start_date', params.start_date);
  if (params.end_date) queryString.append('end_date', params.end_date);

  const response = await fetch(`${API_URL}/api/strategy/ai/train?${queryString.toString()}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || 'Failed to train AI model');
  }

  const responseData = await response.json();
  return responseData.data;
};
