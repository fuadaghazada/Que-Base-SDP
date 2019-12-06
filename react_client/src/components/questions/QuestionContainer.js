import React, { Component } from 'react';
import {
    Container,
    Typography,
    Button,
    ButtonGroup
} from '@material-ui/core';

import QuestionPreview from "./QuestionPreview";
import pagination from '../../utils/pagination';


/***
 *  Filter questions component
 */

class QuestionContainer extends Component {

    /**
     *  Constructor
     */

    constructor(props) {
        super(props);
        this.state = {

            hasData: false,
            numberOfPages: null,
        };
    }

    componentDidMount() {
        if (this.props['questions'] && this.props['handleRequest'] ) {
            this.setState({hasData: true})
        }
    }


    /**
     *  Rendering the question previews
     */

    renderQuestionPreviews = () => {
        const data = this.props['questions']['data'];

        if (data.length === 0)
            return <Typography variant={"h5"}>No results</Typography>;

        return data.map(question => (
            <QuestionPreview
                key={question['_id']}
                data={question}
            />
        ))
    };


    /**
     *  Updating the page - updating the data according to it
     *
     *  @param number - page number
     */

    updatePageNumber = (number) => {

        const handleRequest = this.props['handleRequest'];
        handleRequest(number);
    };


    /**
     *  Rendering the pagination buttons/links
     */

    renderPaginationLinks = () => {

        const currentPage = this.props['page'];
        const numberOfPages =  this.props['questions']['numberOfPages'];
        const pageNumbers = pagination.generatePaginationList(numberOfPages, currentPage);

        // Creating buttons from page numbers
        return pageNumbers.map(number => {

            if (number) {
                return <Button
                            key={number}
                            value={number}
                            onClick={() => this.updatePageNumber(number)}
                        >
                            {number}
                        </Button>
            }
            return <Button key={number}>...</Button>
        })
    };

    render() {
        if (this.state.hasData) {
            return (

                <Container maxWidth={"md"}>

                    {/* Header */}
                    <Typography variant={"h2"}>Questions</Typography>

                    {/* Question Previews */}
                    {this.renderQuestionPreviews()}

                    {/* Pagination Buttons */}
                    <ButtonGroup size="small" aria-label="small outlined button group">
                        {this.renderPaginationLinks()}
                    </ButtonGroup>
                </Container>
            );
        }

        return null;
    }

}

// Exporting the component
export default QuestionContainer
