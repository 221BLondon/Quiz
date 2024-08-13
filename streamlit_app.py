import streamlit as st
import pandas as pd
import math
from pathlib import Path
from question_loader import load_questions  # Import the new question loading function
def previous_question():
    if st.session_state.current_question_index > 0:
        st.session_state.current_question_index -= 1
        st.write(f"Moving to Question Index: {st.session_state.current_question_index}") 
def main():
    st.title("Mock Exam")

    file_path = 'new.csv'  # Path to your CSV file
    df = load_questions(file_path)

    # Initialize session state
    if 'start' not in st.session_state:
        st.session_state.start = False
        st.session_state.current_question_index = 0
        st.session_state.answers = [None] * len(df)
        st.session_state.correct_count = 0
        st.session_state.show_results = False

    def start_exam():
        st.session_state.start = True
        st.session_state.current_question_index = 0
        st.session_state.answers = [None] * len(df)
        st.session_state.correct_count = 0
        st.session_state.show_results = False

    def stop_exam():
        st.session_state.start = False
        st.session_state.show_results = True

    def next_question():
        if st.session_state.current_question_index < len(df) - 1:
            st.session_state.current_question_index += 1

    def handle_answer(submitted_answer):
        index = st.session_state.current_question_index
        row = df.iloc[index]
        correct_answer_key = row['Correct Answer']
        if submitted_answer == correct_answer_key:
            st.session_state.correct_count += 1
        st.session_state.answers[index] = submitted_answer

    # Layout
    col1, col2 = st.columns([3, 1])

    with col1:
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

            # Create a radio button for answers with the previously selected answer preserved
            # print(st.session_state.answers[index])
            # y=option_keys.index(st.session_state.answers[index])
            # print(options[y])
            # z=options[y]
            # previous_index = None if st.session_state.answers[index] is None else z)
            # selected_answer = st.radio("Choose your answer:", options, key="options",
            #                            index=previous_index)
            # Create a radio button for answers with the previously selected answer preserved
            # previous_answer_key = st.session_state.answers[index]
            # previous_answer_index = option_keys.index(previous_answer_key) if previous_answer_key and (previous_answer_key in option_keys) else None
            # st.write(options[previous_answer_index])
            # selected_answer = st.radio("Choose your answer:", options,
            #                            index=options[previous_answer_index] if previous_answer_index and (previous_answer_index in options) else None)
            # Create a radio button for answers with the previously selected answer preserved
            previous_answer_key = st.session_state.answers[index]
            
            # Determine the index of the previous answer if it exists
            previous_answer_index = option_keys.index(previous_answer_key) if previous_answer_key else None
            
            # Conditionally write the previous answer if it exists
            if previous_answer_index is not None:
                st.write(options[previous_answer_index])
            
            # Set the default index for the radio button; if there's no previous answer, don't set a default
            selected_answer = st.radio("Choose your answer:", options, index=previous_answer_index if previous_answer_index is not None else 0)

            if st.button("Submit Answer"):
                if selected_answer is not None:
                    # Map options to keys for comparison
                    selected_answer_key = option_keys[options.index(selected_answer)]
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

    with col2:
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
                button_color = 'lightgreen' if st.session_state.answers[q_index] is not None else 'lightblue'
                
                with cols[i]:
                    button = st.button(btn_label, key=q_index, help=f"Go to Question {q_index + 1}",
                                      use_container_width=True, on_click=lambda idx=q_index: st.session_state.update({"current_question_index": idx}))
                    if button:
                        st.session_state.current_question_index = q_index

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
