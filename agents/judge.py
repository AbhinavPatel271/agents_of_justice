from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from config.prompts import judge_system
import time
from config.config import groq_api_key

class JudgeAgent:
    def __init__(self, system_prompt: str, groq_api_key: str):
        self.system_prompt = system_prompt
        self.llm = ChatGroq(
            api_key=groq_api_key,
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            max_tokens=128,
            temperature=0.5
        )
    

    def format_prompt(self , state: dict) -> str:

        prompt = f"CASE DESCRIPTION:\n REGARDING ANY INFO ABOUT THE CASE, REFER THIS:\n {state['case_context']}"
        prompt += "\n\n\n\n\n\nTHE ENTIRE CHRONOLOGICAL CONVERSATION OF THE COURT TRIAL TILL NOW:\n"

        for _, dict in enumerate(state["conversation"]):
            for key, value in dict.items():
                prompt += f"-> {key} : {value}\n" 
        
        prompt += """
THE COURT HAS CONCLUDED ITS PROCEEDINGS. YOU ARE TO CAREFULLY EXAMINE THE CASE CONTEXT, ENTIRE HEARING, INCLUDING ALL TESTIMONIES, ARGUMENTS, AND EVIDENCE PRESENTED BY BOTH SIDES.
APPLY SOUND LEGAL REASONING, MAINTAIN FAIRNESS AND OBJECTIVITY, AND DELIVER A CLEAR, WELL-JUSTIFIED FINAL VERDICT."
"""
        return prompt 
     
    def __call__(self, state: dict) -> dict:
        user_prompt = self.format_prompt(state)
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "{input}")
        ])
        chain = prompt_template | self.llm
        response = chain.invoke({"input": user_prompt}).content
        state["verdict"] = response
        return state
         


judge = JudgeAgent( judge_system , groq_api_key)
