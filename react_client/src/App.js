import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import Login from './components/auth/Login';
import SignUp from './components/auth/Registration';

/***
 *  Application interface
 */

const App = () => {
  return (
      <Router>
        {/* Public Routes */}
        <Route path="/login/:token?" component={Login}/>
        <Route path="/signUp/" component={SignUp}/>

      </Router>
  );
};

// Exporting the App
export default App;
