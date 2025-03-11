from flask import Flask, render_template, request
import pickle
import pandas as pd
from pymongo import MongoClient

app = Flask(__name__)

# 🔹 Load Trained Model
with open("fraud_detection_model.pkl", "rb") as file:
    model = pickle.load(file)

# 🔹 Load Encoders
with open("label_encoders.pkl", "rb") as file:
    encoders = pickle.load(file)

# ✅ MongoDB Atlas Connection (Replace with your credentials)
MONGO_URI = "mongodb+srv://behalshubham6:12345@cluster0.eqs18.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["fraud_Database"]
collection = db["predictions"]  # ✅ Collection for storing predictions

@app.route("/")
def home():
    return render_template("index.html")  # Load HTML Page

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # ✅ Retrieve User Input from Form
        merchant_category = request.form["merchant_category"]
        transaction_amount = float(request.form["transaction_amount"])
        customer_job = request.form["customer_job"]
        age = int(request.form["age"])
        customer_city = request.form["customer_city"]
        customer_state = request.form["customer_state"]
        merchant_name = request.form["merchant_name"]
        customer_gender = request.form["customer_gender"]
        transaction_month = int(request.form["transaction_month"])

        # ✅ Encoding Function with Error Handling
        def encode_value(column_name, value):
            if column_name in encoders:
                if value in encoders[column_name].classes_:
                    return int(encoders[column_name].transform([value])[0])  # Convert to int
                else:
                    print(f"Warning: '{value}' not in known classes for '{column_name}'. Assigning -1.")
                    return -1  # Default for unknown categories
            else:
                print(f"Error: Encoder for '{column_name}' not found. Assigning -1.")
                return -1  # Default if encoder is missing

        # ✅ Encode Categorical Columns
        merchant_category_encoded = encode_value("merchant_category", merchant_category)
        customer_job_encoded = encode_value("customer_job", customer_job)
        customer_city_encoded = encode_value("customer_city", customer_city)
        customer_state_encoded = encode_value("customer_state", customer_state)
        merchant_name_encoded = encode_value("merchant_name", merchant_name)
        customer_gender_encoded = encode_value("customer_gender", customer_gender)

        # ✅ Prepare Input Data for Model
        input_features = pd.DataFrame([[merchant_category_encoded, transaction_amount, customer_job_encoded, age, 
                                        customer_city_encoded, customer_state_encoded, merchant_name_encoded, 
                                        customer_gender_encoded, transaction_month]],
                                      columns=['merchant_category', 'transaction_amount', 'customer_job', 'age',
                                               'customer_city', 'customer_state', 'merchant_name', 'customer_gender',
                                               'transaction_month'])

        # ✅ Debugging: Print Input Data
        print("Input Features:\n", input_features)

        # ✅ Make Prediction
        prediction = model.predict(input_features)
        result = "Fraud" if prediction[0] == 1 else "Not Fraud"

        # ✅ Save Data + Prediction to MongoDB
        data_to_store = {
            "merchant_category_original": merchant_category,
            "merchant_category_encoded": merchant_category_encoded,
            "transaction_amount": transaction_amount,
            "customer_job_original": customer_job,
            "customer_job_encoded": customer_job_encoded,
            "age": age,
            "customer_city_original": customer_city,
            "customer_city_encoded": customer_city_encoded,
            "customer_state_original": customer_state,
            "customer_state_encoded": customer_state_encoded,
            "merchant_name_original": merchant_name,
            "merchant_name_encoded": merchant_name_encoded,
            "customer_gender_original": customer_gender,
            "customer_gender_encoded": customer_gender_encoded,
            "transaction_month": transaction_month,
            "prediction": result
        }
        collection.insert_one(data_to_store)  # ✅ Insert into MongoDB

        # ✅ Render Result to HTML
        return render_template("index.html", prediction=result)

    except Exception as e:
        print(f"Error: {str(e)}")  # ✅ Print error for debugging
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
