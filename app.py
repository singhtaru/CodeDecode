import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq #using llama model
from langchain_core.prompts import PromptTemplate #making prompt template to model for desired output
from streamlit_ace import st_ace # to get code editor
load_dotenv()
groq_api_key=os.getenv("GROQ_API_KEY")

# name of app and layout
st.set_page_config(page_title="CodeDecode",page_icon="💡", layout="centered")

# title and description
st.title("💡CodeDecode-Your AI Code Buddy ")
st.markdown("Select how you need help in coding.")
task = st.selectbox("Select Task", ["Explain Code and analyze Complexity", "Debug Code", "Optimize Code","Generate Code","Add Comments","Change Language"])

st.divider()

# code input
code_input=""
button=False
language=""
if task=="Explain Code and analyze Complexity":
    code_input=st_ace("📥 Enter your code below:", height=300, placeholder="e.g., def add(a, b): return a + b",theme="twilight",font_size=16,auto_update=True)
    button=st.button("🧠 Explain Code and analyze Complexity")

elif task=="Debug Code":
    code_input=st_ace("📥 Enter your code below:", height=300, placeholder="e.g., def add(a, b): return a + b",theme="twilight",font_size=16,auto_update=True)
    button=st.button("🪲 Debug Code")

elif task=="Optimize Code":
    code_input=st_ace("📥 Enter your code below:", height=300, placeholder="e.g., def add(a, b): return a + b",theme="twilight",font_size=16,auto_update=True)
    button=st.button("⚡ Optimize Code")

elif task=="Generate Code":
    language = st.text_area("Enter Language you want to generate code in",height=70, placeholder="e.g., Python, C++")
    code_input=st.text_area("📥 What code do you need help with:", height=300, placeholder="e.g., generate a code to add two strings")
    button=st.button("✨ Generate Code")
elif task=="Add Comments":
    code_input=st_ace("📥 What code do you need help with:", height=300, placeholder="e.g., def add(a, b): return a + b",theme="twilight",font_size=16,auto_update=True)
    button=st.button("💬 Add Comments")
elif task=="Change Language":
    language = st.text_area("Enter Language you want to generate code in",height=70, placeholder="e.g., Python, C++")
    code_input=st_ace("📥 Enter code you want changed:", height=300, placeholder="e.g., def add(a, b): return a + b",theme="twilight",font_size=16,auto_update=True)
    button=st.button("🌐 Change Language")

st.divider()

if button:
    if not code_input.strip():
        st.warning("Please paste some code first.")
    else:
        with st.spinner("Working on it....."):
            llm=ChatGroq(model="llama3-70b-8192",api_key=groq_api_key,temperature=0.4)
            if task=="Explain Code and analyze Complexity":
                prompt= PromptTemplate.from_template(template=
                    """
                    You are a highly knowledgeable programming tutor 
                    and you need to help the user understand how 
                    {code_input} 
                    is working in simple English such that
                    even a beginner who has just started coding will
                    be able to understand the code. Also explain about
                    the space and time complexity.
                    """
                )
            elif task=="Debug Code":
                prompt= PromptTemplate.from_template(template=
                    """
                    You are a highly knowledgeable programming tutor 
                    and your role is to identify the errors if any in 
                    {code_input} 
                    and tell how those errors can be rectified
                    in simple English such that even a beginner who has
                    just started coding will
                    be able to understand the code.
                    """
                )
            elif task=="Optimize Code":
                prompt= PromptTemplate.from_template(template=
                    """
                    You are a highly knowledgeable programming tutor 
                    and you need to help the user optimize  
                    {code_input} 
                    to make it faster, more efficient, cleaner and 
                    easier to read while following the best coding practices.
                    Possibly try altering the time and space complexity of 
                    the code so that the most efficient solution can be obtained.
                    """
                )
            elif task=="Generate Code":
                prompt= PromptTemplate.from_template(template=
                    """
                    You are a highly knowledgeable programming tutor 
                    and you need to help the user generate code based on  
                    {code_input} in {language} language.
                    Make the code faster, more efficient, cleaner and 
                    easier to read while following the best coding practices.
                    Also after generating code, give explanation about 
                    how code works line by line and how does it relate 
                    to problem statement.Don't mention anything related to
                    actual language that user wants to convert to.
                    """
                )
            elif task=="Add Comments":
                prompt= PromptTemplate.from_template(template=
                    """
                    You are a highly knowledgeable programming tutor 
                    and you need to help the user add comments to  
                    {code_input}. 
                    Ensure that the comments are easy to read and 
                    understand.
                    """
                )
            elif task=="Change Language":
                prompt= PromptTemplate.from_template(template=
                    """
                    You are a highly knowledgeable programming tutor 
                    and you need to help the user convert 
                    {code_input} to {language} language
                    Add comments that are easy to read and 
                    understand. 
                    """
                )
            chain = prompt | llm
            code_explanation = chain.invoke({"code_input": code_input,"language":language})




            st.subheader("📖 Explanation:")
            st.markdown(code_explanation.content)
            st.divider()


st.markdown("---")
st.markdown("🔍 Built with LLaMA 3 via Groq | Streamlit UI | By Taru Singh")
