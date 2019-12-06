"""
    * Entity tags (or entities) are the underlined words we see on the website. Remember, we called them "keywords".

    * Topics are similar to the Entity tags, but contain more general themes that aren't explicitly mentioned in the
    document.

    * Categories are higher-level fields like "science and technology > applied science > chemistry".
"""

import textrazor
import json


class TextClassifier:

    def __init__(self, api_key):

        """Sets the API key.
        :param api_key: API key
        """

        # Set the API key
        textrazor.api_key = api_key

    def analyze(self, properties):

        """Given the name of the input file specifying the classification input, returns the classification result.
        Additionally, it saves the result to an output file (in JSON format).

        :param input_file_name: name of the JSON file storing the classification input (see "input_1.json")
        :param output_file_name: name of the output file (again, in JSON format)
        :return: result of the classification
        """

        # Get the input fields
        text_to_analyze, entity_tags, topics, categories = self.get_classification_properties(properties)

        # **************************************************************************************************************
        # Prepare TextRazor
        # **************************************************************************************************************

        # Extractors tell TextRazor what to extract from the text
        extractors = []

        if entity_tags["extract_entity_tags"] is True:
            extractors.append("entities")
        if topics["extract_topics"] is True:
            extractors.append("topics")

        client = textrazor.TextRazor(extractors=extractors)  # Set the extractors

        if categories["extract_categories"] is True:
            client.set_classifiers(["textrazor_newscodes"])

        # **************************************************************************************************************
        # Run the analysis/classification on the text
        # **************************************************************************************************************

        # Classify the text
        response = client.analyze(text_to_analyze)

        # Process the results (apply the score thresholds specified in the input file)
        processed_results = self.process_results(response, entity_tags, topics, categories)

        # Dump the results to the output file
        # with open(output_file_name, "w") as write_file:
        #     json.dump(processed_results, write_file, indent=2)

        return processed_results

    @staticmethod
    def get_classification_properties(properties):

        """
        Reads the classification input from the input file, and returns its fields.
        :param input_file_name: name of the JSON file storing the classification input (e.g. "input_1.json")
        :return: the text to run the analysis on, plus, the properties regarding entity tags, topics, and categories
        """

        # # Read the input file
        # with open(input_file_name, "r") as read_file:
        #     properties = json.load(read_file)

        # Extract the fields, and return them
        # (You may want to see "input_1.json" to understand the following fields better)

        text_to_analyze = properties["text_to_analyze"]
        entity_tags = properties["entity_tags"]
        topics = properties["topics"]
        categories = properties["categories"]

        return text_to_analyze, entity_tags, topics, categories

    def process_results(self, response, entity_tags, topics, categories):

        """Given the classification output, processes and returns the output fields. Processing involves sorting of the
        items by their score, and applying score thresholds.

        :param response: classification output/result (i.e. response from TextRazor)
        :param entity_tags: desired processing regarding entity tags (i.e. threshold on the relevance score and sorting)
        :param topics: desired processing regarding topics (again, threshold on score)
        :param categories: desired processing regarding categories (again, threshold on score)
        :return: a JSON file storing the processed results
        """

        # Template of the output JSON file
        results = {
            "entity_tags": list(),
            "topics": list(),
            "categories": list()
        }

        # Process entity tags
        if entity_tags["extract_entity_tags"] is True:
            results["entity_tags"] = self.process_entity_tags(response.entities(), entity_tags)

        # Process the topics
        if topics["extract_topics"] is True:
            results["topics"] = self.process_items(response.topics(), topics)

        # Process the categories
        if categories["extract_categories"] is True:
            results["categories"] = self.process_items(response.categories(), categories)

        return results

    @staticmethod
    def process_entity_tags(original_ones, properties):

        """
        Given the original entity tags (resulting from classification), processes and returns those tags.

        The processing step involves sorting them by their relevance score, and applying a threshold on the relevance
        score.
        :param original_ones: original entity tags (from the original response of TextRazor)
        :param properties: processing constraints (threshold value for relevance score)
        :return: dictionary of processed entity tags
        """

        # Sort entity tags by their relevance score
        entities = list(original_ones)
        entities.sort(key=lambda x: x.relevance_score, reverse=True)

        # Get the threshold value for relevance score
        relevance_threshold = properties["relevance_threshold"]

        processed_entity_tags = list()
        seen_entities = set()

        # Process the entries
        for entity in entities:

            # Get rid of the duplicate entity tags
            if entity.id not in seen_entities:

                # Check that current tag's relevance score is greater than the threshold
                if entity.relevance_score >= relevance_threshold:

                    # Create a dictionary containing the id/label, relevance score and confidence score
                    entity_dict = {
                        "label": entity.id,
                        "relevance_score": entity.relevance_score,
                        "confidence_score": entity.confidence_score
                    }

                    # Add it to the processed entity tags
                    processed_entity_tags.append(entity_dict)
                    seen_entities.add(entity.id)

        return processed_entity_tags

    @staticmethod
    def process_items(original_ones, properties):

        """
        Similar to "process_entity_tags", this one processes topics or categories. As they share the same structure,
        this function is reused for both topics and categories. Processing involves applying a threshold on the score.

        :param original_ones: original topics or categories (from the original response of TextRazor)
        :param properties: processing constraints (threshold value for score)
        :return: dictionary of processed topics or categories
        """

        processed_items = list()

        # Get the threshold value for score
        score_threshold = properties["score_threshold"]

        # Apply score threshold
        items = list(original_ones)
        for item in items:

            if item.score >= score_threshold:

                # Create a dictionary for the current item
                item_dict = {
                    "label": item.label,
                    "score": item.score
                }
                processed_items.append(item_dict)  # Append it to the list of processed items

        return processed_items
