import React from 'react';
import {Typography} from "@material-ui/core";

import CustomContainer from '../custom/CustomContainer';
import QuestionPreview from "../questions/QuestionPreview";


/**
 *  Question Container
 */

const QuestionContainer = (props) => {

    const {questions, handleRequest, page, header, styles} = props;
    const numberOfPages = questions['numberOfPages'];

    /**
     *  Rendering the question previews
     */

    const renderQuestionPreviews = () => {

        const data = questions['data'];

        if (data.length === 0)
            return <Typography variant={"h5"}>No results</Typography>;

        return data.map(question => (
            <QuestionPreview
                key={question['_id']}
                data={question}
            />
        ))
    };

    // Returning the render stuff
    return (
        <CustomContainer header={!header ? "Questions" : header}
                         page={page}
                         numberOfPages={numberOfPages}
                         handleRequest={handleRequest}
                         renderPreviews={renderQuestionPreviews}
                         styles={styles}
        >
        </CustomContainer>
    );
};

// Exporting the component
export default QuestionContainer
