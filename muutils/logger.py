"""logger with streams & levels, and a timer context manager

- `SimpleLogger` is an extremely simple logger that can write to both console and a file
- `Logger` class handles levels in a slightly different way than default python `logging`,
	and also has "streams" which allow for different sorts of output in the same logger
	this was mostly made with training models in mind and storing both metadata and loss
- `TimerContext` is a context manager that can be used to time the duration of a block of code
"""

from functools import partial
import sys
import json
import time
from typing import TextIO, Any, Callable
from datetime import timedelta


from muutils.jsonlines import jsonl_load
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

def md_header_function(msg: Any, lvl: int, stream: str|None = None, indent_lvl: str = "  ", extra_indent: str = "", **kwargs) -> str:
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

	lvl_div_10: int = lvl // 10

	msg_processed: str
	if isinstance(msg, dict):
		msg_processed = ", ".join([
			f"{k}: {json_serialize(v)}" 
			for k, v in msg.items()
		])
	else:
		msg_processed = json_serialize(msg)

	if lvl >= 0:
		return f"{extra_indent}{indent_lvl * (lvl_div_10 - 1)}{stream_prefix}#{'#' * lvl_div_10 if lvl else ''} {msg_processed}"
	else:
		exclamation_pts: str = '!' * (abs(lvl) // 10)
		return f"{extra_indent}{exclamation_pts}WARNING{exclamation_pts} {stream_prefix} {msg_processed}"


class Logger(SimpleLogger):
	"""logger with more features, including log levels and streams
		
		### Parameters:
		 - `log_path : str | None`   
		   default log file path
		   (defaults to `None`)
		 - `log_file : AnyIO | None`   
		   default log io, should have a `.write()` method (pass only this or `log_path`, not both)
		   (defaults to `None`)
		 - `timestamp : bool`   
		   whether to add timestamps to every log message (under the `_timestamp` key)
		   (defaults to `True`)
		 - `default_level : int`   
		   default log level for streams/messages that don't specify a level
		   (defaults to `0`)
		 - `console_print_threshold : int`   
		   log level at which to print to the console, anything greater will not be printed unless overridden by `console_print`
		   (defaults to `50`)
		 - `level_header : HeaderFunction`   
		   function for formatting log messages when printing to console
		   (defaults to `md_header_function`)
		 - `stream_files : None | dict[str, str | bool | AnyIO]`   
		   where to send each stream. 
		   	- if `True`, will create a new file for each stream with the stream name
			- if `False`, will not write this stream to a file (using `NullIO`)
			- if is `str`, will create a new file with the given path
			- if is `AnyIO`, will use the given io
		   (defaults to `None`)
		 - `stream_default_levels : None | dict[str, int]`   
		   default levels for each stream, will use `default_level` if not specified
		   (defaults to `None`)
		- `keep_last_msg_time : bool`
		   whether to keep the last message time 
		   (defaults to `True`)

		
		### Raises:
		 - `ValueError` : _description_
		"""		
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
			stream_default_contents: None|dict[str, dict[str, Callable[[], Any]]] = None,
			keep_last_msg_time: bool = True,
		):
		# TODO: cleaner to pass a set of `Stream` classes, rather than these multiple dicts?
		
		# init BaseLogger
		super().__init__(log_file = log_file, log_path = log_path, timestamp = timestamp)
		# level-related
		self._console_print_threshold: int = console_print_threshold
		self._default_level: int = default_level
		self._stream_default_levels: dict[str, int] = (
			stream_default_levels 
			if stream_default_levels 
			else dict()
		)

		# print formatting
		self._level_header: HeaderFunction = level_header

		# stream-related
		self._stream_names: set[str] = set([
			*(
				list() 
				if stream_files is None 
				else [stream for stream in stream_files.keys()]
			),
			*(
				list() 
				if stream_default_contents is None 
				else [stream for stream in stream_default_contents.keys()]
			),
			*[stream for stream in self._stream_default_levels.keys()]
		])

		self._stream_files: dict[str, str|bool|AnyIO] = stream_files if stream_files else dict()

		# add the stderr stream
		self._stream_handles: dict[str, AnyIO] = dict(stderr = sys.stderr)

		# stream handles
		for stream_name, stream_handler_info in self._stream_files.items():
			if isinstance(stream_handler_info, str):
				# if its a string, open a file
				self._stream_handles[stream_name] = open(
					stream_handler_info, 
					'w', 
					encoding = 'utf-8',
				)
			elif isinstance(stream_handler_info, bool):
				# if its a bool and true, open a file with the same name as the stream (in the current dir)
				if stream_handler_info:
					self._stream_handles[stream_name] = open(
						f"{sanitize_fname(stream_name)}.log.jsonl", 
						"w", 
						encoding = 'utf-8',
					)
				else:
					self._stream_handles[stream_name] = NullIO()
			else:
				# if its neither, check it has a `.write()` method
				if not hasattr(stream_handler_info, 'write'):
					raise ValueError(f"stream {stream_name} has invalid handler {stream_handler_info}")
				# ignore type check because we know it has a .write() method, 
				# assume the user knows what they're doing
				self._stream_handles[stream_name] = stream_handler_info # type: ignore 

		# default contents
		# TODO: use weakrefs?
		self._stream_default_contents: dict[str, Callable[[], Any]] = (
			stream_default_contents
			if stream_default_contents
			else {
				k : dict()
				for k in self._stream_names
			}
		)
		# augment defaults with timing
		if self._timestamp:
			for s_name, s_default in self._stream_default_contents.items():
				s_default['_timestamp'] = lambda : time.time()

		# timing compares
		self._keep_last_msg_time: bool = keep_last_msg_time
		# TODO: handle per stream?
		self._last_msg_time: float|None = time.time()



	def __del__(self):
		self._log_file_handle.flush()
		self._log_file_handle.close()

		for stream_handler in self._stream_handles.values():
			stream_handler.flush()
			stream_handler.close()

	def log( # type: ignore # yes, the signatures are different here.
			self, 
			msg: JSONitem = None,
			lvl: int|None = None, 
			stream: str|None = None,
			console_print: bool = False,
			extra_indent: str = "",
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

		# set default level to either global or stream-specific default level
		# ========================================
		if lvl is None:
			if stream is None:
				lvl = self._default_level
			else:
				if stream in self._stream_default_levels:
					lvl = self._stream_default_levels[stream]
				else:
					lvl = self._default_level			

		# print to console with formatting
		# ========================================
		_printed: bool = False
		if (
			console_print 
			or (lvl is None) 
			or (lvl <= self._console_print_threshold)
		):
			# add some formatting
			print(self._level_header(
				msg=msg, 
				lvl=lvl, 
				stream=stream,
				extra_indent=extra_indent,
			))

			# store the last message time
			if self._last_msg_time is not None:
				self._last_msg_time = time.time()

			_printed = True

		
		# convert and add data
		# ========================================
		# converting to dict
		msg_dict: dict
		if not isinstance(msg, dict):
			msg_dict = {"_msg": msg}
		else:
			msg_dict = msg
		
		# level+stream metadata
		if lvl is not None:
			msg_dict["_lvl"] = lvl

		msg_dict["_stream"] = stream

		# extra data in kwargs
		if len(kwargs) > 0:
			msg_dict["_kwargs"] = kwargs

		# add default contents (timing, etc)
		msg_dict = {
			**{
				k : v()
				for k,v in self._stream_default_contents.get(stream, dict()).items()
			},
			**msg_dict,
		}
		
		# write
		# ========================================
		logfile_msg: str = json.dumps(json_serialize(msg_dict)) + '\n'
		if (stream is None) or (stream not in self._stream_handles):
			# write to the main log file if no stream is specified
			self._log_file_handle.write(logfile_msg)
		else:
			# otherwise, write to the stream-specific file
			self._stream_handles[stream].write(logfile_msg)
		
		# if it was important enough to print, flush all streams
		if _printed:
			self.flush_all()

	def log_elapsed_last(
			self,
			lvl: int|None = None, 
			stream: str|None = None,
			console_print: bool = True,
			**kwargs,
		) -> float:
		"""logs the time elapsed since the last message was printed to the console (in any stream)"""
		if self._last_msg_time is None:
			raise ValueError("no last message time!")
		else:
			return self.log(
				{"elapsed_time": round(time.time() - self._last_msg_time, 6)}, 
				lvl=(lvl if lvl is not None else self._console_print_threshold),
				stream=stream,
				console_print=console_print,
				**kwargs,
			)

	def flush_all(self):
		"""flush all streams"""

		self._log_file_handle.flush()

		for stream_handle in self._stream_handles.values():
			stream_handle.flush()
			

	def __getattr__(self, stream: str) -> Callable:
		return partial(self.log, stream = stream)

	def __getitem__(self, stream: str):
		return partial(self.log, stream = stream)

	def __call__(self, *args, **kwargs):
		return self.log(*args, **kwargs)







def gather_val(
		file: str, 
		stream: str, 
		keys: tuple[str], 
		allow_skip: bool = True,
	) -> list[JSONitem]:
	"""by default, skips any items in which any of the keys is missing"""
	data: list[JSONitem] = jsonl_load(file)

	output: list[tuple] = list()

	for item in data:
		# select for the stream
		if ("_stream" in item) and (item["_stream"] == stream):
			# select for the keys
			if all(k in item for k in keys):
				output.append(tuple(item[k] for k in keys))
			elif not allow_skip:
				raise ValueError(f"missing keys '{keys = }' in '{item = }'")
	
	return output




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



def filter_time_str(time: str) -> str:
	"""assuming format `hh:mm:ss`, clips off the hours if its 0
	                    01234567"""
	if (len(time) == 7) and (time[0] == "0"):
		return time[3:]	


class ProgressEstimator:
	"""estimates progress and can give a progress bar"""
	def __init__(
			self, 
			n_total: int,
			pbar_fill: str = "█",
			pbar_empty: str = " ",
			pbar_bounds: tuple[str, str] = ("|", "|"),
		):
		self.n_total: int = n_total
		self.starttime: float = time.time()
		self.pbar_fill: str = pbar_fill
		self.pbar_empty: str = pbar_empty
		self.pbar_bounds: tuple[str, str] = pbar_bounds
		self.total_str_len: int = len(str(n_total))

	def get_timing_raw(self, i: int) -> dict[str, float]:
		"""returns dict(elapsed, per_iter, remaining, percent)"""
		elapsed: float = time.time() - self.starttime
		per_iter: float = elapsed / i
		return dict(
			elapsed = elapsed,
			per_iter = per_iter,
			remaining = (self.n_total - i) * per_iter,
			percent = i / self.n_total,
		)

	def get_pbar(
			self,
			i: int, 
			width: int = 30,
		) -> str:
		"""returns a progress bar"""
		percent_filled: float = i / self.n_total
		# round to nearest integer
		n_filled: int = int(round(percent_filled * width))
		return ''.join([
			self.pbar_bounds[0],
			self.pbar_fill * n_filled,
			self.pbar_empty * (width - n_filled),
			self.pbar_bounds[1],
		])

	def get_progress_default(self, i: int) -> str:
		"""returns a progress string"""
		timing_raw: dict[str, float] = self.get_timing_raw(i)

		percent_str: str = str(int(timing_raw['percent'] * 100)).ljust(2)
		iters_str: str = f"{str(i).ljust(self.total_str_len)}/{self.n_total}"
		timing_str: str 
		return f"{percent_str}% {self.get_pbar(i)}"


def _test():
	with TimerContext() as timer:
		time.sleep(1)
	print(timer.elapsed_time)

if __name__ == "__main__":
	_test()

