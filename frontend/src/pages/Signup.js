import React from 'react';
import { Container, Typography, TextField, Button, Link, Paper, Checkbox, FormControlLabel } from '@material-ui/core';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

function Signup() {
  return (
    <>
      <Navbar />
      <Container maxWidth="sm">
        <Paper style={{ padding: '2rem', margin: '2rem 0' }}>
          <Typography variant="h4" gutterBottom>
            Sign Up
          </Typography>
          <form>
            <TextField label="Name" fullWidth margin="normal" />
            <TextField label="Email" fullWidth margin="normal" />
            <TextField label="Password" type="password" fullWidth margin="normal" />
            <TextField label="Confirm Password" type="password" fullWidth margin="normal" />
            <FormControlLabel
              control={<Checkbox name="terms" />}
              label="Accept Terms and Conditions"
            />
            <Button variant="contained" color="primary" fullWidth>
              Sign Up
            </Button>
            <Link href="/login">Already have an account? Login</Link>
          </form>
        </Paper>
      </Container>
      <Footer />
    </>
  );
}

export default Signup;
