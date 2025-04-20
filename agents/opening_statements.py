from agents.prosecution_lawyer import prosecution_lawyer
from agents.defense_lawyer import defense_lawyer


prosecution_additional_prompt = """
\n\nSTARTING WITH:
Based on context of the case, craft a compelling and well-structured Opening Statement that introduces your position in the trial.
Clearly outline the allegations, emphasize the seriousness of the case, and briefly highlight the key arguments and evidence you intend to rely on.
Speak formally, with confidence and clarity, maintaining a persuasive tone without exaggeration.
Avoid arguing in detail — your short term goal for now is to set the stage, not present your full case. Be professional and respectful.\n\n\n
"""
defense_additional_prompt = """
STARTING WITH:
Based on the case context as well as the opening statement delivered by the Prosecution Lawyer, craft your Opening Statement.
Your goal is to firmly and respectfully challenge the prosecution's narrative, introduce your client's perspective, and briefly present the defense's position.
Raise doubt where appropriate, highlight weaknesses or exaggerations in the prosecution's claims, and assert your intention to reveal the truth.
Use a professional tone, focused language, and avoid detailed argumentation — your objective is to provide a strong introduction, not the full defense.
"""

def open_the_court_hearing(state:dict) -> dict:
    case_context = state["case_context"]
    prosecution_opening = prosecution_lawyer.get_opening_statement(case_context , prosecution_additional_prompt)
    defense_opening = defense_lawyer.get_opening_statement(f"CASE CONTEXT:\n {case_context} \n\n\n\n OPENING STATEMENT OF THE PROSECUTION LAWYER:\n{prosecution_opening}" , defense_additional_prompt)
    state["opening_statements"].append({"prosecution_lawyer" : prosecution_opening})
    state["opening_statements"].append({"defense_lawyer" : defense_opening})
    state["conversation"].append({"prosecution_lawyer" : prosecution_opening})
    state["conversation"].append({"defense_lawyer" : defense_opening})
    state["proceedings"] = [
          { "next_speaker": "defense_lawyer" },
          { "message": "" },
          { "phase_of_court_hearing": "OPENING_PHASE" }
    ]
    print("Opening statements made ✅")
    return state
    