"""logger module, with a `SimpleLogger` class and a `Logger` class

the `Logger` class handles levels in a slightly different way, and also has "streams"
"""

from functools import partial
import sys
import json
import time
from typing import TextIO, Any, Callable

from muutils.misc import sanitize_fname
from muutils.json_serialize import JSONitem, json_serialize

# pylint: disable=arguments-differ, bad-indentation, trailing-whitespace, trailing-newlines, unnecessary-pass, consider-using-with, use-dict-literal

class NullIO:
	"""null IO class"""
	def __init__(self) -> None:
		pass

	def write(self, msg: str) -> int:
		"""write to nothing! this throws away the message"""
		return len(msg)

	def flush(self) -> None:
		"""flush nothing! this is a no-op"""
		pass

	def close(self) -> None:
		"""close nothing! this is a no-op"""
		pass

AnyIO = TextIO|NullIO


class SimpleLogger:
	"""logs training data to a jsonl file"""
	def __init__(
			self,
			log_path: str|None = None,
			log_file: AnyIO|None = None,
			timestamp: bool = True,
		):

		self._timestamp: bool = timestamp
		self._log_path: str|None = log_path
		
		self._log_file_handle: AnyIO

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
				assert log_path is not None
				self._log_file_handle = open(log_path, "w", encoding="utf-8")
	
	def __del__(self):
		self._log_file_handle.flush()
		self._log_file_handle.close()
		# try:
		# 	self._log_file_handle.flush()
		# except Exception as e:
		# 	print(f"[logger_internal] # failed to flush log file: {e}", sys.stderr)
		# try:
		# 	self._log_file_handle.close()
		# except Exception as e:
		# 	print(f"[logger_internal] # failed to close log file: {e}", sys.stderr)

	def log(self, msg: JSONitem, console_print: bool = False, **kwargs):
		"""log a message to the log file, and optionally to the console"""
		if console_print:
			print(msg)
		
		if not isinstance(msg, dict):
			msg = {"_msg": msg}
		
		if self._timestamp:
			msg["_timestamp"] = time.time()

		if len(kwargs) > 0:
			msg["_kwargs"] = kwargs
		
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
			log_file: AnyIO|None = None,
			timestamp: bool = True,
			default_level: int = 0,
			console_print_threshold: int = 50,
			level_header: HeaderFunction = md_header_function,
			stream_files: None|dict[str, str|bool|AnyIO] = None,
			stream_default_levels: None|dict[str, int] = None,
		):
		super().__init__(log_file = log_file, log_path = log_path, timestamp = timestamp)
		self._console_print_threshold: int = console_print_threshold
		self._default_level: int = default_level
		self._level_header: HeaderFunction = level_header
		self._stream_files: dict[str, str|bool|AnyIO] = stream_files if stream_files else dict()
		self._stream_default_levels: dict[str, int] = (
			stream_default_levels 
			if stream_default_levels 
			else dict()
		)

		# add the stderr stream
		self._stream_handles: dict[str, AnyIO] = {'stderr': sys.stderr}

		for stream_name, stream_handler_info in self._stream_files.items():
			if isinstance(stream_handler_info, str):
				# if its a string, open a file
				self._stream_handles[stream_name] = open(
					stream_handler_info, 
					'w', 
					encoding = 'utf-8',
				)
			elif isinstance(stream_handler_info, bool) and stream_handler_info:
				# if its a bool and true, open a file with the same name as the stream (in the current dir)
				self._stream_handles[stream_name] = open(
					f"{sanitize_fname(stream_name)}.log.jsonl", 
					"w", 
					encoding = 'utf-8',
				)
			else:
				# if its neither, check it has a `.write()` method
				if not hasattr(stream_handler_info, 'write'):
					raise ValueError(f"stream {stream_name} has invalid handler {stream_handler_info}")
				# ignore type check because we know it has a .write() method, 
				# assume the user knows what they're doing
				self._stream_handles[stream_name] = stream_handler_info # type: ignore 


	def __del__(self):
		self._log_file_handle.flush()
		self._log_file_handle.close()

		for stream_handler in self._stream_handles.values():
			stream_handler.flush()
			stream_handler.close()

	def log( # type: ignore # yes, the signatures are different here.
			self, 
			msg: JSONitem, 
			lvl: int|None = None, 
			stream: str|None = None,
			console_print: bool = False,
			**kwargs,
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
			print(self._level_header(
				json.dumps(json_serialize(msg)), 
				lvl, 
				stream,
			))
		
		# add metadata
		if not isinstance(msg, dict):
			msg = {"_msg": msg}
		
		if lvl is not None:
			msg["_lvl"] = lvl

		msg["_stream"] = stream
	
		if len(kwargs) > 0:
			msg["_kwargs"] = kwargs

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

	def __call__(self, *args, **kwargs):
		return self.log(*args, **kwargs)



class TimerContext:
	"""context manager for timing code"""
	def __init__(self):
		self.start_time: float = None
		self.end_time: float = None
		self.elapsed_time: float = None
	
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

