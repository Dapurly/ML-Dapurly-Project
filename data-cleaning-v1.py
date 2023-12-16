import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download stopwords
nltk.download('punkt')
nltk.download('stopwords')

def is_relevant(keyword, item):
    # Convert to string and handle NaN values
    keyword = str(keyword) if not pd.isna(keyword) else ''
    item = str(item) if not pd.isna(item) else ''

    # Tokenize and remove stopwords
    keyword_tokens = set(word_tokenize(keyword.lower()))
    item_tokens = set(word_tokenize(item.lower()))
    stop_words = set(stopwords.words('indonesian'))

    # Remove stopwords
    filtered_keyword = keyword_tokens - stop_words
    filtered_item = item_tokens - stop_words

    # Check for exact match or close relevance
    return filtered_keyword == filtered_item or filtered_keyword.issubset(filtered_item)

# Load data
df = pd.read_excel('path_to_your_spreadsheet.xlsx')

# Process each row
cleaned_data = []
for index, row in df.iterrows():
    keyword = row['nama_bahan']
    items = eval(row['nama_bahan_mentah'])
    prices = eval(row['harga_bahan_mentah'])

    cleaned_items = []
    cleaned_prices = []
    for item, price in zip(items, prices):
        if is_relevant(keyword, item):
            cleaned_items.append(item)
            cleaned_prices.append(price)

    cleaned_data.append([keyword, cleaned_items, cleaned_prices])

# Create new DataFrame and save
cleaned_df = pd.DataFrame(cleaned_data, columns=['nama_bahan', 'nama_bahan_mentah', 'harga_bahan_mentah'])
cleaned_df.to_excel('cleaned_data.xlsx', index=False)

