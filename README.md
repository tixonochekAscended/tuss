# `🎯` TUSS (Tix's United Signal System)
This is a _"project"_ that was made in ~30 minutes for absolutely no purpose and exists purely because of my boredom at the moment of coding **TUSS**.

## Installation
There are multiple ways to install this useful piece of a library:
1. Create a new file `tuss.py` in your project and just copy & paste the code from the `tuss.py` file in this repository. As simple as that.
2. Download the file `tuss.py` and put it in the project yourself (time-consuming 🕒).

## Usage
**TUSS** allows you to execute multiple functions at the same time and see how the execution process went via **signals**. You can create signals, add functions to them ("extend onto signals") and call a specific signal to execute all of the functions binded to it, which will return a dictionary with the necessary information on how everything went. Here's a code example:
```py
import tuss

smanager = tuss.SignalManager(verbose=True)
smanager.create_signal("foo")

def square(a: int) -> int:
    if type(a) is not int: raise TypeError
    return a**2

def print_hello() -> None:
    print("Hello!")

smanager.extend_on("foo", [square, print_hello, lambda x: x*2])

results = smanager.call("foo", {
    'square': 2,
    '<lambda>': 13
})

print(results)
```
This small script leads to this output:
```py
Hello!
{
    "square": {"result": True, "returned": 4},
    "print_hello": {"result": True, "returned": None},
    "<lambda>": {"result": True, "returned": 26},
}

```
How to use functions, what arguments need to be provided, their types, what "verbose" is and so on is explained in the **docstrings**. Either read them directly from `tuss.py` or use one of these in your python code: `help(FUNCTION)`, `print(FUNCTION.__doc__)`.
