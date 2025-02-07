from flask import Flask, request, render_template
import pandas as pd
import joblib

app = Flask(__name__)

# Load the saved model and scaler
model = joblib.load('fraud_detection_model.pkl')
scaler = joblib.load('scaler.pkl')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Get data from the form
            step = 1  # or the current step in your process if it's dynamic
            type_transaction = request.form['type']
            amount = int(request.form['amount'])
            oldbalanceOrg = int(request.form['oldbalanceOrg'])
            newbalanceOrig = int(request.form['newbalanceOrig'])
            oldbalanceDest = int(request.form['oldbalanceDest'])
            newbalanceDest = int(request.form['newbalanceDest'])
            isFlaggedFraud = 0  # Assuming no flagged fraud in user input

            # Create input feature array
            data = pd.DataFrame({
                'step': [step],
                'amount': [amount],
                'oldbalanceOrg': [oldbalanceOrg],
                'newbalanceOrig': [newbalanceOrig],
                'oldbalanceDest': [oldbalanceDest],
                'newbalanceDest': [newbalanceDest],
                'isFlaggedFraud': [isFlaggedFraud],
                'type_TRANSFER': [1 if type_transaction == 'TRANSFER' else 0],
                'type_CASH_OUT': [1 if type_transaction == 'CASH_OUT' else 0],
                'type_PAYMENT': [1 if type_transaction == 'PAYMENT' else 0],
                'type_DEBIT': [1 if type_transaction == 'DEBIT' else 0]
            })

            # Ensure the correct order of features
            feature_order = ['step', 'amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest',
                 'isFlaggedFraud', 'type_TRANSFER', 'type_CASH_OUT', 'type_DEBIT', 'type_PAYMENT']

            data = data[feature_order]

            # Scale the features
            data = scaler.transform(data)

            # Predict
            prediction = model.predict(data)
            result = 'Fraud' if prediction[0] == 1 else 'Not Fraud'

        except Exception as e:
            result = f"Error: {str(e)}"
        
        return render_template('index.html', result=result)

    return render_template('index.html', result='')

if __name__ == '__main__':
    app.run(debug=True)
