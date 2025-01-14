import React, { useContext } from 'react';
import { AppBar, Toolbar, Typography, Button, makeStyles, IconButton, Slide, useScrollTrigger } from '@material-ui/core';
import { Link } from 'react-router-dom';
import { ThemeContext } from '../ThemeContext';
import Brightness4Icon from '@material-ui/icons/Brightness4';
import Brightness7Icon from '@material-ui/icons/Brightness7';

const useStyles = makeStyles((theme) => ({
  title: {
    flexGrow: 1,
  },
  link: {
    color: 'inherit',
    textDecoration: 'none',
  },
  appBar: {
    transition: theme.transitions.create(['background-color', 'box-shadow'], {
      duration: theme.transitions.duration.standard,
    }),
  },
  toolbar: {
    display: 'flex',
    justifyContent: 'space-between',
  },
  navLinks: {
    display: 'flex',
    alignItems: 'center',
  },
  navButton: {
    marginLeft: theme.spacing(2),
  },
}));

function HideOnScroll(props) {
  const { children } = props;
  const trigger = useScrollTrigger();

  return (
    <Slide appear={false} direction="down" in={!trigger}>
      {children}
    </Slide>
  );
}

const Header = (props) => {
  const classes = useStyles();
  const { isDarkMode, toggleTheme } = useContext(ThemeContext);

  return (
    <HideOnScroll {...props}>
      <AppBar position="fixed" className={classes.appBar}>
        <Toolbar className={classes.toolbar}>
          <Typography variant="h6" className={classes.title}>
            Deepfake Speech Detection
          </Typography>
          <div className={classes.navLinks}>
            <Button color="inherit" className={classes.navButton}>
              <Link to="/login" className={classes.link}>Login</Link>
            </Button>
            <Button color="inherit" className={classes.navButton}>
              <Link to="/signup" className={classes.link}>Signup</Link>
            </Button>
            <Button color="inherit" className={classes.navButton}>
              <Link to="/manage-account" className={classes.link}>Manage Your Account</Link>
            </Button>
            <IconButton color="inherit" onClick={toggleTheme}>
              {isDarkMode ? <Brightness7Icon /> : <Brightness4Icon />}
            </IconButton>
          </div>
        </Toolbar>
      </AppBar>
    </HideOnScroll>
  );
};

export default Header;
