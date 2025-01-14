import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Home from './pages/Home';
import Login from './pages/Login';
import Signup from './pages/Signup';
import PasswordReset from './pages/PasswordReset';
import Dashboard from './pages/Dashboard';
import ManageAccount from './components/ManageAccount';
import Header from './components/Header';
import Footer from './components/Footer';

const App = () => {
  return (
    <Router>
      <Header />
      <Switch>
        <Route exact path="/" component={Home} />
        <Route path="/login" component={Login} />
        <Route path="/signup" component={Signup} />
        <Route path="/password-reset" component={PasswordReset} />
        <Route path="/dashboard" component={Dashboard} />
        <Route path="/manage-account" component={ManageAccount} />
      </Switch>
      <Footer />
    </Router>
  );
};

export default App;
