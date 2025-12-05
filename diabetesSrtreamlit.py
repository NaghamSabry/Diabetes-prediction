# app_scaled.py
import streamlit as st
import pandas as pd
import joblib
import pickle

# Load model and scaler
with open("diabetes_model2.pkl", "rb") as f:
    model = pickle.load(f)

with open("diabetes_scaler2.pkl", "rb") as f:
    scaler = pickle.load(f)


st.title("Diabetes Risk Prediction (with Scaler)")
st.write("Enter your health information to predict your risk of diabetes.")

# User inputs
Pregnancies = st.number_input("Number of Pregnancies", 0, 20, 0)
Glucose = st.number_input("Glucose Level", 0, 200, 120)
BloodPressure = st.number_input("Blood Pressure (mm Hg)", 0, 140, 70)
SkinThickness = st.number_input("Skin Thickness (mm)", 0, 100, 20)
Insulin = st.number_input("Insulin Level (IU/ml)", 0, 900, 79)
BMI = st.number_input("BMI", 0.0, 70.0, 20.0)
DiabetesPedigreeFunction = st.number_input("Diabetes Pedigree Function", 0.0, 3.0, 0.5)
Age = st.number_input("Age", 1, 120, 30)

# Convert inputs to DataFrame
input_data = pd.DataFrame(
    [[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]],
    columns=['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction',
             'Age'])

# Apply scaler
input_scaled = scaler.transform(input_data)

# Predict button
if st.button("Predict Risk"):
    probability = model.predict_proba(input_scaled)[0][1]
    probability_percent = round(probability * 100, 2)

    # Risk assessment
    if probability < 0.3:
        risk_level = "Low Risk"
    elif probability < 0.7:
        risk_level = "Medium Risk"
    else:
        risk_level = "High Risk"

    # Display result
    st.subheader("Prediction Result")
    st.write(f"Probability of having diabetes: **{probability_percent}%**")
    st.write(f"Risk Level: **{risk_level}**")

    if probability >= 0.5:
        st.error("⚠️ It is likely that you have diabetes. Please consult a doctor.")
    else:
        st.success("✅ You are unlikely to have diabetes, but regular check-ups are recommended.")
