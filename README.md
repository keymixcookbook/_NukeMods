# Python modules to use in a VFX Studio environment
A General scripting format and structure guide

>~/$HOME/.nuke

### Main Components
  - ~/_mod_KuFunc
  - ~/_mod_KuStudio
  - ~/_mod_Drafts
  - menu.py
  - init.py
  - KuFunc.py
  - KuStudio.py

### Formatting Guide for python
Following briefly with Python PEP 8 guidlines, except:

- **UpperCamelCase** for **standalone** functions and modules:
  - `ThisFuntion()`, `ThisModule.py`

> Methods with in a Class is still the same: `ThisClass.itsMethod()`

also includes:
- `$` for variable in comments, ALL_CAP:
  - `$VAR`
- `_` for space in **filenames** and **variables**, or **Folders** (if as prefix):
  - `this_file.ext`, `this_var`, `./this_folder`
- `-` for **other Folders**:
  - `./-misc`
- `""` for strings, `''` for keywords or attributes:
  - `string = "Text"`, `nuke.thisNode()['attributes'].value()`, `ThisFunction(argument='keywords')`


### Script General Format
```python
'''

# Section
- What does this script do
- 1 space up & down

# With 1 Space In-between
- $VARIABLES, $USED_IN, $COMMENTS
- Temp Directory: /$TEMP/directory/_in_comments

'''




########## SECTION TITLE 4 SPACES UP & DOWN ##########





def ThisFunction(arg='keywords', quote='singleQuotes'):

  '''
  - Function description
  - Function name using: UpperCamelCase
  - Variables name using: lowerCamelCase
  - Global/Special variables: ALL_CAP
  '''

  # What does the lines below do
  sec_subSec = "Variable"
  GLOBAL_CONSTANT = "Constant Variable"

  # have 1 space between group of lines
  if quotes: ## comment for one line
    print "String or Messages" ## use double quote
  else:
    print 'properties' ## use single quote


class ThisClass:

  def itsMethod():
    print "3 spaces between Functions"
    print "from last line of the previous"




########## SECTION TITLE 4 SPACES FROM UP LINE ##########





```
