import streamlit as st
import re
import sqlite3
import random

# Function to create the 'responses' table if it doesn't exist
def create_responses_table():
    conn = sqlite3.connect('responses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS responses (
                    id INTEGER PRIMARY KEY,
                    key TEXT UNIQUE,
                    response TEXT
                 )''')
    conn.commit()
    conn.close()

def table_exists(table_name):
    conn = sqlite3.connect('responses.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    return c.fetchone() is not None

# Ensure the responses table exists
if not table_exists('responses'):
    create_responses_table()

def insert_responses():
    try:
        conn = sqlite3.connect('responses.db')
        c = conn.cursor()
        # Insert responses here
        responses = [
    ("R_EATING", "I don't like eating anything because I'm a bot obviously!"),
    ("COLLEGE_NAME", "The name of the college is Om Vindhya Vasini College of IT and Management, also known as OMVVIM"),
    ("FACILITIES", "We offer state-of-the-art computer labs equipped with high-tech computers and projectors in every classroom. Additionally, our facilities include high-speed Wi-Fi connections and air conditioning in each classroom. The college is well-appointed with a cafeteria and ample water supply throughout the campus. Fire safety is a priority; numerous fire extinguishers are strategically installed. Our classrooms are spacious, well-ventilated, and there are four impressive computer labs on-site. Furthermore, our experienced faculty members contribute to a supportive learning environment."),
    ("COURSES", """We provide a variety of courses including:
    - BCA (Bachelor of Computer Application)
    - BBA (Bachelor of Business Administration)
    - BCOM (Bachelor of Commerce)
    - BEd (Bachelor of Education)
    - LLB (Bachelor of Laws)"""),
    ("FACULTIES", "Our college boasts a large team of experienced and supportive faculty members. They offer the best guidance possible and are always ready to impart knowledge on various subjects. Their dedication extends to teaching practical skills, and their friendly nature creates an amicable learning environment."),
    ("ADDRESS", """Opp. Sardar Baug, Near New Bus Stand,
    Sanala Road, Morbi - 363641"""),
    ("FEES", """Fees for our courses are as follows:
    - BCA: ₹60,000
    - BBA: ₹55,000
    - BCOM: ₹40,000
    - BEd: ₹30,000
    - LLB: ₹70,000"""),
    ("PRINCIPAL", "Mr. Dharmendra sir"),
    ("HOD", "Mr. Bhavesh sir"),
    ("TRUSTEE", "Mr. Suman sir"),
    ("ADMISSION", "visit the college once for that."),
    ("CONTACT_INFO", """
    phone number: 4348348992
    email: info@omvvim.com
    instagram: omvvim_college
    facebook: omvvim_college
    website: www.omvvimcollege.com
    """),
    ("about_amit_sir", "Amit Sir is the epitome of experience at our college. He's known for his calm and composed nature and is incredibly skilled in both computer software and hardware. Teaching across different fields like BCA, BCom, and BBA, he's admired for his excellent English speaking skills. He's like an ocean of knowledge, always ready to share, as long as you come prepared to learn."),
    ("about_bhavesh_sir", "Bhavesh Sir, our college's HOD, is renowned for his exceptional programming and development expertise. Beyond his technical prowess, he's deeply passionate about yoga, embodying a serene and insightful demeanor. Known for his diligence, he tirelessly imparts knowledge to students, covering a spectrum of technological tools and programming languages. Ever approachable, he's always there to offer assistance and guidance."),
        ]
        c.executemany("INSERT OR IGNORE INTO responses (key, response) VALUES (?, ?)", responses)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting responses: {e}")
    finally:
        conn.close()

insert_responses()

# Function to fetch response from the database
def get_response_from_db(key):
    conn = sqlite3.connect('responses.db')
    c = conn.cursor()
    try:
        c.execute("SELECT response FROM responses WHERE key=?", (key,))
        response = c.fetchone()
        if response:
            return response[0]
        else:
            return None
    except sqlite3.OperationalError as e:
        print("Error executing SQL query:", e)
        return None
    finally:
        conn.close()

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Counts how many words are present in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculate the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    if has_required_words or single_response:
        return int(percentage*100)
    else:
        return 0
    
def check_all_messages(message):
    highest_prob_list = {}

    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    # Responses 
    # Syntax: response(,[,],required_words=[,])
    # ------------------------------------------------------------------------------
    response('Hello!', ['hello','hi','sup','hey','heyo','heya'], single_response=True)
    response('I\'m doing fine, and you?', ['how', 'are', 'you', 'doing'], required_words=['how'])
    response('Thank you!', ['i', 'love', 'this', 'chatbot'], required_words=['love', 'chatbot'])
    
    # Fetch responses from the database
    response(get_response_from_db("R_EATING"), ['what', 'you', 'eat'], required_words=['you', 'eat'])
    response(get_response_from_db("COLLEGE_NAME"), ['what','is','the','name','of','college'], required_words=['college','name'])
    response(get_response_from_db("FACILITIES"), ['which', 'type', 'of', 'facilities', 'you', 'provide'], required_words=['facilities'])
    response(get_response_from_db("COURSES"), ['which', 'type', 'of', 'courses', 'you', 'offer'], required_words=['courses'])
    response(get_response_from_db("FACULTIES"), ['tell', 'me', 'something', 'about', 'your', 'faculties'], required_words=['faculties'])
    response(get_response_from_db("ADDRESS"), ['what', 'is', 'the', 'address', 'of', 'the', 'college'], required_words=['address'])
    response(get_response_from_db("FEES"), ['what', 'is', 'the', 'fees', 'structure', 'of', 'the', 'college'], required_words=['fees'])
    response(get_response_from_db("PRINCIPAL"), ['who', 'is', 'the', 'principal', 'of', 'the', 'college'], required_words=['principal'])
    response(get_response_from_db("HOD"), ['who', 'is', 'the', 'hod', 'of', 'the', 'college'], required_words=['hod'])
    response(get_response_from_db("TRUSTEE"), ['who', 'is', 'the', 'trustee', 'of', 'the', 'college'], required_words=['trustee'])
    response(get_response_from_db("ADMISSION"), ['how', 'to', 'get', 'admission', 'in', 'this', 'college'], required_words=['admission'])
    response(get_response_from_db("CONTACT_INFO"), ['contact', 'info', 'about', 'the', 'college'], required_words=['contact'])
    response(get_response_from_db("about_amit_sir"), ['tell', 'me', 'something', 'about','amit','sir'], required_words=['amit','sir'])
    response(get_response_from_db("about_bhavesh_sir"), ['tell', 'me', 'something', 'about', 'bhavesh', 'sir'], required_words=['bhavesh', 'sir'])
    # ----------------------------------------------------------------------------

    max_probability = max(highest_prob_list.values(), default=0)
    if max_probability > 0:
        best_match = max(highest_prob_list, key=highest_prob_list.get)
        return best_match
    else:
        return unknown()


def get_response(user_input):

    # Check for exit command
    if user_input.lower() in exit_words:
        print('Goodbye!')
        exit()
        
    split_message = re.split(r'\s+|[,;?!.-]\s*',user_input.lower())
    response = check_all_messages(split_message)
    return response

def main():
    st.title("AI College Assistant")

    user_input = st.text_input("You:")
    
    # Add a "Send" button below the input field
    send_button = st.button("Send")

    # Process user input and display bot response when the button is clicked
    if send_button:
        response = get_response(user_input)
        st.write(f"Bot: {response}")
        

# List of exit words (If the user want to end the chat)
exit_words = ['exit', 'quit', 'bye', 'goodbye', 'stop', 'talk to you later', 'see you', 'end chat', 'finish', 'close chat']

# If the chatbot doesn't know the answer
def unknown():
    response = ['Could you please rephrase that?',
                "...",
                "Sounds about right",
                "What does that mean?"][random.randrange(4)]
    return response

if __name__ == "__main__":
    main()