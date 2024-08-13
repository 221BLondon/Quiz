import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Load questions from CSV file
def load_questions(file_path):
    DATA_FILENAME = Path(__file__).parent / 'new.csv'
    return pd.read_csv(DATA_FILENAME)

def main():
    st.title("Mock Exam")

    file_path = 'questions.csv'  # Path to your downloaded CSV file
    df = load_questions(file_path)

    if 'start' not in st.session_state:
        st.session_state.start = False
        st.session_state.current_question_index = 0
        st.session_state.answers = [None] * len(df)
        st.session_state.correct_count = 0

    def start_exam():
        st.session_state.start = True
        st.session_state.current_question_index = 0
        st.session_state.answers = [None] * len(df)
        st.session_state.correct_count = 0

    def stop_exam():
        st.session_state.start = False

    def next_question():
        if st.session_state.current_question_index < len(df) - 1:
            st.session_state.current_question_index += 1

    def previous_question():
        if st.session_state.current_question_index > 0:
            st.session_state.current_question_index -= 1

    def go_to_question(index):
        st.session_state.current_question_index = index

    if not st.session_state.start:
        if st.button("Start Exam"):
            start_exam()
    else:
        index = st.session_state.current_question_index
        row = df.iloc[index]

        # Display question navigation buttons in rows of 8 columns
        st.subheader("Question Navigation")
        total_questions = len(df)
        rows = math.ceil(total_questions / 8)
        
        for r in range(rows):
            cols = st.columns(8)
            for i in range(8):
                q_index = r * 8 + i
                if q_index >= total_questions:
                    break
                btn_label = f"Q{q_index + 1}"
                with cols[i]:
                    if st.session_state.answers[q_index] is not None:
                        # Color the button green if the question has been answered
                        if st.button(btn_label, key=f"btn_{q_index}", help="Answered", args=(q_index,)):
                            go_to_question(q_index)
                    else:
                        if st.button(btn_label, key=f"btn_{q_index}", args=(q_index,)):
                            go_to_question(q_index)

        st.subheader(f"Question {row['Question Number']}")
        st.write(row['Question'])
        options = [row['Option A'], row['Option B'], row['Option C'], row['Option D']]
        option_keys = ['A', 'B', 'C', 'D']

        # Map options to keys
        option_map = dict(zip(options, option_keys))
        user_answer = st.radio("Choose your answer:", options, key=f"radio_{index}", index=None)  # No default selection

        if st.button("Submit Answer"):
            if user_answer:  # Only process if an answer was selected
                correct_answer_key = row['Correct Answer']
                selected_option_key = option_map[user_answer]

                if selected_option_key == correct_answer_key:
                    st.success("Correct!")
                    st.session_state.correct_count += 1
                else:
                    st.error(f"Wrong! The correct answer was {correct_answer_key}.")
                    st.info(f"Explanation: {row['Explanation']}")

                # Save the user's answer
                st.session_state.answers[index] = selected_option_key
            else:
                st.warning("Please select an answer before submitting.")

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
                st.session_state.start = False
                st.write(f"\nYou got {st.session_state.correct_count} out of {len(df)} questions right.")
                st.write(f"Your score: {st.session_state.correct_count / len(df) * 100:.2f}%")

                st.subheader("Detailed Results:")
                for i, answer in st.session_state.answers:
                    st.write(f"**Question {i+1}:** {df.iloc[i]['Question']}")
                    st.write(f"**Your Answer:** {answer}")
                    st.write(f"**Correct Answer:** {df.iloc[i]['Correct Answer']}")
                    st.write(f"**Explanation:** {df.iloc[i]['Explanation']}")

if __name__ == "__main__":
    main()
