import authServices from '../services/auth.service';

/***
 *  Helper function for getting the Authorization header
 */

const authHeaders = () => {
    // Getting the user
    const user = authServices.getUser();

    if (user && user.token) {
        return {
            Authorization: `Bearer ${user.token}`
        };
    } else {
        return {};
    }
};

// Exporting the functions
export default {
    auth: authHeaders
};
