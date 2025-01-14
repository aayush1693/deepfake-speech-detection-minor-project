import React from 'react';
import { Container, Typography, TextField, Button, Link, Paper } from '@material-ui/core';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

function Login() {
  return (
    <>
      <Navbar />
      <Container maxWidth="sm">
        <Paper style={{ padding: '2rem', margin: '2rem 0' }}>
          <Typography variant="h4" gutterBottom>
            Login
          </Typography>
          <form>
            <TextField label="Email" fullWidth margin="normal" />
            <TextField label="Password" type="password" fullWidth margin="normal" />
            <Button variant="contained" color="primary" fullWidth>
              Login
            </Button>
            <Link href="/password-reset">Forgot Password?</Link>
            <Link href="/signup">Don't have an account? Sign up</Link>
          </form>
        </Paper>
      </Container>
      <Footer />
    </>
  );
}

export default Login;
