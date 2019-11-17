import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import PrivateRoute from './components/custom/PrivateRoute'
import Login from './components/auth/Login';
import SignUp from './components/auth/Registration';
import Home from "./components/Home";

/***
 *  Application interface
 */

const App = () => {
  return (
      <Router>
        {/* Public Routes */}
        <Route path="/login/:token?" component={Login}/>
        <Route path="/signUp/" component={SignUp}/>


        {/* Private Routes */}
        <PrivateRoute path={'/'} component={Home} exact />

      </Router>
  );
};

// Exporting the App
export default App;
