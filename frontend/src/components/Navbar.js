import React from 'react';
import { AppBar, Toolbar, Typography, Button, makeStyles } from '@material-ui/core';
import { Link } from 'react-router-dom';

const useStyles = makeStyles((theme) => ({
  title: {
    flexGrow: 1,
  },
  link: {
    color: 'inherit',
    textDecoration: 'none',
  },
}));

const Navbar = () => {
  const classes = useStyles();

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" className={classes.title}>
          Deepfake Speech Detection
        </Typography>
        <Button color="inherit">
          <Link to="/login" className={classes.link}>Login</Link>
        </Button>
        <Button color="inherit">
          <Link to="/signup" className={classes.link}>Signup</Link>
        </Button>
        <Button color="inherit">
          <Link to="/manage-account" className={classes.link}>Manage Your Account</Link>
        </Button>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
