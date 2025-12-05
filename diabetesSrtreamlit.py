# diabetesStreamlit.py
import streamlit as st
import pickle
import os
# check_requirements.py
import importlib
import streamlit as st



# ====== CSS style ======
st.markdown("""
<style>
body {
    background-color: #f0f4f8;
}
h1 {
    color: #1f77b4;
    text-align: center;
}
.stButton>button {
    background-color: #1f77b4;
    color: white;
    font-weight: bold;
}
.stNumberInput>div>div>input {
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)

st.title("🩺 Diabetes Prediction App")

MODEL_PATH = "diabetes_model2.pkl"

def load_model(path):
    if not os.path.exists(path):
        st.error(f"⚠️ Model file not found: {path}")
        return None
    try:
        with open(path, "rb") as f:
            model = pickle.load(f)
        st.success("✅ Model loaded successfully!")
        return model
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        return None

model = load_model(MODEL_PATH)

if model:
    st.subheader("Enter your details to predict diabetes:")

    col1, col2, col3 = st.columns(3)

    with col1:
        pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=0)
        glucose = st.number_input("Glucose", min_value=0, max_value=200, value=120)
        blood_pressure = st.number_input("Blood Pressure", min_value=0, max_value=150, value=70)

    with col2:
        skin_thickness = st.number_input("Skin Thickness", min_value=0, max_value=100, value=20)
        insulin = st.number_input("Insulin", min_value=0, max_value=900, value=79)
        bmi = st.number_input("BMI", min_value=0.0, max_value=70.0, value=25.0)

    with col3:
        diabetes_pedigree_function = st.number_input("Diabetes Pedigree Function", min_value=0.0, max_value=2.5, value=0.5)
        age = st.number_input("Age", min_value=0, max_value=120, value=33)

    if st.button("Predict"):
        input_data = [[
            pregnancies, glucose, blood_pressure, skin_thickness,
            insulin, bmi, diabetes_pedigree_function, age
        ]]
        try:
            # توقع الفئة
            prediction = model.predict(input_data)
            
            # توقع الاحتمالات
            probabilities = model.predict_proba(input_data)[0]  # [Non-Diabetic prob, Diabetic prob]
            diabetic_prob = probabilities[1] * 100  # بالـ %
            
            st.write(f"💚 Probability of Non-Diabetic: {probabilities[0]*100:.2f}%")
            st.write(f"🩸 Probability of Diabetic: {diabetic_prob:.2f}%")
            
            # النتيجة الرئيسية
            if prediction[0] == 1:
                st.error("🩸 Result: Diabetic")
            else:
                st.success("💚 Result: Non-Diabetic")
        except Exception as e:
            st.error(f"❌ Error during prediction: {e}")




