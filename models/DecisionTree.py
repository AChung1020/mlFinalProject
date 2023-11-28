import pandas as pd
import numpy as np
from gensim.models import Word2Vec
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report

# Load the dataset
df = pd.read_csv('updated_cyberbullying_data.csv')

# Assuming 'text' column contains preprocessed text and 'label' column contains labels
texts = df['text'].apply(lambda x: x.split())  # Splitting preprocessed text into words
labels = df['label'].values

# Train Word2Vec model
word2vec = Word2Vec(sentences=texts, vector_size=100, window=5, min_count=1, workers=4)

# Convert texts to average Word2Vec vectors
def text_to_avg_vector(text):
    vector = np.mean([word2vec.wv[word] for word in text if word in word2vec.wv], axis=0)
    return vector

X = np.array([text_to_avg_vector(text) for text in texts])
y = np.array(labels)

# Handling NaN values (if any)
X = np.nan_to_num(X)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Decision Tree classifier
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Evaluate the model
predictions = model.predict(X_test)
print(classification_report(y_test, predictions))
