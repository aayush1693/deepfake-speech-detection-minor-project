import React from 'react';
import { Container, Typography, TextField, Button, Link, Paper, makeStyles } from '@material-ui/core';
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

function Login() {
  const classes = useStyles();
  const theme = useTheme();

  return (
    <>
      <Navbar />
      <Container maxWidth="sm" className={classes.container}>
        <Paper className={classes.paper}>
          <Typography variant="h4" gutterBottom>
            Login
          </Typography>
          <form className={classes.form}>
            <TextField label="Email" fullWidth margin="normal" />
            <TextField label="Password" type="password" fullWidth margin="normal" />
            <Button variant="contained" color="primary" fullWidth className={classes.submit}>
              Login
            </Button>
            <Link href="/password-reset" className={classes.link}>Forgot Password?</Link>
            <Link href="/signup" className={classes.link}>Don't have an account? Sign up</Link>
          </form>
        </Paper>
      </Container>
      <Footer />
    </>
  );
}

export default Login;
