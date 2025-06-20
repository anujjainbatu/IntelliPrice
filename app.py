import streamlit as st
import pickle
import numpy as np

# Load model and data
pipe = pickle.load(open('pipe.pkl','rb'))
df = pickle.load(open('df.pkl','rb'))

st.set_page_config(page_title="Laptop Price Predictor", page_icon="💻", layout="centered")

st.markdown(
    """
    <style>
    .block-container {
        max-width: 100vw !important;
        padding-left: 5vw;
        padding-right: 5vw;
        padding-top: 2vw;
        padding-bottom: 2vw;
    }
    .stButton>button {
        background-color: #22223b;
        color: #f5f7fa;
        border-radius: 8px;
        font-weight: bold;
        padding: 0.5em 2em;
        margin: 0 auto;
        display: block;
    }
    .result-container {
        background: #e3e6ea;
        border-radius: 12px;
        padding: 1.5em;
        margin-top: 1em;
        text-align: center;
        box-shadow: 0 2px 8px rgba(34,34,59,0.06);
    }
    </style>
    """,
    unsafe_allow_html=True
)

with st.container():
    st.markdown("<h1 style='text-align:center; color:#ffffff;'>💻 Laptop Price Predictor</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center; color:#ffffff;'>Predict the price of a laptop based on its configuration.</h4>", unsafe_allow_html=True)
    st.markdown("")

    col1, col2 = st.columns(2)

    with col1:
        company = st.selectbox('Brand', df['Company'].unique())
        type = st.selectbox('Type', df['TypeName'].unique())
        ram = st.selectbox('RAM (GB)', [2,4,6,8,12,16,24,32,64])
        weight = st.number_input('Weight (kg)', min_value=0.5, max_value=5.0, value=2.0, step=0.1)
        cpu = st.selectbox('CPU', df['Cpu brand'].unique())
        gpu = st.selectbox('GPU', df['Gpu brand'].unique())

    with col2:
        touchscreen = st.radio('Touchscreen', ['No','Yes'], horizontal=True, label_visibility="visible")
        ips = st.radio('IPS Display', ['No','Yes'], horizontal=True, label_visibility="visible")
        screen_size = st.slider('Screen Size (inches)', 10.0, 18.0, 13.0)
        resolution = st.selectbox('Screen Resolution', [
            '1920x1080','1366x768','1600x900','3840x2160',
            '3200x1800','2880x1800','2560x1600','2560x1440','2304x1440'
        ])
        hdd = st.selectbox('HDD (GB)', [0,128,256,512,1024,2048])
        ssd = st.selectbox('SSD (GB)', [0,8,128,256,512,1024])
        os = st.selectbox('Operating System', df['os'].unique())

    st.markdown("---")

    # Center the button
    button_col = st.columns([1,2,1])[1]
    with button_col:
        predict = st.button('Predict Price', use_container_width=True)

    if predict:
        # Prepare input
        touchscreen_val = 1 if touchscreen == 'Yes' else 0
        ips_val = 1 if ips == 'Yes' else 0
        X_res = int(resolution.split('x')[0])
        Y_res = int(resolution.split('x')[1])
        ppi = ((X_res**2) + (Y_res**2))**0.5 / screen_size

        query = np.array([
            company, type, ram, weight, touchscreen_val, ips_val,
            ppi, cpu, hdd, ssd, gpu, os
        ]).reshape(1, 12)

        predicted_price = int(np.exp(pipe.predict(query)[0]))

        st.markdown(
            f"""
            <div class="result-container">
                <h2 style="color:#22223b;">💰 Estimated Price: <span style="color:#007200;">₹ {predicted_price:,}</span></h2>
                <p style="color:#4a4e69;">Note: This is an estimated price based on the selected configuration.</p>
            </div>
            """,
            unsafe_allow_html=True
        )


