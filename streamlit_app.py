import streamlit as st
import pandas as pd
import math
from pathlib import Path
from question_loader import load_questions
import altair as alt
def previous_question():
    if st.session_state.current_question_index > 0:
        st.session_state.current_question_index -= 1

def next_question():
    if st.session_state.current_question_index < len(st.session_state.df) - 1:
        st.session_state.current_question_index += 1
def go_to_question(index):
    st.session_state.current_question_index = index

def start_exam():
    on_option_change()
    st.session_state.start = True
    st.session_state.end = False
    st.session_state.current_question_index = 0
    # st.session_state.answers = [None] * len(st.session_state.df)
    # Initialize 'Your Answer' column in the DataFrame
    st.session_state.df['Your Answer'] = None
    st.session_state.correct_count = 0
    st.session_state.show_results = False

def stop_exam():
    get_correct_answers_count()
    st.session_state.start = False
    st.session_state.show_results = True

def restart_exam():
    start_exam()

# def handle_answer(submitted_answer):
#     index = st.session_state.current_question_index
#     row = st.session_state.df.iloc[index]
#     print(submitted_answer)
#     correct_answer_key = row['Correct Answer']
#     print(correct_answer_key)
#     if submitted_answer == correct_answer_key:
#         st.session_state.correct_count += 1
#     st.session_state.answers[index] = submitted_answer
#     print(st.session_state.answers)
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
def on_submit(index,selected_answer, option_keys_with_placeholder, options_with_placeholder):
    print(selected_answer, option_keys_with_placeholder, options_with_placeholder)
    st.write(f"Selected Answer: {selected_answer}")
    if selected_answer != "Select an option":
        selected_answer_key = option_keys_with_placeholder[options_with_placeholder.index(selected_answer)]
        correct_answer_key = st.session_state.df.iloc[st.session_state.current_question_index]['Correct Answer']
        explanation = st.session_state.df.iloc[st.session_state.current_question_index]['Explanation']
        correct = handle_answer(selected_answer_key, correct_answer_key, explanation)
        print(correct)
        # st.session_state.answers[index] = selected_answer_key
        st.session_state.df.at[index, 'Your Answer'] = selected_answer_key 
        if correct:
            print("here")
            next_question()
    else:
        st.warning("Please select an answer before submitting.")

def handle_answer(selected_answer_key, correct_answer_key, explanation):
    if selected_answer_key == correct_answer_key:
        st.success("Correct!")
        return True
    else:
        st.error(f"Wrong! The correct answer was {correct_answer_key}.")
        st.info(f"Explanation: {explanation}")
        return False
def updatePassPercentage():
    st.session_state.passing_percentage=st.session_state.percentage
def getAnswerText(row,option):
    if option=='A':
        return option+") "+row['Option A']
    elif option=='B':
        return option+") "+row['Option B']
    elif option=='C':
        return option+") "+row['Option C']
    elif option=='D':
        return option+") "+row['Option D']
    else:
        return '';

