import React from 'react';
import { Route, Redirect } from 'react-router-dom';

import authServices from '../../services/auth.service';

/***
 *  Private Route for Authentication purposes
 */

const PrivateRoute = ({ component: Component, ...rest }) => {
    return (
        <Route
            {...rest}
            render={props => {

                const user = authServices.getUser();

                if (!user) {
                    return <Redirect to={{
                        pathname: '/login/',
                        state: { from: props.location }
                    }}/>
                }

                return <Component {...props} />
            }}
        />
    );
};

// Exporting the router
export default PrivateRoute;
