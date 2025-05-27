import streamlit as st
from agents import Agent, OpenAIChatCompletionsModel, RunConfig, Runner
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
import asyncio

st.set_page_config(layout= "wide" , page_title="Translating Agent")
st.title("TRANSLATING AI AGENT 🤖")

load_dotenv()

get_gemini_key = os.getenv("Gemini_API_Key")

if not get_gemini_key:
    raise ValueError("Make sure your API is present in your .env file")


client = AsyncOpenAI(
    api_key= get_gemini_key,
    base_url= "https://generativelanguage.googleapis.com/v1beta/openai/"
)


model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client= client
)

config = RunConfig(
    model = model,
    tracing_disabled = True,
    model_provider = client #type:ignore
) 

Translator_Agent = Agent(
    name = "Translator Agent",
    instructions = """ You are a translating agent. Your task is to translate english language content into Urdu """ 
)

user_input = st.text_area("Enter content to translate from English To Urdu :")

if st.button("Translate"):
    async def main():
        response = await Runner.run(
            Translator_Agent,
            input = user_input,
            run_config= config
        )
        return response.final_output

    result = asyncio.run(main())

    st.write("Translated Text")
    st.write(result)



