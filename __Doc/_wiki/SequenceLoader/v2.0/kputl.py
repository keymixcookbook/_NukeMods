'''

Function to use package-wise

'''




import os




def joinPath(*paths):
    '''joining path to fix windows and OSX symlink to '/' uniformly'''
    try:
        p = os.path.join(*paths).replace('\\', '/')
        return p
    except ValueError:
        pass