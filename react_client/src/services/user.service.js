import axios from 'axios';
// import jwt_decode from 'jwt-decode';

import getHeaders from '../utils/getHeaders';

/***
 *  Handling User services
 */

const USERS_API_URL = "http://localhost:8000/users";     // TODO: This should be handled by 'setupProxy'

/**
 *  [POST]
 */

const getUser = (id) => {

    // Preparing the request URL
    let requestURL = `${USERS_API_URL}/getUser`;

    if (id && typeof(id) === 'string')
        requestURL += `?id=${id}`;

    // Headers
    const headers = {...{'Content-Type': 'application/json'}, ...getHeaders.auth()};

    // Sending GET request
    return axios({
        method: 'get',
        headers: headers,
        url: requestURL
    })
        .then(response => {
            return response.data;
        })
        .catch(err => console.log(err));
};




/**
 *  Exporting the services
 */

export default {
    getUser: getUser
};