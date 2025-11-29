#!/usr/bin/env python3

import magic_quadrant
import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(page_icon=None, layout="wide", initial_sidebar_state=None, menu_items=None)
st.title("Magic Quadrant")

col1, col2 = st.columns([3, 1])
with col1:
	uploaded_file = st.file_uploader("Upload Data", type=["csv", "xls", "xlsx", "json"])
with col2:
	if st.button("Generate sample dataset"):
		df = pd.DataFrame({
			"Project": [f"Project {i+1}" for i in range(20)],
			"Delivery Confidence": np.random.randint(1, 6, size=20),
			"Customer Value": np.random.randint(1, 6, size=20),
		})
		filename = "sample_data.csv"
		st.success("Generated sample dataset with 20 rows")

if uploaded_file is not None:
	# Read the file into a pandas DataFrame depending on the file type
	try:
		filename = uploaded_file.name
		if filename.endswith((".xls", ".xlsx")):
			df = pd.read_excel(uploaded_file)
		elif filename.endswith('.json'):
			# streamlit's UploadedFile has a file buffer we can pass to pandas
			df = pd.read_json(uploaded_file)
		else:
			# CSV by default
			# Support both text and binary uploads
			uploaded_file.seek(0)
			df = pd.read_csv(uploaded_file)
	except Exception as e:
		st.error(f"Could not read uploaded file: {e}")
		df = None

if df is not None:
    st.success(f"Loaded {len(df)} rows and {len(df.columns)} columns from {filename}")
    st.write("Data types:")
    st.write(df.dtypes)
    st.dataframe(df)

    # If numeric columns are present, provide a simple scatter plot
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    text_cols = df.select_dtypes(include=["object", "string"]).columns.tolist()
    if len(numeric_cols) >= 2:
        x = st.sidebar.selectbox("X column", numeric_cols, index=0)
        x_min = st.sidebar.number_input("Lower Limit for X axis", value=float(df[x].min()))
        x_max = st.sidebar.number_input("Upper Limit for X axis", value=float(df[x].max()))
        y = st.sidebar.selectbox("Y column", numeric_cols, index=1)
        y_min = st.sidebar.number_input("Lower Limit for Y axis", value=float(df[y].min()))
        y_max = st.sidebar.number_input("Upper Limit for Y axis", value=float(df[y].max()))
        
        text = st.sidebar.selectbox("Text column", text_cols, index=0)
        lower_left = st.sidebar.text_input("Label for Lower Left Quadrant", value="Niche Players")
        lower_right = st.sidebar.text_input("Label for Lower Right Quadrant", value="Visionaries")
        upper_left = st.sidebar.text_input("Label for Upper Left Quadrant", value="Challengers")
        upper_right = st.sidebar.text_input("Label for Upper Right Quadrant", value="Leaders")
        
        mq = magic_quadrant.create_mq(df, x, x_min, x_max, y, y_min, y_max, text, lower_left, lower_right, upper_left, upper_right)
        st.plotly_chart(mq, use_container_width=True)
    else:
        st.info("The dataset does not contain two numeric columns for plotting.")
