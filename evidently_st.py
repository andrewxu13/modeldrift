import streamlit as st
import json
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Example usage
install('matplotlib')

import streamlit as st
import json
import matplotlib.pyplot as plt

# Assuming the JSON content is loaded into evidently_report_correctly_parsed
# This should be replaced with the correct loading mechanism as per previous steps

def plot_distributions_checked(column_details):
    current_x = column_details['current']['small_distribution']['x']
    current_y = column_details['current']['small_distribution']['y']
    reference_x = column_details['reference']['small_distribution']['x']
    reference_y = column_details['reference']['small_distribution']['y']

    # Check and report if lengths mismatch
    if len(current_x) != len(current_y) or len(reference_x) != len(reference_y):
        st.error(f"Dimension mismatch detected in column '{column_details['column_name']}': current (x,y) lengths = ({len(current_x)}, {len(current_y)}), reference (x,y) lengths = ({len(reference_x)}, {len(reference_y)})")
        return

    plt.figure(figsize=(10, 6))
    plt.plot(current_x, current_y, label='Current', marker='o')
    plt.plot(reference_x, reference_y, label='Reference', marker='x')
    plt.legend()
    plt.title(column_details['column_name'])
    plt.xlabel('Value')
    plt.ylabel('Density')
    st.pyplot(plt)


def interactive_drift_analysis(report):
    st.title("Interactive Data Drift Analysis")

    columns = list(report['metrics'][1]['result']['drift_by_columns'].keys())
    selected_column = st.selectbox("Select a column to analyze:", columns)

    column_details = report['metrics'][1]['result']['drift_by_columns'][selected_column]
    
    if column_details['column_type'] == 'num':
        st.write(f"Statistical Test: {column_details['stattest_name']}")
        st.write(f"Drift Score: {column_details['drift_score']}")
        st.write(f"Drift Detected: {column_details['drift_detected']}")
        plot_distributions_checked(column_details)
    else:
        st.write("Detailed analysis for categorical columns not implemented in this example.")

# Load the JSON data
with open('data_drift_report.json', 'r') as file:
    json_string = json.load(file)
    evidently_report_correctly_parsed = json.loads(json_string)

interactive_drift_analysis(evidently_report_correctly_parsed)



