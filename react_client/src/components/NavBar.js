import React from 'react';

import { makeStyles, fade } from '@material-ui/core/styles';
import FilterListIcon from '@material-ui/icons/FilterList';
import PersonIcon from '@material-ui/icons/Person';
import HomeIcon from '@material-ui/icons/Home';
import NotificationsIcon from '@material-ui/icons/Notifications';
import SearchIcon from '@material-ui/icons/Search';
import {AppBar, Toolbar, Link, Typography} from '@material-ui/core';

import SignOut from "./auth/SignOut";
import Search from "./Search";


// Styles
const useStyles = makeStyles( theme => ({
    root: {
        marginBottom: "50px"
    },
    item: {
        color: "white",
        textAlign: "center",
        textDecoration: "none",
        '&:hover': {
            textDecoration: "none",
            backgroundColor: fade(theme.palette.common.white, 0.25),
        },
        padding: "20px",
        paddingTop: "30px"
    },
    search: {
        position: 'relative',
        borderRadius: theme.shape.borderRadius,
        backgroundColor: fade(theme.palette.common.white, 0.15),
        '&:hover': {
            backgroundColor: fade(theme.palette.common.white, 0.25),
        },
        marginLeft: 0,
        width: '100%',
        [theme.breakpoints.up('sm')]: {
            marginLeft: theme.spacing(1),
            width: 'auto',
        }
    },
    searchIcon: {
        width: theme.spacing(7),
        height: '100%',
        position: 'absolute',
        pointerEvents: 'none',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    },
    inputRoot: {
        color: 'inherit',
    },
    inputInput: {
        padding: theme.spacing(1, 1, 1, 7),
        transition: theme.transitions.create('width'),
        width: '100%',
        [theme.breakpoints.up('sm')]: {
            width: 120,
            '&:focus': {
                width: 200,
            },
        },
    }
  }));


/***
 *  Navigation Bar
 */

const NavBar = () => {

    const styles = useStyles();

    // NavBar render
    return (

      <AppBar position="static" className={styles.root}>
        <Toolbar>

            {/* Links */}
            <Link  href='/' className={styles.item}>
                <HomeIcon />
                <Typography>Home</Typography>
            </Link>

            <Link  href='/findQuestion' className={styles.item}>
                <SearchIcon />
                <Typography>Find Question</Typography>
            </Link>

            <Link  href='/filterQuestions' className={styles.item}>
                <FilterListIcon />
                <Typography>Filter Questions</Typography>
            </Link>

            <Link  href='/userDetails' className={styles.item}>
                <PersonIcon />
                <Typography>User Details</Typography>
            </Link>

            <Link  href='/friendRequests' className={styles.item}>
                <NotificationsIcon />
                <Typography>Friend Requests</Typography>
            </Link>

            {/* Search bar */}
            <Search styles={styles}/>

            {/* Sign out */}
            <SignOut/>
        </Toolbar>
      </AppBar>

    );
};

export default NavBar
