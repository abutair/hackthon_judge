import streamlit as st
import requests
import pandas as pd
from io import BytesIO

# Constants
BACKEND_URL = 'http://127.0.0.1:5000'

def judge_submission_page():
    st.title("Judge Submission Page")

    st.write("Enter your hackathon idea, upload your code file, and provide any additional documentation to receive a score and feedback:")

    idea = st.text_area("Hackathon Idea")
    code_file = st.file_uploader("Upload Code File", type=['py', 'txt', 'zip'])
    #documentation = st.text_area("Additional Documentation")

    if st.button("Submit"):
        if not idea:
            st.error("Please enter an idea.")
        else:
            code_content = ""
            if code_file is not None:
                code_content = code_file.read().decode('utf-8')
            
            payload = {
                'idea': idea,
                'code': code_content,
                #'documentation': documentation
            }
            response = requests.post(f'{BACKEND_URL}/judge', json=payload)
            if response.status_code == 200:
                result = response.json().get('result')
                st.write("Evaluation Result:")
                st.success(result)
            else:
                st.error("There was an error processing your request.")

def organizer_schedule_upload_page():
    st.title("Organizer Schedule Upload Page")

    st.write("Upload your schedule document (Excel or CSV):")
    uploaded_file = st.file_uploader("Choose a file", type=['xlsx', 'csv'])

    if uploaded_file is not None:
        # Send the file to the backend
        response = requests.post(
            f'{BACKEND_URL}/upload_schedule',
            files={'file': uploaded_file.getvalue()}
        )
        
        if response.status_code == 200:
            schedule_data = response.json().get('schedule')
            df = pd.read_json(schedule_data, orient='records')
            
            st.write("Parsed Schedule:")
            st.dataframe(df)
            
            # Additional functionality to set reminders (placeholder)
            if st.button("Set Reminders"):
                st.success("Reminders set for upcoming judging sessions.")
        else:
            st.error("There was an error processing your request.")

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Judge Submission Page", "Organizer Schedule Upload Page"])

    if page == "Judge Submission Page":
        judge_submission_page()
    elif page == "Organizer Schedule Upload Page":
        organizer_schedule_upload_page()

if __name__ == '__main__':
    main()
