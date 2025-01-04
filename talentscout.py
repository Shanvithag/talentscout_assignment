import streamlit as st
import openai
import pymysql  #Importing it for database connection establishment

#Set your OpenAI API key
openai.api_key = "you-key-here"

#Database connection
def connect_to_db():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',       #Default MySQL user
            password='',       #Leave blank if no password
            database='talentscout'
        )
        return connection
    except pymysql.MySQLError as e:
        st.error(f"Database connection failed: {e}")
        return None

#Save candidate data to the database
def save_candidate_to_db(data):
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = """
            INSERT INTO candidates (name, email, phone, experience, position, location, tech_stack, answers)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                data['name'], data['email'], data['phone'], data['experience'],
                data['position'], data['location'], data['tech_stack'], data['answers']
            )
        )
        conn.commit()
        conn.close()

#Configure Streamlit page
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    layout="centered",
    initial_sidebar_state="expanded",
)

#Title and introduction
st.title("TalentScout Hiring Assistant")
st.write(
    "Welcome! I'm your intelligent assistant on behalf of TalentScout, here to help with the initial screening process."
)

#Sidebar information
st.sidebar.title("About TalentScout")
st.sidebar.info(
    "This intelligent chatbot collects your details and generates technical questions based on the declared tech stack. "
)

#Candidate information form
st.header("Step 1: Candidate Information")
name = st.text_input("Full Name", placeholder="Enter your full name")
email = st.text_input("Email Address", placeholder="Enter your email")
phone = st.text_input("Phone Number", placeholder="Enter your phone number")
experience = st.number_input("Years of Experience", min_value=0, step=1)
position = st.text_input("Desired Position(s)", placeholder="Enter the job title you're applying for")
location = st.text_input("Current Location", placeholder="Enter your current city/state")
tech_stack = st.text_area(
    "Tech Stack",
    placeholder="List technologies you're proficient in (e.g., Python, Django, React, SQL)",
)

#Submit information
if st.button("Submit Information"):
    if not name or not email or not tech_stack:
        st.error("Please fill in all the necessary fields.")
    else:
        st.success("Information submitted successfully!")
        st.session_state["user_data"] = {
            "name": name,
            "email": email,
            "phone": phone,
            "experience": experience,
            "position": position,
            "location": location,
            "tech_stack": tech_stack,
        }

#Generate technical questions
if "user_data" in st.session_state and "tech_stack" in st.session_state["user_data"]:
    st.header("Step 2: Technical Question Generation")
    tech_stack_input = st.session_state["user_data"]["tech_stack"]

    with st.spinner("Generating questions..."):
        prompt = f"Generate 3 technical interview questions for a candidate proficient in the following tech stack: {tech_stack_input}."
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=150,
            )
            questions = response.choices[0].message["content"].strip()
            st.subheader("Technical Questions:")
            st.write(questions)

            #Answer input fields
            answers = []
            question_list = [q.strip() for q in questions.split("\n") if q.strip()]
            for idx, question in enumerate(question_list):
                answer = st.text_area(f"Answer for Question {idx + 1}: ", placeholder="Your answer here", key=f"answer_{idx}")
                answers.append(answer)

            #Submit answers
            if st.button("Submit Answers"):
                if any(answer == "" for answer in answers):
                    st.error("Please answer all the questions.")
                else:
                    candidate_data = st.session_state["user_data"]
                    candidate_data["answers"] = " | ".join(answers)
                    save_candidate_to_db(candidate_data)
                    st.success("Your answers have been submitted successfully!")

        except openai.error.OpenAIError as e:
            st.error(f"OpenAI Error: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

#End conversation
if st.button("End Conversation"):
    st.success("Thank you for your time! We’ll get back to you soon.")
