import TextClassifier
import sys

# The following API key is mine, limited to 500 requests per day
my_api_key = "a1d06d38ab618db113866db22344e6eccc49af1d4603088f11a6cd43"

# Instantiate a classifier
classifier = TextClassifier.TextClassifier(my_api_key)

# Specify the input file along with its "json" format
input_file = sys.argv[1]

# Classify the text in the input file, and save the result in an output file
output_file = sys.argv[2]
classifier.analyze(input_file, output_file)

print("Done!")

