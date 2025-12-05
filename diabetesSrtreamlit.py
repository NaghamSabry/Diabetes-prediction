import streamlit as st
import pickle
import os

st.set_page_config(
    page_title="Diabetes Prediction App",
    page_icon="🩺",
    layout="wide"
)

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
    st.subheader("Enter your details:")

    col1, col2, col3 = st.columns(3)

    with col1:
        pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=0)
        glucose = st.slider("Glucose", 0, 200, 120)
        blood_pressure = st.slider("Blood Pressure", 0, 150, 70)

    with col2:
        skin_thickness = st.slider("Skin Thickness", 0, 100, 20)
        insulin = st.slider("Insulin", 0, 900, 79)
        bmi = st.slider("BMI", 0.0, 70.0, 25.0)

    with col3:
        diabetes_pedigree_function = st.slider("Diabetes Pedigree Function", 0.0, 2.5, 0.5)
        age = st.slider("Age", 0, 120, 33)

    if st.button("Predict"):
        input_data = [[
            pregnancies, glucose, blood_pressure, skin_thickness,
            insulin, bmi, diabetes_pedigree_function, age
        ]]

        try:
            prediction = model.predict(input_data)
            probabilities = model.predict_proba(input_data)[0]

            diabetic_prob = round(probabilities[1] * 100, 2)

            st.subheader("📊 Diabetes Probability")
            st.write(f"🩸 **Probability of Diabetic: {diabetic_prob}%**")
            st.progress(int(diabetic_prob))

            if diabetic_prob >= 70:
                st.error("🔥 **Risk Level: HIGH RISK**")
                st.info("💡 Immediate lifestyle changes are recommended. Please consult your doctor.")
            elif diabetic_prob >= 40:
                st.warning("🟠 **Risk Level: MEDIUM RISK**")
                st.info("💡 Maintain a healthy lifestyle and monitor your glucose levels.")
            else:
                st.success("🟢 **Risk Level: LOW RISK**")
                st.info("💡 You are in a good range. Keep up your healthy habits!")

        except Exception as e:
            st.error(f"❌ Error during prediction: {e}")
