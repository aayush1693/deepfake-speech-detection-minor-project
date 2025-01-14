import React from 'react';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Home from './pages/Home';
import Login from './pages/Login';
import Signup from './pages/Signup';
import PasswordReset from './pages/PasswordReset';
import Dashboard from './pages/Dashboard';
import ManageAccount from './components/ManageAccount';
import Header from './components/Header';
import Footer from './components/Footer';
import Sidebar from './components/Sidebar';
import Layout from './components/Layout';
import { makeStyles } from '@material-ui/core';

const useStyles = makeStyles((theme) => ({
  content: {
    marginLeft: 240,
    padding: theme.spacing(3),
  },
}));

const App = () => {
  const classes = useStyles();

  return (
    <Router>
      <Header />
      <Sidebar />
      <Layout>
        <main className={classes.content}>
          <Switch>
            <Route path="/" component={Home} />
            <Route path="/login" component={Login} />
            <Route path="/signup" component={Signup} />
            <Route path="/password-reset" component={PasswordReset} />
            <Route path="/dashboard" component={Dashboard} />
            <Route path="/manage-account" component={ManageAccount} />
          </Switch>
        </main>
      </Layout>
      <Footer />
    </Router>
  );
};

export default App;
