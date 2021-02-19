'''

custom logging object and module

'''




#-------------------------------------------------------------------------------
#-Import Modules
#-------------------------------------------------------------------------------




import logging




#-------------------------------------------------------------------------------
#-Terminal Foramts
#-------------------------------------------------------------------------------




class col:

	# Per TYPE
	LEVEL 			= ' \033[1;37;45m '
	LINENUM			= ' \033[0;30;47m '
	MODULE			= ' \033[1;33;42m '
	MSG 			= ' \033[0m '

	# Themes Per Status
	DEBUG			= ' \033[1;37;44m '
	INFO			= ' \033[2;30;46m '
	WARNING			= ' \033[2;30;43m '
	ERROR			= ' \033[1;31;40m '
	CRITICAL		= ' \033[1;33;41m '

	# Basic Components
	RESET			= '\033[0m '
	ENDLN			= ' \033[0m'
	BOLD			= '\033[1m '
	DISABLE			= '\033[2m '
	ITALIC			= '\033[3m '
	UNDERLINE		= '\033[4m '
	REVERSE			= '\033[7m '
	INVISIBLE		= '\033[8m '
	STRIKE			= '\033[9m '

	class fg:
		RED			= '\033[1;31m '
		GREEN		= '\033[1;32m '
		BLUE		= '\033[1;34m '
		CYAN		= '\033[1;36m '
		YELLOW		= '\033[1;93m '
		MAGENTA		= '\033[1;95m '

	class bg:
		RED			= '\033[1;41m '
		GREEN		= '\033[1;42m '
		BLUE		= '\033[1;44m '
		CYAN		= '\033[1;46m '
		YELLOW		= '\033[1;46m '
		MAGENTA		= '\033[1;45m '

	def bracket(col,msg):
		'''bracketing string with coloring
		@col: (obj) color object
		@msg: (str) message with bracket with
		return: (str) message bracked
		'''
		return str(col + msg + ' \033[0m')




#-------------------------------------------------------------------------------
#-Logger
#-------------------------------------------------------------------------------




log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)




#-------------------------------------------------------------------------------
#-Handlers and Formatters
#-------------------------------------------------------------------------------



# Create Handler
handler_stream = logging.StreamHandler()
handler_file = logging.FileHandler('kulogger.log')

# Set Formatter
formatter_stream = logging.Formatter(''.join([
					col.LEVEL, "%(levelname)s", 
					col.LINENUM, "Ln:%(lineno)d",
					col.MSG, '\t|',
					# col.MODULE, "%(module)s",
					col.MSG, "%(message)s"
					]))
formatter_file = logging.Formatter("%(levelname)s:Ln:%(lineno)d@%(module)s || %(message)s")

# Assign Formatter and set handler levels
handler_stream.setFormatter(formatter_stream)
handler_file.setFormatter(formatter_file)
handler_file.setLevel(logging.ERROR) # Only to log Error level

# Add Handlers
log.addHandler(handler_stream)
# log.addHandler(handler_file)



#-------------------------------------------------------------------------------
#-Testing Display
#-------------------------------------------------------------------------------




if __name__ == '__main__':
	'''for displaying testing'''

	log.setLevel(logging.DEBUG)

	str_d = (col.DEBUG, '10 debug message', col.MSG , "Detailed information, Diagnosing problems.")
	str_i = (col.INFO, '20 Info message', col.MSG , "Confirmation that things are working as expected.")
	str_w = (col.WARNING, '30 warning message', col.MSG , "An indication that something unexpected happened")
	str_e = (col.ERROR, '40 error message', col.MSG , "The software has not been able to perform some function.")
	str_c = (col.CRITICAL, '50 critical message', col.MSG , "The program itself may be unable to continue running.")

	log.debug(''.join(str_d))
	log.info(''.join(str_i))
	log.warning(''.join(str_w))
	log.error(''.join(str_e))
	log.critical(''.join(str_c))

	print('\n' + col.MSG + "FG Test Color" + col.ENDLN)
	print(col.fg.RED + 'fg red'+ col.ENDLN)
	print(col.fg.GREEN + 'fg green'+ col.ENDLN)
	print(col.fg.BLUE + 'fg blue'+ col.ENDLN)
	print(col.fg.CYAN + 'fg cyan'+ col.ENDLN)
	print(col.fg.YELLOW + 'fg yellow'+ col.ENDLN)
	print(col.fg.MAGENTA + 'fg magenta'+ col.ENDLN)

	print('\n' + col.MSG + "BG Test Color"+ col.ENDLN)
	print(col.bg.RED + 'bg red'+ col.ENDLN)
	print(col.bg.GREEN + 'bg green'+ col.ENDLN)
	print(col.bg.BLUE + 'bg blue'+ col.ENDLN)
	print(col.bg.CYAN + 'bg cyan'+ col.ENDLN)
	print(col.bg.YELLOW + 'bg yellow'+ col.ENDLN)
	print(col.bg.MAGENTA + 'bg magenta'+ col.ENDLN)

	print('\n' + col.MSG + "Bracked Color"+ col.ENDLN)
	print("this message is"+ col.bracket(col.fg.GREEN, "Bracked") + "with \'col.bracket()\'")