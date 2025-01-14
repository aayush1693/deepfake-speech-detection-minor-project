import React from 'react';
import { makeStyles } from '@material-ui/core';
import AppRoutes from './routes';

const useStyles = makeStyles((theme) => ({
  content: {
    marginLeft: 240,
    padding: theme.spacing(3),
  },
}));

const App = () => {
  const classes = useStyles();

  return (
    <div>
      <main className={classes.content}>
        <AppRoutes />
      </main>
    </div>
  );
};

export default App;
