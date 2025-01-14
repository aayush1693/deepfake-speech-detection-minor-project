import React from 'react';
import { Container, Typography, Button, Grid, makeStyles } from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
  heroSection: {
    backgroundColor: theme.palette.primary.main,
    color: theme.palette.primary.contrastText,
    padding: theme.spacing(8, 0),
    textAlign: 'center',
  },
  ctaButton: {
    marginTop: theme.spacing(4),
  },
  featuresSection: {
    padding: theme.spacing(8, 0),
  },
  featureItem: {
    textAlign: 'center',
    padding: theme.spacing(2),
  },
}));

const Home = () => {
  const classes = useStyles();

  return (
    <div>
      <div className={classes.heroSection}>
        <Container>
          <Typography variant="h2" component="h1" gutterBottom>
            Welcome to Deepfake Speech Detection
          </Typography>
          <Typography variant="h5" component="p" gutterBottom>
            Detect deepfake audio with ease and accuracy.
          </Typography>
          <Button variant="contained" color="secondary" className={classes.ctaButton}>
            Get Started
          </Button>
        </Container>
      </div>
      <div className={classes.featuresSection}>
        <Container>
          <Typography variant="h4" component="h2" gutterBottom>
            Features
          </Typography>
          <Grid container spacing={4}>
            <Grid item xs={12} sm={6} md={4} className={classes.featureItem}>
              <Typography variant="h6" component="h3">
                Deepfake Detection
              </Typography>
              <Typography variant="body1">
                Analyze audio files to detect deepfake content with high confidence.
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6} md={4} className={classes.featureItem}>
              <Typography variant="h6" component="h3">
                Audio Transcription
              </Typography>
              <Typography variant="body1">
                Transcribe audio files using advanced machine learning models.
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6} md={4} className={classes.featureItem}>
              <Typography variant="h6" component="h3">
                User-Friendly Interface
              </Typography>
              <Typography variant="body1">
                Enjoy a modern and responsive user interface designed for ease of use.
              </Typography>
            </Grid>
          </Grid>
        </Container>
      </div>
    </div>
  );
};

export default Home;
