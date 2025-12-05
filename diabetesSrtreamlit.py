import streamlit as st
import pickle
import os

# ===================== CONSTANT COLORS =====================
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
st.title("🩺 Diabetes Prediction App")

# ===================== LOAD MODEL =====================
MODEL_PATH = "diabetes_model2.pkl"

def load_model(path):
    if not os.path.exists(path):
        st.error(f"⚠️ Model file not found: {path}")
        return None
    try:
        with open(path, "rb") as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        return None

model = load_model(MODEL_PATH)

# ===================== INPUTS =====================
if model:
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

    # ===================== PREDICTION =====================
    if st.button("Predict"):
        input_data = [[
            pregnancies, glucose, blood_pressure, skin_thickness,
            insulin, bmi, diabetes_pedigree_function, age
        ]]

        prediction = model.predict(input_data)
        probabilities = model.predict_proba(input_data)[0]
        diabetic_prob = probabilities[1] * 100

        # ====== COLOR BASED ON RISK ======
        if diabetic_prob >= 70:
            bar_color = "red"
            risk = "High Risk"
        elif diabetic_prob >= 40:
            bar_color = "orange"
            risk = "Medium Risk"
        else:
            bar_color = "green"
            risk = "Low Risk"

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

        # ====== RESULT TEXT ======
        if prediction[0] == 1:
            st.error("🧪 The model predicts: **Diabetic**")
        else:
            st.success("💚 The model predicts: **Non-Diabetic**")

        # ====== ADVICE ======
        st.markdown("---")
        st.subheader("📌 Advice")
        if diabetic_prob >= 70:
            st.write("⚠️ **High risk!** Please consult a doctor as soon as possible.")
        elif diabetic_prob >= 40:
            st.write("🟠 **Medium risk**. Consider improving diet, exercise, and regular checkups.")
        else:
            st.write("🟢 **Low risk**. Keep up the healthy lifestyle!")
