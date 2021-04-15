# Python modules to use in a VFX Studio environment
A General scripting format and structure guide

[Tool Documentation Page](https://github.com/tianlunjiang/_NukeStudio/wiki)

### Main Components
  - `./_pkg_KuFunc`
    - `__int__.py`
    - `mod_KuUtility.py`
  - `./_pkg_KuStudio`
    - `__int__.py`
    - `mod_KuStudio.py`
  - `./_mod_Drafts`
  - `./_mod_Download`
  - `menu.py`
  - `menu_items.py`
  - `menu_defaults.py`
  - `kputil.py`
  - `init.py`
  - `Qt.py`

### Installation
  - Download this entire folder `/_NukeStudio`
  - Copy `init.edit.py` and `menu.edit.py` to `~/$HOME/.nuke`
  - In `init.edit.py`
    - `os.environ['KU_PKG_PATH'] = "Where /_NukeStudio is in abs path"`
    - `os.environ['KU_STUDIO_ENV'] = "Studio Name"`

### Version Control
  - **Update Board** linked with [Trello](https://trello.com/b/4FR8ZOcZ)
  - **Newly Started File** goes to `/_mod_Draft` with prefix `dft_`
  - **New Versions** of exsisting modules:
    - Duplicate the module and **rename**: `Upd_mod_ThisMod.v#s#.py`
    - Create a **Trello Card** with same name
    - must indicate version number, and what's new

### IDE
  - VSCode desktop
  - [Gitpod web-IDE](https://gitpod.io/workspaces/)

### Title
section includes description, author, copyright, current os, etc
```python
'''

Oneline description of the module

'''


import platform


__VERSION__		= '0.0'
__OS__			  = platform.system()
__AUTHOR__	 	= "Tianlun Jiang"
__WEBSITE__		= "jiangovfx.com"
__COPYRIGHT__	= "copyright (c) %s - %s" % (__AUTHOR__, __WEBSITE__)

__TITLE__		  = "MODENAME v%s" % __VERSION__


...
```

### Version Control
Defined at the beginning of the module, at module level
``` python
def _version_():
    ver='''

    version 1.1
    - feature bug fix
    - feature refine/optimization

    version 1.0
    - new feature added

    version 0
    - Basic features

    '''
    return ver
```


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
