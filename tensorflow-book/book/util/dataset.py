import os
import requests
from zipfile import ZipFile
import csv
import numpy as np
import re

def get_spam_text_dataset():

    save_file_name = os.path.join('temp','temp_spam_data.csv')

    # Create directory if it doesn't exist
    if not os.path.exists('temp'):
        os.makedirs('temp')

    if os.path.isfile(save_file_name):
        text_data = []
        with open(save_file_name, 'r') as temp_output_file:
            reader = csv.reader(temp_output_file)
            for row in reader:
                text_data.append(row)
    else:
        zip_url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip'
        r = requests.get(zip_url)
        z = ZipFile(io.BytesIO(r.content))
        file = z.read('SMSSpamCollection')
        # Format Data
        text_data = file.decode()
        text_data = text_data.encode('ascii',errors='ignore')
        text_data = text_data.decode().split('\n')
        text_data = [x.split('\t') for x in text_data if len(x)>=1]
        
        # And write to csv
        with open(save_file_name, 'w') as temp_output_file:
            writer = csv.writer(temp_output_file)
            writer.writerows(text_data)

    texts = [x[1] for x in text_data]
    target = [x[0] for x in text_data]

    # Relabel 'spam' as 1, 'ham' as 0
    target = [1 if x == 'spam' else 0 for x in target]

    return texts, target

def shuffle_dataset(text, target):
    shuffled_ix = np.random.permutation(np.arange(len(target)))
    return text[shuffled_ix], target[shuffled_ix]

def split_dataset(texts, target, length, rate=0.8):
    texts, target = shuffle_dataset(texts, target)
    train_indices = np.random.choice(length, round(length*rate), replace=False)
    test_indices = np.array(list(set(range(length)) - set(train_indices)))
    texts_train = np.array([x for ix, x in enumerate(texts) if ix in train_indices])
    texts_test = np.array([x for ix, x in enumerate(texts) if ix in test_indices])
    target_train = np.array([x for ix, x in enumerate(target) if ix in train_indices])
    target_test = np.array([x for ix, x in enumerate(target) if ix in test_indices])
    return texts_train, texts_test, target_train, target_test

# Create a text cleaning function
def clean_text(text_string):
    text_string = re.sub(r'([^\s\w]|_|[0-9])+', '', text_string)
    text_string = " ".join(text_string.split())
    text_string = text_string.lower()
    return text_string

