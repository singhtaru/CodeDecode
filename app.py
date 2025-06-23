import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq #using llama model
from langchain.prompts import PromptTemplate #making prompt template to model for desired output
from langchain.chains import  LLMChain #combines prompt and model to create a chain

load_dotenv()
groq_api_key=os.getenv("GROQ_API_KEY")

# name of app and layout
st.set_page_config(page_title="CodeDecode",page_icon="💡", layout="centered")

# title and description
st.title("💡 AI Code Explainer ")
st.markdown("Paste your code below in any language and get an explanation in simple English.")



# code input
code_input=st.text_area("📥 Enter your code below:", height=300, placeholder="e.g., def add(a, b): return a + b")
if st.button("🧠 Explain Code"):
    if not code_input.strip():
        st.warning("Please paste some code first.")
    else:
        with st.spinner("Explaining code....."):
            llm=ChatGroq(model="llama3-70b-8192",api_key=groq_api_key,temperature=0.4)
            prompt= PromptTemplate.from_template(template=
                """
                You are a highly knowledgeable programming tutor 
                and you need to help the user understand how 
                {code_input} 
                is working in simple English such that
                even a beginner who has just started coding will
                be able to understand the code.
                Identify the errors if any in code and tell how those 
                errors can be rectified. Also suggest what changes could
                the user make to make the code better. 
                """
            )
            chain=prompt | llm
            code_explanation=chain.invoke({"code_input":code_input})

            st.subheader("📖 Explanation:")
            st.markdown(code_explanation.content)