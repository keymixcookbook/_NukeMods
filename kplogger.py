'''

custom logging object and module

'''




#-------------------------------------------------------------------------------
#-Import Modules
#-------------------------------------------------------------------------------




import logging
import sys
import os




#-------------------------------------------------------------------------------
#-Global Variable
#-------------------------------------------------------------------------------




LEVEL_TO_STR = {
	10: 'DEBUG',
	20: 'INFO',
	30: 'WARNING',
	40: 'ERROR',
	50: 'CRITICAL'
}




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
	RESET			= '\033[0m'
	ENDLN			= '\033[0m'
	BOLD			= '\033[1m'
	DISABLE			= '\033[2m'
	ITALIC			= '\033[3m'
	UNDERLINE		= '\033[4m'
	REVERSE			= '\033[7m'
	INVISIBLE		= '\033[8m'
	STRIKE			= '\033[9m'

	class fg:
		RED			= '\033[1;31m'
		GREEN		= '\033[1;32m'
		BLUE		= '\033[1;34m'
		CYAN		= '\033[1;36m'
		YELLOW		= '\033[1;93m'
		MAGENTA		= '\033[1;95m'

	class bg:
		RED			= '\033[1;41m'
		GREEN		= '\033[1;42m'
		BLUE		= '\033[1;44m'
		CYAN		= '\033[1;46m'
		YELLOW		= '\033[1;46m'
		MAGENTA		= '\033[1;45m'

	class msg:
		'''message presets'''
		DONE		= '\t\t\033[1;32m >>> DONE <<< \033[0m'



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




log = logging.getLogger('kplogger')

loglevel = os.getenv('KPENV') 
if loglevel: print('==========\nlogging level: %s\n==========' % LEVEL_TO_STR[int(loglevel)]) 
else: 
	loglevel = logging.INFO
	print('ENV not set, level set to 20:INFO')
log.setLevel(int(loglevel))




#-------------------------------------------------------------------------------
#-Custom Formatter Class
#-------------------------------------------------------------------------------




class KuFormatter(logging.Formatter):
	'''source: https://stackoverflow.com/questions/1343227/can-pythons-logging-format-be-modified-depending-on-the-message-log-level/8349076'''


	FORMATS = {
		logging.DEBUG		: ''.join([col.DEBUG, 	"%(levelname)s %(module)s", col.LINENUM, "Ln:%(lineno)d", col.MSG, "%(message)s", col.ENDLN]),
		logging.INFO 		: ''.join([col.MSG, 		"%(message)s", col.ENDLN]),
		logging.ERROR		: ''.join([col.ERROR, 	"%(levelname)s", col.LINENUM, "Ln:%(lineno)d", col.MSG, "%(message)s", col.ENDLN]),
		logging.WARNING		: ''.join([col.WARNING, 	"%(levelname)s", col.LINENUM, "Ln:%(lineno)d", col.MSG, "%(message)s", col.ENDLN]),
		logging.CRITICAL	: ''.join([col.CRITICAL, "%(levelname)s", col.LINENUM, "Ln:%(lineno)d", col.MSG, "%(message)s", col.ENDLN]),
	}

	def format(self, record):
		log_fmt = self.FORMATS[record.levelno]
		formatter = logging.Formatter(log_fmt)
		return formatter.format(record)




#-------------------------------------------------------------------------------
#-Handlers and Formatters
#-------------------------------------------------------------------------------



# Create Handler
handler_stream = logging.StreamHandler()

# Set Formatter
formatter_stream = KuFormatter()

# Assign Formatter and set handler levels
handler_stream.setFormatter(formatter_stream)

# Add Handlers
log.addHandler(handler_stream)


def add_FileHandler(log, logname, fmt="%(asctime)s, %(message)s"):
	'''create, set and add file handler
	@log: (obj) logging object
	@logname: (str) name of the log file
	@fmt: (str) format for file handler
	return: (obj) log object with FileHandler added
	'''

	_handler = logging.FileHandler(logname)
	_formatter = logging.Formatter(fmt,"%Y-%m-%d %H:%M:%S")
	_handler.setFormatter(_formatter)
	# _handler.setLevel(logging.INFO) # Only to log Error level
	
	# Add Handler
	log.addHandler(_handler)

	return log




#-------------------------------------------------------------------------------
#-Testing Display
#-------------------------------------------------------------------------------




if __name__ == '__main__':
	'''for displaying testing'''

	log.setLevel(logging.DEBUG)

	# str_d = (col.DEBUG, '10 debug message', col.MSG , "Detailed information, Diagnosing problems.")
	# str_i = (col.INFO, '20 Info message', col.MSG , "Confirmation that things are working as expected.")
	# str_w = (col.WARNING, '30 warning message', col.MSG , "An indication that something unexpected happened")
	# str_e = (col.ERROR, '40 error message', col.MSG , "The software has not been able to perform some function.")
	# str_c = (col.CRITICAL, '50 critical message', col.MSG , "The program itself may be unable to continue running.")

	# log.debug(''.join(str_d))
	# log.info(''.join(str_i))
	# log.warning(''.join(str_w))
	# log.error(''.join(str_e))
	# log.critical(''.join(str_c))

	log.debug("Debug Message")
	log.info("Info Message")
	log.warning("Warning Message")
	log.error("Error Message")
	log.critical("critical Message")

	# print('\n' + col.MSG + "FG Test Color" + col.ENDLN)
	# print(col.fg.RED + 'fg red'+ col.ENDLN)
	# print(col.fg.GREEN + 'fg green'+ col.ENDLN)
	# print(col.fg.BLUE + 'fg blue'+ col.ENDLN)
	# print(col.fg.CYAN + 'fg cyan'+ col.ENDLN)
	# print(col.fg.YELLOW + 'fg yellow'+ col.ENDLN)
	# print(col.fg.MAGENTA + 'fg magenta'+ col.ENDLN)

	# print('\n' + col.MSG + "BG Test Color"+ col.ENDLN)
	# print(col.bg.RED + 'bg red'+ col.ENDLN)
	# print(col.bg.GREEN + 'bg green'+ col.ENDLN)
	# print(col.bg.BLUE + 'bg blue'+ col.ENDLN)
	# print(col.bg.CYAN + 'bg cyan'+ col.ENDLN)
	# print(col.bg.YELLOW + 'bg yellow'+ col.ENDLN)
	# print(col.bg.MAGENTA + 'bg magenta'+ col.ENDLN)

	# print('\n' + col.MSG + "Bracked Color"+ col.ENDLN)
	# print("this message is"+ col.bracket(col.fg.GREEN, "Bracked") + "with \'col.bracket()\'")