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
 *  [POST]
 */

const updateUser = (data) => {

    // Preparing the request URL
    let requestURL = `${USERS_API_URL}/updateUser`;
    // Headers
    const headers = {...{'Content-Type': 'application/json'}, ...getHeaders.auth()};

    // Sending POST request
    return axios({
        method: 'post',
        headers: headers,
        url: requestURL,
        data: data
    })
        .then(response => {

            return response.data;
        })
        .catch(err => console.log(err));
};

/**
 *  [GET]
 */

const getFriends = (page = null, id) => {

    let requestURL = `${USERS_API_URL}/getFriends`;

    if (id && typeof(id) === 'string')
        requestURL += `?id=${id}`;

    if (page && typeof(page) === 'number')
        requestURL += `&page=${page}`;

    // Headers
    const headers = {...{'Content-Type': 'application/json'}, ...getHeaders.auth()};

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
 *  [GET]
 */

const getWaitList = (page = null, id) => {

    let requestURL = `${USERS_API_URL}/getWaitList`;

    if (id && typeof(id) === 'string')
        requestURL += `?id=${id}`;

    if (page && typeof(page) === 'number')
        requestURL += `&page=${page}`;

    // Headers
    const headers = {...{'Content-Type': 'application/json'}, ...getHeaders.auth()};

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
    getUser: getUser,
    updateUser: updateUser
};
