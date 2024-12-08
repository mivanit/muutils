import inspect
import sys
from copy import deepcopy
from dataclasses import dataclass
from typing import (
    Annotated,
    Any,
    Callable,
    Optional,
    Union,
    _SpecialForm,
    _type_check,
    get_type_hints,
)


class Description(str):
    pass


class ArgProcessor:
    def __init__(self, func) -> None:
        self.func = func

    def __call__(self, *args, **kwargs) -> Any:
        return self.func(*args, **kwargs)


# Description: Callable[[str], type] = lambda x : NewType(x, str)(x)


class NoValue:
    pass


@_SpecialForm
def NoValueOptional(self, parameters):
    arg = _type_check(parameters, f"{self} requires a single type.")
    return Union[arg, NoValue]


@dataclass
class ArgumentSignature:
    """signature and metadata about a function argument"""

    name: str
    keyword_only: bool
    positional_only: bool
    type: NoValueOptional[type] = NoValue
    default: NoValueOptional[Any] = NoValue
    description: Optional[str] = None
    processor: NoValueOptional[ArgProcessor] = NoValue

    def to_docstring_item(self) -> str:
        desc_processed: str = (
            self.description.replace("\n", "\n\t")
            if self.description is not None
            else ""
        )
        if not isinstance(self.default, NoValue):
            return f" - `{self.name} : {self.type.__name__}` {desc_processed} "
        else:
            return f" - `{self.name} : {self.type.__name__} = {self.default}` {desc_processed} "


@dataclass
class FunctionSignature:
    """signature and metadata about a function"""

    name: str
    doc: str
    args: list[ArgumentSignature]
    return_type: type

    @property
    def args_positional(self) -> list[ArgumentSignature]:
        return [a for a in self.args if not a.keyword_only]

    @property
    def args_pos_only(self) -> list[ArgumentSignature]:
        return [x for x in self.args if x.positional_only]

    @property
    def args_kw_only(self) -> list[ArgumentSignature]:
        return [x for x in self.args if x.keyword_only]

    def to_docstring(self) -> str:
        return "\n".join(
            [
                self.doc or "",
                "# Arguments:",
                "\n".join([x.to_docstring_item() for x in self.args]),
                "# Returns:",
                f"return : {self.return_type}",
            ]
        )


def process_signature(func: Callable) -> None:
    argspec: inspect.FullArgSpec = inspect.getfullargspec(func)

    # print(json.dumps(json_serialize(argspec), indent=4))
    args_all_names: list[str] = argspec.args
    if argspec.varargs is not None:
        args_all_names.append("*" + argspec.varargs)
    args_all_names.extend(argspec.kwonlyargs)
    if argspec.varkw is not None:
        args_all_names.append("**" + argspec.varkw)

    # get the base type signatures
    # ==============================
    args_types: dict[str, type] = get_type_hints(func)

    # get default values
    # ==============================
    args_defaults: dict[str, Any] = dict()
    # chop the values without default values from `argspec.args`
    ordered_args_with_defaults: list[str] = deepcopy(
        argspec.args[: -len(argspec.defaults)]
    )
    # zip them up with defaults and add them to dict
    for arg, default in zip(ordered_args_with_defaults, argspec.defaults):
        args_defaults[arg] = default
    # add keyword only args
    args_defaults.update(
        {
            arg: default
            for arg, default in zip(argspec.kwonlyargs, argspec.kwonlydefaults)
        }
    )

    # get the annotations
    # ==============================
    args_annotations: dict[str, tuple] = {
        k: v.__metadata__
        for k, v in get_type_hints(func, include_extras=True).items()
        if hasattr(v, "__metadata__")
    }

    # get the descriptions, by getting all strings in the annotation
    # ==============================
    args_descriptions: dict[str, Description] = dict()
    for k, v in args_annotations.items():
        desc_items: list[str] = [x for x in v if isinstance(x, (str, Description))]
        # if anything found
        if len(desc_items) > 0:
            args_descriptions[k] = Description("\n".join(desc_items))

    # get the processors, by getting only things marked as `ArgProcessor`
    # ==============================
    args_processors: dict[str, ArgProcessor] = dict()
    for k, v in args_annotations.items():
        if isinstance(v, ArgProcessor):
            args_processors[k] = v

    args: list[ArgumentSignature] = [
        ArgumentSignature(
            name=arg,
            keyword_only=arg in argspec.kwonlyargs,
            positional_only=False,
            type=args_types.get(arg, Any),
            default=args_defaults.get(arg, NoValue),
            description=args_descriptions.get(arg, None),
            processor=args_processors.get(arg, NoValue),
        )
        for arg in argspec.args
    ]

    return FunctionSignature(
        name=func.__name__,
        doc=func.__doc__,
        args=args,
        return_type=func.__annotations__["return"],
    )


