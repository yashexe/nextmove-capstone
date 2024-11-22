import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle

# Load processed data
data = pd.read_csv('machine_learning/data/processed_emails.csv')

# Split data into features and labels
X = data['processed_content']
y = data['category']

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize TF-IDF Vectorizer with a limit on max features (adjustable for larger datasets)
tfidf = TfidfVectorizer(max_features=1000)

# Fit and transform training data, transform test data
X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

# Initialize and train Logistic Regression model
logreg_model = LogisticRegression(max_iter=1000)
logreg_model.fit(X_train_tfidf, y_train)

# Make predictions on the test set
y_test_pred = logreg_model.predict(X_test_tfidf)

# Make predictions on the training set
y_train_pred = logreg_model.predict(X_train_tfidf)

# Evaluate the model on the training set
train_accuracy = accuracy_score(y_train, y_train_pred)

# Evaluate the model on the test set
test_accuracy = accuracy_score(y_test, y_test_pred)
print(f"\nTraining Set Accuracy: {train_accuracy * 100:.2f}%")
print(f"Test Set Accuracy: {test_accuracy * 100:.2f}%")
print("\nTest Set Classification Report:")
print(classification_report(y_test, y_test_pred))
print("\nTest Set Confusion Matrix:")
print(confusion_matrix(y_test, y_test_pred))

# Save the trained model and TF-IDF vectorizer for future use
with open('machine_learning/model/logistic_regression_model.pkl', 'wb') as model_file:
    pickle.dump(logreg_model, model_file)
with open('machine_learning/model/tfidf_vectorizer.pkl', 'wb') as vectorizer_file:
    pickle.dump(tfidf, vectorizer_file)

print("Logistic Regression model and vectorizer saved successfully.")

 # Run Command: python .\machine_learning\model\train_logistic_regression.py in \nextmove-capstone> 
