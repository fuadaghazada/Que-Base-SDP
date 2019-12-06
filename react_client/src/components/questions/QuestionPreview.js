import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import {
    Card,
    CardActionArea,
    CardContent,
    Typography,
    Link,
    Grid
} from '@material-ui/core';


/**
 *  Styles
 */
const useStyles = makeStyles({
    card: {
        maxWidth: 700,
    }
});


/**
 *   Question Preview (functional component)
 */

const QuestionPreview = (props) => {

    const {_id, title, viewCount} = props['data'];
    const classes = useStyles();

    return (

        <Card className={classes.card}>
            <CardActionArea>
                {/* Card content */}
                <CardContent>
                    <Grid container direction="row">
                        <Grid container item xs={8} >
                            <Typography component={"h2"}>{title}</Typography>
                        </Grid>
                        <Grid container item xs={4} justify={"flex-end"}>
                            <Typography component={"p"}>Views: {viewCount}</Typography>
                        </Grid>
                        <Link href={`/questionDetails/${_id}`}>View Question</Link>
                    </Grid>
                </CardContent>
            </CardActionArea>
        </Card>
    );
};

// Exporting the component
export default QuestionPreview;
