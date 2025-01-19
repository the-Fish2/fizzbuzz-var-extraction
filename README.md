Make a venv:

python3 -m venv ~./xxxxxxx
source ~/xxxxxxx/fizzbuzz-var-extraction/bin/activate

To get the correct state output for the LLM tests: python run_functions.py llm_tests state_output_logs,test_scores

Generally, this is of the form python run_functions.py [directory for state output extraction] [directories to exclude]

To generate LLM state output, 