from flask import Flask, render_template, request
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import os
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']
    df = pd.read_csv(file)

    if 'date' in df.columns and 'coffee_type' in df.columns and 'units_sold' in df.columns:
        summary = df.groupby('coffee_type')['units_sold'].sum().reset_index()
        top_coffee = summary.sort_values(by='units_sold', ascending=False).iloc[0]

        plt.figure(figsize=(8, 5))
        plt.bar(summary['coffee_type'], summary['units_sold'], color='#a9744f')
        plt.title('Total Coffee Sales by Type')
        plt.xlabel('Coffee Type')
        plt.ylabel('Units Sold')
        plt.tight_layout()

        chart_path = os.path.join('static', 'sales_chart.png')
        plt.savefig(chart_path)
        plt.close()
        prediction = f"The most sold coffee is likely to be: {top_coffee['coffee_type']} ({top_coffee['units_sold']} cups)"

        return render_template("result.html",
                               prediction=prediction,
                               columns=df.columns,
                               data=df.head(20).values,chart_url=chart_path)
    else:
        return "CSV must contain 'date', 'coffee_type', and 'units_sold' columns.", 400


if __name__ == '__main__':
    app.run(debug=True)
