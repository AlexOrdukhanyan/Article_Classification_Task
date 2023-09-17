import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.naive_bayes import MultinomialNB
# from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score, classification_report

# change the path of the csv file accordingly
data = pd.read_csv('corpus_articles.csv', encoding='utf-8')

# a little preprocess

"""
armenian_stopwords = [
    'այդ', 'այլ', 'այն', 'այս', 'դու', 'դուք', 'եմ', 'են', 'ենք', 'ես',
    'եք', 'է', 'էի', 'էին', 'էիր', 'էիք', 'էր', 'ըստ', 'թ', 'ի', 'ին', 'իսկ',
    'իր', 'հետ', 'մեջ', 'մի', 'ն', 'նա',
    'նաև', 'նրա', 'որ', 'ու', 'ում',
    'վրա', 'և'
]

def preprocess_text(text):
    text = text.lower()
    words = text.split()
    filtered_words = [word for word in words if word not in armenian_stopwords]
    return ' '.join(filtered_words)

data['Article Text'] = data['Article Text'].apply(preprocess_text)
"""

data['Article Text'].fillna('', inplace=True)

# splitting the data into training, validation, and testing parts
X_train, X_temp, y_train, y_temp = train_test_split(data['Article Text'], data['Category'], test_size=0.3, random_state=42)
X_validation, X_test, y_validation, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# creating a TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer(max_features=100000)

# transforming the training, validation and test data using the vectorizer
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_validation_tfidf = tfidf_vectorizer.transform(X_validation)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

# defining hyperparameters to tune
param_grid = {'alpha': [0.012, 0.02, 0.0123, 0.0124]}
# with max_features = 5000
# [0.1, 0.5, 1.0, 2.0] best is 0.1 | validation_accuracy = 0.7635 test_accuracy = 0.7488
# [0.1, 0.05, 0.2, 0.075] best is 0.05 | validation_accuracy = 0.7734 test_accuracy = 0.7586
# [0.05, 0.06, 0.025, 0.04] best is 0.04 | validation_accuracy = 0.7685 test_accuracy = 0.7586

# with max_features = 10000
# [0.03, 0.04, 0.025, 0.01] best is 0.03 | validation_accuracy = 0.7931 test_accuracy = 0.7586
# Create a Multinomial Naive Bayes classifier

# with max_features = 15000
# [0.05, 0.04, 0.02, 0.01] best is 0.04 | validation_accuracy = 0.7882 test_accuracy = 0.7635

# classifier = MultinomialNB()

# defining the classifier
classifier = SGDClassifier(loss='squared_hinge', penalty='l2', alpha=0.2, random_state=42, max_iter=15, tol=None)

# performing a grid search for the best hyperparameter
grid_search = GridSearchCV(classifier, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
grid_search.fit(X_train_tfidf, y_train)

best_alpha = grid_search.best_params_['alpha']

# training a new classifier with the best hyperparameter
best_classifier = MultinomialNB(alpha=best_alpha)
best_classifier.fit(X_train_tfidf, y_train)

y_validation_pred = best_classifier.predict(X_validation_tfidf)

validation_accuracy = accuracy_score(y_validation, y_validation_pred)

y_test_pred = best_classifier.predict(X_test_tfidf)

test_accuracy = accuracy_score(y_test, y_test_pred)

report_validation = classification_report(y_validation, y_validation_pred, zero_division=1)
report_test = classification_report(y_test, y_test_pred, zero_division=1)


print(f'Best Alpha: {best_alpha}')

print(f'Validation Accuracy: {validation_accuracy:.4f}')

print(f'Validation Classification Report:\n{report_validation}')

print(f'Test Accuracy: {test_accuracy:.4f}')

print(f'Test Classification Report:\n{report_test}')