def main():
    st.title("Mock Exam")
    # if 'df' in st.session_state:
    #     st.write(st.session_state.df.empty)

    # file_path = 'new.csv'  # Path to your CSV file
    global uploaded_file
    if 'passing_percentage' not in st.session_state:
        st.session_state.passing_percentage=75

    # df = load_questions(file_path)

    # Initialize session state
    if 'start' not in st.session_state:
        st.session_state.start = False
        st.session_state.end = False
        st.session_state.current_question_index = 0
        st.session_state.df = pd.DataFrame()
        st.session_state.correct_count = 0
        st.session_state.show_results = False
        st.session_state.triggered_by_dropdown = False
        st.write('You can practice mcq exams here; there are four possible answers for each question. Your customized question answers can be uploaded as a CSV file in the same format as the sample CSV file. For using the uploaded question-based exam, you need to choose the custom option from the dropdown menu.')
        st.write('Go to sidebar and start exam')
    # Initialize session state for the dropdown
    if 'dropdown_options' not in st.session_state:
        st.session_state.dropdown_options = ["Default","Custom"]


    # Sidebar for navigation and restarting
    with st.sidebar:
        print("is empty",st.session_state.df.empty)
        with st.expander('Custom Exam'):
            st.write("You can upload your on mcq question answer as a csv file. You can download the sample csv file from below.")
            with open("sample_mcq.csv", "rb") as file:
                btn = st.download_button(
                    label="Download Sample csv",
                    data=file,
                    file_name="sample_mcq.csv",
                    mime="image/png",
                )
            # if st.session_state.df.empty:
            # Add a file uploader that only accepts CSV files
            uploaded_file = st.file_uploader("Upload a CSV file", type="csv",disabled=st.session_state.start)
            if st.session_state.start:
                st.write('You cannot upload a file while exam in progress,Please finish current exam.')
            # Enable dropdown only if a file is uploaded
            if uploaded_file is not None:
                # Add the filename to the dropdown options if it's not already there
                filename = uploaded_file.name
                st.session_state.selected_file = uploaded_file.name
                # if filename not in st.session_state.dropdown_options:
                #     st.session_state.dropdown_options.append(filename)
                    # st.experimental_rerun()  # Rerun the app to update the dropdown

                # Enable the dropdown
                selected_option = st.sidebar.selectbox(
                    "Select type of exam",
                    st.session_state.dropdown_options,
                    key="dropdown",  # Assign a key to track this widget
                    on_change=on_option_change,
                    disabled=st.session_state.start

                )
            else:
                selected_option = st.sidebar.selectbox(
                    "Select type of exam",
                    ["Default"],
                    key="dropdown",  # Assign a key to track this widget
                    on_change=on_option_change,
                    disabled=True

                )
        # Trigger method when dropdown value changes
        # Check if dropdown value has changed
        # if st.session_state.get('triggered_by_dropdown', False):
        #     on_option_change(selected_option)
        #     st.session_state['triggered_by_dropdown'] = False  # Reset the trigger

        # Update a state based on the dropdown selection and load the appropriate file
        # if st.session_state.df.empty:

        st.number_input("Pass percentage",help="Enter the precentage of answer need to pass the exam in between 0-100",min_value=0,max_value=100,step=1,value=st.session_state.passing_percentage,key="percentage",on_change=updatePassPercentage)
        # st.number_input("Insert a number",0,100,value=75,step=1,on_change=updatePassPercentage,args=(st.session_state.passing_percentage),key="passing_percentage")
        st.write(st.session_state.passing_percentage)
        if st.session_state.show_results:
            st.button("Restart Exam", on_click=restart_exam)
        elif not st.session_state.start:
            st.button("Start Exam", on_click=start_exam)
        else:
            if st.session_state.start:
                st.button("Finish Exam", on_click=stop_exam)
                st.subheader("Jump to Question")
                with st.container(border=True,height=300):
                    total_questions = len(st.session_state.df)
                    num_rows = math.ceil(total_questions / 8)

                    for r in range(num_rows):
                        cols = st.columns(8)
                        for i in range(8):
                            q_index = r * 8 + i
                            if q_index >= total_questions:
                                break
                    
                            btn_label = str(q_index + 1)
                            button_type = 'primary' if st.session_state.answers[q_index] is not None else 'secondary'
                    
                            with cols[i]:
                                if st.button(btn_label, key=f"btn_{q_index}" ,type=f"{button_type}"):
                                    go_to_question(q_index)
        

    
    if st.session_state.show_results:
        # st.write("## Exam Summary")

        # Calculate the score percentage
        score_percentage = st.session_state.correct_count / len(st.session_state.df) * 100

        # Set the color based on whether the user passed or failed
        score_color = "green" if score_percentage >= st.session_state.passing_percentage else "red"

        # Display the score with color
        st.subheader(f"**Exam Summary | You Scored :{score_color}[{score_percentage:.2f}%]**")

        if score_percentage >= st.session_state.passing_percentage:
            st.subheader(":green[Congratulations! You've Passed!]")
        else:
            st.subheader(":red[Unfortunately, You Did Not Pass]")
            st.write(f":exclamation: You needed at least {st.session_state.passing_percentage}% to pass.")

        st.write(f":memo: You answered {st.session_state.correct_count} out of {len(st.session_state.df)} questions correctly.")

        # Define the variables
        correct_answers = st.session_state.correct_count
        incorrect_answers = len(st.session_state.df) - correct_answers

        # Create the pie chart data
        data = pd.DataFrame({
            'Category': ['Correct', 'Incorrect'],
            'Count': [correct_answers, incorrect_answers]
        })

        # Generate the pie chart using Altair
        pie_chart = alt.Chart(data).mark_arc().encode(
            theta=alt.Theta(field="Count", type="quantitative"),
            color=alt.Color(field="Category", type="nominal"),
            tooltip=['Category', 'Count']
        ).properties(
            title="Correct vs Incorrect Answers"
        )

        st.altair_chart(pie_chart, use_container_width=True)

        results = []

        # Iterate through each answer
        st.write(st.session_state.df)
        for i, question_row in st.session_state.df.iterrows():
            if question_row['Your Answer'] is not None:
                # Get the details of each question
                question_row = st.session_state.df.iloc[i]
                results.append({
                    "Question Number": i + 1,
                    "Question": question_row['Question'],
                    "Your Answer": getAnswerText(question_row,question_row['Your Answer']),
                    "Correct Answer": getAnswerText(question_row,question_row['Correct Answer']),
                    "Explanation": question_row['Explanation']
                })
        
        # Convert the list of results to a DataFrame
        results_df = pd.DataFrame(results)
        if 'Your Answer' in results_df.columns and 'Correct Answer' in results_df.columns:
            incorrect_df = results_df[results_df['Your Answer'] != results_df['Correct Answer']]
            correct_df = results_df[results_df['Your Answer'] == results_df['Correct Answer']]

        # Display the DataFrame as a table
        st.subheader("Detailed Results")
        if all(answer is None for answer in st.session_state.df['Your Answer']):
            st.write("You haven't answered any question.")
            return
        else:
            tab1, tab2, tab3= st.tabs(["Wrong","Correct","All"])
            with tab1:
                st.header("Incorrect Answers")
                if incorrect_df:
                    st.table(incorrect_df)  # Display the table
                else:
                    st.write('No data available')
            with tab2:
                st.header("Correct Answers")
                if correct_df:
                    st.table(correct_df)  # Display the table
                else:
                    st.write('No data available')
            with tab3:
                st.header("All")
                st.table(results_df)  # Display the table


    # elif not st.session_state.start:
    #     # Only show the "Start Exam" button if the exam has not started and hasn't ended
    #     if not st.session_state.end:
    #         if st.button("Start Exam"):
    #             start_exam()
    elif st.session_state.show_results:
        st.session_state.end = True
    elif st.session_state.start:
        if st.session_state.start:
            render_question()
