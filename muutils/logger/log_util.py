from muutils.json_serialize import JSONitem, json_serialize
from muutils.jsonlines import jsonl_load

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

