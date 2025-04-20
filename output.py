import pandas as pd
import os
from graph import courtroom_execution , CourtroomState

# Load input CSV
df = pd.read_csv("./utility_files/cases.csv")
print(df.head(2))

# Load previously saved results if they exist
output_file = "./utility_files/verdicts.csv"
if os.path.exists(output_file):
    results_df = pd.read_csv(output_file)
    processed_ids = set(results_df["ID"].tolist())
else:
    results_df = pd.DataFrame(columns=["ID", "VERDICT"])
    processed_ids = set()

# Main loop
for i, row in df.iterrows():
    # if row["id"] not in [0,1]:   
    #     continue
    if row["id"] in processed_ids:
        continue

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

    case_text = row["text"]
    initial_state["textual_case_description"] = case_text

    try:
        final_state = courtroom_execution.invoke(initial_state)
        print(f"Case {row['id']} verdict:", final_state["verdict"])

        # Save result to file immediately
        new_row = pd.DataFrame([{"ID": row["id"], "VERDICT": final_state["verdict"]}])
        results_df = pd.concat([results_df, new_row], ignore_index=True)
        results_df.to_csv(output_file, index=False)

    except Exception as e:
        print(f"Error processing Case {row["id"]}: {e}")
        break  # stop here but keep all previous results
