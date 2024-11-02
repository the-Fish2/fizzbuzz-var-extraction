This is the sample unit test for FizzBuzz!

FizzBuzz: printing out values of fizz and buzz

Intermediary states are currently being extracted

To run, build a venv:

python3 -m venv ~./xxxxxxx
source ~/xxxxxxx/fizzbuzz-var-extraction/bin/activate

Then, just run 

python run_tests.py 

to see variable extraction at each test case function

Most important files with the state output code are run_tests.py (code for running state injection on unit tests) and state_injection.py (code for building state injection)

I'm working on the file run_functions.py for extracting intermediary states from each function called in the code base.