"""logger with streams & levels, and a timer context manager

- `SimpleLogger` is an extremely simple logger that can write to both console and a file
- `Logger` class handles levels in a slightly different way than default python `logging`,
	and also has "streams" which allow for different sorts of output in the same logger
	this was mostly made with training models in mind and storing both metadata and loss
- `TimerContext` is a context manager that can be used to time the duration of a block of code
"""

from dataclasses import dataclass, field
from functools import partial
import sys
import json
import time
from typing import Sequence, TextIO, Any, Callable
from datetime import timedelta
from pip._internal.operations.freeze import freeze


from muutils.jsonlines import jsonl_load
from muutils.misc import sanitize_fname
from muutils.json_serialize import JSONitem, json_serialize

# pylint: disable=arguments-differ, bad-indentation, trailing-whitespace, trailing-newlines, unnecessary-pass, consider-using-with, use-dict-literal




class SysInfo:
	"""getters for various information about the system"""
	@staticmethod
	def get_python() -> dict:
		"""details about python version"""
		ver_tup = sys.version_info
		return {
			"version": sys.version,
			"major": ver_tup[0],
			"minor": ver_tup[1],
			"micro": ver_tup[2],
			"releaselevel": ver_tup[3],
			"serial": ver_tup[4],
		}

	@staticmethod
	def get_pip() -> dict:
		"""installed packages info"""
		pckgs: list[str] = [x for x in freeze(local_only=True)]
		return {
			"n_packages": len(pckgs),
			"packages": pckgs,
		}

	@staticmethod
	def get_pytorch() -> dict:
		"""pytorch and cuda information"""
		try:
			import torch
		except Exception as e:
			return {
				"importable": False,
				"error": str(e),
			}

		output: dict = {"importable": True}

		output["torch.__version__"] = torch.__version__
		output["torch.version.cuda"] = torch.version.cuda
		output["torch.version.debug"] = torch.version.debug
		output["torch.version.git_version"] = torch.version.git_version
		output["torch.version.hip"] = torch.version.hip
		output["torch.cuda.is_available()"] = torch.cuda.is_available()
		output["torch.cuda.device_count()"] = torch.cuda.device_count()
		output["torch.cuda.is_initialized()"] = torch.cuda.is_initialized()

		if torch.cuda.is_available():
			import os
			cuda_version_nvcc : str = os.popen("nvcc --version").read()
			output["nvcc --version"] = cuda_version_nvcc.split('\n')

			if torch.cuda.device_count() > 0:
				n_devices: int = torch.cuda.device_count()
				output["torch.cuda.current_device()"] = torch.cuda.current_device()
				output["torch devices"] = []
				for current_device in range(n_devices):
					try:
						# print(f'checking current device {current_device} of {torch.cuda.device_count()} devices')
						# print(f'\tdevice {current_device}')
						# dev_prop = torch.cuda.get_device_properties(torch.device(0))
						# print(f'\t    name:                   {dev_prop.name}')
						# print(f'\t    version:                {dev_prop.major}.{dev_prop.minor}')
						# print(f'\t    total_memory:           {dev_prop.total_memory}')
						# print(f'\t    multi_processor_count:  {dev_prop.multi_processor_count}')
						# print(f'\t')
						dev_prop = torch.cuda.get_device_properties(current_device)
						output["torch devices"].append({
							"device": current_device,
							"name": dev_prop.name,
							"version": {f"major": dev_prop.major, "minor": dev_prop.minor},
							"total_memory": dev_prop.total_memory,
							"multi_processor_count": dev_prop.multi_processor_count,
						})
					except Exception as e:
						output["torch devices"].append({
							"device": current_device,
							"error": str(e),
						})
		return output

	@staticmethod
	def get_platform() -> dict:
		import platform
		items = [
			"platform",
			"machine",
			"processor",
			"system",
			"version",
			"architecture",
			"uname",
			"node",
			"python_branch",
			"python_build",
			"python_compiler",
			"python_implementation",
		]

		return {
			x: getattr(platform, x)()
			for x in items
		}

	@classmethod
	def get_all(cls) -> dict:
		return {
			"python": cls.get_python(),
			"pip": cls.get_pip(),
			"pytorch": cls.get_pytorch(),
			"platform": cls.get_platform(),
		}

if __name__ == "__main__":
	print(json.dumps(json_serialize(SysInfo.get_all()), indent=2))




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
			self._log_file_handle = sys.stdout

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


