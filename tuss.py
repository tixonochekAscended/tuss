from typing import Callable, Union, Optional, Any
from collections.abc import Iterable

class TussException(Exception):
    pass

class SignalManager:
    def __init__(self, verbose: bool) -> None:
        """
        Initializes a new SignalManager.

        :param verbose: Whether errors should be raised or ignored, and instead a function will return a boolean value.
        :type verbose: bool
        """
        self.saf: dict[str, list[Callable]] = {}
        self.verbose = verbose

    def create_signal(self, signal_name: str) -> Optional[bool]:
        """
        Creates a new signal.

        :param signal_name: The name of the new signal.
        :type signal_name: str

        :return: True if the signal was created, False if it already exists and verbose is False.
        :rtype: Optional[bool]
        """
        if signal_name in self.saf.keys(): 
            if not self.verbose: return False
            raise TussException(f"Signal {signal_name} already exists.")
        self.saf[signal_name] = []
        return True

    def extend_on(self, signal_name: str, fns: Union[Callable, list[Callable]]) -> Optional[bool]:
        """
        Extends a signal with new functions.

        :param signal_name: The name of the signal to extend.
        :type signal_name: str
        :param fns: The functions to add to the signal, or a single function.
        :type fns: Union[Callable, list[Callable]]

        :return: True if the functions were successfully added, False if the signal does not exist and verbose is False.
        :rtype: Optional[bool]
        """
        if not signal_name in self.saf.keys():
            if not self.verbose: return False
            raise TussException(f"Signal {signal_name} does not exist.")
        if callable(fns): fns = [fns];
        self.saf[signal_name].extend(fns)
        return True
    
    def call(self, signal_name: str, args: dict[str, tuple] = {}) -> Optional[dict[str, dict[str, Union[bool, Any]]]]:
        """
        Calls a signal with the given arguments.

        :param signal_name: The name of the signal to call.
        :type signal_name: str
        :param args: The arguments to pass to the functions, in the form of a dictionary where the keys are the function names
                     and the values are tuples of arguments to pass to the functions.
        :type args: dict[str, tuple]

        :return: A dictionary with the results of calling the functions, where the keys are the function names and the values
                 are dictionaries with keys 'result' (a boolean indicating whether the function call was successful) and
                 'returned' (the return value of the function, or None if the call failed).
        :rtype: Optional[dict[str, dict[str, Union[bool, Any]]]]
        """
        if not signal_name in self.saf.keys():
            if not self.verbose: return False
            raise TussException(f"Signal {signal_name} does not exist.")
        results: dict[str, bool] = {}
        for fn in self.saf[signal_name]:
            try: 
                ret: Any = None
                if fn.__name__ in args.keys(): 
                    if not isinstance(args[fn.__name__], Iterable): ret = fn(*[args[fn.__name__]])
                    else: ret = fn(*args[fn.__name__])
                else: ret = fn()
                results[fn.__name__] = {
                    'result': True,
                    'returned': ret
                }
            except:
                if not self.verbose: results[fn.__name__] = {
                    'result': False,
                    'returned': None
                }
                else: raise TussException(f"Failed to call {fn.__name__} while executing signal {signal_name}.")
        return results
