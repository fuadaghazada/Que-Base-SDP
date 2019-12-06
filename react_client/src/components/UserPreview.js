import React from 'react';

/**
    User Preview (functional component)
*/

const UserPreview = (props) => {
    console.log(props['data'])

    const {username} = props['data'];
    
    return (
        <div>
            <p>{username}</p>
        </div>
    );
};

// Exporting the component
export default UserPreview;
