-----------
DESCRIPTION
-----------

I have prepared a sample input file named "SampleInput.json". The fields in that JSON file are explained below:

    - text_to_analyze:
            The text on which you want to perform the analysis/classification.

    - entity_tags:
            These are what we called "keywords". If you want to extract keywords from the input text, write
            "true" for "extract_entity_tags" field.

            "relevance_threshold" takes values between 0 and 1, and acts as a threshold value on the relevance score of
            entity tags. You can set it as you like (use "0" to get all entity tags).

    - topics:
            These are similar to entity tags, but are more general terms usually. If you want to extract topics,
            again, set "extract_topics" as "true".

            "score_threshold" is a threshold on topics' score, ranging from 0 to 1. Usually, there are many topics,
            you may want to use 0.5 or more to filter some of them.

    - categories:
            Categories are like "science and technology > applied science > chemistry". To extract categories,
            assign "true" to "extract_categories".

            Score threshold is, again, the same: between 0 and 1. Categories, as far as I observed, tend to have small
            score values. As a result, you can keep this threshold small (around 0.6 for instance).

----------------
RUNNING THE CODE
----------------
Run the code as:

            python main.py <name_of_the_input_file> <name_of_the_output_file>"

To run the sample, you can use:

            python main.py SampleInput.json output.json