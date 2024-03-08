from flask import Flask, render_template, request
import requests
import json
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime, timedelta

app = Flask(__name__)

# Replace with your actual Azure ML endpoint and key
scoring_uri = '<your_azure_ml_endpoint>'
api_key = '<your_api_key>'  # Replace with your actual key if needed

def generate_future_dates(start_date, periods=3, freq='M'):
    # Generate future dates for the next 'periods' months
    future_dates = [(start_date + timedelta(days=30 * i)).strftime('%Y%m') for i in range(1, periods + 1)]
    return future_dates

def get_predictions(dates):
    # Prepare the data in JSON format
    data = {"data": [[date] for date in dates]}
    headers = {'Content-Type': 'application/json'}
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'
    
    # Send the request to the Azure ML endpoint
    response = requests.post(scoring_uri, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch prediction: {response.text}")

@app.route('/', methods=['GET', 'POST'])
def index():
    graph_url = None
    if request.method == 'POST':
        start_date = datetime.utcnow()
        future_dates = generate_future_dates(start_date)
        predictions = get_predictions(future_dates)

        # Plotting the predictions
        plt.figure(figsize=(10, 5))
        plt.plot(future_dates, predictions, marker='o', linestyle='-')
        plt.title('Future Price Predictions for Jackets')
        plt.xlabel('Date (YYYYMM)')
        plt.ylabel('Predicted Price')
        plt.grid(True)
        
        # Save plot to a BytesIO buffer
        img = io.BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        img.seek(0)
        graph_url = base64.b64encode(img.getvalue()).decode('utf8')
        plt.close()

    return render_template('index.html', graph_url=graph_url)

if __name__ == '__main__':
    app.run(debug=True)