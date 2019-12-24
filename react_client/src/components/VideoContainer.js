import React from 'react';
import YouTube from 'react-youtube';
import { makeStyles } from "@material-ui/core";
import { Container, Typography } from "@material-ui/core";


// Styles
const useStyles = makeStyles( theme => ({
    root: {
        marginTop: "100px",
    },
    container: {
        display: "flex",
        justifyContent: "center"
    },
    element: {
        marginTop: "20px",
        display: "block",
        marginBottom: "20px"
    },
    text: {
        fontSize: "20px",
        fontStyle: "italic",
        marginBottom: "20px"
    },
    videoContainer: {
        marginBottom: "25px"
    }
}));

/**
 *  Video Container
 */

const VideoContainer = (props) => {

    const styles = useStyles();

    const { videoData } = props;

    let videos = [];
    if (videoData) {
        videos = videoData
    }

    /**
     *   For rendering the videos
     */
    const renderVideos = (videos) => {

        const size = videos.length;
        if (size === 0) {
            return <Typography variant={"body1"} className={styles.text}>{"No videos found"}</Typography>
        }

        return videos.map((video, i) => {
           return (
               <div className={styles.videoContainer}>
                   <Typography variant={"body1"} className={styles.text}>{video['title']}</Typography>
                   <YouTube
                       videoId={video['id']}
                       className={styles.element}
                       key={video['id']}
                   />

                   {(i !== size - 1) && <hr/>}
               </div>

           )
        });
    };

    return (
        <div className={styles.root}>
            {/* Header */}
            <Typography variant={"h2"} gutterBottom>{"Videos"}</Typography>
            <Container maxWidth={"md"} className={styles.container}>
                {/* Videos */}
                <div>
                    {renderVideos(videos)}
                </div>

            </Container>
        </div>
    );
};

// Exporting the component
export default VideoContainer;
