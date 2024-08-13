import streamlit as st
import pandas as pd
from pathlib import Path

# Load questions from CSV file
def load_questions(file_path):
    DATA_FILENAME = Path(__file__).parent / 'new.csv'
    return pd.read_csv(DATA_FILENAME)

def main():
    st.title("Interactive Mock Exam")

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

    # Sidebar for navigation and exam details
    with st.sidebar:
        st.header("Navigation")

        if not st.session_state.start:
            if st.button("Start Exam"):
                start_exam()
        else:
            st.button("Stop Exam", on_click=stop_exam)

            # Collapsible Jump to Question Section
            with st.expander("Jump to a Question"):
                total_questions = len(df)
                rows = math.ceil(total_questions / 8)
                for r in range(rows):
                    cols = st.columns(8)
                    for i in range(8):
                        q_index = r * 8 + i
                        if q_index >= total_questions:
                            break
                        btn_label = f"Q{q_index + 1}"
                        btn_color = "lightgreen" if st.session_state.answers[q_index] is not None else "lightcoral"
                        # Use a markdown button for custom styling
                        st.markdown(f'''
                            <style>
                                .stButton button {{
                                    background-color: {btn_color};
                                    border: 1px solid #ddd;
                                    border-radius: 5px;
                                    padding: 10px;
                                    color: black;
                                }}
                                .stButton button:hover {{
                                    background-color: {btn_color};
                                }}
                            </style>
                            ''', unsafe_allow_html=True)
                        with cols[i]:
                            if st.button(btn_label, key=f"nav_{q_index}"):
                                go_to_question(q_index)

            # Detailed Results
            if st.session_state.start and st.button("Finish Exam"):
                st.session_state.start = False
                st.write(f"\nYou got {st.session_state.correct_count} out of {len(df)} questions right.")
                st.write(f"Your score: {st.session_state.correct_count / len(df) * 100:.2f}%")

                # Show detailed results
                st.subheader("Detailed Results")
                for i, answer in enumerate(st.session_state.answers):
                    if answer is not None:
                        st.write(f"**Question {i + 1}:** {df.iloc[i]['Question']}")
                        st.write(f"**Your Answer:** {answer}")
                        st.write(f"**Correct Answer:** {df.iloc[i]['Correct Answer']}")
                        st.write(f"**Explanation:** {df.iloc[i]['Explanation']}")

    # Main content area
    if st.session_state.start:
        index = st.session_state.current_question_index
        row = df.iloc[index]

        st.subheader(f"Question {index + 1}: {row['Question']}")
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
                st.button("Previous", on_click=previous_question)
        with col2:
            if st.session_state.current_question_index < len(df) - 1:
                st.button("Next", on_click=next_question)

if __name__ == "__main__":
    main()
