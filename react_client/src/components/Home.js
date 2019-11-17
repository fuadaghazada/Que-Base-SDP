import React, { Component } from 'react';
import NavBar from "./NavBar";


/**
    Home Component
*/

class Home extends Component {

    render() {
        return (
            <div>
                <NavBar />
                <h1>Welcome to the home page</h1>
            </div>
        );
    }

}

// Exporting the component
export default Home;
