import os
import json
import traceback
import pandas as pd
import streamlit as st
from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.logger import logging
from dotenv import load_dotenv

from langchain.callbacks import get_openai_callback

from src.mcqgenerator.MCQGenerator import generate_evaluate_chain

#loading json file
with open("D:\GenAI\mcqgen\Response.json","r") as file:
    RESPONSE_JSON=json.load(file)

#creating a title for the app
    st.title("MCQ Creator App with Langchain")

# Creat a form using st.form
    with st.form("user_inputs"):
        #file upload
        uploaded_file=st.file_uploader("Upload a PDF or a txt file")

        #Input fields
        mcq_count=st.number_input("No. of MCQs", min_value=3, max_value=50)
      
        #Subject 
        subject=st.text_input("Insert subject", max_chars=20)

        # quiz tone
        tone=st.text_input("Difficulty lvl of question", max_chars=20, placeholder="Simple")

        #Add button
        button=st.form_submit_button("Create MCQs")

        if button and uploaded_file is not None and mcq_count and subject and tone:
            with st.spinner("Loading..."):
                try:
                    text=read_file(uploaded_file)
                    # Count tokens and API call cost in $USD
                    with get_openai_callback() as cb:
                        response=generate_evaluate_chain(
                      {
                       "text": text,
                       "number": mcq_count,
                       "subject":subject,
                        "tone": tone,
                        "response_json": json.dumps(RESPONSE_JSON)
                       }
                     
                     )
                except Exception as e:
                    traceback.print_exception(type(e),e,e.__traceback__)
                    st.error("Error")

                else:
                    print(f"Total Tokens:{cb.total_tokens}")
                    print(f"Prompt Tokens:{cb.prompt_tokens}")
                    print(f"Completion Tokens:{cb.completion_tokens}")
                    print(f"Total Cost:{cb.total_cost}")

                    if isinstance(response,dict):
                        #Extract quiz data from response
                        quiz=response.get("quiz",None)
                        if quiz is not None:
                            table_data = get_table_data(quiz)
                            if table_data is not None:
                                df=pd.DataFrame(table_data)
                                df.index=df.index+1
                                st.table(df)
                                #Displays the review in a text box as well
                                st.text_area(label="Review", value=response['review'])
                            else:
                                st.error("Error in the table data")

                    else:
                        st.write(response)
