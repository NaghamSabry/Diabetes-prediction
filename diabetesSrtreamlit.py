# diabetesStreamlit.py
import streamlit as st
import pickle
import os

# ===== Global Style =====
st.set_page_config(page_title="Diabetes Prediction", page_icon="🩺", layout="wide")

st.markdown("""
<style>
body {
    background-color: #eef5f9;
}
h1 {
    color: #2b6cb0;
    text-align: center;
}
.result-box {
    padding: 15px;
    border-radius: 10px;
    text-align: center;
    font-size: 20px;
    margin-top: 10px;
}
.success-box {
    background-color: #c6f6d5;
    color: #22543d;
}
.error-box {
    background-color: #fed7d7;
    color: #742a2a;
}
</style>
""", unsafe_allow_html=True)

st.title("🩺 Diabetes Prediction App")

MODEL_PATH = "diabetes_model2.pkl"

# ===== Load Model =====
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

# ========== UI ==========
if model:
    st.subheader("➡️ Enter your details")

    col1, col2, col3 = st.columns(3)

    with col1:
        pregnancies = st.slider("Pregnancies", 0, 20, 1)
        glucose = st.slider("Glucose", 0, 200, 120)
        blood_pressure = st.slider("Blood Pressure", 0, 150, 70)

    with col2:
        skin_thickness = st.slider("Skin Thickness", 0, 100, 20)
        insulin = st.slider("Insulin", 0, 900, 80)
        bmi = st.slider("BMI", 0, 70, 25)

    with col3:
        diabetes_pedigree_function = st.slider("Diabetes Pedigree Function", 0.0, 2.5, 0.5)
        age = st.slider("Age", 0, 120, 33)

    if st.button("🚀 Predict"):
        input_data = [[
            pregnancies, glucose, blood_pressure, skin_thickness,
            insulin, bmi, diabetes_pedigree_function, age
        ]]

        try:
            prediction = model.predict(input_data)
            probabilities = model.predict_proba(input_data)[0]
            diabetic_prob = probabilities[1] * 100
            non_diabetic_prob = probabilities[0] * 100

            # ===== Probability Bars =====
            st.subheader("📊 Prediction Probability")

            st.write("💚 Non-Diabetic Probability")
            st.progress(int(non_diabetic_prob))

            st.write("🩸 Diabetic Probability")
            st.progress(int(diabetic_prob))

            # ===== Result Box =====
            if prediction[0] == 1:
                st.markdown(f"""
                <div class="result-box error-box">
                    🩸 <b>Result: Diabetic</b><br>
                    Please consider consulting a healthcare specialist for further evaluation.
                </div>
                """, unsafe_allow_html=True)

                st.info("💡 **Tip:** Maintaining a healthy diet, regular exercise, and monitoring glucose levels can significantly reduce risks.")

            else:
                st.markdown(f"""
                <div class="result-box success-box">
                    💚 <b>Result: Non-Diabetic</b><br>
                    Great job! Keep up your healthy lifestyle.
                </div>
                """, unsafe_allow_html=True)

                st.success("💡 **Tip:** Continue staying active and eating balanced meals to maintain good health!")

        except Exception as e:
            st.error(f"❌ Error during prediction: {e}")
