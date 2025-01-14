import React from 'react';
import { Container, Typography, TextField, Button, Link, Paper } from '@material-ui/core';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

function PasswordReset() {
  return (
    <>
      <Navbar />
      <Container maxWidth="sm">
        <Paper style={{ padding: '2rem', margin: '2rem 0' }}>
          <Typography variant="h4" gutterBottom>
            Password Reset
          </Typography>
          <form>
            <TextField label="Email" fullWidth margin="normal" />
            <Button variant="contained" color="primary" fullWidth>
              Send Reset Link
            </Button>
            <Link href="/login">Return to Login</Link>
          </form>
        </Paper>
      </Container>
      <Footer />
    </>
  );
}

export default PasswordReset;
