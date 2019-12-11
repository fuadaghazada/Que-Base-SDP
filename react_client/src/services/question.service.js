import axios from 'axios';
// import jwt_decode from 'jwt-decode';

import getHeaders from '../utils/getHeaders';

/***
 *  Handling Question services
 */

const QUESTIONS_API_URL = "http://localhost:8000/questions";     // TODO: This should be handled by 'setupProxy'

/**
 *  [POST] Find Similar Questions
 */

const findSimilarQuestions = (data, page = null, threshold = null) => {

    // Preparing the request URL
    let requestURL = `${QUESTIONS_API_URL}/findSimilarQuestions`;

    if (page && typeof(page) === 'number')
        requestURL += `?page=${page}`;

    if (threshold && typeof(threshold) === 'number')
        requestURL += `&threshold=${threshold}`;

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
 *  [POST]
 */

const getQuestions = (data, page = null) => {

    // Preparing the request URL
    let requestURL = `${QUESTIONS_API_URL}/getQuestions`;

    if (page && typeof(page) === 'number')
        requestURL += `?page=${page}`;

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

const getQuestion = (id) => {

    // Preparing the request URL
    let requestURL = `${QUESTIONS_API_URL}/getQuestion`;

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

const getUserQuestions = (id, page = null) => {

    // Preparing the request URL
    let requestURL = `${QUESTIONS_API_URL}/getUserQuestions`;

    if (id && typeof(id) === 'string')
        requestURL += `?id=${id}`;

    if (page && typeof(page) === 'number')
        requestURL += `&page=${page}`;

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

const favoriteQuestion = (id) => {

    // Preparing the request URL
    let requestURL = `${QUESTIONS_API_URL}/favoriteQuestion`;

    if (id && typeof(id) === 'string')
        requestURL += `?id=${id}`;

    // Headers
    const headers = {...{'Content-Type': 'application/json'}, ...getHeaders.auth()};

    // Sending POST request
    return axios({
        method: 'post',
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

const postInsertQuestion = (data) => {

    // Preparing the request URL
    let requestURL = `${QUESTIONS_API_URL}/insertQuestion`;

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
 *  Exporting the services
 */

export default {
    findSimilarQuestions: findSimilarQuestions,
    getQuestions: getQuestions,
    getQuestion: getQuestion,
    getUserQuestions: getUserQuestions,
    favoriteQuestion: favoriteQuestion,
    postInsertQuestion: postInsertQuestion
};
