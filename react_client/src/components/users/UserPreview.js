import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import {
    Typography,
    Card,
    CardActionArea,
    CardContent,
    Link,
    Grid
} from '@material-ui/core';
import Avatar from '@material-ui/core/Avatar';
import { red, purple, indigo, blue, cyan, teal, green, lime, amber, blueGrey, brown } from '@material-ui/core/colors';

/**
    This function hashes a string to generate some color. There are, currently, 11 different color options.
*/
function generateColor(str) {

    // Define a list of colors
    const colors = [red, purple, indigo, blue, cyan, teal, green, lime, amber, blueGrey, brown];

    // The hashing strategy is to sum the squares of ascii values of all characters in the string and,
    // then, to apply the modulo operation (using some prime number) on the sum
    let i, sum = 0;

    for (i = 0; i < str.length; i++) {  // For each character in the input string

        let asciiVal = str.charCodeAt(i);   // Get the ascii value of the current character
        sum += asciiVal * asciiVal;    // Take the square of it and add to our running sum
    }

    // Use the modulo operator (with some prime number) on the sum to get a unique value (hopefully)
    const somePrimeNumber = 47;
    const uniqueVal = sum % somePrimeNumber;

    // Return the corresponding color in the list
    const index = uniqueVal % colors.length;  // Ensure that the index does not exceed the length of the color array
    return colors[index];
}

/**
    User Preview (functional component)
*/

const UserPreview = (props) => {

    // console.log(props['data'])
    const {username, _id} = props['data'];
    const useStyles = makeStyles({
        card: {
            width: '100%',
        },
        color: {
            color: '#fff',
            backgroundColor: generateColor(username)[500],
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
                        <Grid container item md={10} >
                            <Link href={`/userDetails/${_id}`}><Typography className={classes.font}>{username}</Typography></Link>
                        </Grid>
                    </Grid>
                </CardContent>
            </CardActionArea>
        </Card>


    );
};

// Exporting the component
export default UserPreview;
