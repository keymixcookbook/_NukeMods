# Python Project Name

Oneline description of the python project

## Features
- Features
- Features
- Features


## Package Content

Package structure primary follows Python guidlines with few adjustments

**Default Contents:**
- `__main__.py`: main executable
- `uisetup`: main ui module
- `resources/`: resources files ie. images, help documents, etc
- `utility/`: any supporting utility functions and modules
  - `__init__.py`: main utility functions goes here, unless specific
- `tests/`: unit test files
  - `test_main.py`
- `Qt.py`: PyQt module
- `README.md`: Readme file, module description
- `requirements.txt`: dependencies manifest
- `LICENSE`: license file

**Optional Contents:**
- `config.json`: settings and configeration file

### Formatting Guide for python
Following briefly with Python PEP 8 guidelines, except:

- **Utility Function**
  - `utilityFunction()` - **lowerCamelCase**
- **Methods and Regular Functions**
  - `function_and_methods()` - **lower_case**
- **Module's main function**
  - `mod_ThisModule.ThisModule()` - **UpperCamelCase**
  - module name keeps the same
- **Module with Class when instance**
  - `mod_ClassModule.ClassModule.run()` - **UpperCamelCase**
    - `ClassModule = Core_ClassModule()`
  - `get_thisMethod()`, `set_thisMethod()` - **lower_lowerCamelCase**



**also includes:**
- `<>` for variable in comments:
  - `<var>`
- `_` for space in **filenames** and **variables**, or **Folders** (if as prefix):
  - `this_file.ext`, `this_var`, `./this_folder`
- `__` for **other Folders** that is not part of the package:
  - `./__misc`
- `"s"` for multiword strings, `'s'` for keywords or attributes,`'''str'''` for doc string:
  - `string = 'word'`, `nuke.thisNode()['attributes'].value()`, `ThisFunction(argument='keywords')`
  - `"More than one word"`
  - `'''for one/more line function description'''`


**doc strings**
```python
def func(args, kargs):
  '''oneline description of the function
  @args: (type) description of this arg
  @kargs='value': descripon of this karg's value
  return: (type) description of what is returned
  '''
```

### Script General Format
```python
'''

Oneline description of the module

'''


import platform


__VERSION__='1.0'
__OS__=platform.system()
__AUTHOR__="Tianlun Jiang"
__COPYRIGHT__="copyright %s" % __AUTHOR__

__TITLE__=__file__.split('_')[1].split('.')[0]

def _version_():
    ver='''

    version 0
    - Basic features

    '''
    return ver




#------------------------------------------------------------------------------
#-Section Title 4 Space up and Down (Capital Letters) 
#-( '#' x 1, '-' x 78 )
#------------------------------------------------------------------------------




def this_function(args, kargs):
  '''oneline description of the function
  @args: (type) description of this arg
  @kargs='value': descripon of this karg's value
  return: (type) description of what is returned
  '''

  # What does the lines below do
  sec_subSec = 'Variable'
  GLOBAL_CONSTANT = "Constant Variable"

  # have 1 space between group of lines
  if quotes: ## comment for one line
    print "String or Messages" ## use double quote
  else:
    print 'properties' ## use single quote

  
  def another_function():
    print("2 spaces between functions and classes")


this_function( one_space_margin )


class Core_ThisClass(Inheritance):
  '''Class Object contain core functions'''
  def __init__(self):
    super(ThisClass, self).__int__()

    self.set_default()

  def set_default(self):
    '''set default values when initializing'''

  def its_method(self):
    print "1 space between Methods..."
    print "...from last line of the previous"

  def run(self):
    '''Main method for running the class'''
    self.show()


class Core_ThisClass:
  '''Class Object as a container for core class'''
  def __init__(self):
      super(Core_ThisClass, self).__init__()

      self.core = Core_ThisClass()




#------------------------------------------------------------------------------
#-Section Title 4 Space up and Down (Capital Letters)
#------------------------------------------------------------------------------




ThisClass = Core_ThisClass()
```

---

**Copyright © Tianlun Jiang**
