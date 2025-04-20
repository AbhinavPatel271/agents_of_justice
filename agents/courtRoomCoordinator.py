import json , time
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from config.prompts import courtroom_coordinator_system_prompt
from config.config import groq_api_key

class CourtroomCoordinatorLLM:
    def __init__(self, groq_api_key, system_prompt):
        self.llm = ChatGroq(api_key=groq_api_key, model_name="meta-llama/llama-4-scout-17b-16e-instruct" )
        self.system_prompt = system_prompt

    def format_prompt(self , state:dict) -> str:
        statement_count = 1
        total_count = len(state["conversation"])
        prompt = f"CASE DESCRIPTION:\n REGARDING ANY INFO ABOUT THE CASE, REFER THIS:\n {state['case_context']}"
        prompt += "\n\n\nCONVERSATION OF THE COURT TRIAL TILL NOW:\n"
        
        if(total_count<7):
           add_statement = True
        else: add_statement = False   
        for _, dict in enumerate(state["opening_statements"]):
            for key, value in dict.items():
                if(add_statement):
                    prompt += f"Opening statement by the {key}:\n"
                    prompt += f"{statement_count}-> {key} : {value}\n"
                statement_count += 1
        start_index = total_count-6 if (total_count >=8) else 2
        for i, dict in enumerate(state["conversation"][2:]):
            for key, value in dict.items():
                if(i+2 >= start_index):
                    prompt += f"{statement_count}-> {key}  :  {value}\n"  
                statement_count += 1      
        prompt += f"\n\n The current PHASE of the court proceeding is : {state["proceedings"][2]["phase_of_court_hearing"]} and number of statements till now : {total_count}"
        return prompt
    
    def __call__(self, state: dict) -> dict:
        # time.sleep(8)
        state["execution_step"] += 1

        user_prompt = self.format_prompt(state)
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "{input}")
        ])
        chain = prompt_template | self.llm
        response = chain.invoke({"input": user_prompt}).content

        previous_speaker = state["proceedings"][0]["next_speaker"]
        interrogation_phase_counter = 5

        if(state["execution_step"] < interrogation_phase_counter):
           state["proceedings"] = json.loads(response)
        elif(state["execution_step"] == interrogation_phase_counter):
         state["proceedings"] = [
          { "next_speaker": "prosecution_lawyer" },
          { "message": "***Deliver your closing statements and final remarks to the judge, advocating firmly for justice and truth.***" },
          { "phase_of_court_hearing": "CLOSING_PHASE" }]
        elif(state["execution_step"] == (interrogation_phase_counter+1)):
         state["proceedings"] = [
          { "next_speaker": "defense_lawyer" },
          { "message": "***The prosecution has delivered their closing statement. Now, present your final remarks to the judge, defending your client and seeking justice.***" },
          { "phase_of_court_hearing": "CLOSING_PHASE" }]
        elif(state["execution_step"] == (interrogation_phase_counter+2)):
         state["proceedings"] = [
          { "next_speaker": "judge" },
          { "message": "" },
          { "phase_of_court_hearing": "THE_END" }]
           

        next_speaker = state["proceedings"][0]["next_speaker"]
        print(f"Case in proceeding ✅. Phase of hearing - {state["proceedings"][2]["phase_of_court_hearing"]} | Previous speaker:{previous_speaker} | Next Speaker:{next_speaker}")
        return state





courtroom_coordinator = CourtroomCoordinatorLLM(groq_api_key , courtroom_coordinator_system_prompt)