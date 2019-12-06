import React from 'react';
import {
    Container,
    Typography,
    Button,
    ButtonGroup
} from '@material-ui/core';

import pagination from '../../utils/pagination';


/***
 *  Filter questions component
 */

const CustomContainer = (props) => {

    const { header, renderPreviews, page, numberOfPages, handleRequest } = props;

    /**
     *  Updating the page - updating the data according to it
     *
     *  @param number - page number
     */

    const updatePageNumber = (number) => {
        handleRequest(number);
    };


    /**
     *  Rendering the pagination buttons/links
     */

    const renderPaginationLinks = () => {

        const pageNumbers = pagination.generatePaginationList(numberOfPages, page);

        // Creating buttons from page numbers
        return pageNumbers.map(number => {

            if (number) {
                return <Button
                            key={number}
                            value={number}
                            onClick={() => updatePageNumber(number)}
                        >
                            {number}
                        </Button>
            }
            return <Button key={number}>...</Button>
        })
    };

    return (

        <Container maxWidth={"md"}>

            {/* Header */}
            <Typography variant={"h2"}>{header}</Typography>

            {/* Question Previews */}
            {renderPreviews()}

            {/* Pagination Buttons */}
            <ButtonGroup size="small" aria-label="small outlined button group">
                {renderPaginationLinks()}
            </ButtonGroup>

        </Container>
    );

}

// Exporting the component
export default CustomContainer
