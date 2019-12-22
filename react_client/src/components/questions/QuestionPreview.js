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
        width: "100%",
        marginBottom: "5px"
    }
});


/**
 *   Question Preview (functional component)
 */

const QuestionPreview = (props) => {

    const {_id, title, viewCount, labels, similarityRate, confidenceRate} = props['data'];
    const classes = useStyles();

    return (

        <Card className={classes.card}>
            <CardActionArea>
                {/* Card content */}
                <CardContent>
                    <Grid container direction="row">
                        <Grid container item md={5} >
                            <Typography component={"h2"}>{title}</Typography>
                        </Grid>
                        <Grid container item md={3}>
                            {labels && <Typography component={"p"}><strong>Labels:</strong> {labels.toString()}</Typography>}
                        </Grid>

                        <Grid container item md={2}>
                            {similarityRate && <Typography component={"p"}><strong>Similarity rate:</strong> {similarityRate} %</Typography>}
                            {confidenceRate && <Typography component={"p"}><strong>Confidence rate:</strong> {confidenceRate}</Typography>}
                        </Grid>

                        <Grid container item md={2} justify={"flex-end"}>
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
