# agents_of_justice
<p><a href="https://docs.google.com/document/d/1A4M_RekCB74_SG6VDbJOCRz8wJuf4t9P1gz3PHm8apA/edit?usp=sharing"> Google form link </br>  </a> - containing the approach </p>

<h3>File structure:</h3>
<p>
  Entry point - <a href="graph.py"> graph.py </a> - This file defines the structure of the courtroom: THE GRAPH OF THE COURTROOM SIMULATION 
</br>Agents/tools used in graph.py:
  <ul>
    <li> <a href="case_analyser.py"> case_analyser.py </a> </li>
    <li> <a href="dynamic_prompt_generation.py"> dynamic_prompt_generation.py </a></li>
    <li> <a href="courtRoomCoordinator.py"> courtRoomCoordinator.py </a> </li>
    <li> <a href="prosecution_lawyer.py"> prosecution_lawyer.py </a> </li>
    <li> <a href="defense_lawyer.py"> defense_lawyer.py </a> </li>
    <li> <a href="plaintiff.py"> plaintiff.py </a> </li>
    <li> <a href="defendant.py"> defendant.py </a> </li>
    <li> <a href="judge.py"> judge.py </a> </li>
    <li> <a href="opening_statements.py"> opening_statements.py </a> </li>
  </ul>
   <p>All system prompts - <a href="prompts.py"> prompts.py </a> </p>
   <p>For generating outputs of the competition : <a href="output.py"> output.py </a> </p>
</p>

</br></hr></br>
<p>I have used langgraph for creating the courtroom simulation.</p>
<p>
  <strong>LangGraph</strong> is a lightweight framework built on top of LangChain that enables building stateful, multi-agent applications using a graph-based execution model. It's ideal for coordinating LLM-powered agents and managing conversational or task-oriented flows with complex logic. </br>It follows a graph based structure consisting of nodes and edges , where nodes represent the agents/tools/functions and edges represent the relation between these nodes.
</p>
<h3>Here is a graph of the courtroom created by me:</h3>
<img src="courtroom_graph.png" alt="Courtroom graph" />

