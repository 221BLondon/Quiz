import pandas as pd
import streamlit as st

# Load questions from CSV file
def load_questions(file_path):
    return pd.read_csv(file_path)

# Streamlit app
def main():
    st.title("Mock Exam")
    
    file_path = 'https://docs.google.com/spreadsheets/d/1FpUvZMMIC2aFxxA4bmmSlPaVuBCY36aR8-qKWSKyrQ0/edit?usp=sharing'  # Path to your CSV file
    df = load_questions(file_path)
    
    num_questions = len(df)
    correct_count = 0
    answers = []
    
    for index, row in df.iterrows():
        st.subheader(f"Question {row['Question Number']}")
        st.write(row['Question'])
        options = [row['Option A'], row['Option B'], row['Option C'], row['Option D']]
        user_answer = st.radio("Choose your answer:", options, key=index)
        
        if st.button("Submit Answer", key=f"submit_{index}"):
            if user_answer == row['Correct Answer']:
                st.success("Correct!")
                correct_count += 1
            else:
                st.error(f"Wrong! The correct answer was {row['Correct Answer']}.")
                st.info(f"Explanation: {row['Explanation']}")
            
            answers.append({
                'Question': row['Question'],
                'User Answer': user_answer,
                'Correct Answer': row['Correct Answer'],
                'Explanation': row['Explanation']
            })
    
    if st.button("Finish Exam"):
        st.write(f"\nYou got {correct_count} out of {num_questions} questions right.")
        st.write(f"Your score: {correct_count / num_questions * 100:.2f}%")
        
        st.subheader("Detailed Results:")
        for answer in answers:
            st.write(f"**Question:** {answer['Question']}")
            st.write(f"**Your Answer:** {answer['User Answer']}")
            st.write(f"**Correct Answer:** {answer['Correct Answer']}")
            st.write(f"**Explanation:** {answer['Explanation']}")

if __name__ == "__main__":
    main()
