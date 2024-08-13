import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Load questions from CSV file
def load_questions(file_path):
    return pd.read_csv(file_path)

def main():
    st.title("Mock Exam")

    file_path = 'questions.csv'  # Path to your downloaded CSV file
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

    def previous_question():
        if st.session_state.current_question_index > 0:
            st.session_state.current_question_index -= 1

    def handle_answer(submitted_answer):
        index = st.session_state.current_question_index
        row = df.iloc[index]
        correct_answer_key = row['Correct Answer']
        if submitted_answer == correct_answer_key:
            st.session_state.correct_count += 1
        st.session_state.answers[index] = submitted_answer

    # Layout
    col1, col2 = st.columns([2, 1])

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

            # Create a selectbox for answers without default selection
            selected_answer = st.radio("Choose your answer:", options, key="options", index=None if st.session_state.answers[index] is None else options.index(st.session_state.answers[index]))

            if st.button("Submit Answer"):
                # Map options to keys for comparison
                selected_answer_key = option_keys[options.index(selected_answer)]
                handle_answer(selected_answer_key)
                correct_answer_key = row['Correct Answer']
                if selected_answer_key == correct_answer_key:
                    st.success("Correct!")
                else:
                    st.error(f"Wrong! The correct answer was {correct_answer_key}.")
                    st.info(f"Explanation: {row['Explanation']}")

            # Navigation buttons
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.session_state.current_question_index > 0:
                    if st.button("Previous"):
                        previous_question()
            with col2:
                if st.session_state.current_question_index < len(df) - 1:
                    if st.button("Next"):
                        next_question()
            with col3:
                if st.button("Finish Exam"):
                    stop_exam()

    with col2:
        if st.session_state.start or st.session_state.show_results:
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
                        if st.button(btn_label, key=q_index, help=f"Go to Question {q_index + 1}",
                                     use_container_width=True, on_click=lambda idx=q_index: st.session_state.update({"current_question_index": idx}),
                                     args=(q_index,)):
                            st.session_state.current_question_index = q_index

    # Results and details at the bottom
    if st.session_state.show_results:
        st.subheader("Exam Details")
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
