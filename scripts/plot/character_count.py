import os

captions = []

# Loop through all the txt files in the directory
for filename in os.listdir(r'C:\Users\sofis\Downloads\Untitled-1 (1)\Data\captions_clean'):
    if filename.endswith('.txt'):
        # Read the caption from the txt file and append it to the captions list
        with open(os.path.join(r'C:\Users\sofis\Downloads\Untitled-1 (1)\Data\captions_clean', filename), 'r') as f:
            caption = f.read().strip()
            captions.append(caption)

# Plot a histogram of caption lengths
import matplotlib.pyplot as plt

plt.hist([len(caption) for caption in captions], bins=50)
plt.xlabel('Caption length (characters)')
plt.ylabel('Number of captions')
plt.show()
