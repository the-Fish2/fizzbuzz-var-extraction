#This is the function I'm testing! Just fizzbuzz -- simple. The test should only realy output the correct values of i. 

def fizzbuzz(i):
    additionalTestCase = "Hi!"
    if i % 15 == 0:
        return "FizzBuzz"
    elif i % 5 == 0:
        return "Buzz"
    elif i % 3 == 0:
        return "Fizz"
    else:
        return i
    
def main():
    for i in range(1, 101):
        print(fizzbuzz(i))

if __name__ == '__main__':
    main()
