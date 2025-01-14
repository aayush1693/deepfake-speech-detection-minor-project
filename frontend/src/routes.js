import React from 'react';
import { Route, Switch } from 'react-router-dom';
import Home from './pages/Home';
import Login from './pages/Login';
import Signup from './pages/Signup';
import PasswordReset from './pages/PasswordReset';
import Dashboard from './pages/Dashboard';

const AppRoutes = () => {
  return (
    <Switch>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/password-reset" element={<PasswordReset />} />
      <Route path="/dashboard" element={<Dashboard />} />
    </Switch>
  );
};

export default AppRoutes;
