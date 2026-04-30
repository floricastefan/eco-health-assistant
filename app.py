import streamlit as st
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

#incarcam cheia api
load_dotenv()

st.title("🌱 Eco-Health Assistant")
st.subheader("Personal Health & Nutrition Advisor")

system_instructions = """
            Ești un asistent personal expert în nutriție, fitness și un stil de viață sănătos. 
            Numele tău este Eco-Health Assistant.
            
            REGULI STRICTE DE COMPORTAMENT:
            1. Răspunzi MEREU în limba română, folosind un ton empatic și prietenos.
            2. Oferi sfaturi doar despre: nutriție, antrenamente sportive (sală), recuperare și somn.
            3. LIMITĂ DE DOMENIU: Dacă utilizatorul te întreabă despre orice alt subiect (ex: programare, mașini, istorie), refuză politicos și spune-i că expertiza ta este limitată la sănătate și fitness.
            4. DISCLAIMER MEDICAL: La finalul fiecărui răspuns, adaugă un mic avertisment că sfaturile tale au rol informativ și nu înlocuiesc consultul unui medic.
            """

#creeam conexiunea daca nu exista deja
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

#creeam conversatia daca nu exista deja cu toate 'setarile' implementate + istoric chat
if "chat_session" not in st.session_state:
    st.session_state.chat_session = st.session_state.client.chats.create(
        model='gemini-flash-latest',
        config=types.GenerateContentConfig(system_instruction=system_instructions)
    )
    st.session_state.chat_history = []

#parcurgem mesajele si le afisam cu rolul corespunzator
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["text"])

user_query = st.chat_input("Întreabă-mă ceva despre nutriție...")

#verificam daca user-ul a scris ceva si adaugam in istoricul conversatiei
if user_query:
    with st.chat_message("user"):
        st.write(user_query)
    st.session_state.chat_history.append({"role": "user", "text": user_query})

    #scriem raspunsul la intrebare si adaugam in istoricul conversatiei
    with st.spinner('Asistentul gândește...'):
        try:
            response = st.session_state.chat_session.send_message(user_query)

            with st.chat_message("assistant"):
                st.write(response.text)
            st.session_state.chat_history.append({"role": "assistant", "text": response.text})

        except Exception as e:
            st.error(f"Connection error: {e}")