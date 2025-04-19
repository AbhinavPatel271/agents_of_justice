from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from prompts import case_analysing_prompt
from config import groq_api_key


def analyser(state: dict) -> dict:
    case_summariser = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    api_key=groq_api_key,
    max_tokens=1024,
    temperature=0.5,
)
    textual_case_description = state["textual_case_description"]
    prompt_template = ChatPromptTemplate.from_messages([
            ("system", case_analysing_prompt),
            ("human", "{input}")
        ])
    user_prompt = f"COMPLETE TEXTUAL CASE DESCRIPTION :-\n {textual_case_description}"
    chain = prompt_template | case_summariser
    detailed_summary = chain.invoke({"input": user_prompt}).content
    state["case_context"] = detailed_summary
    print("Case analysed ✅")
    return state