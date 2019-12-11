import React from 'react';


const UserOverview = (props) => {

    const { firstname, lastname } = props.userData;

    return (
        <div>
            <h1>{firstname}</h1>
            <h1>{lastname}</h1>
        </div>
    )
};

// Exporting the component
export default UserOverview;
