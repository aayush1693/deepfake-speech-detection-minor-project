import React, { useState } from 'react';
import { Container, Typography, Button, Grid, Paper, CircularProgress, LinearProgress, Snackbar } from '@material-ui/core';
import { DropzoneArea } from 'material-ui-dropzone';
import axios from 'axios';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import MuiAlert from '@mui/lab/Alert';

function Alert(props) {
  return <MuiAlert elevation={6} variant="filled" {...props} />;
}

const Dashboard = () => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState(null);

  const handleFileChange = (newFiles) => {
    setFiles(newFiles);
  };

  const handleUpload = async () => {
    if (files.length === 0) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', files[0]);

    try {
      const response = await axios.post('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResults(response.data);
      setHistory([...history, response.data]);
    } catch (error) {
      setError('Error uploading file. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setError(null);
  };

  return (
    <>
      <Navbar />
      <Container maxWidth="lg">
        <Paper style={{ padding: '2rem', margin: '2rem 0' }}>
          <Typography variant="h4" gutterBottom>
            Dashboard
          </Typography>
          <Typography variant="h6" gutterBottom>
            Upload Audio File
          </Typography>
          <DropzoneArea
            onChange={handleFileChange}
            acceptedFiles={['audio/*']}
            filesLimit={1}
            dropzoneText="Drag and drop an audio file here or click"
          />
          <Button
            variant="contained"
            color="primary"
            onClick={handleUpload}
            disabled={loading || files.length === 0}
            style={{ marginTop: 16 }}
          >
            {loading ? <CircularProgress size={24} /> : 'Upload'}
          </Button>
          {results && (
            <>
              <LinearProgress variant="determinate" value={results.confidenceScore * 100} />
              <Typography variant="h6" gutterBottom>
                Prediction Score: {results.confidenceScore * 100}%
              </Typography>
              <Typography variant="h6" gutterBottom>
                Audio Transcription: {results.transcription}
              </Typography>
              <Typography variant="h6" gutterBottom>
                Detailed Breakdown
              </Typography>
              <Grid container spacing={4}>
                <Grid item xs={12} md={6}>
                  <Paper style={{ padding: '1rem' }}>
                    <Typography variant="body1">{results.analysisBreakdown}</Typography>
                  </Paper>
                </Grid>
              </Grid>
              <Button variant="contained" color="primary" style={{ marginTop: '1rem' }}>
                Download Report
              </Button>
            </>
          )}
        </Paper>
        <Paper style={{ padding: '2rem', margin: '2rem 0' }}>
          <Typography variant="h4" gutterBottom>
            History
          </Typography>
          {history.length === 0 ? (
            <Typography>No previously analyzed files.</Typography>
          ) : (
            <Grid container spacing={2}>
              {history.map((item, index) => (
                <Grid item key={index} xs={12}>
                  <Typography>File: {item.fileName}</Typography>
                  <Typography>Confidence Score: {item.confidenceScore}</Typography>
                  <Typography>Transcription: {item.transcription}</Typography>
                  <Typography>Analysis Breakdown: {item.analysisBreakdown}</Typography>
                </Grid>
              ))}
            </Grid>
          )}
        </Paper>
      </Container>
      <Snackbar open={!!error} autoHideDuration={6000} onClose={handleClose}>
        <Alert onClose={handleClose} severity="error">
          {error}
        </Alert>
      </Snackbar>
      <Footer />
    </>
  );
};

export default Dashboard;
