from datetime import datetime
from colorama import init, Fore
import os
import traceback

# Initialize colorama
init(autoreset=True)

class Logger:
    def __init__(self):
        """
        Initializes the Logger instance.
        
        This method creates a log directory if it doesn't exist and sets the log file path.
        """
        log_dir = ".logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        self.log_file = f"{log_dir}/{datetime.now().date().isoformat()}.log"

    def _write_log(self, level, message):
        """
        Writes a log message to the log file with a given level and message.
        
        Returns:
            str: The formatted log message.
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{level} @ {timestamp}] - {message}"
        with open(self.log_file, 'a') as file:
            file.write(log_message + '\n')
        return log_message

    def info(self, message):
        """
        Use this method for general information that highlights the progress of the application.
        """
        log_message = self._write_log("INFO", message)
        print(Fore.GREEN + log_message)

    def success(self, message):
        """
        Use this method to indicate successful completion of an operation.
        """
        log_message = self._write_log("SUCCESS", message)
        print(Fore.GREEN + log_message)
        
    def notice(self, message):
        """
        Use this method to indicate a redundant but correct action, such as trying to turn on something that is already on.
        """
        log_message = self._write_log("NOTICE", message)
        print(Fore.GREEN + log_message)

    def warning(self, message):
        """
        Use this method to indicate a potential problem or important situation that should be noted.
        """
        log_message = self._write_log("WARNING", message)
        print(Fore.YELLOW + log_message)

    def debug(self, message):
        """
        Use this method for detailed information, typically of interest only when diagnosing problems.
        """
        log_message = self._write_log("DEBUG", message)
        print(Fore.BLUE + log_message)

    def error(self, message):
        """
        Use this method to indicate a significant problem that has occurred.
        """
        log_message = self._write_log("ERROR", message)
        print(Fore.RED + log_message)
    
    def exception(self, exception, message=None, expected=True, log_traceback=True):
        """
        Logs an exception message along with the traceback.
        
        Use this method to log exceptions that occur during the execution of the program.
        
        Args:
            exception (Exception): The exception instance to log.
            message (str, optional): Additional message to log with the exception.
            expected (bool, optional): Indicates if the exception was expected (caught using try-except). Defaults to True.
            log_traceback (bool, optional): Indicates if the traceback details should be logged. Defaults to True.
        """
        exception_title = f"{type(exception).__name__}:\n {str(exception)}\n"
        if log_traceback:
            exception_message = ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))
        else:
            exception_message = str(exception)
        exception_type = "EXPECTED EXCEPTION" if expected else "UNEXPECTED EXCEPTION"
        if message:
            log_message = self._write_log(exception_type, f"{message} - {exception_title}\n{exception_message}")
        else:
            log_message = self._write_log(exception_type, f"{exception_title}\n{exception_message}")
        print(Fore.MAGENTA + log_message)

    def httprequest(self, req, response):
        """
        Logs an HTTP request and its response status.
        
        Use this method to log details of incoming HTTP requests and their responses.
        """
        log_message = self._write_log(
            "REQUEST",
            f"{req.remote_addr} - {req.method} {req.url} - Status: {response.status_code}"
        )
        print(Fore.CYAN + log_message)

# Instantiate Logger at the module level
log = Logger()

if __name__ == '__main__':
    # Usage example:
    log.info('hello world')
    log.success('task completed successfully')
    log.warning('this is a warning')
    log.debug('this is a debug message')
    log.error('this is an error')
    try:
        1 / 0  # This will raise a ZeroDivisionError
    except ZeroDivisionError as e:
        log.exception(e, "An error occurred while performing division")