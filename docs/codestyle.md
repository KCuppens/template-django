# Coding style and standards

The development team is international. Please use English for class/methods/variables names, in documentation and in commits. Whenever something is untranslatable, add a comment to explain the role (e.g. *Canton is one of the 26 member states of Switzerland.*)

## General coding style
> Programs are meant to be read by humans and only incidentally for computers to execute.
>
>Donald Knuth

- Keep functions / methods short: a good rule of thumb is that you should not scroll down to see an entire function
- Keep files short: more than 1000 lines of code in a single file seem really long, perhaps it could be refactored
- Name things so that a human can read them easily (not too long, too specific, no acronyms, ...)


## Python style
- You should install [pre-commit](https://pre-commit.com/). This will enforce black, isort and flake8 are installed and run automatically before you can commit your work.
- All files should be formatted using the [black](https://black.readthedocs.io/en/stable/) auto-formatter.
- The project repository includes an `.editorconfig` file. We recommend using a text editor with [EditorConfig](https://editorconfig.org/) support (e.g. PyCharm, VisualStudio) to avoid indentation and whitespace issues. The Python files use 4 spaces for indentation and the HTML files use 2 spaces.
- Unless otherwise specified, follow [PEP 8](https://peps.python.org/pep-0008/).
Use [flake8](https://pypi.org/project/flake8/) to check for problems in this area. Note that our `setup.cfg` file contains some excluded errors that we don’t consider as gross violations. Remember that PEP 8 is only a guide, so respect the style of the surrounding code as a primary goal.
- Use underscores, not camelCase, for variable, function and method names (i.e. `employee.set_employment_type()`, not `employee.setEmploymentType()`.
- Use InitialCaps for class names (e.g. `CompanyInsuranceGroupSalaryRange`).
- Use constants wherever possible, especially when dealing with MEGA field names.

### Imports
Use [isort](https://github.com/PyCQA/isort#readme) to automate import sorting. The guidelines are included in the `setup.cfg` file:
- Put imports in these groups: future, standard library, django components, third-party libraries, other *{app_name}* components, local components, try/excepts. Place all `import module statements` before `from module import objects` in each section. Use absolute imports for other *{app_name}* components and relative imports for local components.
- On each line, alphabetize the items with the upper case items grouped before the lowercase items.
- Break long lines using parentheses and indent continuation lines by 4 spaces. Include a trailing comma after the last import and put the closing parenthesis on its own line.
- Use a single blank line between the last import and any module level code, and use two blank lines above the first function or class.



For example (comments are for explanatory purposes only):

``` Python
# future
from __future__ import unicode_literals

# standard library
import json

# Django
from django.http import HttpRequest

# third-party
from rest_framework.viewsets import GenericViewSet, ModelViewSet

# {app_name} components
from billing.api.v1.permissions import SubscriptionPermissions
from billing.tasks import sync_employees_subscription

# Local components
from .serializers import (
    EmployeeSerializer,
    EmployeeUpdateSerializer,
)
```

## Template style
- Put one (and only one) space between the curly brackets and the tag contents.

## Models style
- Field names should be all lowercase, using underscores instead of camelCase.
- The `class Meta` should appear after the fields are defined, with a single blank line separating the fields and the class definition.
- The order of model inner classes and standard methods should be as follows:
    - All database fields
    - Custom manager attributes
    - `class Meta`
    - Properties, [magic methods](https://rszalski.github.io/magicmethods/), public methods
    - Reading order: As a rule of thumb, put methods above all methods called from their body.


## Documentation
Generally speaking, useful documents and comments are always encouraged. Better at the wrong place than not written down.


### Developer-facing documentation
Notes and guides that developers need in order to set up and maintain a project are located it here in `docs/` folder:
- installation
- tests
- deployment
- ...


### Documentation inside python code
The more a module, model or method is obscure the more it should be commented.

#### Docstrings
Docstrings can be used to describe functions, methods or classes.
```python
def say_hello(name):
    """A simple function that says hello... Richie style"""
```

If a whole module is to be documented (e.g. *What is the purpose of the `progress` module?*), do it with a docstring in the `__init__.py` file of the module

## Exceptions and Sentry

In general:

0. Do not catch any exception unless you have a really good reason to. Let it bubble up.
1. Do not use sentry specific report functions. Use `logger.exception` and `logger.warning` instead. https://docs.sentry.io/platforms/python/guides/logging/#usage
2. Do not create and throw a different exception in an except block. If you must please use chaining https://docs.python.org/3/tutorial/errors.html#exception-chaining.
3. Do not use very unspecific exception catching if you can avoid it.
4. Try to not log and report errors twice.

### Do not do this

```python
try:
    ...
except Exception as e:
    exception_sentry(e)
    raise Exception(f"Failed suppressing salary with error: {e}")
```

### But do this

```python
try:
    ...
except SalarySuppressionError as error: # If you are catching a specific error because you want to do something special
    # We need to do something specific about SalarySuppressionError here 
    user.notify("Salary suppression did not work")
    # we re-raise the same exception, sentry will catch it eventually unless it is explicitly silenced by a caller.
    raise error
# any other error that is not SalarySuppressionError should bubble up normally
```

#### Comments

- Code Description: Comments can be used to explain the intent of specific sections of code:
```
# Attempt a connection based on previous settings. If unsuccessful,
# prompt user for new settings
```
- Tagging: The use of tagging can be used to label specific sections of code where known issues or areas of improvement are located. Some examples are: BUG, FIXME, and TODO:
```
# FIXME: rename this method name when new function is available
```
- Parameters: because of laziness but also of readability, we tend not to use python's type hints. Prefer docstrings when parameter types are not trivially guessed.
