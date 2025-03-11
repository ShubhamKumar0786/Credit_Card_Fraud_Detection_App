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
<<<<<<< HEAD
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
=======
        # ✅ Retrieve User Input Safely
        form_data = request.form
        required_fields = ["merchant_category", "transaction_amount", "customer_job", "age", "customer_city",
                           "customer_state", "merchant_name", "customer_gender", "transaction_month"]
        
        for field in required_fields:
            if field not in form_data:
                return f"Error: Missing field '{field}' in form submission."
        
        transaction_amount = float(form_data["transaction_amount"])
        age = int(form_data["age"])
        transaction_month = int(form_data["transaction_month"])
        
        # ✅ Encoding Function with Error Handling
        def encode_value(column_name, value):
            if column_name in encoders:
                if value in encoders[column_name].classes_:
                    return int(encoders[column_name].transform([value])[0])
                else:
                    print(f"Warning: '{value}' not in known classes for '{column_name}'. Assigning -1.")
                    return -1  # Default for unknown categories
            else:
                print(f"Error: Encoder for '{column_name}' not found. Assigning -1.")
                return -1  # Default if encoder is missing
        
        # ✅ Encode Categorical Columns
        encoded_features = {
            "merchant_category": encode_value("merchant_category", form_data["merchant_category"]),
            "customer_job": encode_value("customer_job", form_data["customer_job"]),
            "customer_city": encode_value("customer_city", form_data["customer_city"]),
            "customer_state": encode_value("customer_state", form_data["customer_state"]),
            "merchant_name": encode_value("merchant_name", form_data["merchant_name"]),
            "customer_gender": encode_value("customer_gender", form_data["customer_gender"])
        }

        # ✅ Prepare Input Data for Model
        input_features = pd.DataFrame([[
            encoded_features["merchant_category"], transaction_amount, encoded_features["customer_job"], age,
            encoded_features["customer_city"], encoded_features["customer_state"], encoded_features["merchant_name"],
            encoded_features["customer_gender"], transaction_month
        ]], columns=[
            'merchant_category', 'transaction_amount', 'customer_job', 'age',
            'customer_city', 'customer_state', 'merchant_name', 'customer_gender', 'transaction_month'
        ])
>>>>>>> 2f9e2b0 (first commit)

        # ✅ Make Prediction
        prediction = model.predict(input_features)[0]
        result = "Fraud" if prediction == 1 else "Not Fraud"

<<<<<<< HEAD
        # ✅ Render Result in HTML
=======
>>>>>>> 2f9e2b0 (first commit)
        return render_template("index.html", prediction=result)
    
    except Exception as e:
<<<<<<< HEAD
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True, threaded=True)  # ✅ Use threaded=True to fix socket issues
=======
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> 2f9e2b0 (first commit)
