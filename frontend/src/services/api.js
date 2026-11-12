import axios from 'axios';

// Point at the Flask service directly in development, or through a proxy
// (REACT_APP_API_URL) in production builds.
const baseURL = process.env.REACT_APP_API_URL || '';

const client = axios.create({
  baseURL,
  timeout: 120000,
});

const errorMessage = (error) => {
  if (error.response && error.response.data && error.response.data.error) {
    return error.response.data.error;
  }
  return 'Could not reach the analysis service. Please try again.';
};

export const analyzeAudio = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const { data } = await client.post('/api/predict', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return data;
  } catch (error) {
    throw new Error(errorMessage(error));
  }
};

export const fetchServiceHealth = async () => {
  const { data } = await client.get('/api/health');
  return data;
};

export default client;
