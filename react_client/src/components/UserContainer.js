import React from 'react';
import {Typography} from "@material-ui/core";

import CustomContainer from './custom/CustomContainer';
import UserPreview from "./UserPreview";


/**
 *  User Container
 */

const UserContainer = (props) => {

    const {users, handleRequest, page} = props;
    const numberOfPages = users['numberOfPages'];

    /**
     *  Rendering the question previews
     */

    const renderUserPreviews = () => {

        const data = users['data'];

        if (data.length === 0)
            return <Typography variant={"h5"}>No results</Typography>;

        return data.map(user => (
            <UserPreview
                key={user['_id']}
                data={user}
            />
        ))
    };

    // Returning the render stuff
    return (
        <CustomContainer header={"Users"}
                         page={page}
                         numberOfPages={numberOfPages}
                         handleRequest={handleRequest}
                         renderPreviews={renderUserPreviews}
        >
        </CustomContainer>
    );
};

// Exporting the component
export default UserContainer
