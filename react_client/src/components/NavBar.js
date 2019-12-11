import React from 'react';

import { makeStyles } from '@material-ui/core/styles';
import FilterListIcon from '@material-ui/icons/FilterList';
import PersonIcon from '@material-ui/icons/Person';
import HomeIcon from '@material-ui/icons/Home';
import PublishIcon from '@material-ui/icons/Publish';
import {AppBar, Toolbar, Link, Typography} from '@material-ui/core';

import SignOut from "./auth/SignOut";


// Styles
const useStyles = makeStyles( theme => ({
    root: {
        padding: "10px",
        marginBottom: "50px"
    },
    item: {
        color: "white",
        textAlign: "center",
        marginRight: "50px",
        textDecoration: "none"
    }
  }));


/***
 *  Navigation Bar
 */

const NavBar = () => {

    const styles = useStyles();

    return (

      <AppBar position="static" className={styles.root}>
        <Toolbar>
            <Link  href='/' className={styles.item}>
                <HomeIcon />
                <Typography>Home</Typography>
            </Link>

            <Link  href='/uploadQuestion' className={styles.item}>
                <PublishIcon />
                <Typography>Upload Question</Typography>
            </Link>

            <Link  href='/filterQuestions' className={styles.item}>
                <FilterListIcon />
                <Typography>Filter Questions</Typography>
            </Link>

            <Link  href='/userDetails' className={styles.item}>
                <PersonIcon />
                <Typography>User Details</Typography>
            </Link>

            <SignOut/>
        </Toolbar>
      </AppBar>

    );
};

export default NavBar
