#!/usr/bin/env python3

import numpy as np
import pandas as pd
import streamlit as st

import mq_chart, data_cache

ABOUT = """
	This app allows you to create Magic Quadrant charts from your own datasets.
	Upload a CSV, Excel, or JSON file containing at least two numeric columns and one text column.
	You can also use the sample dataset provided.
	
	**Instructions:**
	1. Upload your dataset using the file uploader on the left, or click "Use sample dataset".
	2. Select the variables for the X and Y axes from the sidebar.
	3. Choose a text column to label the points in the chart.
	4. Customize the quadrant names as desired.
	
	**Note:** The app uses Plotly for interactive charting and Streamlit for the web interface.
"""

def get_data():
	uploaded_file = st.file_uploader("Upload your data file (CSV, Excel, JSON)", type=['csv', 'xls', 'xlsx', 'json'])
	use_sample = st.button("Use sample dataset")

	if uploaded_file is not None:
		df, filename = data_cache.read_uploaded_file(uploaded_file)
	elif use_sample:
		df, filename = data_cache.example_data()
	else:
		df = None
		filename = None

	if df is not None:
		st.success(f"Loaded {len(df)} rows and {len(df.columns)} columns from {filename}")
		st.write("Data types:")
		st.write(df.dtypes)
		st.dataframe(df)

		# Store in session state
		st.session_state.df = df
		st.session_state.filename = filename
	elif 'df' in st.session_state:
		df = st.session_state.df
		filename = st.session_state.filename

	return df, filename


def create_chart(df):
	st.sidebar.header("Chart Settings")

	text = st.sidebar.selectbox("Display Label", text_cols, index=0)

	with st.sidebar.expander("X Axis", expanded=True):
		x = st.selectbox("Variable", numeric_cols, index=0)
		cols = st.columns(2)
		with cols[0]:
			x_min = st.number_input("Lower Limit", value=float(df[x].min()))
		with cols[1]:
			x_max = st.number_input("Upper Limit", value=float(df[x].max()))

	numeric_cols2 = numeric_cols.copy()
	numeric_cols2.remove(x)

	with st.sidebar.expander("Y Axis", expanded=True):
		y = st.selectbox("Variable", numeric_cols2, index=0, key="y")
		cols = st.columns(2)
		with cols[0]:
			y_min = st.number_input("Lower Limit", value=float(df[y].min()), key="y_min")
		with cols[1]:
			y_max = st.number_input("Upper Limit", value=float(df[y].max()), key="y_max")

	with st.sidebar.expander("Quadrant Name", expanded=True):
		cols = st.columns(2)
		with cols[0]:
			upper_left = st.text_input("Upper Left", value="Challengers")
		with cols[1]:
			upper_right = st.text_input("Upper Right", value="Leaders")

		cols = st.columns(2)
		with cols[0]:
			lower_left = st.text_input("Lower Left", value="Niche Players")
		with cols[1]:
			lower_right = st.text_input("Lower Right", value="Visionaries")

	mq = mq_chart.create(df, x, x_min, x_max, y, y_min, y_max, text, lower_left, lower_right, upper_left, upper_right)

	return mq

		

st.set_page_config(page_icon=None, layout="wide", initial_sidebar_state=None, menu_items=None)

st.title("Magic Quadrant")


with st.expander("ℹ️ About", expanded=False):
	st.markdown(ABOUT)	


with st.expander("📁 Data Source", expanded=True):
	df, filename = get_data()

if df is not None:
	# If numeric columns are present, provide a simple scatter plot
	numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
	text_cols = df.select_dtypes(include=["object", "string"]).columns.tolist()

	if len(numeric_cols) < 2:
		st.info("The dataset does not contain two numeric columns for plotting.")
	else:
		mq = create_chart(df)
		with st.expander("📊 Magic Quadrant", expanded=True):
			st.info("Use the left panel to customize the chart settings.", icon="ℹ️")
			st.plotly_chart(mq, width='stretch')


