from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from prompts import defendant_additional_prompt
from config import groq_api_key


class DefendantAgent:
    def __init__(self, groq_api_key: str):
        self.llm = ChatGroq(
            api_key=groq_api_key, 
            model_name="llama3-8b-8192",
            max_tokens=256,
            temperature=0.7
        )

    def format_prompt(self , state: dict) -> str:

        prompt = f"CASE DESCRIPTION:\n REGARDING ANY INFO ABOUT THE CASE, REFER THIS:\n {state['case_context']}"
        prompt += "\n\n\n\n\nCONVERSATION OF THE COURT TRIAL TILL NOW:\n"

        for _, dict in enumerate(state["conversation"][-4:-1]):
            for key, value in dict.items():
                speaker = "YOU-(Defendant)" if key == "defendant" else key
                prompt += f"-> {speaker} : {value}\n" 
        last_responder , last_response = list(state["conversation"][-1].items())[0]
        prompt += f"""
        THE LAST STATEMENT WAS BY - {last_responder}
        STATEMENT - {last_response}
"""
        prompt += f"""\n\n
        You are called by the court coordinator and there is message from his side-
        {state["proceedings"][1]["message"]}\n
        PHASE OF THE COURT HEARING - {state["proceedings"][2]["phase_of_court_hearing"]}
"""        
        prompt += "\n\nBASED ON THE CONVERSATION TILL NOW (paying closer attention to the last statement) AND THE MESSAGE FROM THE COURT COORDINATOR\n PRESENT YOUR STATEMENT IN FRONT OF THE COURT :-"
        return prompt 
     
    def __call__(self, state: dict) -> dict:
        system_prompt = state["system_prompts"][1]["defendant_system"]
        system_prompt += f"\n\n\n {defendant_additional_prompt}"
        user_prompt = self.format_prompt(state)
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}")
        ])
        chain = prompt_template | self.llm
        response = chain.invoke({"input": user_prompt}).content
        state["conversation"].append({"defendant" : response})
        return state
         

    


defendant = DefendantAgent(groq_api_key)