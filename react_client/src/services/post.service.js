import axios from 'axios';

import getHeaders from '../utils/getHeaders';

/***
 *  Handling Post services
 */

const POST_API_URL = "http://localhost:8000/posts";     // TODO: This should be handled by 'setupProxy'


/**
 *  [GET]
 */

const getPost = (id) => {

    // Preparing the request URL
    let requestURL = `${POST_API_URL}/getPost`;

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
 *  [GET]
 */

const getPosts = () => {

    // Preparing the request URL
    let requestURL = `${POST_API_URL}/getPosts`;

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
    getPost: getPost,
    getPosts: getPosts
};
