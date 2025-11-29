#/usr/bin/env python3

import pandas as pd
import streamlit as st

@st.cache_data
def example_data():
	data = {
		"Vendor": ["Vendor A", "Vendor B", "Vendor C", "Vendor D",
				"Vendor E", "Vendor F", "Vendor G", "Vendor H"],
		"Ability to Execute": [9, 8, 5, 4, 7, 6, 3, 2],
		"Completeness of Vision": [9, 5, 9, 4, 6, 3, 7, 2]
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