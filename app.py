import streamlit as st
import numpy as np
import pandas as pd
import pickle

# -------------------- Load Model & Transformers --------------------

# Load trained model
with open('xgb_classifier.pkl', 'rb') as file:
    model = pickle.load(file)

# Load label encoders
with open('label_encoder_customer_state.pkl', 'rb') as file:
    label_encoder_customer_state = pickle.load(file)

with open('label_encoder_merchant_category.pkl', 'rb') as file:
    label_encoder_merchant_category = pickle.load(file)

with open('label_encoder_customer_gender.pkl', 'rb') as file:
    label_encoder_customer_gender = pickle.load(file)

with open('label_encoder_customer_job.pkl', 'rb') as file:
    label_encoder_customer_job = pickle.load(file)

# Load StandardScaler
with open('st_x.pkl', 'rb') as file:
    st_x = pickle.load(file)

# -------------------- Streamlit UI --------------------

st.set_page_config(page_title="Credit Card Fraud Detector", page_icon="💳")
st.title('💳 Credit Card Fraud Detection App')
st.markdown("Predict whether a transaction is **fraudulent or legitimate** using model insights.")

# -------------------- User Input --------------------

merchant_category = st.selectbox('Merchant Category', label_encoder_merchant_category.classes_)
transaction_amount = st.number_input('Transaction Amount', min_value=0.0)
customer_gender = st.selectbox('Customer Gender', label_encoder_customer_gender.classes_)
customer_state = st.selectbox('Customer State', label_encoder_customer_state.classes_)
city_population = st.number_input('City Population', min_value=0)
customer_job = st.selectbox('Customer Job', label_encoder_customer_job.classes_)
transaction_year = st.selectbox('Transaction Year', list(range(2000, 2026)))
transaction_month = st.slider('Transaction Month', 1, 12)
transaction_date = st.slider('Transaction Date', 1, 31)
transaction_hour = st.slider('Transaction Hour', 0, 23)
transaction_minute = st.slider('Transaction Minute', 0, 59)
age = st.number_input('Age', min_value=1, max_value=120)

# -------------------- Encode + Create Input DataFrame --------------------

input_data = pd.DataFrame([[
    label_encoder_merchant_category.transform([merchant_category])[0],
    transaction_amount,
    label_encoder_customer_gender.transform([customer_gender])[0],
    label_encoder_customer_state.transform([customer_state])[0],
    city_population,
    label_encoder_customer_job.transform([customer_job])[0],
    transaction_year,
    transaction_month,
    transaction_date,
    transaction_hour,
    transaction_minute,
    age
]], columns=[
    'merchant_category',
    'transaction_amount',
    'customer_gender',
    'customer_state',
    'city_population',
    'customer_job',
    'transaction_year',
    'transaction_month',
    'transaction_date',
    'transaction_hour',
    'transaction_minute',
    'age'
])


# -------------------- Scaling --------------------

input_data_scaled = st_x.transform(input_data)

# -------------------- Prediction --------------------

prediction = model.predict(input_data_scaled)
prediction_proba = model.predict_proba(input_data_scaled)[0][1]

# -------------------- Output --------------------

st.subheader('🔍 PRediction Result')
st.write(f'**Fraud Probability:** `{prediction_proba:.2f}`')

if prediction[0] == 1:
    st.write('⚠️ This transaction is likely to be **fraudulent**.')
else:
    st.write('✅ This transaction is **not likely** to be fraudulent.')
