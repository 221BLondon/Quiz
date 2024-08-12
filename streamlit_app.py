import pandas as pd
import streamlit as st

# Load questions from CSV file
def load_questions(file_path):
    DATA_FILENAME = Path(__file__).parent/'new.csv'
    return pd.read_csv(DATA_FILENAME)

def main():
    st.title("Mock Exam")

    file_path = 'questions.csv'  # Path to your downloaded CSV file
    df = load_questions(file_path)

    if 'start' not in st.session_state:
        st.session_state.start = False
        st.session_state.current_question_index = 0
        st.session_state.answers = []
        st.session_state.correct_count = 0

    def start_exam():
        st.session_state.start = True
        st.session_state.current_question_index = 0
        st.session_state.answers = []
        st.session_state.correct_count = 0

    def stop_exam():
        st.session_state.start = False

    def next_question():
        if st.session_state.current_question_index < len(df) - 1:
            st.session_state.current_question_index += 1

    def previous_question():
        if st.session_state.current_question_index > 0:
            st.session_state.current_question_index -= 1

    if not st.session_state.start:
        if st.button("Start Exam"):
            start_exam()
    else:
        index = st.session_state.current_question_index
        row = df.iloc[index]

        st.subheader(f"Question {row['Question Number']}")
        st.write(row['Question'])
        options = [row['Option A'], row['Option B'], row['Option C'], row['Option D']]
        user_answer = st.radio("Choose your answer:", options, key=index)

        if st.button("Submit Answer"):
            if user_answer == row['Correct Answer']:
                st.success("Correct!")
                st.session_state.correct_count += 1
            else:
                st.error(f"Wrong! The correct answer was {row['Correct Answer']}.")
                st.info(f"Explanation: {row['Explanation']}")

            st.session_state.answers.append({
                'Question': row['Question'],
                'User Answer': user_answer,
                'Correct Answer': row['Correct Answer'],
                'Explanation': row['Explanation']
            })

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
                for answer in st.session_state.answers:
                    st.write(f"**Question:** {answer['Question']}")
                    st.write(f"**Your Answer:** {answer['User Answer']}")
                    st.write(f"**Correct Answer:** {answer['Correct Answer']}")
                    st.write(f"**Explanation:** {answer['Explanation']}")

if __name__ == "__main__":
    main()
