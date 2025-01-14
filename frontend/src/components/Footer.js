import React from 'react';
import { AppBar, Toolbar, Typography, Link, makeStyles } from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
  footer: {
    top: 'auto',
    bottom: 0,
    backgroundColor: theme.palette.primary.main,
    color: theme.palette.primary.contrastText,
    padding: theme.spacing(2),
  },
  link: {
    color: 'inherit',
    textDecoration: 'none',
    margin: theme.spacing(1),
  },
}));

const Footer = () => {
  const classes = useStyles();

  return (
    <AppBar position="static" className={classes.footer}>
      <Toolbar>
        <Typography variant="body1" align="center" style={{ flexGrow: 1 }}>
          <Link href="/privacy-policy" className={classes.link}>Privacy Policy</Link>
          <Link href="/terms" className={classes.link}>Terms</Link>
          <Link href="/contact" className={classes.link}>Contact</Link>
        </Typography>
      </Toolbar>
    </AppBar>
  );
};

export default Footer;
