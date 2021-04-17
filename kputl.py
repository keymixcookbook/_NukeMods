'''

Function to use package-wise

'''




#-------------------------------------------------------------------------------
#-Module Import
#-------------------------------------------------------------------------------




import os
import inspect
import math




#-------------------------------------------------------------------------------
#-Functions
#-------------------------------------------------------------------------------




def joinPath(*paths):
    '''joining path to fix windows and OSX symlink to '/' uniformly'''
    try:
        p = os.path.join(*paths).replace('\\', '/')
        return p
    except ValueError:
        pass


def nukeColor(r,g,b):
	'''convert rgb to nuke 16 bit value
	@r,g,b: (float) float rgb values 0-1
	return: 8-bit ints
	'''
	return int('%02x%02x%02x%02x' % (
		r * 255, g * 255, b * 255, 0 * 255), 
		16
		)


def hsv2rgb(h, s, v):
	'''convert hsv to rgb
	return: r, g, b (ints)
	'''
	# Source: http://code.activestate.com/recipes/576919-python-rgb-and-hsv-conversion/
	h = float(h)
	s = float(s)
	v = float(v)
	h60 = h / 60.0
	h60f = math.floor(h60)
	hi = int(h60f) % 6
	f = h60 - h60f
	p = v * (1 - s)
	q = v * (1 - f * s)
	t = v * (1 - (1 - f) * s)
	r, g, b = 0, 0, 0
	if hi == 0: r, g, b = v, t, p
	elif hi == 1: r, g, b = q, v, p
	elif hi == 2: r, g, b = p, v, t
	elif hi == 3: r, g, b = p, q, v
	elif hi == 4: r, g, b = t, p, v
	elif hi == 5: r, g, b = v, p, q
	r, g, b = int(r * 255), int(g * 255), int(b * 255)
	return r, g, b
