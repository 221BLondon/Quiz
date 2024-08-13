import streamlit as st
import pandas as pd
import math
from pathlib import Path
from question_loader import load_questions

def previous_question():
    if st.session_state.current_question_index > 0:
        st.session_state.current_question_index -= 1

def next_question():
    if st.session_state.current_question_index < len(df) - 1:
        st.session_state.current_question_index += 1
def go_to_question(index):
    st.session_state.current_question_index = index

def start_exam():
    st.session_state.start = True
    st.session_state.current_question_index = 0
    st.session_state.answers = [None] * len(df)
    st.session_state.correct_count = 0
    st.session_state.show_results = False

def stop_exam():
    st.session_state.start = False
    st.session_state.show_results = True

def restart_exam():
    start_exam()

def handle_answer(submitted_answer):
    index = st.session_state.current_question_index
    row = df.iloc[index]
    correct_answer_key = row['Correct Answer']
    if submitted_answer == correct_answer_key:
        st.session_state.correct_count += 1
    st.session_state.answers[index] = submitted_answer
# Inject custom CSS to style the buttons in the sidebar
st.markdown(
    """
    <style>
    .correct-button {
        background-color: lightgreen !important;
        color: black !important;
    }
    .incorrect-button {
        background-color: lightblue !important;
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
def main():
    st.title("Mock Exam")

    file_path = 'new.csv'  # Path to your CSV file
    global df
    df = load_questions(file_path)

    # Initialize session state
    if 'start' not in st.session_state:
        st.session_state.start = False
        st.session_state.current_question_index = 0
        st.session_state.answers = [None] * len(df)
        st.session_state.correct_count = 0
        st.session_state.show_results = False

    # Sidebar for navigation and restarting
    with st.sidebar:
        if st.session_state.show_results:
            st.button("Restart Exam", on_click=restart_exam)
        else:
            if st.session_state.start:
                st.subheader("Jump to Question")
                total_questions = len(df)
                num_rows = math.ceil(total_questions / 8)

                for r in range(num_rows):
                    cols = st.columns(8)
                    for i in range(8):
                        q_index = r * 8 + i
                        if q_index >= total_questions:
                            break

                        btn_label = str(q_index + 1)
                        # button_color = 'lightgreen' if st.session_state.answers[q_index] is not None else 'lightblue'

                        # with cols[i]:
                        #     st.button(btn_label, key=q_index, help=f"Go to Question {q_index + 1}",
                        #               use_container_width=True, on_click=lambda idx=q_index: st.session_state.update({"current_question_index": idx}))
                        # # Assign CSS classes to buttons based on whether the question has been answered
                        button_class = "correct-button" if st.session_state.answers[q_index] is not None else "incorrect-button"
                        
                        with cols[i]:
                            button_html = f"""
                            <button class="{button_class}" style="width: 100%;" onClick="go_to_question({q_index})">
                                {btn_label}
                            </button>
                            """
                            st.markdown(button_html, unsafe_allow_html=True)

    if not st.session_state.start:
        if st.button("Start Exam"):
            start_exam()
    else:
        index = st.session_state.current_question_index
        row = df.iloc[index]

        st.subheader(f"Question {row['Question Number']}")
        st.write(row['Question'])
        options = [row['Option A'], row['Option B'], row['Option C'], row['Option D']]
        option_keys = ['A', 'B', 'C', 'D']

        # Include a placeholder for no selection
        options_with_placeholder = ["Select an option"] + options
        option_keys_with_placeholder = [None] + option_keys

        # Determine the index of the previous answer if it exists
        previous_answer_key = st.session_state.answers[index]
        previous_answer_index = option_keys_with_placeholder.index(previous_answer_key) if previous_answer_key and previous_answer_key in option_keys_with_placeholder else 0

        selected_answer = st.radio("Choose your answer:", options_with_placeholder, index=previous_answer_index)

        if st.button("Submit Answer"):
            if selected_answer != "Select an option":
                selected_answer_key = option_keys_with_placeholder[options_with_placeholder.index(selected_answer)]
                handle_answer(selected_answer_key)
                correct_answer_key = row['Correct Answer']
                if selected_answer_key == correct_answer_key:
                    st.success("Correct!")
                else:
                    st.error(f"Wrong! The correct answer was {correct_answer_key}.")
                    st.info(f"Explanation: {row['Explanation']}")
            else:
                st.warning("Please select an answer before submitting.")

        # Navigation buttons
        st.button("Previous", on_click=previous_question, disabled=st.session_state.current_question_index == 0)
        st.button("Next", on_click=next_question, disabled=st.session_state.current_question_index == len(df) - 1)
        st.button("Finish Exam", on_click=stop_exam)

    if st.session_state.show_results:
        st.write("# Exam Details")
        st.write(f"You have answered {st.session_state.correct_count} out of {len(df)} questions correctly.")
        st.write(f"Your score: {st.session_state.correct_count / len(df) * 100:.2f}%")
        st.subheader("Detailed Results")
        for i, answer in enumerate(st.session_state.answers):
            if answer is not None:
                st.write(f"**Question {i + 1}:** {df.iloc[i]['Question']}")
                st.write(f"**Your Answer:** {answer}")
                st.write(f"**Correct Answer:** {df.iloc[i]['Correct Answer']}")
                st.write(f"**Explanation:** {df.iloc[i]['Explanation']}")

if __name__ == "__main__":
    main()

