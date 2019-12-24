import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import {
    Typography,
    Card,
    CardActionArea,
    CardContent,
    Link,
    Grid,
    Button
} from '@material-ui/core';
import Avatar from '@material-ui/core/Avatar';
import PersonAddIcon from '@material-ui/icons/PersonAdd';
import PeopleIcon from '@material-ui/icons/People';


import color from '../../utils/color';
import userServices from '../../services/user.service';

/**
    User Preview (functional component)
*/

const UserPreview = (props) => {

    // console.log(props['data'])
    const {username, _id, state} = props['data'];
    const useStyles = makeStyles({
        card: {
            width: '100%',
            marginBottom: "5px"
        },
        color: {
            color: '#fff',
            backgroundColor: color.generateColor(username)[500],
          },
        font: {
            fontSize: 22,
            textDecoration: null
        }
    });
    const classes = useStyles();

    return (
        <Card className = {classes.card}>
            <CardActionArea>
                <CardContent>
                    <Grid container direction="row" alignItems='center'>
                        <Grid container item md={2} >
                            <Avatar className={classes.color}>{username[0].toUpperCase()}</Avatar>
                        </Grid>
                        <Grid container item md={8} >
                            <Link href={`/userDetails/${_id}`}><Typography className={classes.font}>{username}</Typography></Link>
                        </Grid>
                        <Grid container item md={2} >
                            {state && generateUserState(state, _id)}
                        </Grid>
                    </Grid>
                </CardContent>
            </CardActionArea>
        </Card>
    );
};


const sendFriendRequest = (id) => {
    userServices.sendFriendRequest(id)
        .then(response => {
            console.log(response.data)
        })
        .catch(err => {
            console.log(err);
        })
};


const acceptFriendRequest = (id) => {
    userServices.acceptFriendRequest(id)
        .then(response => {
            console.log(response.data)
        })
        .catch(err => {
            console.log(err);
        })
};


/**
 *  Generating state from the user
 */
const generateUserState = (state, id) => {

    switch (state) {
        case 1:
            return <Typography variant={"body1"}><i>Your friend</i></Typography>;
        case 2:
            return <Button onClick={() => acceptFriendRequest(id)}><PeopleIcon /></Button>;
        case 3:
            return <Typography variant={"body1"}><i>Requested</i></Typography>;
        case 4:
            return <Button onClick={() => sendFriendRequest(id)}><PersonAddIcon /></Button>
        default:
            return null
    }
};

// Exporting the component
export default UserPreview;
