import React from 'react';
import { Link } from 'react-router-dom';
import SignOut from "./auth/SignOut";

/***
 *  Navigation Bar
 */

const NavBar = () => {
    return (
        <div>
            <Link to='/'>Home</Link>
            <Link to='/uploadQuestion'>Upload Question</Link>
            <Link to='/filterQuestions'>Filter Questions</Link>
            <Link to='/userDetails'>User Details</Link>
            <SignOut />
        </div>
    );
};

export default NavBar
