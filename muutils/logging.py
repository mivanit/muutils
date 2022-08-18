from functools import partial
import sys
import json
import time
from typing import TextIO, Any, Callable

from muutils.misc import sanitize_fname
from muutils.json_serialize import JSONitem, json_serialize

# pylint: disable=arguments-differ

class NullIO:
	"""null IO class"""
	def __init__(self) -> None:
		pass

	def write(self, msg: str) -> None:
		pass

	def flush(self) -> None:
		pass

	def close(self) -> None:
		pass


class SimpleLogger:
	"""logs training data to a jsonl file"""
	def __init__(
			self, 
			log_path: str|None = None, 
			log_file: TextIO|None = None, 
			timestamp: bool = True,
		):

		self._timestamp: bool = timestamp
		self._log_path: str|None = log_path
		
		if (log_path is None) and (log_file is None):
			print("[logger_internal] # no log file specified, will only write to console", sys.stderr)
			self._log_file_handle = NullIO()

		elif (log_path is not None) and (log_file is not None):
			raise ValueError("cannot specify both log_path and log_file, use streams in `SimpleLogger`")
		else:
			# now exactly one of the two is None
			if log_file is not None:
				self._log_file_handle = log_file
			else:
				self._log_file_handle = open(log_path, "w")
	
	def __del__(self):
		try:
			self._log_file_handle.flush()
			print("[logger_internal] # failed to flush log file", sys.stderr)
		except:
			pass
		try:
			self._log_file_handle.close()
			print("[logger_internal] # failed to close log file", sys.stderr)
		except:
			pass

	def log(self, msg: "JSONitem", console_print: bool = False):
		if console_print:
			print(msg)
		
		if not isinstance(msg, dict):
			msg = {"_msg": msg}
		
		if self._timestamp:
			msg["_timestamp"] = time.time()
		
		self._log_file_handle.write(json.dumps(json_serialize(msg)) + '\n')



# takes message, level, other data, and outputs message with appropriate header
HeaderFunction = Callable[[str, int, Any], str]

def md_header_function(msg: str, lvl: int, stream: str|None = None, **kwargs) -> str:
	"""standard header function. will output
	
	- `# {msg}`
		
		for levels in [0, 9]

	- `## {msg}`
		
		for levels in [10, 19], and so on

	- `[{stream}] # {msg}`

		for a non-`None` stream, with level headers as before

	- `!WARNING! [{stream}] {msg}`
		
		for level in [-9, -1]

	- `!!WARNING!! [{stream}] {msg}`
		
		for level in [-19, -10] and so on
	
	"""
	stream_prefix: str = ''
	if stream is not None:
		stream_prefix = f'[{stream}] '

	if lvl >= 0:
		return f"{stream_prefix}#{'#' * (lvl // 10) if lvl else ''} {msg}"
	else:
		exclamation_pts: str = '!' * (abs(lvl) // 10)
		return f"{exclamation_pts}WARNING{exclamation_pts} {stream_prefix}{msg}"


class Logger(SimpleLogger):
	"""logger with more features, including log levels and streams"""
	def __init__(
			self, 
			log_path: str|None = None, 
			log_file: TextIO|None = None,
			timestamp: bool = True,
			default_level: int = 0,
			console_print_threshold: int = 50,
			level_header: HeaderFunction = md_header_function,
			stream_files: None|dict[str, str|bool|TextIO] = None,
			stream_default_levels: None|dict[str, int] = None,
		):
		super().__init__(log_file = log_file, log_path = log_path, timestamp = timestamp)
		self._console_print_threshold = console_print_threshold
		self._default_level = default_level
		self._level_header = level_header
		self._stream_files = stream_files if stream_files else dict()
		self._stream_default_levels = stream_default_levels if stream_default_levels else dict()

		# add the stderr stream
		self._stream_handles: dict[str, TextIO] = {'stderr': sys.stderr}

		for stream_name, stream_handler_info in self._stream_files.items():
			if isinstance(stream_handler_info, str):
				# if its a string, open a file
				self._stream_handles[stream_name] = open(stream_handler_info, 'w', encoding = 'utf-8')
			elif isinstance(stream_handler_info, bool) and stream_handler_info:
				# if its a bool and true, open a file with the same name as the stream (in the current dir)
				self._stream_handles[stream_name] = open(f"{sanitize_fname(stream_name)}.log.jsonl", "w", encoding = 'utf-8')
			else:
				# if its neither, check it has a `.write()` method
				if not hasattr(stream_handler_info, 'write'):
					raise ValueError(f"stream {stream_name} has invalid handler {stream_handler_info}")
				self._stream_handles[stream_name] = stream_handler_info


	def __del__(self):
		self._log_file_handle.flush()
		self._log_file_handle.close()

	def log(
			self, 
			msg: "JSONitem", 
			lvl: int|None = None, 
			stream: str|None = None,
			console_print: bool = False,
		):
		"""logging function
		
		### Parameters:
		 - `msg : JSONitem`   
		   message (usually string or dict) to be logged
		 - `lvl : int | None`   
		   level of message (lower levels are more important)
		   (defaults to `None`)
		 - `console_print : bool`   
		   override `console_print_threshold` setting
		   (defaults to `False`)
		 - `stream : str | None`   
		   whether to log to a stream (defaults to `None`), which logs to the default `None` stream
		   (defaults to `None`)
		"""		

		# set default level
		if lvl is None:
			if stream is None:
				lvl = self._default_level
			else:
				if stream in self._stream_default_levels:
					lvl = self._stream_default_levels[stream]
				else:
					lvl = self._default_level			

		# print to console with formatting
		if (
			console_print 
			or (lvl is None) 
			or (lvl <= self._console_print_threshold)
		):
			print(self._level_header(msg, lvl, stream))
		
		# add metadata
		if not isinstance(msg, dict):
			msg = {"_msg": msg}
		
		if lvl is not None:
			msg["_lvl"] = lvl

		msg["_stream"] = stream

		if self._timestamp:
			msg["_timestamp"] = time.time()
		
		# write
		logfile_msg: str = json.dumps(json_serialize(msg)) + '\n'
		if (stream is None) or (stream not in self._stream_handles):
			# write to the main log file if no stream is specified
			self._log_file_handle.write(logfile_msg)
		else:
			# otherwise, write to the stream
			self._stream_handles[stream].write(logfile_msg)

	def __getattr__(self, stream: str) -> Callable:
		return partial(self.log, stream = stream)

	def __getitem__(self, stream: str):
		return partial(self.log, stream = stream)

	log.__getitem__ = lambda self, *args, **kwargs: self.log(*args, **kwargs)

	def __call__(self, *args, **kwargs):
		return self.log(*args, **kwargs)



class TimerContext:
	"""context manager for timing code"""
	def __init__(self):
		self.start_time: float = None
		self.end_time: float = None
	
	def __enter__(self):
		self.start_time = time.time()
		return self
	
	def __exit__(self, exc_type, exc_val, exc_tb):
		self.end_time = time.time()
		self.elapsed_time = self.end_time - self.start_time
		return False



def _test():
	with TimerContext() as timer:
		time.sleep(1)
	print(timer.elapsed_time)

if __name__ == "__main__":
	_test()







