def say_hello(name):
    """Prints a hello-message with your name

    Args:
        name (string): your name
    """

    assert type(name) == str, "Name must be a string."

    print(f"Hello {name}!")
