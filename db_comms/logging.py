import time

class Logger:
	def __init__(self, filename):
		self.log = open(filename, 'w')
		self.last_command_time = None
		self.log.write(time.strftime("[%d/%m/%Y] [%H:%M:%S]") + " - Session started\n")

	def log_command(self, command):
		self.last_command_time = time.clock()
		log_string = time.strftime("[%H:%M:%S] ") + command + "\n"
		self.log.write(log_string)

	def log_completion(self, error, print_error=False):
		if error == None:
			self.log.write("Completed in {} seconds\n".format(time.clock() - self.last_command_time))
		else:
			self.log.write("Error: " + error + "\n")
			if print_error:
				print "\n" + error + "!\n"

	def close_log(self):
		self.log.close()
