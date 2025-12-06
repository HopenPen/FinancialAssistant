from catboost import CatBoostClassifier, Pool
from sklearn.model_selection import train_test_split
from joblib import dump
import pandas as pd

loaded_data = pd.read_csv('ci_data.csv')
X = loaded_data.drop(columns=['Date2', 'Category'])
Y = loaded_data['Category']

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

X_train = X_train.drop(columns=['Date', 'RefNo'])
X_test = X_test.drop(columns=['Date', 'RefNo'])

categoty_model = CatBoostClassifier(iterations=1000, learning_rate=0.1, depth=6)
categoty_model.fit(X_train, Y_train, verbose=10)


dump(categoty_model, 'category_model.joblib')