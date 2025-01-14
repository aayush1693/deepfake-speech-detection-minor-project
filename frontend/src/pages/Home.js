import React from 'react';
import { Container, Typography, Button, Grid, Paper, makeStyles } from '@material-ui/core';
import { useSpring, animated } from 'react-spring';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

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
  const fadeIn = useSpring({ opacity: 1, from: { opacity: 0 } });

  return (
    <>
      <Navbar />
      <animated.div style={fadeIn} className={classes.heroSection}>
        <Container maxWidth="lg">
          <Typography variant="h2" gutterBottom>
            Uncover the Truth Behind Audio Files
          </Typography>
          <Typography variant="h5" gutterBottom>
            Easily detect manipulated or synthetic audio content with our advanced detection tool.
          </Typography>
          <Button variant="contained" color="secondary" href="/signup" className={classes.ctaButton}>
            Get Started
          </Button>
        </Container>
      </animated.div>
      <Container maxWidth="lg" className={classes.featuresSection}>
        <Grid container spacing={4}>
          <Grid item xs={12} md={4}>
            <Paper className={classes.featureItem}>
              <Typography variant="h6">Audio Analysis</Typography>
              <Typography>Analyze audio files for deepfake detection.</Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper className={classes.featureItem}>
              <Typography variant="h6">Real-Time Results</Typography>
              <Typography>Get results instantly after uploading your audio file.</Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper className={classes.featureItem}>
              <Typography variant="h6">Secure Platform</Typography>
              <Typography>Your data is safe with us.</Typography>
            </Paper>
          </Grid>
        </Grid>
      </Container>
      <Container maxWidth="lg">
        <Paper style={{ padding: '2rem', margin: '2rem 0' }}>
          <Typography variant="h4" gutterBottom>
            Testimonials
          </Typography>
          <Typography>"This tool is amazing!" - User A</Typography>
          <Typography>"Highly recommend for detecting deepfake audio." - User B</Typography>
        </Paper>
      </Container>
      <Footer />
    </>
  );
};

export default Home;
