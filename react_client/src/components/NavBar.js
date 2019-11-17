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
            <SignOut />
        </div>
    );
};

export default NavBar
