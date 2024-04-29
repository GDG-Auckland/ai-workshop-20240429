import PIL.Image
import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
import PIL
import base64

st.set_page_config(layout = "wide")
genai.configure(api_key="AIzaSyCOU1JKjlgCHW-Fe2reqEMyKhChydhHF-k")

#Initialise some state variables
if "quiz_history" not in st.session_state:
    st.session_state["quiz_history"] = pd.DataFrame(
        {
            "question": pd.Series(dtype="str"),
            "correct_answer": pd.Series(dtype="str"),
            "user_answer": pd.Series(dtype="str"),
            "is_correct": pd.Series(dtype="bool"),
        }
    )
if "quiz_counter" not in st.session_state:
    st.session_state["quiz_counter"] = 0

@st.cache_data
def get_questions():
    quiz_df = pd.read_csv("data/questions.csv")
    return quiz_df

def check_a():
    pass

def check_answer(current_quiz):
    if st.session_state["input_answer"] is None:
        return
    explanation=""
    input_image_bytes = st.session_state["input_answer"]
    model = genai.GenerativeModel(st.session_state["model_selector"])
    prompt = (
        ""
    )
    st.info(prompt, icon="🤖")
    image = PIL.Image.open(input_image_bytes)
    response = model.generate_content([prompt, image])

    explanation = response.text
    score = int((response.text.split("\n")[0]).split("/")[0])
    is_correct = score>=8

    st.session_state["quiz_history"] = pd.concat([
            st.session_state["quiz_history"],
            pd.DataFrame(
                [{
                    "question" : current_quiz["question"],
                    "correct_answer" : current_quiz["answer"],
                    "user_answer" : f"data:image/png;base64,{base64.b64encode(st.session_state['input_answer'].getvalue()).decode()}",
                    "is_correct" : is_correct
                }]
            )],
            ignore_index=True
        )
    if is_correct:
        st.success(explanation if explanation else "Correct!", icon="✅")
    else:
        st.error(explanation if explanation else "Incorrect!", icon="❌")
    st.session_state["quiz_counter"] = st.session_state["quiz_counter"] + 1

def main():
    quiz_df = get_questions()
    quiz_index = st.session_state["quiz_counter"] % len(quiz_df)
    current_quiz = quiz_df.iloc[quiz_index]

    st.title("Quizzes!")
    st.header("This page provides you a list of static quizzes to answer!")
    st.divider()
    models = [ x.name for x in genai.list_models()]
    filtered_models = list(filter(lambda x: 'vision' in x, models))
    st.selectbox("Model", filtered_models, key="model_selector")
    with st.form("quiz_form", clear_on_submit = True):
        st.subheader(current_quiz["question"])
        st.file_uploader("Answer:", key="input_answer")
        st.form_submit_button(label="Submit", on_click=check_answer, kwargs={"current_quiz": current_quiz})
        
    # Show the quiz history if it's not empty
    if not st.session_state["quiz_history"].empty:
        st.dataframe(
            st.session_state["quiz_history"],
            column_config = {
                "question": "Question",
                "correct_answer" : "Correct Answer",
                "user_answer" : st.column_config.ImageColumn("Your Answer"),
                "is_correct" : "Correct?"
            }
        )
    
main()



