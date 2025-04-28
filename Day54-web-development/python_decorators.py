import time

def delay_decorator(function):
    def wrapper_function():
        # Do something before the function
        time.sleep(2)
        function()
        # Do something after the function
    return wrapper_function

@delay_decorator
def say_hello():
    print("Hello")

@delay_decorator
def say_goodbye():
    print("Goodbye")

def say_greeting():
    print("How are you?")