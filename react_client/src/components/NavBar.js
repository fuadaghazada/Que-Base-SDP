import React from 'react';
import { Link } from 'react-router-dom';
import SignOut from "./auth/SignOut";
import { makeStyles } from '@material-ui/core/styles';
import BottomNavigation from '@material-ui/core/BottomNavigation';
import BottomNavigationAction from '@material-ui/core/BottomNavigationAction';
import FilterListIcon from '@material-ui/icons/FilterList';
import PersonIcon from '@material-ui/icons/Person';
import { useHistory } from "react-router-dom";
import HomeIcon from '@material-ui/icons/Home';
import PublishIcon from '@material-ui/icons/Publish';

import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';

const useStyles = makeStyles( theme => ({
    root: {
      width: 800,
    },
    menuButton: {
      marginRight: theme.spacing(2),
    },
    title: {
      flexGrow: 1,
    },
  }));

/***
 *  Navigation Bar
 */

const NavBar = () => {
    const classes = useStyles();
    let history = useHistory();
    const redirect = (event, newValue) => {
        
        
        
        // Display the overview of the user
        if (newValue === 0) {
            history.push('/')
        }
        // Display the favorite questions of the user
        else if (newValue === 1) {
            history.push('/uploadQuestion')        }
        // Display the friends of the user
        else if (newValue === 2) {
            history.push('/filterQuestions')
        }  
        else if (newValue === 3) {
            history.push('/userDetails')
        }  
    }

    return (
    /*    <div>
            <Link to='/'>Home</Link>
            <Link to='/uploadQuestion'>Upload Question</Link>
            <Link to='/filterQuestions'>Filter Questions</Link>
            <Link to='/userDetails'>User Details</Link>
            <SignOut />
        </div> */
        <div>
        <BottomNavigation
        onChange={redirect}
        showLabels
        className={classes.root}
        >   
        <BottomNavigationAction label={<Link to='/'>Home</Link>} icon={<HomeIcon />} />
        <BottomNavigationAction label={<Link to='/uploadQuestion'>Upload Question</Link>} icon={<PublishIcon />} />
        <BottomNavigationAction label={<Link to='/filterQuestions'>Filter Questions</Link>} icon={<FilterListIcon />} />
        <BottomNavigationAction label={<Link to='/userDetails'>User Details</Link>} icon={<PersonIcon />} />
        <SignOut /> 
      </BottomNavigation>

      <AppBar position="static">
      <Toolbar>
        
        <div> 
        <HomeIcon />
        <Link to='/'>Home</Link>
        </div>
        <div>
        <PublishIcon />
        <Link to='/uploadQuestion'>Upload Question</Link>
        </div>
        <div>
        <FilterListIcon />
        <Link to='/filterQuestions'>Filter Questions</Link>
        </div>
        <div>
        <PersonIcon />
        <Link to='/userDetails'>User Details</Link>
        </div>
        <SignOut />
      </Toolbar>
      </AppBar>
      </div>
        
    );
};

export default NavBar
