import os
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from collections import Counter

nltk.download('stopwords')

caption_folder = r'C:\Users\sofis\Downloads\Untitled-1 (1)\Data\captions_clean'
stop_words = set(stopwords.words('english'))

all_captions = ''
for filename in os.listdir(caption_folder):
    if filename.endswith('.txt'):
        with open(os.path.join(caption_folder, filename), 'r') as f:
            caption = f.read().lower()
            caption = ' '.join([word for word in caption.split() if word not in stop_words and word.isalpha()])
            all_captions += caption

# Get the 10 most common words
word_count = Counter(all_captions.split()).most_common(10)
words, counts = zip(*word_count)
plt.figure(figsize=(8, 6))
# Plot the bar chart
plt.bar(words, counts)
plt.title('Most Common Words in Captions')
plt.xlabel('Words')
plt.ylabel('Count')
plt.show()
