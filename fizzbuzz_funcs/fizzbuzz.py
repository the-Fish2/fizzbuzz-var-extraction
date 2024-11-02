""" 
Implements the FizzBuzz problem for an input number i. 
"""


def fizzbuzz(i: int) -> str:
    randomLocalVariable = 1
    if i % 15 == 0:
        return "FizzBuzz"
    elif i % 5 == 0:
        return "Buzz"
    elif i % 3 == 0:
        return "Fizz"
    else:
        return str(i)


def main() -> None:
    for i in range(1, 101):
        print(fizzbuzz(i))


if __name__ == "__main__":
    main()
