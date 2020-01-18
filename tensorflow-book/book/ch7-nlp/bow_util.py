import os
import csv
import requests
import string
from zipfile import ZipFile
import io
import numpy as np

save_file_name = os.path.join('temp','temp_spam_data.csv')

def get_texts_data():

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

def normalize_text(texts):
    # Lower case
    texts = [x.lower() for x in texts]

    # Remove punctuation
    texts = [''.join(c for c in x if c not in string.punctuation) for x in texts]

    # Remove numbers
    texts = [''.join(c for c in x if c not in '0123456789') for x in texts]

    # Trim extra whitespace
    texts = [' '.join(x.split()) for x in texts]
    return texts

def split_dataset(texts, target, length, rate=0.8):
    train_indices = np.random.choice(length, round(length*rate), replace=False)
    test_indices = np.array(list(set(range(length)) - set(train_indices)))
    texts_train = [x for ix, x in enumerate(texts) if ix in train_indices]
    texts_test = [x for ix, x in enumerate(texts) if ix in test_indices]
    target_train = [x for ix, x in enumerate(target) if ix in train_indices]
    target_test = [x for ix, x in enumerate(target) if ix in test_indices]
    return texts_train, texts_test, target_train, target_test

