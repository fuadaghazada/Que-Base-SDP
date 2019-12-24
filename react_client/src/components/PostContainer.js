import React from 'react';
import {Typography} from "@material-ui/core";

import CustomContainer from './custom/CustomContainer';
import Post from "./Post";


/**
 *  Question Container
 */

const PostContainer = (props) => {

    const {posts, handleRequest, page, header, styles} = props;
    const numberOfPages = posts['numberOfPages'];

    /**
     *  Rendering the question previews
     */

    const renderPosts = () => {

        const data = posts['data'];

        if (data.length === 0)
            return <Typography variant={"h5"}>No results</Typography>;

        return data.map(post => (
            <Post
                key={post['_id']}
                data={post}
            />
        ))
    };

    // Returning the render stuff
    return (
        <CustomContainer header={!header ? "Feed" : header}
                         page={page}
                         numberOfPages={numberOfPages}
                         handleRequest={handleRequest}
                         renderPreviews={renderPosts}
                         styles={styles}
        >
        </CustomContainer>
    );
};

// Exporting the component
export default PostContainer
