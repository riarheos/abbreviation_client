"""
The AbbreviationClient is a simple framework for creating CLI applications.
It parses command line according to the natural language.

E.g.:

from abbbreviation_client import AutoAbbreviationClient

class Foo(AutoAbbreviationClient):
    client_name = 'Foo Client'

    def bar_baz(self, data=''):
        pass

def main():
    Foo().run()
"""

import sys
import inspect
from collections import namedtuple
from .Colors import red, green, yellow
from .ParameterTypes import StringParameterType, ParameterType
from .Errors import BadArgumentsError


MethodInfo = namedtuple('MethodInfo', ['doc', 'params', 'name_path'])
ParamInfo = namedtuple('ParamInfo', ['name', 'default', 'annotation'])
Empty = inspect.Parameter.empty


def client_handler(fun):
    """ The decorator to extract useful info from class methods """
    doc = inspect.getdoc(fun)
    params = inspect.signature(fun).parameters
    name_path = fun.__name__.split('_')

    param_map = {}
    for name, param in params.items():
        if name == 'self':
            continue

        ann = param.annotation
        if not isinstance(param.annotation, ParameterType):
            if ann == Empty:
                ann = StringParameterType()
            else:
                ann = StringParameterType(ann)

        param_map[name] = ParamInfo(name, param.default, ann)

    fun.method_info = MethodInfo(doc, param_map, name_path)
    return fun


class AbbreviationClient:
    """
    The abbreviation client. Depends on the client_handler decorator
    usage on the subclasses. For a full-auto version that maps all
    non-private methods see into the AutoAbbreviationClient class.
    """
    client_name = 'Generic abbreviation client'

    def __init__(self):
        self._command_tree = {}     # {name} -> {name} -> .. -> MethodInfo
        self._command_list = []     # [ MethodInfo, ... ]
        self._name = sys.argv.pop(0)

        # extract method info into a command tree
        for name in dir(self):
            method = getattr(self, name)
            if name != 'run' and hasattr(method, 'method_info'):
                path = method.method_info.name_path
                ptr = self._command_tree
                for item in path[:-1]:
                    if item not in ptr:
                        ptr[item] = {}
                    ptr = ptr[item]
                ptr[path[-1]] = method

                self._command_list.append(method.method_info)

    def run(self):
        """ Run methods base on the command line """
        try:
            self._run_command_line()
            return
        except IndexError:
            error_string = 'Not enough arguments'
        except BadArgumentsError as err:
            error_string = err
        print()
        print(red(error_string))
        self.help()

    @client_handler
    def help(self):
        """ Display help """
        print('\n%s\n' % yellow(self.client_name))
        print('USAGE: %s <command>' % self._name)
        print('Commands can be unambiguously abbreviated.\n')

        for command in self._command_list:
            out_string = green(' '.join(command.name_path))
            for name, param in command.params.items():
                out_string += ' ' + param.annotation.format_help(param)

            print('  * %-45s' % out_string)
            print('    %s' % command.doc)
            print()

    def _run_command_line(self):
        """ Parses command line and runs required methods """

        def find_full_argument(all_possibles, short_argument):
            """ Finds a non-ambiguous non-abbreviated argument """
            possibles = [x for x in all_possibles if x.startswith(short_argument)]
            if not possibles:
                raise BadArgumentsError('Unknown argument "%s"' % short_argument)
            if len(possibles) > 1:
                raise BadArgumentsError('Ambiguous argument "%s" (possible: %s)' % (short_argument, ', '.join(possibles)))
            return possibles[0]

        # find the method on the tree
        method = self._command_tree
        while isinstance(method, dict):
            arg = sys.argv.pop(0)
            method = method[find_full_argument(method, arg)]

        # find required positional args
        args = []
        for name, param in method.method_info.params.items():
            if param.default == Empty:
                _, data = param.annotation.extract_param(param, sys.argv)
                args.append(data)

        # extract all optional params
        optional_params = {}
        for name, param in method.method_info.params.items():
            if param.default != Empty:
                param.annotation.append_optional_names(param, optional_params)

        kwargs = {}
        while sys.argv:
            key = find_full_argument(optional_params, sys.argv[0])
            key, data = optional_params[key].annotation.extract_param(optional_params[key], sys.argv)
            kwargs[key] = data

        method(*args, **kwargs)


class AutoAbbreviationClient(AbbreviationClient):
    """
    Works like AbbreviationClient but treats all non-private methods
    as ones with @client_handler on them.
    """
    def __init__(self):
        for name in dir(self):
            method = getattr(self.__class__, name)
            if inspect.isfunction(method) and not name.startswith('_'):
                client_handler(method)

        super().__init__()
