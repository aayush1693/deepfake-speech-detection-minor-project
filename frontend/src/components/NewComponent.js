import React from 'react';
import { Container, Typography, Button, makeStyles } from '@material-ui/core';
import { useTheme } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  root: {
    padding: theme.spacing(4),
    textAlign: 'center',
  },
  button: {
    marginTop: theme.spacing(2),
  },
}));

const NewComponent = () => {
  const classes = useStyles();
  const theme = useTheme();

  return (
    <Container className={classes.root}>
      <Typography variant="h4" gutterBottom>
        New Reusable Component
      </Typography>
      <Typography variant="body1" gutterBottom>
        This is a new reusable component to improve the design of the app.
      </Typography>
      <Button variant="contained" color="primary" className={classes.button}>
        Click Me
      </Button>
    </Container>
  );
};

export default NewComponent;
