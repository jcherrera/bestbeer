## @package db_comms.logging
#  Logging for the comms communications.
import time

## A class variable of the session class contains ,ethods for logging any interaction with the database.
#
#  
class Logger:
	## Class constructor
	#  @param self The object pointer.
	#  @param filename The naem of the log file.
	def __init__(self, filename):
		## Pinter to the open file.
		self.log = open(filename, 'w')
		## Timestamp of last comms command
		self.last_command_time = None
		self.log.write(time.strftime("[%d/%m/%Y] [%H:%M:%S]") + " - Session started\n")

	## Logs a comms command in log with a timestamp.
	#  @param self The object pointer.
	#  @param command The query performed on the database.
	def log_command(self, command):
		self.last_command_time = time.clock()
		log_string = time.strftime("[%H:%M:%S] ") + command + "\n"
		self.log.write(log_string)

	## Logs the success or failure of previous command.
	#  @param self The object pointer.
	#  @param error The error. =None if successful.
	#  @param print_error Prints error to stdout if set to True.
	def log_completion(self, error, print_error=False):
		if error == None:
			self.log.write("Completed in {} seconds\n".format(time.clock() - self.last_command_time))
		else:
			self.log.write("Error: " + error + "\n")
			if print_error:
				print "\n" + error + "!\n"

	## Closes log file.
	#  @param self The object pointer.
	def close_log(self):
		self.log.close()
