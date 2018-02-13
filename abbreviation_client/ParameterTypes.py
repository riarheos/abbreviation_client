"""
Different parameter types that can be used in annotations in
the client class
"""
from .Colors import blue, green
from inspect import Parameter
from .Errors import BadArgumentsError


class ParameterType:
    """ The abstract base parameter type """
    def __init__(self, arg=None):
        self.arg = arg

    def format_help(self, parameter):
        text = self._help_info(parameter)
        if parameter.default == Parameter.empty:
            return green(text)
        else:
            return blue('[%s]' % text)

    def extract_param(self, parameter, args):
        return NotImplementedError()

    @staticmethod
    def append_optional_names(parameter, params: dict):
        params[parameter.name] = parameter

    def _help_info(self, parameter):
        return NotImplementedError()


class BooleanParameterType(ParameterType):
    """ The boolean parameter type with optional helper name"""
    def _help_info(self, parameter):
        return '[no]' + (self.arg or parameter.name)

    @staticmethod
    def append_optional_names(parameter, params: dict):
        params[parameter.name] = parameter
        params['no' + parameter.name] = parameter

    def extract_param(self, parameter, args):
        arg = args.pop(0)
        if parameter.name.startswith(arg):
            return parameter.name, True
        if ('no' + parameter.name).startswith(arg):
            return parameter.name, False
        raise BadArgumentsError('Specify either %s or no%s' % (parameter.name, parameter.name))


class StringParameterType(ParameterType):
    """ Generic string parameter type, no checks in it """
    def _help_info(self, parameter):
        return '%s %s' % (parameter.name, self.arg or 'XXX')

    def extract_param(self, parameter, args):
        _ = args.pop(0)
        arg = args.pop(0)
        return parameter.name, arg


class EnumParameterType(ParameterType):
    """ The enum type, works like string but has conditional checks """
    def _help_info(self, parameter):
        return '%s <%s>' % (parameter.name, '|'.join(self.arg))

    def extract_param(self, parameter, args):
        _ = args.pop(0)
        arg = args.pop(0)
        if arg not in self.arg:
            raise BadArgumentsError('Only one of %s is allowed' % (', '.join(['"%s"' % x for x in self.arg])))
        return parameter.name, arg


class PositionalParameterType(ParameterType):
    """ The positional type, works like string but has no name prefix """
    def _help_info(self, parameter):
        return '<%s>' % (self.arg or parameter.name)

    def extract_param(self, parameter, args):
        arg = args.pop(0)
        return parameter.name, arg
