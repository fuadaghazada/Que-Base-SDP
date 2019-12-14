import React, { Component } from 'react';
import { Redirect } from "react-router-dom";

import {InputBase} from "@material-ui/core";
import SearchIcon from "@material-ui/core/SvgIcon/SvgIcon";

/**
 *  Search component (Generic as possible
 */

class Search extends Component {

    constructor(props) {
        super(props);
        this.state = {

            searchValue: null,
            redirect: false,
        };
    }

    handleChange = (e) => {
        if (e.target.value !== "") {
            this.setState({[e.target.name]: e.target.value})
        } else {
            this.setState({[e.target.name]: null})
        }
    };

    handleSearch = (e) => {
        const {searchValue} = this.state;

        if (searchValue && e.keyCode === 13) {
            this.setState({redirect: true})
        }
    };

    render() {
        const {styles} = this.props;
        const { searchValue, redirect } = this.state;

        if (redirect) {
            return <Redirect to={`/searchUsers/${searchValue}`}/>
        }

        return (
            <div className={styles.search}>
                <div className={styles.searchIcon}>
                    <SearchIcon />
                </div>
                <InputBase
                    placeholder="Search username…"
                    name={"searchValue"}
                    onChange={this.handleChange}
                    onKeyDown={this.handleSearch}
                    classes={{
                        root: styles.inputRoot,
                        input: styles.inputInput,
                    }}
                    inputProps={{ 'aria-label': 'search' }}
                />
            </div>
        )
    }


}

// Exporting the component
export default Search;
