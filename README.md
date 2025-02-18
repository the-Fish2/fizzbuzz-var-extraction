# LLM - State Output Extraction

How much do LLMs really understand code? 

This project aims to explore that. Here, I use Python's AST to extract intermediate variable states manually through running any test cases in a codebase through my TestRunner. Then, I compare this output to LLM models' equivalent variable-state code extraction to see an LLM's ability to understand how code works and tracks line-by-line. 

This is also built for LLM understanding of larger codebases. Generating this intermediate state extraction of code and providing it to the LLM on failing tests gives the LLM the ability to localize and more accurately solve a problem, and more generally, the state extractions here can be clearly used for additional training data for chain-of-thought reasoning. 


Make a venv:

python3 -m venv ~./xxxxxxx
source ~/xxxxxxx/fizzbuzz-var-extraction/bin/activate

To get the correct state output for the LLM tests: python run_functions.py llm_tests state_output_logs,test_scores

Generally, this is of the form python run_functions.py [directory for state output extraction] [directories to exclude]

To generate LLM state output, 
