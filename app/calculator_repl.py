########################
# Calculator REPL       #
########################

from decimal import Decimal
import logging
import os

from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver, LoggingObserver
from app.operations import OperationFactory
from app.ui import success, error, info, value

# UI Color
USE_COLOR = os.getenv("CALCULATOR_USE_COLOR", "true").lower() == "true"


def cyan(text: str) -> str:
    return f"\033[36m{text}\033[0m"

def printc(msg, func=cyan):
    if USE_COLOR:
        print(func(msg))
    else:
        print(msg)


        
# Calculator logic
def calculator_repl():
    """
    Command-line interface for the calculator.

    Implements a Read-Eval-Print Loop (REPL) that continuously prompts the user
    for commands, processes arithmetic operations, and manages calculation history.
    """
    try:
        # Initialize the Calculator instance
        calc = Calculator()

        # Register observers for logging and auto-saving history
        calc.add_observer(LoggingObserver())
        calc.add_observer(AutoSaveObserver(calc))

        printc("Calculator started. Type 'help' for commands.", info)

        while True:
            try:
                # Prompt the user for a command
                command = input("\nEnter command: ").lower().strip()

                if command == 'help':
                    # Display available commands
                    printc("\nAvailable commands:", info)
                    printc("  add, subtract, multiply, divide, power, root, modulus, intdiv, percentage, absdiff - Perform calculations", info)
                    printc("  history - Show calculation history", info)
                    printc("  clear - Clear calculation history", info)
                    printc("  undo - Undo the last calculation", info)
                    printc("  redo - Redo the last undone calculation", info)
                    printc("  save - Save calculation history to file", info)
                    printc("  load - Load calculation history from file", info)
                    printc("  exit - Exit the calculator", info)
                    continue

                if command == 'exit':
                    # Attempt to save history before exiting
                    try:
                        calc.save_history()
                        printc("History saved successfully.", info)
                    except Exception as e:
                        printc(f"Warning: Could not save history: {e}", error)
                    printc("Goodbye!", info)
                    break

                if command == 'history':
                    # Display calculation history
                    history = calc.show_history()
                    if not history:
                        printc("No calculations in history", info)
                    else:
                        printc("\nCalculation History:", info)
                        for i, entry in enumerate(history, 1):
                            print(f"{i}. {entry}")
                    continue

                if command == 'clear':
                    # Clear calculation history
                    calc.clear_history()
                    printc("History cleared", info)
                    continue

                if command == 'undo':
                    # Undo the last calculation
                    if calc.undo():
                        printc("Operation undone", info)
                    else:
                        printc("Nothing to undo", info)
                    continue

                if command == 'redo':
                    # Redo the last undone calculation
                    if calc.redo():
                        printc("Operation redone", info)
                    else:
                        printc("Nothing to redo", info)
                    continue

                if command == 'save':
                    # Save calculation history to file
                    try:
                        calc.save_history()
                        printc("History saved successfully", info)
                    except Exception as e:
                        printc(f"Error saving history: {e}", error)
                    continue

                if command == 'load':
                    # Load calculation history from file
                    try:
                        calc.load_history()
                        printc("History loaded successfully", info)
                    except Exception as e:
                        printc(f"Error loading history: {e}", error)
                    continue

                if command in ['add', 'subtract', 'multiply', 'divide', 'power', 'root', 'modulus', 'intdiv', 'percentage', 'absdiff']:
                    # Perform the specified arithmetic operation
                    try:
                        printc("\nEnter numbers (or 'cancel' to abort):", info)
                        a = input("First number: ")
                        if a.lower() == 'cancel':
                            printc("Operation cancelled", info)
                            continue
                        b = input("Second number: ")
                        if b.lower() == 'cancel':
                            printc("Operation cancelled", info)
                            continue

                        # Create the appropriate operation instance using the Factory pattern
                        operation = OperationFactory.create_operation(command)
                        calc.set_operation(operation)

                        # Perform the calculation
                        result = calc.perform_operation(a, b)

                        # Normalize the result if it's a Decimal
                        if isinstance(result, Decimal):
                            result = result.normalize()

                        printc(f"\nResult: {result}")
                    except (ValidationError, OperationError) as e:
                        # Handle known exceptions related to validation or operation errors
                        printc(f"Error: {e}", error)
                    except Exception as e:
                        # Handle any unexpected exceptions
                        printc(f"Unexpected error: {e}", error)
                    continue

                # Handle unknown commands
                printc(f"Unknown command: '{command}'. Type 'help' for available commands.", info)

            except KeyboardInterrupt:
                # Handle Ctrl+C interruption gracefully
                printc("\nOperation cancelled", info)
                continue
            except EOFError:
                # Handle end-of-file (e.g., Ctrl+D) gracefully
                printc("\nInput terminated. Exiting...", info)
                break
            except Exception as e:
                # Handle any other unexpected exceptions
                printc(f"Error: {e}", error)
                continue

    except Exception as e:
        # Handle fatal errors during initialization
        printc(f"Fatal error: {e}", error)
        logging.error(f"Fatal error in calculator REPL: {e}")
        raise
