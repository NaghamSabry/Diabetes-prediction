import streamlit as st
import pickle
import os

# ============================ #
#       UI THEME CONTROL       #
# ============================ #

# Toggle for Dark / Light mode
mode = st.sidebar.radio("Theme Mode", ["Light Mode", "Dark Mode"])

if mode == "Dark Mode":
    st.markdown("""
    <style>
    body { background-color: #111 !important; }
    .stApp { background-color: #111 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    body { background-color: #f5f7fa !important; }
    .stApp { background-color: #f5f7fa !important; color: black !important; }
    </style>
    """, unsafe_allow_html=True)

# ============================ #
#        Page Settings         #
# ============================ #
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

# ============================ #
#          Main App           #
# ============================ #

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

            # Determine bar color
            if diabetic_prob >= 70:
                bar_color = "red"
                level = "HIGH RISK"
            elif diabetic_prob >= 40:
                bar_color = "orange"
                level = "MEDIUM RISK"
            else:
                bar_color = "green"
                level = "LOW RISK"

            # Colored progress bar (custom HTML)
            st.markdown(f"""
                <div style="border-radius: 8px; width: 100%; background-color: #ddd;">
                    <div style="
                        width: {diabetic_prob}%;
                        background-color: {bar_color};
                        padding: 10px;
                        color: white;
                        border-radius: 8px;
                        text-align: center;">
                        {diabetic_prob}%
                    </div>
                </div>
            """, unsafe_allow_html=True)

            st.write(f"📌 **Risk Level: {level}**")

            # Advice
            if level == "HIGH RISK":
                st.error("🔥 You are at **high risk**. Please consult a doctor soon.")
            elif level == "MEDIUM RISK":
                st.warning("🟠 Medium risk. Maintain healthy habits & monitor your sugar.")
            else:
                st.success("🟢 Low risk. Keep up the great lifestyle!")

        except Exception as e:
            st.error(f"❌ Error during prediction: {e}")
