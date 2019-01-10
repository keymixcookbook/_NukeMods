# Python modles to use in a VFX Studio enviroment

# Main Components
  - ~/_mod_KuFunc
  - ~/_mod_KuStudio
  - ~/_mod_Drafts
  - menu.py
  - init.py
  - KuFunc.py
  - KuStudio.py

# Formatting Guide for python

## Script General Format
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
  GLOBAL = "Global Variable"

  # have 1 space between group of lines
  if quotes: ## comment for one line
    print "String or Messages" ## use double quote
  else:
    print 'properties' ## use single quote



def OtherFunction():
  print "3 spaces between Functions"
  print "from last line of the previous"




########## SECTION TITLE 4 SPACES FROM UP LINE ##########





```