@dataclass
class LoggingStream:
	"""properties of a logging stream
	
	- `name: str` name of the stream
	- `aliases: set[str]` aliases for the stream
		(calls to these names will be redirected to this stream. duplicate alises will result in errors)
		TODO: perhaps duplicate alises should result in duplicate writes?
	- `file: str|bool|AnyIO|None` file to write to
		- if `None`, will write to standard log
		- if `True`, will write to `name + ".log"`
		- if `False` will "write" to `NullIO` (throw it away)
		- if a string, will write to that file
		- if a fileIO type object, will write to that object
	- `default_level: int|None` default level for this stream
	- `default_contents: dict[str, Callable[[], Any]]` default contents for this stream
	- `last_msg: tuple[float, Any]|None` last message written to this stream (timestamp, message)
	"""
	name: str
	aliases: set[str] = field(default_factory=tuple)
	file: str|bool|AnyIO|None = None
	default_level: int|None = None
	default_contents: dict[str, Callable[[], Any]] = field(default_factory=dict)
	
	# TODO: implement last-message caching
	# last_msg: tuple[float, Any]|None = None 

	def __post_init__(self):
		self.aliases = set(self.aliases)
		if any(x.startswith('_') for x in self.aliases):
			raise ValueError("stream names or aliases cannot start with an underscore, sorry")
		self.aliases.add(self.name)
		self.default_contents["_timestamp"] = time.time
		self.default_contents["_stream"] = lambda: self.name

	
	def __str__(self) -> str:
		return f"LoggingStream()"


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
			default_level: int = 0,
			console_print_threshold: int = 50,
			level_header: HeaderFunction = md_header_function,
			streams: dict[str, LoggingStream]|Sequence[LoggingStream] = (),
			keep_last_msg_time: bool = True,
			# junk args
			timestamp: bool = True,
			**kwargs,
		):

		# junk arg checking
		# ==================================================
		if len(kwargs) > 0:
			raise ValueError(f"unrecognized kwargs: {kwargs}")
		
		if not timestamp:
			raise ValueError("timestamp must be True -- why would you not want timestamps?")
		
		# basic setup
		# ==================================================
		# init BaseLogger
		super().__init__(log_file = log_file, log_path = log_path, timestamp = timestamp)

		# level-related
		self._console_print_threshold: int = console_print_threshold
		self._default_level: int = default_level

		# set up streams
		self._streams: dict[str, LoggingStream] = streams if isinstance(streams, dict) else {s.name: s for s in streams}
		# default error stream
		if "error" not in self._streams:
			self._streams["error"] = LoggingStream("error", aliases = {"err",})

		# check alias duplicates
		alias_set: set[str] = set()
		for stream in self._streams.values():
			for alias in stream.aliases:
				if alias in alias_set:
					raise ValueError(f"alias {alias} is already in use")
				alias_set.add(alias)

		# add aliases
		for stream in tuple(self._streams.values()):
			for alias in stream.aliases:
				if alias not in self._streams:
					self._streams[alias] = stream

		# print formatting
		self._level_header: HeaderFunction = level_header

		print({k : str(v) for k,v in self._streams.items()})

		# stream handles
		# ==================================================
		self._stream_handles: dict[str, AnyIO] = dict()
		for stream_alias, stream_obj in self._streams.items():
			handler: AnyIO|None = self.process_handler(stream_obj)
			if handler is not None:
				self._stream_handles[stream_alias] = handler

		# timing
		# ==================================================
		# timing compares
		self._keep_last_msg_time: bool = keep_last_msg_time
		# TODO: handle per stream?
		self._last_msg_time: float|None = time.time()

	@staticmethod
	def process_handler(stream_obj: LoggingStream) -> AnyIO:
		if stream_obj.file is None:
			return None
		elif isinstance(stream_obj.file, str):
			# if its a string, open a file
			return open(
				stream_obj.file, 
				'w', 
				encoding = 'utf-8',
			)
		elif isinstance(stream_obj.file, bool):
			# if its a bool and true, open a file with the same name as the stream (in the current dir)
			if stream_obj.file:
				return open(
					f"{sanitize_fname(stream_obj.name)}.log.jsonl", 
					"w", 
					encoding = 'utf-8',
				)
			else:
				return NullIO()
		else:
			# if its neither, check it has `.write()` and `.flush()` methods
			if (
					(not hasattr(stream_obj.file, 'write')
					or (not callable(stream_obj.file.write))
					or (not hasattr(stream_obj.file, 'flush'))
					or (not callable(stream_obj.file.flush)))
					or (not hasattr(stream_obj.file, 'close'))
					or (not callable(stream_obj.file.close))
				):
				raise ValueError(f"stream {stream_obj.name} has invalid handler {stream_obj.file}")
			# ignore type check because we know it has a .write() method, 
			# assume the user knows what they're doing
			return stream_obj.file # type: ignore 

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

		# add to known stream names if not present
		if stream not in self._streams:
			self._streams[stream] = LoggingStream(stream)

		# set default level to either global or stream-specific default level
		# ========================================
		if lvl is None:
			if stream is None:
				lvl = self._default_level
			else:
				if self._streams[stream].default_level is not None:
					lvl = self._streams[stream].default_level
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

		# msg_dict["_stream"] = stream # moved to LoggingStream

		# extra data in kwargs
		if len(kwargs) > 0:
			msg_dict["_kwargs"] = kwargs

		# add default contents (timing, etc)
		msg_dict = {
			**{
				k : v()
				for k,v in self._streams[stream].default_contents.items()
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
		if stream.startswith("_"):
			raise AttributeError(f"invalid stream name {stream} (no underscores)")
		return partial(self.log, stream = stream)

	def __getitem__(self, stream: str):
		return partial(self.log, stream = stream)

	def __call__(self, *args, **kwargs):
		return self.log(*args, **kwargs)


def get_any_from_stream(stream: list[dict], key: str) -> None:
	"""get the first value of a key from a stream. errors if not found"""
	for msg in stream:
		if key in msg:
			return msg[key]

	raise KeyError(f"key '{key}' not found in stream")


def gather_stream(
		file: str, 
		stream: str, 
	) -> list[JSONitem]:
	data: list[JSONitem] = jsonl_load(file)

	output: list[tuple] = list()

	for item in data:
		# select for the stream
		if ("_stream" in item) and (item["_stream"] == stream):
			output.append(item)
	return output

def gather_val(
		file: str, 
		stream: str, 
		keys: tuple[str], 
		allow_skip: bool = True,
	) -> list[JSONitem]:
	"""gather specific keys from a specific stream in a log file"""
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


# def _test():
# 	with TimerContext() as timer:
# 		time.sleep(1)
# 	print(timer.elapsed_time)

# if __name__ == "__main__":
# 	_test()

