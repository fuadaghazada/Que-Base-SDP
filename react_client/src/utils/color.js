import { red, purple, indigo, blue, cyan, teal, green, lime, amber, blueGrey, brown } from '@material-ui/core/colors';

/**
    This function hashes a string to generate some color. There are, currently, 11 different color options.
 */
const generateColor = (str) => {

    // Define a list of colors
    const colors = [red, purple, indigo, blue, cyan, teal, green, lime, amber, blueGrey, brown];

    // The hashing strategy is to sum the squares of ascii values of all characters in the string and,
    // then, to apply the modulo operation (using some prime number) on the sum
    let i, sum = 0;

    for (i = 0; i < str.length; i++) {  // For each character in the input string

        let asciiVal = str.charCodeAt(i);   // Get the ascii value of the current character
        sum += asciiVal * asciiVal;    // Take the square of it and add to our running sum
    }

    // Use the modulo operator (with some prime number) on the sum to get a unique value (hopefully)
    const somePrimeNumber = 47;
    const uniqueVal = sum % somePrimeNumber;

    // Return the corresponding color in the list
    const index = uniqueVal % colors.length;  // Ensure that the index does not exceed the length of the color array
    return colors[index];

};

// Exporting the functions
export default {
    generateColor: generateColor
};
