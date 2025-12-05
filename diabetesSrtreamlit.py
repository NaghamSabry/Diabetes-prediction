import streamlit as st
import pickle
import os

# =========================
#     PAGE CONFIG
# =========================
st.set_page_config(page_title="Diabetes Prediction", page_icon="🩺", layout="wide")

# =========================
#      THEME SWITCH
# =========================
mode = st.sidebar.selectbox("🌗 Choose Theme", ["Light Mode", "Dark Mode"])

if mode == "Dark Mode":
    st.markdown("""
    <style>
    body { background-color: #1e1e1e; color: white; }
    .stProgress > div > div { background-color: #4caf50; }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    body { background-color: #eef5f9; }
    </style>
    """, unsafe_allow_html=True)

# =========================
#     PAGE TITLE
# =========================
st.title("🩺 Diabetes Prediction App")

MODEL_PATH = "diabetes_model2.pkl"

# =========================
#     LOAD MODEL
# =========================
def load_model(path):
    if not os.path.exists(path):
        st.error(f"⚠️ Model file not found: {path}")
        return None
    try:
        with open(path, "rb") as f:
            return pickle.load(f)
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        return None

model = load_model(MODEL_PATH)

# =========================
#          FORM
# =========================
if model:
    st.subheader("➡️ Enter your details")

    col1, col2, col3 = st.columns(3)

    # Pregnancies = ONLY +/− buttons
    with col1:
        pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=0, step=1)
        glucose = st.slider("Glucose", 0, 200, 120)
        blood_pressure = st.slider("Blood Pressure", 0, 150, 70)

    with col2:
        skin_thickness = st.slider("Skin Thickness", 0, 100, 20)
        insulin = st.slider("Insulin", 0, 900, 80)
        bmi = st.slider("BMI", 0, 70, 25)

    with col3:
        diabetes_pedigree_function = st.slider("Diabetes Pedigree Function", 0.0, 2.5, 0.5)
        age = st.slider("Age", 0, 120, 33)

    # =========================
    #      PREDICT BUTTON
    # =========================
    if st.button("🚀 Predict"):
        input_data = [[
            pregnancies, glucose, blood_pressure, skin_thickness,
            insulin, bmi, diabetes_pedigree_function, age
        ]]

        try:
            prediction = model.predict(input_data)
            probabilities = model.predict_proba(input_data)[0]

            diabetic_prob = round(probabilities[1] * 100, 2)
            non_diabetic_prob = round(probabilities[0] * 100, 2)

            st.subheader("📊 Prediction Probability")

            # ========= Non-Diabetic Bar =========
            st.write(f"💚 Non-Diabetic: **{non_diabetic_prob}%**")
            st.progress(int(non_diabetic_prob))

            # ========= Diabetic Bar =========
            st.write(f"🩸 Diabetic: **{diabetic_prob}%**")
            st.progress(int(diabetic_prob))

            # ========= Result Box + Advice =========
            if prediction[0] == 1:
                st.error("🩸 **Result: Diabetic**")
                st.info("💡 Tip: Try regular exercise, reducing sugar intake, and checking blood glucose levels.")
            else:
                st.success("💚 **Result: Non-Diabetic**")
                st.info("💡 Tip: Keep a balanced diet, stay active, and maintain a healthy lifestyle!")

        except Exception as e:
            st.error(f"❌ Error during prediction: {e}")
