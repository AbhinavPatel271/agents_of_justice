import json
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from config.prompts import dynamic_prompting_system
from config.config import groq_api_key

def dynamic_prompting(state: dict) -> dict:
    prompt_generator = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    api_key=groq_api_key,
    max_tokens=1024,
    temperature=0.7,
)
    prompt_template = ChatPromptTemplate.from_messages([
            ("system", dynamic_prompting_system),
            ("human", "{input}")
        ])
    
    textual_case_description = state["textual_case_description"]
    chain = prompt_template | prompt_generator
    user_prompt = f"COMPLETE TEXTUAL CASE DESCRIPTION :-\n {textual_case_description} \n\n\n\n\n\n CASE SUMMARY TO TAKE REFERRENCE FROM :-\n {state['case_context']}"
    response = chain.invoke({"input": user_prompt})
    # print("Raw LLM response:\n", response.content)
    # print("Type of response:", type(response.content))
    prompts = json.loads(response.content)
    state["system_prompts"].append({"plaintiff_system" : prompts[0]["plaintiff"]})
    state["system_prompts"].append({"defendant_system" : prompts[1]["defendant"]})

    print("Dynamic prompts generated ✅")
    return state