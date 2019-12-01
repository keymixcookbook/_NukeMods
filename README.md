# Python modules to use in a VFX Studio environment
A General scripting format and structure guide

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
  - `menuItems.py`
  - `menuDefaults.py`
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
    - Duplicate the module and **rename**: `Upd.mod_ThisMod.v#.#`
    - Create a **Trello Card** with same name
    - must indicate version number, and what's new

### IDE
  - Atom desktop
  - [Gitpod web-IDE](https://gitpod.io/workspaces/)

###### Version Control
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
- **Module as Function**
  - `mod_ThisModule.ThisModule()` - **UpperCamelCase**
  - module name keeps the same
- **Module as Class**
  - `mod_ClassModule.ClassModule.run()` - **UpperCamelCase**
    - `ClassModule = Core_ClassModule()`
  - `getMethod()`, `setMethod()` - **lowerCamelCase**



also includes:
- `<>` for variable in comments:
  - `<var>`
- `_` for space in **filenames** and **variables**, or **Folders** (if as prefix):
  - `this_file.ext`, `this_var`, `./this_folder`
- `__` for **other Folders** that is not part of the package:
  - `./__misc`
- `"s"` for multiword strings, `'s'` for keywords or attributes,`'''str'''` for function description:
  - `string = 'word'`, `nuke.thisNode()['attributes'].value()`, `ThisFunction(argument='keywords')`
  - `"More than one word"`
  - `'''for one/more line function description'''`


### Script General Format
```python
def _version_():
    ver='''

    version 0
    - Basic features

    '''
    return ver




########## Section Title 4 Space up and Down (Capital Letters) ##########





def ThisFunction(arg='keywords', quote='singleQuotes'):

  '''Function description
  @args: description (type)
  @kargs: description (type, <default value>)
  return: variables (type)
  '''

  # What does the lines below do
  sec_subSec = 'Variable'
  GLOBAL_CONSTANT = "Constant Variable"

  # have 1 space between group of lines
  if quotes: ## comment for one line
    print "String or Messages" ## use double quote
  else:
    print 'properties' ## use single quote


class Core_ThisClass(Inheritance):
  '''Class Object contain core functions'''
  def __init__(self):
    super(ThisClass, self).__int__()

    self.setDefault()

  def setDefault(self):
    '''set default values when initializing'''


  def itsMethod(self):
    print "2 spaces between Functions..."
    print "...from last line of the previous"


  def run(self):
    '''Main method for running the class'''
    self.show()

class Main_ThisClass:
  '''Class Object as a container for core class'''
  def __init__(self):
      super(Main_ThisClass, self).__init__()

      self.core = Core_ThisClass()


# create instance when script is loaded
ThisClass = Core_ThisClass()




########## Section Title 4 Space from the last line, start on the 5th line ##########





```
