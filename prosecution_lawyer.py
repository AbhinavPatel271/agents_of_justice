from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from prompts import prosecution_system
from config import groq_api_key

class ProsecutionLawyerAgent:
    def __init__(self, system_prompt: str, groq_api_key: str):
        self.system_prompt = system_prompt
        self.llm = ChatGroq(
            api_key=groq_api_key,
            model_name="llama3-70b-8192",
            max_tokens=256,
            temperature=0.7
        )
    
    def get_opening_statement(self , case_context: str , additional_prompt: str = "") -> str:
        system_prompt = self.system_prompt + additional_prompt
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}")
        ])
        chain = prompt_template | self.llm
        opening_statement = chain.invoke({"input": case_context}).content
        return opening_statement

    def format_prompt(self , state: dict) -> str:

        prompt = f"CASE DESCRIPTION:\n REGARDING ANY INFO ABOUT THE CASE, REFER THIS:\n {state['case_context']}"
        prompt += "\n\n\n\nCONVERSATION OF THE COURT TRIAL TILL NOW:\n"

        for _, dict in enumerate(state["conversation"][:-1]):
            for key, value in dict.items():
                speaker = "YOU-(Prosecution Lawyer)" if key == "prosecution_lawyer" else key
                prompt += f"-> {speaker} : {value}\n" 
        last_responder , last_response = list(state["conversation"][-1].items())[0]       
        prompt += f"""
        THE LAST STATEMENT WAS BY - {last_responder}
        STATEMENT - {last_response}
"""
        prompt += f"""\n\n
        You are called by the court coordinator and there is message from his side-
        --> message: {state["proceedings"][1]["message"]}\n
        PHASE OF THE COURT HEARING - {state["proceedings"][2]["phase_of_court_hearing"]}
"""        
        prompt += "SPECIAL NOTE:- '''Your response must reflect what has already unfolded in the trial and should contribute to maintaining the continuity and logical flow of the courtroom proceedings.'''"
        prompt += "\n\nBASED ON THE CONVERSATION TILL NOW (paying closer attention to the last statement) AND THE MESSAGE FROM THE COURT COORDINATOR\n PRESENT YOUR STATEMENT IN FRONT OF THE COURT TO PROCEED THE HEARING:-"
        return prompt 
     
    def __call__(self, state: dict) -> dict:
        user_prompt = self.format_prompt(state)
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "{input}")
        ])
        chain = prompt_template | self.llm
        response = chain.invoke({"input": user_prompt}).content
        state["conversation"].append({"prosecution_lawyer" : response})
        return state
         


prosecution_lawyer = ProsecutionLawyerAgent( prosecution_system , groq_api_key)