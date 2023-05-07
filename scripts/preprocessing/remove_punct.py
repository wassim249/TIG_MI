import os
import string

input_folder = "C:/Users/sofis/Downloads/Untitled-1 (1)/captions"
output_folder = "C:/Users/sofis/Downloads/Untitled-1 (1)/captions_clean"

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through all the files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        # Open the input file and read its contents
        with open(os.path.join(input_folder, filename), "r") as f:
            text = f.read()
        
        # Remove punctuations from the text using the string module
        text = text.translate(str.maketrans("", "", string.punctuation+string.digits))
        
        # Write the cleaned text to the output file
        output_filename = os.path.join(output_folder, filename)
        with open(output_filename, "w") as f:
            f.write(text)
