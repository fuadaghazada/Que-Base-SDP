import React, { Component } from 'react';
import UserPreview from "./UserPreview";

import pagination from '../utils/pagination';

/***
 *  Filter questions component
 */

class UserContainer extends Component {

    /**
     *  Constructor
     */

    constructor(props) {
        super(props);
        this.state = {

            hasData: false,
            numberOfPages: null,
        };
    }

    componentDidMount() {
        if (this.props['users'] && this.props['handleRequest'] ) {
            this.setState({hasData: true})
        }
    }


    /**
     *  Rendering the question previews
     */

    renderUserPreviews = () => {
        const data = this.props['users']['data'];

        if (data.length === 0)
            return <p>No results</p>;

        return data.map(user => (
            <UserPreview
                key={user['_id']}
                data={user}
            />
        ))
    };


    /**
     *  Updating the page - updating the data according to it
     *
     *  @param number - page number
     */

    updatePageNumber = (number) => {

        const handleRequest = this.props['handleRequest'];
        handleRequest(number);
    };


    /**
     *  Rendering the pagination buttons/links
     */

    renderPaginationLinks = () => {

        const currentPage = this.props['page'];
        const numberOfPages =  this.props['users']['numberOfPages'];
        const pageNumbers = pagination.generatePaginationList(numberOfPages, currentPage);

        // Creating buttons from page numbers
        return pageNumbers.map(number => {

            if (number) {
                return <button
                            key={number}
                            value={number}
                            onClick={() => this.updatePageNumber(number)}
                        >
                            {number}
                        </button>
            }
            return <button key={number}>...</button>
        })
    };

    render() {
        if (this.state.hasData) {
            return (
                <div>

                    <h1>Users</h1>
                    {this.renderUserPreviews()}
                    {this.renderPaginationLinks()}
                </div>
            );
        }

        return <div></div>

    }

}

// Exporting the component
export default UserContainer
