import React from 'react';
import { Link } from 'react-router-dom'
/**
    Question Preview (functional component)
*/

const QuestionPreview = (props) => {
    
    const {_id, title, viewCount} = props['data'];

    return (
        <div>
            <h2>{title}</h2>
            <p>Views: {viewCount}</p>
            <Link to={{
            pathname: '/questionDetails',
                state: {
            questionId: _id
            }
            }}>Go to Question</Link>
        </div>
    );
};

// Exporting the component
export default QuestionPreview;
