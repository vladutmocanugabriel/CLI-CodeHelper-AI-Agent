# main.py

import sys
import argparse
from pkg.calculator import Calculator
from pkg.render import render


def main():
    parser = argparse.ArgumentParser(description="Evaluate a mathematical expression.")
    parser.add_argument("expression", help="The expression to evaluate")
    args = parser.parse_args() 

    calculator = Calculator()
    expression = args.expression  # Get expression from command line
    try:
        result = calculator.evaluate(expression)
        to_print = render(expression, result)
        print(to_print)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()