def render_question():
    index = st.session_state.current_question_index
        # Ensure the DataFrame exists in the session state
    if 'df' not in st.session_state:
        st.warning("DataFrame is not initialized. Please upload a file or load data.")
        return

    df = st.session_state.df
    print(index,len(df))
    # Ensure the index is valid
    index = 0  # Example index; replace with your logic
    if index >= len(df) or index < 0:
        st.error("Invalid index. Please make sure you're accessing a valid row.")
        return
    if st.session_state.current_question_index>-1:
        index = st.session_state.current_question_index
        # Access the row safely
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

        st.button("Submit Answer",on_click=on_submit,args=(index,selected_answer, option_keys_with_placeholder, options_with_placeholder, ),key="on_submit_button")
        # Navigation buttons
        st.button("Previous", on_click=previous_question, disabled=st.session_state.current_question_index == 0,key="previous_question_button")
        st.button("Next", on_click=next_question, disabled=st.session_state.current_question_index == len(df) - 1,key="next_question_button")
# def on_submit(selected_answer,option_keys_with_placeholder,options_with_placeholder):
    
#     print("on_submit")
#     if selected_answer != "Select an option":
#         selected_answer_key = option_keys_with_placeholder[options_with_placeholder.index(selected_answer)]
#         correct_answer_key = row['Correct Answer']
#         explanation = row['Explanation']
#         # Trigger the handle_answer function
#         handle_answer(selected_answer_key, correct_answer_key, explanation)
#     else:
#         st.warning("Please select an answer before submitting.")
def on_option_change():
    selected_option = st.session_state['dropdown']
    print(selected_option)
    if selected_option == "Custom":
        st.session_state.df = pd.read_csv(uploaded_file)
        st.write(f"Using the uploaded file: {st.session_state.selected_file}")
        print('aaaa')
        st.session_state.answers = [None] * len(st.session_state.df)
    elif selected_option == "Default":
        st.session_state.selected_file = "Default"
        st.session_state.df = load_questions('smc.csv')  # Load the default file
        st.write(f"Using the default file")
        print("sdsadas")
        st.session_state.answers = [None] * len(st.session_state.df)
    else:
        st.write("You selected another option")
    st.session_state['triggered_by_dropdown'] = True
# def get_correct_answers_count():
#     correct_count = 0
#     for i, answer in enumerate(st.session_state.answers):
#         if answer is not None:
#             correct_answer_key = st.session_state.df.iloc[i]['Correct Answer']
#             if answer == correct_answer_key:
#                 correct_count += 1
#     st.session_state.correct_count = correct_count
#     return correct_count
def get_correct_answers_count():
    correct_count = 0
    df = st.session_state.df
    for i in range(len(df)):
        if df.at[i, 'Your Answer'] == df.at[i, 'Correct Answer']:
            correct_count += 1
    st.session_state.correct_count = correct_count
    return correct_count

if __name__ == "__main__":
    main()

