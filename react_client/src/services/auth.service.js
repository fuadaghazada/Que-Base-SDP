import axios from 'axios';
import jwt_decode from 'jwt-decode';

import getHeaders from '../utils/getHeaders';

/***
 *  Handling Authentication services
 */

const AUTH_API_URL = "http://localhost:8000/auth";     // TODO: This should be handled by 'setupProxy'


/**
 *  Login
 */

const login = (data) => {

    // Sending POST request
    return axios({
        method: 'post',
        headers: {'Content-Type': 'application/json'},
        url: `${AUTH_API_URL}/login`,
        data: data
    })
        .then(response => {

            setUser(response.data.token);
            return response.data;
        })
        .catch(err => console.log(err));
};

/**
 *  Sign up
 */

const signUp = (data) => {

    // Sending POST request
    return axios({
        method: 'post',
        headers: {'Content-Type': 'application/json' },
        url: `${AUTH_API_URL}/register`,
        data: data
    })
        .then(response => {
            return response.data;
        })
        .catch(err => console.log(err));
};


/**
 *  Setting the user
 */

const setUser = (token) => {
    // Saving to local storage
    if (token)
        localStorage.setItem('userToken', token);
};

/**
 *  Getting user data
 */

const getUser = () => {

    if (localStorage.getItem('userToken')) {
        // Getting token data from saved token
        const userToken = localStorage.getItem('userToken');

        try {
            const decodedUser = jwt_decode(userToken);

            if (new Date().getTime() < decodedUser.exp) {
                localStorage.removeItem('userToken');
                return null;
            }

            // Successful return
            return (userToken) && {
                user: decodedUser,
                token: userToken
            };
        } catch(err) {
            console.log("Invalid token");
            localStorage.removeItem('userToken');
        }
    }
};

/**
 *  Sign out
 */

const signOut = () => {

    // Sending post request
    return axios({
        method: 'post',
        headers: getHeaders.auth(),
        url: `${AUTH_API_URL}/logout`,
    })
        .then(response => {
            if (response.data.success) {

                // Removing the user token from the local storage
                localStorage.removeItem('userToken');
                return { redirect: true };

            } else {
                return { redirect: false };
            }
        })
        .catch(err => {

            console.log(getHeaders.auth())

            console.log(err);
            return { redirect: false };
        });
};


/**
 *  Exporting the services
 */

export default {
    login: login,
    signUp: signUp,
    signOut: signOut,
    getUser: getUser,
    setUser: setUser
};
