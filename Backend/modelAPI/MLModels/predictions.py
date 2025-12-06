from joblib import load 
import pandas as pd
import os

def make_dataframe(withdrawal, deposit, balance):
    data = {
        'Withdrawal': [withdrawal],
        'Deposit': [deposit],
        'Balance': [balance]
    }
    return pd.DataFrame(data)

def load_category_model():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    categoty_model = load(os.path.join(BASE_DIR, 'category_model.joblib'))
    return categoty_model

def make_prediction(input_data):
    model = load_category_model()
    prediction = model.predict(input_data)
    return(prediction[0][0])

if __name__ == "__main__":
    X_test_sample = pd.DataFrame({
        'Withdrawal': [150],
        'Deposit': [0],
        'Balance': [1587.23]
        })

    print(make_prediction(X_test_sample))
