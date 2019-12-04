import React from 'react';

/**
    Question Preview (functional component)
*/

const QuestionPreview = (props) => {
    
    const {title, viewCount} = props['data'];

    return (
        <div>
            <h2>{title}</h2>
            <p>Views: {viewCount}</p>
        </div>
    );
};

// Exporting the component
export default QuestionPreview;