# use functools.wraps
def docstring_updater(func: Callable) -> Callable:
    signature: FunctionSignature = process_signature(func)
    func.__doc__ = signature.to_docstring()
    return func


@docstring_updater
def main(
    dumb_file: str,
    /,
    no_default: Annotated[str, "this has no deafault", "lol"],
    use_erdos: Annotated[
        bool,
        "asdkljasdkljsad",
        ArgProcessor(
            lambda x: bool(x.lower() == "true") if isinstance(x, str) else bool(x)
        ),
    ] = False,
    # index_file: str = 'example_data/example_index.index',
    index_file: str = "/mnt/ssd-0/lichess/preprocessed/25M_high_elo.index",
    output_folder: str = "example_data",
    num_games: int = 100,
    *,
    keyword_only_arg: str = "default string",
) -> bool:
    """base docstring"""

    pass


@docstring_updater
def main_other(
    dumb_file: str,
    /,
    use_erdos: bool = False,
    *args,
    keyword_only_arg: str = "default string",
    **kwargs,
) -> bool:
    pass


@docstring_updater
def main_third(
    another_dumb: str,
    dumb_file: str = "default value for no-keyword arg",
    n_things: int = 10,
    /,
    use_erdos: Annotated[
        bool,
        "asdkljasdkljsad",
        ArgProcessor(
            lambda x: bool(x.lower() == "true") if isinstance(x, str) else bool(x)
        ),
    ] = False,
    # index_file: str = 'example_data/example_index.index',
    index_file: str = "/mnt/ssd-0/lichess/preprocessed/25M_high_elo.index",
    output_folder: str = "example_data",
    num_games: int = 100,
    *,
    keyword_only_arg: str = "default string",
) -> bool:
    pass


JSONData = Union[bool, int, float, str, list, dict]


def substring_mask(data: str, quote_symbol: str = "'") -> list[bool]:
    """iterate over a string, returning a list of bools on whether each character is within quotes"""

    output: list[bool] = list()

    # start by assuming we're not in a string
    in_string_current: bool = False
    in_string_next: bool = False
    is_escaped: bool = False

    # iterate over the string
    for i, c in enumerate(data):
        # handle escape chars
        if is_escaped:
            is_escaped = False
        elif c == "\\":
            is_escaped = True
        elif not in_string_current and c == quote_symbol:
            # if we're not in a string and we see a quote, we're in a string
            in_string_current = True
            in_string_next = True
        elif in_string_current and c == quote_symbol:
            # if we're in a string and we see a quote, we're no longer in a string
            in_string_current = True
            in_string_next = False
        elif not in_string_current:
            # if we're not in a string, add the character to the output
            pass
        else:
            # if we're in a string, ignore the character
            pass

        print(i, c, "\t", in_string_current)
        output.append(in_string_current)

        in_string_current = in_string_next

    return output


def split_Lmask(data: str, mask: bool) -> tuple[list[str], list[bool]]:
    """given a mask, split the data into runs of strings which either are or are not masked"""

    output_strings: list[str] = list()
    output_masks: list[bool] = list()

    prev_mask: Optional[bool] = None

    for c, m in zip(data, mask):
        if prev_mask is None:
            # if none, we are at the start of a string. start a new run
            prev_mask = m
            output_masks.append(m)
            output_strings.append(c)

        elif m == prev_mask:
            # continue the last run
            assert m == output_masks[-1]
            output_strings[-1] += c

        else:
            # start a new run
            output_masks.append(m)
            output_strings.append(c)
            prev_mask = m

    return output_strings, output_masks


def invert_mask(mask: list[bool]) -> list[bool]:
    """invert a mask"""
    return [not x for x in mask]


def display_str_with_mask(data: str) -> None:
    mask = substring_mask(data)
    print(data)
    print("".join(["*" if x else " " for x in mask]))


def apply_replace_within_Lmask(
    data: list[str],
    mask: list[bool],
    replace_from: str,
    replace_to: str,
) -> str:
    """apply a replace to a string, but only within a mask"""

    output: list[str] = list()

    for c, m in zip(data, mask):
        if m:
            output.append(c.replace(replace_from, replace_to))
        else:
            output.append(c)

    return output


def argv_json_preprocessor(data: str) -> str:
    pass


def custom_json_loader(data: str) -> JSONData:
    # first, isolate all indices

    pass


if __name__ == "__main__":
    data = " ".join(sys.argv)
    display_str_with_mask(data)
    print(split_into_runs(data, substring_mask(data)))


# process_signature(main)
# process_signature(main_other)
# process_signature(main_third)


# print(main.__name__)
# print(main.__doc__)
# print('\n\n\n')

# print(main_other.__name__)
# print(main_other.__doc__)
# print('\n\n\n')

# print(main_third.__name__)
# print(main_third.__doc__)
# print('\n\n\n')
