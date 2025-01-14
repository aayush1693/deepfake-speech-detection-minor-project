import React, { useState } from 'react';
import { Container, Typography, Button, Grid, Paper, CircularProgress } from '@material-ui/core';
import { DropzoneArea } from 'material-ui-dropzone';
import axios from 'axios';

const Dashboard = () => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [history, setHistory] = useState([]);

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
      console.error('Error uploading file:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      <Paper style={{ padding: 16 }}>
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
      </Paper>
      {results && (
        <Paper style={{ padding: 16, marginTop: 16 }}>
          <Typography variant="h6">Results</Typography>
          <Typography>Confidence Score: {results.confidenceScore}</Typography>
          <Typography>Transcription: {results.transcription}</Typography>
          <Typography>Analysis Breakdown: {results.analysisBreakdown}</Typography>
        </Paper>
      )}
      <Paper style={{ padding: 16, marginTop: 16 }}>
        <Typography variant="h6">History</Typography>
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
  );
};

export default Dashboard;
