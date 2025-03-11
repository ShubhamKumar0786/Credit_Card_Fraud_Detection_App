from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load Trained Model
with open("fraud_detection_model.pkl", "rb") as file:
    model = pickle.load(file)

# Load Encoders
with open("label_encoders.pkl", "rb") as file:
    encoders = pickle.load(file)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # ✅ Get User Input
        merchant_category = request.form["merchant_category"]
        transaction_amount = float(request.form["transaction_amount"])
        customer_job = request.form["customer_job"]
        age = int(request.form["age"])
        customer_city = request.form["customer_city"]
        customer_state = request.form["customer_state"]
        merchant_name = request.form["merchant_name"]
        customer_gender = request.form["customer_gender"]
        transaction_month = int(request.form["transaction_month"])

        # ✅ Encoding Function
        def encode_value(column_name, value):
            if column_name in encoders and value in encoders[column_name].classes_:
                return int(encoders[column_name].transform([value])[0])
            return -1

        # ✅ Encode Categorical Values
        merchant_category_encoded = encode_value("merchant_category", merchant_category)
        customer_job_encoded = encode_value("customer_job", customer_job)
        customer_city_encoded = encode_value("customer_city", customer_city)
        customer_state_encoded = encode_value("customer_state", customer_state)
        merchant_name_encoded = encode_value("merchant_name", merchant_name)
        customer_gender_encoded = encode_value("customer_gender", customer_gender)

        # ✅ Prepare Input Data
        input_features = pd.DataFrame([[merchant_category_encoded, transaction_amount, customer_job_encoded, age, 
                                        customer_city_encoded, customer_state_encoded, merchant_name_encoded, 
                                        customer_gender_encoded, transaction_month]],
                                      columns=['merchant_category', 'transaction_amount', 'customer_job', 'age',
                                               'customer_city', 'customer_state', 'merchant_name', 'customer_gender',
                                               'transaction_month'])

        # ✅ Make Prediction
        prediction = model.predict(input_features)
        result = "Fraud" if prediction[0] == 1 else "Not Fraud"

        # ✅ Render Result in HTML
        return render_template("index.html", prediction=result)

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True, threaded=True)  # ✅ Use threaded=True to fix socket issues
