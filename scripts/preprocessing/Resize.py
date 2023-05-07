import os
from PIL import Image

input_folder = r"C:\Users\sofis\Downloads\Untitled-1 (1)\Bs4_Images"
output_folder = r"C:\Users\sofis\Downloads\Untitled-1 (1)\Bs4_Images_resized"

# Create the output folder if it does not exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through all the files in the input folder
for filename in os.listdir(input_folder):
    # Check if the file is an image
    if filename.endswith(".jpg"):
        # Open the image
        img = Image.open(os.path.join(input_folder, filename))
        if img.mode != "RGB":
            img = img.convert("RGB")
        
        # Resize the image
        img = img.resize((512, 512))

        # Save the resized image to the output folder
        output_filename = os.path.join(output_folder, filename)
        img.save(output_filename)
