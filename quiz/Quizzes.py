import streamlit as st
import pandas as pd
import os
import google.generativeai as genai 

st.set_page_config(page_title="Quizzes", layout = "wide")
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

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
    explanation=""
    input_answer = st.session_state["input_answer"]
    if st.session_state["is_use_gemini"]:
        # model = genai.GenerativeModel('gemini-pro')
        model = genai.GenerativeModel(st.session_state["model_selector"])
        prompt = (
            "What is the accuracy of the given answer to the given question.\n" +
            "Always start the response with '{score}/10', explain the answer afterwards.\n" +
            "When evaluating answers, ignore letter accents.\n" +
            "Examples\n" +
            "Question: What is the capital of New Zealand?\n" +
            "Answer: Wellington\n" + 
            "Response: 10/10\n" + 
            "The answer is correct since Wellington is the capital of New Zealand!\n" +
            "Question: What is the national bird of New Zealand?\n" +
            "Answer: Kiwifruit\n" + 
            "Response: 4/10\n" +
            "The answer is not correct since kiwifruit is a fruit, and not a type of bird. The correct answer is kiwi.\n" +
            "Question: " + current_quiz["question"] + "\n"
            "Answer: " + input_answer + "\n"
            "Response:"
        )
        st.info(prompt, icon="🤖")
        response = model.generate_content(prompt)
        explanation = response.text
        score = int((response.text.split("\n")[0]).split("/")[0])
        is_correct = score>=8
    else:
        # If not using Gemini, perform a static check
        is_correct = input_answer.lower() == current_quiz["answer"].lower()

    st.session_state["quiz_history"] = pd.concat([
            st.session_state["quiz_history"],
            pd.DataFrame(
                [{
                    "question" : current_quiz["question"],
                    "correct_answer" : current_quiz["answer"],
                    "user_answer" : input_answer,
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
    is_use_gemini = st.checkbox("Use AI to check answer?", key="is_use_gemini")
    if is_use_gemini:
        models = [ x.name for x in genai.list_models()]
        filtered_models = list(filter(lambda x: 'gemini' in x and 'vision' not in x, models))
        st.selectbox("Model", filtered_models, key="model_selector")
    with st.form("quiz_form", clear_on_submit = True):
        st.subheader(current_quiz["question"])
        st.text_input("Answer:", key="input_answer")
        st.form_submit_button(label="Submit", on_click=check_answer, kwargs={"current_quiz": current_quiz})
        
    # Show the quiz history if it's not empty
    if not st.session_state["quiz_history"].empty:
        st.dataframe(
            st.session_state["quiz_history"],
            column_config = {
                "question": "Question",
                "correct_answer" : "Correct Answer",
                "user_answer" : "Your Answer",
                "is_correct" : "Correct?"
            }
        )
    
main()



