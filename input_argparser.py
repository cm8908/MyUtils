from argparse import ArgumentParser, Namespace, ArgumentError, SUPPRESS, _UNRECOGNIZED_ARGS_ATTR
import sys as _sys

class ArgumentParserManualInput(ArgumentParser):
    def __init__(self, debug=False, pass_defaults=False, strict_check=True, *args, **kwargs):
        self.debug = debug
        self.pass_defaults = pass_defaults
        self.strict_check = strict_check
        if self.pass_defaults:
            print("type_required is set to True while debug set to False... Setting debug to True")
            self.debug = True
        super(ArgumentParserManualInput, self).__init__(*args, **kwargs)
    
    def parse_args(self, args=None, namespace=None):
        try:
            return super(ArgumentParserManualInput, self).parse_args(args, namespace)
        except:
            print("=======Please type the arguments manually======")
            namespace = Namespace()
            actions = self._get_optional_actions() + self._get_positional_actions()
            for i in range(1, len(actions)):
                action = actions[i]
                if self.pass_defaults and action.default is not None:
                    setattr(namespace, action.dest, action.type(action.default))
                    continue
                    

                value = input(f'{action.dest:<10} (type: {action.type.__name__:>5}) [default: {str(action.default):>5}] = ')
                if self.strict_check:
                    while value == '' and action.default is None:
                        print("Please specify argument!")
                        value = input(f'{action.dest:<10} (type: {action.type.__name__:>5}) [default: {str(action.default):>5}] = ')
                

                    while action.choices is not None and action.type(value) not in action.choices:
                        print("Available choices = ", action.choices)
                        value = input(f'{action.dest:<10} (type: {action.type.__name__:>5}) [default: {str(action.default):>5}] = ')
 
                value = action.default if value == '' else value
                if value is not None:
                    value = action.type(value)
                setattr(namespace, action.dest, value)
            return namespace

def defaults(value, default=None):
    if default is None:
        return default
    else:
        return value
if __name__ == '__main__':
    parser = ArgumentParserManualInput(debug=True)
    parser.add_argument('--')