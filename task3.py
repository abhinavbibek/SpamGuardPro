# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 10:26:26 2023

@author: bibek
"""

import pandas as pd
import os

def read_spam():
    category = 'spam'
    directory = r'C:\Users\bibek\Desktop\Spyder\JP Morgan\enron1\spam'
    return read_category(category, directory)

def read_ham():
    category = 'ham'
    directory = r'C:\Users\bibek\Desktop\Spyder\JP Morgan\enron1\ham'
    return read_category(category, directory)

def read_category(category, directory):
    emails = []
    for filename in os.listdir(directory):
        if not filename.endswith(".txt"):
            continue
        with open(os.path.join(directory, filename), 'r') as fp:
            try:
                content = fp.read()
                emails.append({'name': filename, 'content': content, 'category': category})
            except Exception as e:
                print(f'skipped {filename}: {str(e)}')
                content = fp.read()
                emails.append({'name':filename, 'content':content, 'category': category})
    return emails

ham = read_ham()
spam = read_spam()

df = pd.concat([pd.DataFrame.from_records(ham), pd.DataFrame.from_records(spam)], ignore_index=True)

import re

def preprocessor(e):
    return(e.lower())

import operator
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

def extract_date(filename):
    match=re.search(r'\d{4}-\d{2}-\d{2}',filename)
    if match:
        return match.group(0)
    return None

def print_stats():
    total_legitimate = len(ham)
    total_spam = len(spam)
    total_emails = total_legitimate + total_spam
    ham_dates = [extract_date(email['name']) for email in ham]
    spam_dates = [extract_date(email['name']) for email in spam]
    ham_min_date = min(filter(None, ham_dates))
    ham_max_date = max(filter(None, ham_dates))
    spam_min_date = min(filter(None, spam_dates))
    spam_max_date = max(filter(None, spam_dates))


    print("Legitimate")
    print("----------")
    print("- Owner: farmer-d")
    print(f"- Total number: {total_legitimate} emails")
    print(f"- Date of first email: {ham_min_date}")
    print(f"- Date of last email: {ham_max_date}")
    print("- Similars deletion: No")
    print("- Encoding: No")
    print("\n")

    
    print("Spam")
    print("----")
    print("- Owner: GP")
    print(f"- Total number: {total_spam} emails")
    print(f"- Date of first email: {spam_min_date}")
    print(f"- Date of last email: {spam_max_date}")
    print("- Similars deletion: No")
    print("- Encoding: No")
    print("\n")


    print(f"Spam:Legitimate rate = 1:{total_legitimate // total_spam}")
    print(f"Total number of emails (legitimate + spam): {total_emails}")

df = pd.DataFrame.from_records(ham + spam)
vectorizer=CountVectorizer(preprocessor=preprocessor)
x=vectorizer.fit_transform(df['content'])
y=df['category']
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)
model = LogisticRegression(max_iter=1000)
model.fit(x_train, y_train)
y_pred = model.predict(x_test)


accuracy = accuracy_score(y_test, y_pred)
confusion_mat = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

# Print the evaluation results
print("\n\n\n")
print("Model Evaluation")
print("-----------------")
print("Accuracy:", accuracy)
print("Confusion Matrix:\n", confusion_mat)
print("\nClassification Report:\n", class_report)
print("\n\n\n")

print_stats()

feature_names = vectorizer.get_feature_names_out()

# Print the first 20 features (words)
print("First 20 features (words):", feature_names[:20])

feature_coefficients = dict(zip(feature_names, model.coef_[0]))

# Sort features based on coefficients (importance)
sorted_features = sorted(feature_coefficients.items(), key=operator.itemgetter(1), reverse=True)

# Print the top 10 positive features (associated with spam)
print("\nTop 10 Positive Features (Spam):")
print("--------------------------------")
for feature, coef in sorted_features[:10]:
    print(f"{feature}: {coef}")

# Print the top 10 negative features (associated with ham)
print("\nTop 10 Negative Features (Ham):")
print("--------------------------------")
for feature, coef in sorted_features[-10:]:
    print(f"{feature}: {coef}")
