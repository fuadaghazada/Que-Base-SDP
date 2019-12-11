import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import PrivateRoute from './components/custom/PrivateRoute'
import Login from './components/auth/Login';
import SignUp from './components/auth/Registration';
import Home from "./components/Home";
import UploadQuestion from "./components/questions/UploadQuestion";
import FilterQuestions from "./components/questions/FilterQuestions";
import UserDetails from "./components/users/UserDetails";
import QuestionDetails from "./components/questions/QuestionDetails";
import FriendRequests from "./components/users/FriendRequests";

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
        <PrivateRoute path={'/uploadQuestion'} component={UploadQuestion} />
        <PrivateRoute path={'/filterQuestions'} component={FilterQuestions} />
        <PrivateRoute path={'/userDetails/:id?'} component={UserDetails} />
        <PrivateRoute path={'/questionDetails/:id'} component={QuestionDetails} />
        <PrivateRoute path={'/friendRequests'} component={FriendRequests} />

      </Router>
  );
};

// Exporting the App
export default App;
