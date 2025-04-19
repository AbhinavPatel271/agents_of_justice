from typing import TypedDict, List, Optional, Dict
from langgraph.graph import StateGraph , START , END
from case_analyser import analyser
from dynamic_prompt_generation import dynamic_prompting
from opening_statements import open_the_court_hearing
from courtRoomCoordinator import courtroom_coordinator
from prosecution_lawyer import prosecution_lawyer
from defense_lawyer import defense_lawyer
from plaintiff import plaintiff
from defendant import defendant
from judge import judge

class CourtroomState(TypedDict):
    textual_case_description: str
    case_context: str
    opening_statements: List[Dict[str, str]]
    conversation: List[Dict[str, str]]
    system_prompts: List[Dict[str, str]] 
    proceedings: List[Dict[str, str]] 
    execution_step : int
    verdict: Optional[str]


courtroom = StateGraph(CourtroomState)

courtroom.add_node("analyser", analyser)
courtroom.add_node("dynamic_prompting", dynamic_prompting)
courtroom.add_node("opening_the_case", open_the_court_hearing)
courtroom.add_node("courtroom_coordinator", courtroom_coordinator)
courtroom.add_node("prosecution_lawyer", prosecution_lawyer)
courtroom.add_node("defense_lawyer", defense_lawyer)
courtroom.add_node("defendant", defendant)
courtroom.add_node("plaintiff", plaintiff)
courtroom.add_node("judge" , judge)

courtroom.add_edge(START , "analyser")
courtroom.add_edge("analyser" , "dynamic_prompting")
courtroom.add_edge("dynamic_prompting" , "opening_the_case")
courtroom.add_edge("opening_the_case", "courtroom_coordinator")

def get_node(state: dict) -> str:
    if not state["proceedings"]:
        return "prosecution_lawyer"
    return state["proceedings"][0]["next_speaker"]

courtroom.add_conditional_edges("courtroom_coordinator" , get_node )


courtroom.add_edge("prosecution_lawyer", "courtroom_coordinator")
courtroom.add_edge("defense_lawyer", "courtroom_coordinator")
courtroom.add_edge("defendant", "courtroom_coordinator")
courtroom.add_edge("plaintiff", "courtroom_coordinator")
courtroom.add_edge("judge", END)



courtroom_execution = courtroom.compile()
initial_state: CourtroomState = {
    "textual_case_description" : "",
    "case_context": "",
    "opening_statements": [],
    "conversation": [],
    "system_prompts": [],
    "proceedings": [],
    "execution_step" : 2,
    "verdict": None
}
# try:
#     final_state = courtroom_execution.invoke(initial_state , {"recursion_limit": 50})
#     print(f"\n\n\n\n\n\nThe final decision of judge: {final_state['verdict']}")
#     print(f"\n\n\n\n\n Conversation :")
#     for i , dict in enumerate(final_state['conversation']):
#         print("\n")
#         for key, value in dict.items():
#           print(f"{i+1}-> {key} : {value}")
#     print(f"\n\n\n\n\n\nFinal decision of the judge : \n {final_state['verdict']}")            

# except Exception as e:
#     print("An error occurred during the courtroom execution.")
#     print(f"Error: {e}")
#     print(f"\n\n\n\nConversation so far:")
#     for i , dict in enumerate(initial_state['conversation']):
#         print("\n")
#         for key, value in dict.items():
#           print(f"{i+1}-> {key} : {value}")

