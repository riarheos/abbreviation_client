# Abbreviation client
There comes a time when you want to write a console client. That one has to handle lots of actions and lots of options. And of course the options must be optional. Enter abbreviation client. This library let's you do the task with ease:

Consider the following code:

```python3
from abbreviation_client import AutoAbbreviationClient


class TestClient(AutoAbbreviationClient):
    client_name = 'Test Client'

    def greet(self, name, kind='beautiful'):
        """ Greets the user """
        print(f'hello, {kind} {name}')


if __name__ == '__main__':
    TestClient().run()
```

This snippet creates a full-blown console client (that even allows for unambiguous abbreviations):

```bash
$ ./ac.py

Not enough arguments

Test Client

USAGE: ./ac.py <command>
Commands can be unambiguously abbreviated.

  * greet name XXX [kind XXX]
    Greets the user

  * help
    Display help
    
    
$ ./ac.py greet name world kind amazing
hello, amazing world

$ ./ac.py g n sir k kind
hello, kind sir

$ ./ac.py gr n girl
hello, beautiful girl
```

Cool, isn't it?

## API

### AutoAbbreviationClient

The `AutoAbbreviationClient` class tries to do all the magic. If you inherit your class from it, all the public methods are automatically considered as the client actions. The python descriptions and default values are passed as-is.

You may set the `client_name` property to specify the client name for the documentation.

Example:
```python
class Foo(AutoAbbreviationClient):
    client_name = "Foo client"

    def method(self, argument, optional_argument='default value'):
        """ Method description """
        pass
```
