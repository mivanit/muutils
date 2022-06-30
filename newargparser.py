from typing import (
	Callable, NamedTuple, get_type_hints, Dict, List, Any, Union, Annotated, NewType, TypeVar, Optional, _SpecialForm, _type_check
)
import inspect
import json
import sys
from copy import deepcopy
from dataclasses import dataclass, field
import functools

from json_serialize import json_serialize



class Description(str): pass
class ArgProcessor:
	def __init__(self, func) -> None:
		self.func = func
	
	def __call__(self, *args, **kwargs) -> Any:
		return self.func(*args, **kwargs)

# Description: Callable[[str], type] = lambda x : NewType(x, str)(x)

class NoValue: pass

@_SpecialForm
def NoValueOptional(self, parameters):
    arg = _type_check(parameters, f"{self} requires a single type.")
    return Union[arg, NoValue]

@dataclass
class ArgumentSignature:
	"""signature and metadata about a function argument"""
	name : str
	keyword_only : bool
	positional_only : bool
	type : NoValueOptional[type] = NoValue
	default : NoValueOptional[Any] = NoValue
	description : Optional[str] = None
	processor : NoValueOptional[ArgProcessor] = NoValue

	def to_docstring_item(self) -> str:
		desc_processed: str = self.description.replace('\n', '\n\t') if self.description is not None else ''
		if not isinstance(self.default, NoValue):
			return f" - `{self.name} : {self.type.__name__}` {desc_processed} "
		else:
			return f" - `{self.name} : {self.type.__name__} = {self.default}` {desc_processed} "

@dataclass
class FunctionSignature:
	"""signature and metadata about a function"""
	name : str
	doc : str
	args : List[ArgumentSignature]
	return_type : type

	@property
	def args_positional(self) -> List[ArgumentSignature]:
		return [a for a in self.args if not a.keyword_only]
	
	@property
	def args_pos_only(self) -> List[ArgumentSignature]:
		return [x for x in self.args if x.positional_only]
	
	@property
	def args_kw_only(self) -> List[ArgumentSignature]:
		return [x for x in self.args if x.keyword_only]


	def to_docstring(self) -> str:
		return '\n'.join([
			self.doc or '',
			'# Arguments:',
			'\n'.join([x.to_docstring_item() for x in self.args]),
			'# Returns:',
			f'return : {self.return_type}',
		])




def process_signature(func : Callable) -> None:

	argspec: inspect.FullArgSpec = inspect.getfullargspec(func)

	# print(json.dumps(json_serialize(argspec), indent=4))
	args_all_names: List[str] = argspec.args
	if argspec.varargs is not None:
		args_all_names.append('*' + argspec.varargs)
	args_all_names.extend(argspec.kwonlyargs)
	if argspec.varkw is not None:
		args_all_names.append('**' + argspec.varkw)
	
	# get the base type signatures
	# ==============================
	args_types : Dict[str,type] = get_type_hints(func)

	# get default values
	# ==============================
	args_defaults : Dict[str, Any] = dict()
	# chop the values without default values from `argspec.args`
	ordered_args_with_defaults : List[str] = deepcopy(argspec.args[:-len(argspec.defaults)])
	# zip them up with defaults and add them to dict
	for arg, default in zip(ordered_args_with_defaults, argspec.defaults):
		args_defaults[arg] = default
	# add keyword only args
	args_defaults.update({
		arg : default
		for arg, default in zip(argspec.kwonlyargs, argspec.kwonlydefaults)
	})

	
	# get the annotations
	# ==============================
	args_annotations : Dict[str,tuple] = {
		k : v.__metadata__
		for k,v in get_type_hints(func, include_extras=True).items()
		if hasattr(v, '__metadata__')
	}

	# get the descriptions, by getting all strings in the annotation
	# ==============================
	args_descriptions : Dict[str, Description] = dict()
	for k,v in args_annotations.items():
		desc_items : List[str] = [
			x
			for x in v
			if isinstance(x, (str, Description))
		]
		# if anything found
		if len(desc_items) > 0:
			args_descriptions[k] = Description('\n'.join(desc_items))

	# get the processors, by getting only things marked as `ArgProcessor`
	# ==============================
	args_processors : Dict[str,ArgProcessor] = dict()
	for k,v in args_annotations.items():
		if isinstance(v, ArgProcessor):
			args_processors[k] = v


	args: List[ArgumentSignature] = [
		ArgumentSignature(
			name = arg,
			keyword_only = arg in argspec.kwonlyargs,
			positional_only = False,
			type = args_types.get(arg, Any),
			default = args_defaults.get(arg, NoValue),
			description = args_descriptions.get(arg, None),
			processor = args_processors.get(arg, NoValue),
		)
		for arg in argspec.args
	]
	
	return FunctionSignature(
		name=func.__name__,
		doc=func.__doc__,
		args=args,
		return_type=func.__annotations__['return'],
	)



# use functools.wraps
def docstring_updater(func : Callable) -> Callable:
	signature: FunctionSignature = process_signature(func)
	func.__doc__ = signature.to_docstring()
	return func


@docstring_updater
def main(
        dumb_file : str,
        /,
		no_default : Annotated[str, 'this has no deafault', 'lol'],
        use_erdos: Annotated[bool, 
			'asdkljasdkljsad',
			ArgProcessor(lambda x: 
				bool(x.lower() == 'true')
				if isinstance(x,str)
				else bool(x)
			),
		] = False,
        # index_file: str = 'example_data/example_index.index',
        index_file: str = "/mnt/ssd-0/lichess/preprocessed/25M_high_elo.index",
        output_folder: str = "example_data",
        num_games: int = 100,
        *,
        keyword_only_arg : str = "default string",
    ) -> bool:
	"""base docstring"""

	pass


@docstring_updater
def main_other(
        dumb_file : str,
        /,
		use_erdos: bool = False,
        *args,
		keyword_only_arg : str = "default string",
        **kwargs,
    ) -> bool:

	pass


@docstring_updater
def main_third(
		another_dumb : str,
        dumb_file : str = 'default value for no-keyword arg',
		n_things : int = 10,
        /,
        use_erdos: Annotated[bool, 
			'asdkljasdkljsad',
			ArgProcessor(lambda x: 
				bool(x.lower() == 'true')
				if isinstance(x,str)
				else bool(x)
			),
		] = False,
        # index_file: str = 'example_data/example_index.index',
        index_file: str = "/mnt/ssd-0/lichess/preprocessed/25M_high_elo.index",
        output_folder: str = "example_data",
        num_games: int = 100,
        *,
        keyword_only_arg : str = "default string",
    ) -> bool:

	pass

# process_signature(main)	
# process_signature(main_other)
# process_signature(main_third)


print(main.__name__)
print(main.__doc__)
print('\n\n\n')

print(main_other.__name__)
print(main_other.__doc__)
print('\n\n\n')

print(main_third.__name__)
print(main_third.__doc__)
print('\n\n\n')
