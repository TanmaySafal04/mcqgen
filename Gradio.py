import os
import json
import traceback
import pandas as pd
import streamlit as st
from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.logger import logging
from dotenv import load_dotenv
import Gradio as gr
from langchain.callbacks import get_openai_callback

from src.mcqgenerator.MCQGenerator import generate_evaluate_chain

#loading json file
with open("D:\GenAI\mcqgen\Response.json","r") as file:
    RESPONSE_JSON=json.load(file)

gr.close_all()

def mcq(input_file,subject,tone,mcq_count):
    text = read_file(input_file)
    try:          
        # Count tokens and API call cost in $USD
        with get_openai_callback() as cb:
            output=generate_evaluate_chain(
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
        gr.error("Error")

               
    print(f"Total Tokens:{cb.total_tokens}")
    print(f"Prompt Tokens:{cb.prompt_tokens}")
    print(f"Completion Tokens:{cb.completion_tokens}")
    print(f"Total Cost:{cb.total_cost}")

    if isinstance(output,dict):
                        #Extract quiz data from response
                        quiz=output.get("quiz",None)
                        if quiz is not None:
                            table_data = get_table_data(quiz)
                            if table_data is not None:
                                df=pd.DataFrame(table_data)
                                df.index=df.index+1
                                #gr.Dataframe(type="numpy",header =["MCQ","CHOICES","Correct Answer"] row_count=mcq_count, col_count=3)
                                #Displays the review in a text box as well
                                #st.text_area(label="Review", value=output['review'])
                            else:
                                gr.error("Error in the table data")
    return df

#Inputs
subject = gr.inputs.Textbox(label="Subject")
tone =  gr.inputs.Textbox(label="Difficulty level")
mcq_count =  gr.inputs.Number(label="No. of MCQs")
upload_file = gr.inputs.File(label="Upload File", type="file")



demo = gr.Interface(fn=mcq,
                    title="MCQ Creator App",
                    inputs=[upload_file,subject,tone,mcq_count],
                    output=gr.Dataframe(type="pandas",header =["MCQ","CHOICES","Correct Answer"] row_count=mcq_count, col_count=3)
                                       
                    )

if __name__ == "__main__":
    demo.launch(share=True)

