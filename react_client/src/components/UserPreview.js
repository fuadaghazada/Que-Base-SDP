import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import {
    Card,
    CardActionArea,
    CardContent,
    Link,
    Grid
} from '@material-ui/core';
import Avatar from '@material-ui/core/Avatar';
import { deepOrange} from '@material-ui/core/colors'; // TODO: More colors should be implemented. 

const useStyles = makeStyles({
    card: {
        maxWidth: 200,
    },
    orange: {
        color: '#fff',
        backgroundColor: deepOrange[500],
      }
});

/**
    User Preview (functional component)
*/

const UserPreview = (props) => {
    console.log(props['data'])
    const classes = useStyles();
    const {username, _id} = props['data'];
    
    return (
        <Card className = {classes.card}>
            <CardActionArea>
                <CardContent>
                    <Grid container direction="row" alignItems='center'>
                        <Grid container item xs={4} >
                            <Avatar className={classes.orange}>{username[0].toUpperCase()}</Avatar>
                        </Grid>
                        <Grid container item xs={8} >
                            <Link href={`/userDetails/${_id}`}>{username}</Link>
                        </Grid>
                    </Grid>
                </CardContent>
            </CardActionArea>
        </Card>
           
        
    );
};

// Exporting the component
export default UserPreview;
