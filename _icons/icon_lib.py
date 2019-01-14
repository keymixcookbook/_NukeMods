'''
![GitHub Logo](/images/logo.png)
Format: ![Alt Text](url)
'''


import os

this_dir = os.path.join(os.path.dirname(__file__), "_src")

icons = [i for i in os.listdir(this_dir) if ".png" in i]

print this_dir

with open("_icons/README.md", 'w') as lib:
    lib.writelines("# Nuke Icons\n\n")
    lib.writelines("| IMG | Filename |\n")
    lib.writelines("| :---: | :--- |\n")
    for i in icons:
        lib.writelines("|![{name}](./_src/{filename})|{name}|\n".format(name=os.path.splitext(i)[0], filename=i))
