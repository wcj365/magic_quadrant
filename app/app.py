#!/usr/bin/env python3

import numpy as np
import pandas as pd
import streamlit as st

import magic_quadrant

st.set_page_config(page_icon=None, layout="wide", initial_sidebar_state=None, menu_items=None)

st.title("Magic Quadrant")

@st.cache_data
def example_data():	
	data = {
		"Vendor": ["Vendor A", "Vendor B", "Vendor C", "Vendor D",
				"Vendor E", "Vendor F", "Vendor G", "Vendor H"],
		"Ability to Execute": [9, 8, 5, 4, 7, 6, 3, 2],
		"Completeness of Vision": [9, 5, 9, 4, 6, 3, 7, 2],
		"Quadrant": ["Leader", "Challenger", "Visionary", "Niche Player",
					"Leader", "Challenger", "Visionary", "Niche Player"]
	}

	# Create DataFrame
	df = pd.DataFrame(data)
	filename = "sample_data.csv"
	return df, filename


@st.cache_data
def read_uploaded_file(uploaded_file):

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

	return df, filename


if 'df' in st.session_state:
	df = st.session_state.df
	filename = st.session_state.filename
else:
    df = None
    filename = ""
	

col1, col2 = st.columns([3, 1])

with col1:
	uploaded_file = st.file_uploader("Upload Data", type=["csv", "xls", "xlsx", "json"])
	if uploaded_file is not None:
		# Read the file into a pandas DataFrame depending on the file type
		try:
			df, filename = read_uploaded_file(uploaded_file)
			# Cache the dataframe in session state
			st.session_state.df = df
			st.session_state.filename = filename
		except Exception as e:
			st.error(f"Could not read uploaded file: {e}")

with col2:
	if st.button("Use sample dataset"):
		df, filename = example_data()
		# Cache the dataframe in session state
		st.session_state.df = df
		st.session_state.filename = filename


if df is not None:
    st.success(f"Loaded {len(df)} rows and {len(df.columns)} columns from {filename}")
    st.write("Data types:")
    st.write(df.dtypes)
    st.dataframe(df)

    # If numeric columns are present, provide a simple scatter plot
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    text_cols = df.select_dtypes(include=["object", "string"]).columns.tolist()
    if len(numeric_cols) >= 2:
        x = st.sidebar.selectbox("X Axis", numeric_cols, index=0)
        x_min = st.sidebar.number_input("Lower Limit for X", value=float(df[x].min()))
        x_max = st.sidebar.number_input("Upper Limit for X", value=float(df[x].max()))

        numeric_cols2 = numeric_cols.copy()
        numeric_cols2.remove(x)
        y = st.sidebar.selectbox("Y Axis", numeric_cols2, index=0)
        y_min = st.sidebar.number_input("Lower Limit for Y", value=float(df[y].min()))
        y_max = st.sidebar.number_input("Upper Limit for Y", value=float(df[y].max()))
        
        text = st.sidebar.selectbox("Display Label", text_cols, index=0)
        lower_left = st.sidebar.text_input("Name for Lower Left Quadrant", value="Niche Players")
        lower_right = st.sidebar.text_input("Name for Lower Right Quadrant", value="Visionaries")
        upper_left = st.sidebar.text_input("Name for Upper Left Quadrant", value="Challengers")
        upper_right = st.sidebar.text_input("Name for Upper Right Quadrant", value="Leaders")
        
        mq = magic_quadrant.create_mq(df, x, x_min, x_max, y, y_min, y_max, text, lower_left, lower_right, upper_left, upper_right)
        st.plotly_chart(mq, width='stretch')
    else:
        st.info("The dataset does not contain two numeric columns for plotting.")
