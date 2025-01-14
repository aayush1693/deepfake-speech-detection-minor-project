import React from 'react';
import { Container, Typography, TextField, Button, Link, Paper, Checkbox, FormControlLabel, makeStyles } from '@material-ui/core';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { useTheme } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  container: {
    marginTop: theme.spacing(4),
  },
  paper: {
    padding: theme.spacing(4),
    margin: theme.spacing(2, 0),
  },
  form: {
    marginTop: theme.spacing(2),
  },
  submit: {
    marginTop: theme.spacing(2),
  },
  link: {
    marginTop: theme.spacing(1),
    display: 'block',
  },
}));

function Signup() {
  const classes = useStyles();
  const theme = useTheme();

  return (
    <>
      <Navbar />
      <Container maxWidth="sm" className={classes.container}>
        <Paper className={classes.paper}>
          <Typography variant="h4" gutterBottom>
            Sign Up
          </Typography>
          <form className={classes.form}>
            <TextField label="Name" fullWidth margin="normal" />
            <TextField label="Email" fullWidth margin="normal" />
            <TextField label="Password" type="password" fullWidth margin="normal" />
            <TextField label="Confirm Password" type="password" fullWidth margin="normal" />
            <FormControlLabel
              control={<Checkbox name="terms" />}
              label="Accept Terms and Conditions"
            />
            <Button variant="contained" color="primary" fullWidth className={classes.submit}>
              Sign Up
            </Button>
            <Link href="/login" className={classes.link}>Already have an account? Login</Link>
          </form>
        </Paper>
      </Container>
      <Footer />
    </>
  );
}

export default Signup;
