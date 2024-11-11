import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

# Download necessary NLTK data files (only need to do this once)
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize stop words and lemmatizer
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    """
    Preprocesses input text by: 
    removing non-alphanumeric characters, 
    converting to lowercase,
    tokenizing, removing stop words, and lemmatizing.
    
    Args:
        text (str): The email content to preprocess.
    
    Returns:
        str: The preprocessed text.
    """
    # Remove non-alphanumeric characters
    text = re.sub(r'\W', ' ', text)
    # Convert to lowercase
    text = text.lower()
    # Tokenize, remove stop words, and lemmatize
    text = ' '.join([lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words])
    return text
