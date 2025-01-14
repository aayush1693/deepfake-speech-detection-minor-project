import React from 'react';
import { Container, Typography, Link, makeStyles } from '@material-ui/core';
import { useTheme } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  footer: {
    padding: theme.spacing(3, 2),
    marginTop: 'auto',
    backgroundColor: theme.palette.background.paper,
  },
  link: {
    margin: theme.spacing(1),
  },
}));

function Footer() {
  const classes = useStyles();
  const theme = useTheme();

  return (
    <footer className={classes.footer}>
      <Container maxWidth="lg">
        <Typography variant="body1">
          &copy; {new Date().getFullYear()} Deepfake Speech Detection. All rights reserved.
        </Typography>
        <Link href="/privacy-policy" className={classes.link}>Privacy Policy</Link>
        <Link href="/terms-of-service" className={classes.link}>Terms of Service</Link>
        <Link href="https://facebook.com" target="_blank" className={classes.link}>Facebook</Link>
        <Link href="https://twitter.com" target="_blank" className={classes.link}>Twitter</Link>
      </Container>
    </footer>
  );
}

export default Footer;
