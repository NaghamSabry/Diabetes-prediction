import streamlit as st
import pickle
import os

# ===================== DARK / LIGHT MODE =====================
mode = st.sidebar.radio("Theme", ["Light", "Dark"])

if mode == "Dark":
    bg_color = "#000000"
    text_color = "#ffffff"
    card_color = "#161b22"
    button_bg = "#30363d"
    button_text = "#ffffff"
else:
    bg_color = "#f0f4f8"
    text_color = "#000000"
    card_color = "#ffffff"
    button_bg = "#1f77b4"
    button_text = "#ffffff"

# ===================== CUSTOM CSS =====================
st.markdown(f"""
<style>
body {{
    background-color: {bg_color};
    color: {text_color};
}}
h1, h2, h3, p, label {{
    color: {text_color} !important;
}}
.stButton>button {{
    background-color: {button_bg} !important;
    color: {button_text} !important;
    font-weight: bold;
    border-radius: 8px;
}}
div[data-baseweb="slider"]>div>div {{
    background: {card_color};
}}
</style>
""", unsafe_allow_html=True)

# ===================== TITLE =====================
st.title("🩺 Diabetes Prediction App (Demo)")

# ===================== INPUTS =====================
st.subheader("Enter your details:")

col1, col2, col3 = st.columns(3)

with col1:
    pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, step=1)
    glucose = st.slider("Glucose", 0, 200, 120)
    blood_pressure = st.slider("Blood Pressure", 0, 150, 70)

with col2:
    skin_thickness = st.slider("Skin Thickness", 0, 100, 20)
    insulin = st.slider("Insulin", 0, 900, 79)
    bmi = st.slider("BMI", 0.0, 70.0, 25.0)

with col3:
    diabetes_pedigree_function = st.slider("Diabetes Pedigree Function", 0.0, 2.5, 0.5)
    age = st.slider("Age", 0, 120, 33)

# ===================== MOCK PROBABILITY CALCULATION =====================
# Fake probability for demo purposes, varies with sliders
diabetic_prob = min(100, max(0, 
    0.15*glucose + 0.1*age + 0.2*bmi + 5*pregnancies + 0.1*insulin - 10
))

# ====== COLOR BASED ON RISK ======
if diabetic_prob >= 70:
    bar_color = "red"
    risk = "High Risk"
    advice = "⚠️ High risk! Please consult a doctor."
elif diabetic_prob >= 40:
    bar_color = "orange"
    risk = "Medium Risk"
    advice = "🟠 Medium risk. Improve diet and exercise."
else:
    bar_color = "green"
    risk = "Low Risk"
    advice = "🟢 Low risk. Keep healthy lifestyle!"

# ====== SHOW PROGRESS BAR ======
st.write(f"### 🩸 Diabetes Probability: **{diabetic_prob:.2f}%** ({risk})")
st.markdown(f"""
<div style="border-radius: 10px; height: 25px; background-color: #ddd;">
    <div style="width:{diabetic_prob}%; 
                height: 25px; 
                background-color:{bar_color};
                border-radius: 10px;">
    </div>
</div>
""", unsafe_allow_html=True)

# ====== ADVICE ======
st.markdown("---")
st.subheader("📌 Advice")
st.write(advice)

