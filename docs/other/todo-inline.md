 # Inline TODOs


# HACK

## [`muutils/json_serialize/serializable_dataclass.py`](/muutils/json_serialize/serializable_dataclass.py)

- ExceptionGroup not supported in py < 3.11, so get a random exception from the dict  
  local link: [`/muutils/json_serialize/serializable_dataclass.py#296`](/muutils/json_serialize/serializable_dataclass.py#296) 
  | view on GitHub: [muutils/json_serialize/serializable_dataclass.py#L296](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_dataclass.py#L296)
  | [Make Issue](https://github.com/mivanit/muutils/issues/new?title=ExceptionGroup%20not%20supported%20in%20py%20%3C%203.11%2C%20so%20get%20a%20random%20exception%20from%20the%20dict&body=%23%20source%0A%0A%5B%60muutils%2Fjson_serialize%2Fserializable_dataclass.py%23L296%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fmuutils%2Fblob%2Fmain%2Fmuutils%2Fjson_serialize%2Fserializable_dataclass.py%23L296%29%0A%0A%23%20context%0A%60%60%60python%0A%20%20%20%20%20%20%20%20on_typecheck_error.process%28%0A%20%20%20%20%20%20%20%20%20%20%20%20f%22Exceptions%20while%20validating%20types%20of%20fields%20on%20%7Bself.__class__.__name__%7D%3A%20%7B%5Bx.name%20for%20x%20in%20cls_fields%5D%7D%22%0A%20%20%20%20%20%20%20%20%20%20%20%20%2B%20%22%5Cn%5Ct%22%0A%20%20%20%20%20%20%20%20%20%20%20%20%2B%20%22%5Cn%5Ct%22.join%28%5Bf%22%7Bk%7D%3A%5Ct%7Bv%7D%22%20for%20k%2C%20v%20in%20exceptions.items%28%29%5D%29%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20except_cls%3DValueError%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%23%20HACK%3A%20ExceptionGroup%20not%20supported%20in%20py%20%3C%203.11%2C%20so%20get%20a%20random%20exception%20from%20the%20dict%0A%20%20%20%20%20%20%20%20%20%20%20%20except_from%3Dlist%28exceptions.values%28%29%29%5B0%5D%2C%0A%20%20%20%20%20%20%20%20%29%0A%0A%20%20%20%20return%20results%0A%60%60%60&labels=enhancement)

  ```python
on_typecheck_error.process(
            f"Exceptions while validating types of fields on {self.__class__.__name__}: {[x.name for x in cls_fields]}"
            + "\n\t"
            + "\n\t".join([f"{k}:\t{v}" for k, v in exceptions.items()]),
            except_cls=ValueError,
            # HACK: ExceptionGroup not supported in py < 3.11, so get a random exception from the dict
            except_from=list(exceptions.values())[0],
        )

    return results
  ```


- this is kind of ugly, but it fixes a lot of issues for when we do recursive loading with ZANJ  
  local link: [`/muutils/json_serialize/serializable_dataclass.py#799`](/muutils/json_serialize/serializable_dataclass.py#799) 
  | view on GitHub: [muutils/json_serialize/serializable_dataclass.py#L799](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_dataclass.py#L799)
  | [Make Issue](https://github.com/mivanit/muutils/issues/new?title=this%20is%20kind%20of%20ugly%2C%20but%20it%20fixes%20a%20lot%20of%20issues%20for%20when%20we%20do%20recursive%20loading%20with%20ZANJ&body=%23%20source%0A%0A%5B%60muutils%2Fjson_serialize%2Fserializable_dataclass.py%23L799%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fmuutils%2Fblob%2Fmain%2Fmuutils%2Fjson_serialize%2Fserializable_dataclass.py%23L799%29%0A%0A%23%20context%0A%60%60%60python%0A%20%20%20%20%20%20%20%20%23%20done%20locally%20since%20it%20depends%20on%20args%20to%20the%20decorator%0A%20%20%20%20%20%20%20%20%23%20%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%0A%20%20%20%20%20%20%20%20%23%20mypy%20thinks%20this%20isnt%20a%20classmethod%0A%20%20%20%20%20%20%20%20%40classmethod%20%20%23%20type%3A%20ignore%5Bmisc%5D%0A%20%20%20%20%20%20%20%20def%20load%28cls%2C%20data%3A%20dict%5Bstr%2C%20Any%5D%20%7C%20T%29%20-%3E%20Type%5BT%5D%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20%23%20HACK%3A%20this%20is%20kind%20of%20ugly%2C%20but%20it%20fixes%20a%20lot%20of%20issues%20for%20when%20we%20do%20recursive%20loading%20with%20ZANJ%0A%20%20%20%20%20%20%20%20%20%20%20%20if%20isinstance%28data%2C%20cls%29%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20return%20data%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20assert%20isinstance%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20data%2C%20typing.Mapping%0A%60%60%60&labels=enhancement)

  ```python
# done locally since it depends on args to the decorator
        # ======================================================================
        # mypy thinks this isnt a classmethod
        @classmethod  # type: ignore[misc]
        def load(cls, data: dict[str, Any] | T) -> Type[T]:
            # HACK: this is kind of ugly, but it fixes a lot of issues for when we do recursive loading with ZANJ
            if isinstance(data, cls):
                return data

            assert isinstance(
                data, typing.Mapping
  ```





# NOTE

## [`muutils/dictmagic.py`](/muutils/dictmagic.py)

- this process is not meant to be reversible, and is intended for pretty-printing and visualization purposes  
  local link: [`/muutils/dictmagic.py#334`](/muutils/dictmagic.py#334) 
  | view on GitHub: [muutils/dictmagic.py#L334](https://github.com/mivanit/muutils/blob/main/muutils/dictmagic.py#L334)
  | [Make Issue](https://github.com/mivanit/muutils/issues/new?title=this%20process%20is%20not%20meant%20to%20be%20reversible%2C%20and%20is%20intended%20for%20pretty-printing%20and%20visualization%20purposes&body=%23%20source%0A%0A%5B%60muutils%2Fdictmagic.py%23L334%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fmuutils%2Fblob%2Fmain%2Fmuutils%2Fdictmagic.py%23L334%29%0A%0A%23%20context%0A%60%60%60python%0A%29%20-%3E%20dict%5Bstr%2C%20Any%5D%3A%0A%20%20%20%20%22%22%22condense%20a%20nested%20dict%2C%20by%20condensing%20numeric%20or%20matching%20keys%20with%20matching%20values%20to%20ranges%0A%0A%20%20%20%20combines%20the%20functionality%20of%20%60condense_nested_dicts_numeric_keys%28%29%60%20and%20%60condense_nested_dicts_matching_values%28%29%60%0A%0A%20%20%20%20%23%20NOTE%3A%20this%20process%20is%20not%20meant%20to%20be%20reversible%2C%20and%20is%20intended%20for%20pretty-printing%20and%20visualization%20purposes%0A%20%20%20%20it%27s%20not%20reversible%20because%20types%20are%20lost%20to%20make%20the%20printing%20pretty%0A%0A%20%20%20%20%23%20Parameters%3A%0A%20%20%20%20%20-%20%60data%20%3A%20dict%5Bstr%2C%20Any%5D%60%0A%20%20%20%20%20%20%20%20data%20to%20process%0A%60%60%60&labels=NOTE)

  ```python
) -> dict[str, Any]:
    """condense a nested dict, by condensing numeric or matching keys with matching values to ranges

    combines the functionality of `condense_nested_dicts_numeric_keys()` and `condense_nested_dicts_matching_values()`

    # NOTE: this process is not meant to be reversible, and is intended for pretty-printing and visualization purposes
    it's not reversible because types are lost to make the printing pretty

    # Parameters:
     - `data : dict[str, Any]`
        data to process
  ```




## [`muutils/json_serialize/serializable_dataclass.py`](/muutils/json_serialize/serializable_dataclass.py)

- if ZANJ is not installed, then failing to register the loader handler doesnt matter  
  local link: [`/muutils/json_serialize/serializable_dataclass.py#141`](/muutils/json_serialize/serializable_dataclass.py#141) 
  | view on GitHub: [muutils/json_serialize/serializable_dataclass.py#L141](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_dataclass.py#L141)
  | [Make Issue](https://github.com/mivanit/muutils/issues/new?title=if%20ZANJ%20is%20not%20installed%2C%20then%20failing%20to%20register%20the%20loader%20handler%20doesnt%20matter&body=%23%20source%0A%0A%5B%60muutils%2Fjson_serialize%2Fserializable_dataclass.py%23L141%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fmuutils%2Fblob%2Fmain%2Fmuutils%2Fjson_serialize%2Fserializable_dataclass.py%23L141%29%0A%0A%23%20context%0A%60%60%60python%0A%20%20%20%20%20%20%20%20%20%20%20%20from%20zanj.loading%20import%20%28%20%20%23%20type%3A%20ignore%5Bimport%5D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20LoaderHandler%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20register_loader_handler%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20except%20ImportError%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20%23%20NOTE%3A%20if%20ZANJ%20is%20not%20installed%2C%20then%20failing%20to%20register%20the%20loader%20handler%20doesnt%20matter%0A%20%20%20%20%20%20%20%20%20%20%20%20%23%20warnings.warn%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%23%20%20%20%20%20%22ZANJ%20not%20installed%2C%20cannot%20register%20serializable%20dataclass%20loader.%20ZANJ%20can%20be%20found%20at%20https%3A%2F%2Fgithub.com%2Fmivanit%2FZANJ%20or%20installed%20via%20%60pip%20install%20zanj%60%22%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%23%20%20%20%20%20ZanjMissingWarning%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%23%20%29%0A%20%20%20%20%20%20%20%20%20%20%20%20return%0A%60%60%60&labels=NOTE)

  ```python
from zanj.loading import (  # type: ignore[import]
                LoaderHandler,
                register_loader_handler,
            )
        except ImportError:
            # NOTE: if ZANJ is not installed, then failing to register the loader handler doesnt matter
            # warnings.warn(
            #     "ZANJ not installed, cannot register serializable dataclass loader. ZANJ can be found at https://github.com/mivanit/ZANJ or installed via `pip install zanj`",
            #     ZanjMissingWarning,
            # )
            return
  ```





# TODO

## [`muutils/dictmagic.py`](/muutils/dictmagic.py)

-   
  local link: [`/muutils/dictmagic.py#276`](/muutils/dictmagic.py#276) 
  | view on GitHub: [muutils/dictmagic.py#L276](https://github.com/mivanit/muutils/blob/main/muutils/dictmagic.py#L276)
  | [Make Issue](https://github.com/mivanit/muutils/issues/new?title=Issue%20from%20inline%20todo&body=%23%20source%0A%0A%5B%60muutils%2Fdictmagic.py%23L276%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fmuutils%2Fblob%2Fmain%2Fmuutils%2Fdictmagic.py%23L276%29%0A%0A%23%20context%0A%60%60%60python%0A%20%20%20%20data%3A%20dict%5Bstr%2C%20Any%5D%2C%0A%20%20%20%20val_condense_fallback_mapping%3A%20Optional%5BCallable%5B%5BAny%5D%2C%20Hashable%5D%5D%20%3D%20None%2C%0A%29%20-%3E%20dict%5Bstr%2C%20Any%5D%3A%0A%20%20%20%20%22%22%22condense%20a%20nested%20dict%2C%20by%20condensing%20keys%20with%20matching%20values%0A%0A%20%20%20%20%23%20Examples%3A%20TODO%0A%0A%20%20%20%20%23%20Parameters%3A%0A%20%20%20%20%20-%20%60data%20%3A%20dict%5Bstr%2C%20Any%5D%60%0A%20%20%20%20%20%20%20%20data%20to%20process%0A%20%20%20%20%20-%20%60val_condense_fallback_mapping%20%3A%20Callable%5B%5BAny%5D%2C%20Hashable%5D%20%7C%20None%60%0A%60%60%60&labels=enhancement)

  ```python
data: dict[str, Any],
    val_condense_fallback_mapping: Optional[Callable[[Any], Hashable]] = None,
) -> dict[str, Any]:
    """condense a nested dict, by condensing keys with matching values

    # Examples: TODO

    # Parameters:
     - `data : dict[str, Any]`
        data to process
     - `val_condense_fallback_mapping : Callable[[Any], Hashable] | None`
  ```




## [`muutils/json_serialize/json_serialize.py`](/muutils/json_serialize/json_serialize.py)

- allow for custom serialization handler name  
  local link: [`/muutils/json_serialize/json_serialize.py#153`](/muutils/json_serialize/json_serialize.py#153) 
  | view on GitHub: [muutils/json_serialize/json_serialize.py#L153](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/json_serialize.py#L153)
  | [Make Issue](https://github.com/mivanit/muutils/issues/new?title=allow%20for%20custom%20serialization%20handler%20name&body=%23%20source%0A%0A%5B%60muutils%2Fjson_serialize%2Fjson_serialize.py%23L153%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fmuutils%2Fblob%2Fmain%2Fmuutils%2Fjson_serialize%2Fjson_serialize.py%23L153%29%0A%0A%23%20context%0A%60%60%60python%0A%20%20%20%20return%20obj.serialize%28%29%0A%0A%0ADEFAULT_HANDLERS%3A%20MonoTuple%5BSerializerHandler%5D%20%3D%20tuple%28BASE_HANDLERS%29%20%2B%20%28%0A%20%20%20%20SerializerHandler%28%0A%20%20%20%20%20%20%20%20%23%20TODO%3A%20allow%20for%20custom%20serialization%20handler%20name%0A%20%20%20%20%20%20%20%20check%3Dlambda%20self%2C%20obj%2C%20path%3A%20hasattr%28obj%2C%20%22serialize%22%29%0A%20%20%20%20%20%20%20%20and%20callable%28obj.serialize%29%2C%0A%20%20%20%20%20%20%20%20serialize_func%3D_serialize_override_serialize_func%2C%0A%20%20%20%20%20%20%20%20uid%3D%22.serialize%20override%22%2C%0A%20%20%20%20%20%20%20%20desc%3D%22objects%20with%20.serialize%20method%22%2C%0A%60%60%60&labels=enhancement)

  ```python
return obj.serialize()


DEFAULT_HANDLERS: MonoTuple[SerializerHandler] = tuple(BASE_HANDLERS) + (
    SerializerHandler(
        # TODO: allow for custom serialization handler name
        check=lambda self, obj, path: hasattr(obj, "serialize")
        and callable(obj.serialize),
        serialize_func=_serialize_override_serialize_func,
        uid=".serialize override",
        desc="objects with .serialize method",
  ```




## [`muutils/json_serialize/serializable_dataclass.py`](/muutils/json_serialize/serializable_dataclass.py)

- there is some duplication here with register_loader_handler  
  local link: [`/muutils/json_serialize/serializable_dataclass.py#130`](/muutils/json_serialize/serializable_dataclass.py#130) 
  | view on GitHub: [muutils/json_serialize/serializable_dataclass.py#L130](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_dataclass.py#L130)
  | [Make Issue](https://github.com/mivanit/muutils/issues/new?title=there%20is%20some%20duplication%20here%20with%20register_loader_handler&body=%23%20source%0A%0A%5B%60muutils%2Fjson_serialize%2Fserializable_dataclass.py%23L130%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fmuutils%2Fblob%2Fmain%2Fmuutils%2Fjson_serialize%2Fserializable_dataclass.py%23L130%29%0A%0A%23%20context%0A%60%60%60python%0A%20%20%20%20%22%22%22Register%20a%20serializable%20dataclass%20with%20the%20ZANJ%20import%0A%0A%20%20%20%20this%20allows%20%60ZANJ%28%29.read%28%29%60%20to%20load%20the%20class%20and%20not%20just%20return%20plain%20dicts%0A%0A%0A%20%20%20%20%23%20TODO%3A%20there%20is%20some%20duplication%20here%20with%20register_loader_handler%0A%20%20%20%20%22%22%22%0A%20%20%20%20global%20_zanj_loading_needs_import%0A%0A%20%20%20%20if%20_zanj_loading_needs_import%3A%0A%20%20%20%20%20%20%20%20try%3A%0A%60%60%60&labels=enhancement)

  ```python
"""Register a serializable dataclass with the ZANJ import

    this allows `ZANJ().read()` to load the class and not just return plain dicts


    # TODO: there is some duplication here with register_loader_handler
    """
    global _zanj_loading_needs_import

    if _zanj_loading_needs_import:
        try:
  ```


- how to handle fields which are not `init` or `serialize`?  
  local link: [`/muutils/json_serialize/serializable_dataclass.py#210`](/muutils/json_serialize/serializable_dataclass.py#210) 
  | view on GitHub: [muutils/json_serialize/serializable_dataclass.py#L210](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_dataclass.py#L210)
  | [Make Issue](https://github.com/mivanit/muutils/issues/new?title=how%20to%20handle%20fields%20which%20are%20not%20%60init%60%20or%20%60serialize%60%3F&body=%23%20source%0A%0A%5B%60muutils%2Fjson_serialize%2Fserializable_dataclass.py%23L210%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fmuutils%2Fblob%2Fmain%2Fmuutils%2Fjson_serialize%2Fserializable_dataclass.py%23L210%29%0A%0A%23%20context%0A%60%60%60python%0A%20%20%20%20%23%20do%20nothing%20case%0A%20%20%20%20if%20not%20_field.assert_type%3A%0A%20%20%20%20%20%20%20%20return%20True%0A%0A%20%20%20%20%23%20if%20field%20is%20not%20%60init%60%20or%20not%20%60serialize%60%2C%20skip%20but%20warn%0A%20%20%20%20%23%20TODO%3A%20how%20to%20handle%20fields%20which%20are%20not%20%60init%60%20or%20%60serialize%60%3F%0A%20%20%20%20if%20not%20_field.init%20or%20not%20_field.serialize%3A%0A%20%20%20%20%20%20%20%20warnings.warn%28%0A%20%20%20%20%20%20%20%20%20%20%20%20f%22Field%20%27%7B_field.name%7D%27%20on%20class%20%7Bself.__class__%7D%20is%20not%20%60init%60%20or%20%60serialize%60%2C%20so%20will%20not%20be%20type%20checked%22%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20FieldIsNotInitOrSerializeWarning%2C%0A%20%20%20%20%20%20%20%20%29%0A%60%60%60&labels=enhancement)

  ```python
# do nothing case
    if not _field.assert_type:
        return True

    # if field is not `init` or not `serialize`, skip but warn
    # TODO: how to handle fields which are not `init` or `serialize`?
    if not _field.init or not _field.serialize:
        warnings.warn(
            f"Field '{_field.name}' on class {self.__class__} is not `init` or `serialize`, so will not be type checked",
            FieldIsNotInitOrSerializeWarning,
        )
  ```


- are the types hashable? does this even make sense?  
  local link: [`/muutils/json_serialize/serializable_dataclass.py#515`](/muutils/json_serialize/serializable_dataclass.py#515) 
  | view on GitHub: [muutils/json_serialize/serializable_dataclass.py#L515](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_dataclass.py#L515)
  | [Make Issue](https://github.com/mivanit/muutils/issues/new?title=are%20the%20types%20hashable%3F%20does%20this%20even%20make%20sense%3F&body=%23%20source%0A%0A%5B%60muutils%2Fjson_serialize%2Fserializable_dataclass.py%23L515%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fmuutils%2Fblob%2Fmain%2Fmuutils%2Fjson_serialize%2Fserializable_dataclass.py%23L515%29%0A%0A%23%20context%0A%60%60%60python%0A%20%20%20%20%20%20%20%20%22deep%20copy%20by%20serializing%20and%20loading%20the%20instance%20to%20json%22%0A%20%20%20%20%20%20%20%20return%20self.__class__.load%28json.loads%28json.dumps%28self.serialize%28%29%29%29%29%0A%0A%0A%23%20cache%20this%20so%20we%20don%27t%20have%20to%20keep%20getting%20it%0A%23%20TODO%3A%20are%20the%20types%20hashable%3F%20does%20this%20even%20make%20sense%3F%0A%40functools.lru_cache%28typed%3DTrue%29%0Adef%20get_cls_type_hints_cached%28cls%3A%20Type%5BT%5D%29%20-%3E%20dict%5Bstr%2C%20Any%5D%3A%0A%20%20%20%20%22cached%20typing.get_type_hints%20for%20a%20class%22%0A%20%20%20%20return%20typing.get_type_hints%28cls%29%0A%60%60%60&labels=enhancement)

  ```python
"deep copy by serializing and loading the instance to json"
        return self.__class__.load(json.loads(json.dumps(self.serialize())))


# cache this so we don't have to keep getting it
# TODO: are the types hashable? does this even make sense?
@functools.lru_cache(typed=True)
def get_cls_type_hints_cached(cls: Type[T]) -> dict[str, Any]:
    "cached typing.get_type_hints for a class"
    return typing.get_type_hints(cls)
  ```




## [`muutils/json_serialize/serializable_field.py`](/muutils/json_serialize/serializable_field.py)

- add field for custom comparator (such as serializing)  
  local link: [`/muutils/json_serialize/serializable_field.py#55`](/muutils/json_serialize/serializable_field.py#55) 
  | view on GitHub: [muutils/json_serialize/serializable_field.py#L55](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_field.py#L55)
  | [Make Issue](https://github.com/mivanit/muutils/issues/new?title=add%20field%20for%20custom%20comparator%20%28such%20as%20serializing%29&body=%23%20source%0A%0A%5B%60muutils%2Fjson_serialize%2Fserializable_field.py%23L55%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fmuutils%2Fblob%2Fmain%2Fmuutils%2Fjson_serialize%2Fserializable_field.py%23L55%29%0A%0A%23%20context%0A%60%60%60python%0A%20%20%20%20%20%20%20%20%5D%20%3D%20dataclasses.MISSING%2C%0A%20%20%20%20%20%20%20%20init%3A%20bool%20%3D%20True%2C%0A%20%20%20%20%20%20%20%20repr%3A%20bool%20%3D%20True%2C%0A%20%20%20%20%20%20%20%20hash%3A%20Optional%5Bbool%5D%20%3D%20None%2C%0A%20%20%20%20%20%20%20%20compare%3A%20bool%20%3D%20True%2C%0A%20%20%20%20%20%20%20%20%23%20TODO%3A%20add%20field%20for%20custom%20comparator%20%28such%20as%20serializing%29%0A%20%20%20%20%20%20%20%20metadata%3A%20Optional%5Btypes.MappingProxyType%5D%20%3D%20None%2C%0A%20%20%20%20%20%20%20%20kw_only%3A%20Union%5Bbool%2C%20dataclasses._MISSING_TYPE%5D%20%3D%20dataclasses.MISSING%2C%0A%20%20%20%20%20%20%20%20serialize%3A%20bool%20%3D%20True%2C%0A%20%20%20%20%20%20%20%20serialization_fn%3A%20Optional%5BCallable%5B%5BAny%5D%2C%20Any%5D%5D%20%3D%20None%2C%0A%20%20%20%20%20%20%20%20loading_fn%3A%20Optional%5BCallable%5B%5BAny%5D%2C%20Any%5D%5D%20%3D%20None%2C%0A%60%60%60&labels=enhancement)

  ```python
] = dataclasses.MISSING,
        init: bool = True,
        repr: bool = True,
        hash: Optional[bool] = None,
        compare: bool = True,
        # TODO: add field for custom comparator (such as serializing)
        metadata: Optional[types.MappingProxyType] = None,
        kw_only: Union[bool, dataclasses._MISSING_TYPE] = dataclasses.MISSING,
        serialize: bool = True,
        serialization_fn: Optional[Callable[[Any], Any]] = None,
        loading_fn: Optional[Callable[[Any], Any]] = None,
  ```


- should we do this check, or assume the user knows what they are doing?  
  local link: [`/muutils/json_serialize/serializable_field.py#65`](/muutils/json_serialize/serializable_field.py#65) 
  | view on GitHub: [muutils/json_serialize/serializable_field.py#L65](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_field.py#L65)
  | [Make Issue](https://github.com/mivanit/muutils/issues/new?title=should%20we%20do%20this%20check%2C%20or%20assume%20the%20user%20knows%20what%20they%20are%20doing%3F&body=%23%20source%0A%0A%5B%60muutils%2Fjson_serialize%2Fserializable_field.py%23L65%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fmuutils%2Fblob%2Fmain%2Fmuutils%2Fjson_serialize%2Fserializable_field.py%23L65%29%0A%0A%23%20context%0A%60%60%60python%0A%20%20%20%20%20%20%20%20loading_fn%3A%20Optional%5BCallable%5B%5BAny%5D%2C%20Any%5D%5D%20%3D%20None%2C%0A%20%20%20%20%20%20%20%20deserialize_fn%3A%20Optional%5BCallable%5B%5BAny%5D%2C%20Any%5D%5D%20%3D%20None%2C%0A%20%20%20%20%20%20%20%20assert_type%3A%20bool%20%3D%20True%2C%0A%20%20%20%20%20%20%20%20custom_typecheck_fn%3A%20Optional%5BCallable%5B%5Btype%5D%2C%20bool%5D%5D%20%3D%20None%2C%0A%20%20%20%20%29%3A%0A%20%20%20%20%20%20%20%20%23%20TODO%3A%20should%20we%20do%20this%20check%2C%20or%20assume%20the%20user%20knows%20what%20they%20are%20doing%3F%0A%20%20%20%20%20%20%20%20if%20init%20and%20not%20serialize%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20raise%20ValueError%28%22Cannot%20have%20init%3DTrue%20and%20serialize%3DFalse%22%29%0A%0A%20%20%20%20%20%20%20%20%23%20need%20to%20assemble%20kwargs%20in%20this%20hacky%20way%20so%20as%20not%20to%20upset%20type%20checking%0A%20%20%20%20%20%20%20%20super_kwargs%3A%20dict%5Bstr%2C%20Any%5D%20%3D%20dict%28%0A%60%60%60&labels=enhancement)

  ```python
loading_fn: Optional[Callable[[Any], Any]] = None,
        deserialize_fn: Optional[Callable[[Any], Any]] = None,
        assert_type: bool = True,
        custom_typecheck_fn: Optional[Callable[[type], bool]] = None,
    ):
        # TODO: should we do this check, or assume the user knows what they are doing?
        if init and not serialize:
            raise ValueError("Cannot have init=True and serialize=False")

        # need to assemble kwargs in this hacky way so as not to upset type checking
        super_kwargs: dict[str, Any] = dict(
  ```


- `custom_value_check_fn`: function taking the value of the field and returning whether the value itself is valid. if not provided, any value is valid as long as it passes the type test  
  local link: [`/muutils/json_serialize/serializable_field.py#261`](/muutils/json_serialize/serializable_field.py#261) 
  | view on GitHub: [muutils/json_serialize/serializable_field.py#L261](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/serializable_field.py#L261)
  | [Make Issue](https://github.com/mivanit/muutils/issues/new?title=%60custom_value_check_fn%60%3A%20function%20taking%20the%20value%20of%20the%20field%20and%20returning%20whether%20the%20value%20itself%20is%20valid.%20if%20not%20provided%2C%20any%20value%20is%20valid%20as%20long%20as%20it%20passes%20the%20type%20test&body=%23%20source%0A%0A%5B%60muutils%2Fjson_serialize%2Fserializable_field.py%23L261%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fmuutils%2Fblob%2Fmain%2Fmuutils%2Fjson_serialize%2Fserializable_field.py%23L261%29%0A%0A%23%20context%0A%60%60%60python%0A%20%20%20%20note%20that%20if%20not%20using%20ZANJ%2C%20and%20you%20have%20a%20class%20inside%20a%20container%2C%20you%20MUST%20provide%0A%20%20%20%20%60serialization_fn%60%20and%20%60loading_fn%60%20to%20serialize%20and%20load%20the%20container.%0A%20%20%20%20ZANJ%20will%20automatically%20do%20this%20for%20you.%0A%0A%20%20%20%20%23%20TODO%3A%20%60custom_value_check_fn%60%3A%20function%20taking%20the%20value%20of%20the%20field%20and%20returning%20whether%20the%20value%20itself%20is%20valid.%20if%20not%20provided%2C%20any%20value%20is%20valid%20as%20long%20as%20it%20passes%20the%20type%20test%0A%20%20%20%20%22%22%22%0A%20%20%20%20assert%20len%28_args%29%20%3D%3D%200%2C%20f%22unexpected%20positional%20arguments%3A%20%7B_args%7D%22%0A%20%20%20%20return%20SerializableField%28%0A%20%20%20%20%20%20%20%20default%3Ddefault%2C%0A%20%20%20%20%20%20%20%20default_factory%3Ddefault_factory%2C%0A%60%60%60&labels=enhancement)

  ```python
note that if not using ZANJ, and you have a class inside a container, you MUST provide
    `serialization_fn` and `loading_fn` to serialize and load the container.
    ZANJ will automatically do this for you.

    # TODO: `custom_value_check_fn`: function taking the value of the field and returning whether the value itself is valid. if not provided, any value is valid as long as it passes the type test
    """
    assert len(_args) == 0, f"unexpected positional arguments: {_args}"
    return SerializableField(
        default=default,
        default_factory=default_factory,
  ```




## [`muutils/json_serialize/util.py`](/muutils/json_serialize/util.py)

- after "except when class mismatch" is False, shouldn't we then go to "field keys match"?  
  local link: [`/muutils/json_serialize/util.py#226`](/muutils/json_serialize/util.py#226) 
  | view on GitHub: [muutils/json_serialize/util.py#L226](https://github.com/mivanit/muutils/blob/main/muutils/json_serialize/util.py#L226)
  | [Make Issue](https://github.com/mivanit/muutils/issues/new?title=after%20%22except%20when%20class%20mismatch%22%20is%20False%2C%20shouldn%27t%20we%20then%20go%20to%20%22field%20keys%20match%22%3F&body=%23%20source%0A%0A%5B%60muutils%2Fjson_serialize%2Futil.py%23L226%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fmuutils%2Fblob%2Fmain%2Fmuutils%2Fjson_serialize%2Futil.py%23L226%29%0A%0A%23%20context%0A%60%60%60python%0A%20%20%20%20%23%20Raises%3A%0A%20%20%20%20-%20%60TypeError%60%3A%20if%20the%20dataclasses%20are%20of%20different%20classes%0A%20%20%20%20-%20%60AttributeError%60%3A%20if%20the%20dataclasses%20have%20different%20fields%0A%0A%20%20%20%20%23%20TODO%3A%20after%20%22except%20when%20class%20mismatch%22%20is%20False%2C%20shouldn%27t%20we%20then%20go%20to%20%22field%20keys%20match%22%3F%0A%20%20%20%20%60%60%60%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5BSTART%5D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%E2%96%BC%0A%20%20%20%20%20%20%20%20%20%20%20%E2%94%8C%E2%94%80%E2%94%80%E2%94%80%E2%94%80%E2%94%80%E2%94%80%E2%94%80%E2%94%80%E2%94%80%E2%94%80%E2%94%80%E2%94%90%20%20%E2%94%8C%E2%94%80%E2%94%80%E2%94%80%E2%94%80%E2%94%80%E2%94%80%E2%94%80%E2%94%80%E2%94%80%E2%94%90%0A%20%20%20%20%20%20%20%20%20%20%20%E2%94%82dc1%20is%20dc2%3F%E2%94%9C%E2%94%80%E2%96%BA%E2%94%82%20classes%20%E2%94%82%0A%60%60%60&labels=enhancement)

  ```python
# Raises:
    - `TypeError`: if the dataclasses are of different classes
    - `AttributeError`: if the dataclasses have different fields

    # TODO: after "except when class mismatch" is False, shouldn't we then go to "field keys match"?
    ```
              [START]
                 ▼
           ┌───────────┐  ┌─────────┐
           │dc1 is dc2?├─►│ classes │
  ```




## [`muutils/logger/logger.py`](/muutils/logger/logger.py)

- handle per stream?  
  local link: [`/muutils/logger/logger.py#98`](/muutils/logger/logger.py#98) 
  | view on GitHub: [muutils/logger/logger.py#L98](https://github.com/mivanit/muutils/blob/main/muutils/logger/logger.py#L98)
  | [Make Issue](https://github.com/mivanit/muutils/issues/new?title=handle%20per%20stream%3F&body=%23%20source%0A%0A%5B%60muutils%2Flogger%2Flogger.py%23L98%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fmuutils%2Fblob%2Fmain%2Fmuutils%2Flogger%2Flogger.py%23L98%29%0A%0A%23%20context%0A%60%60%60python%0A%20%20%20%20%20%20%20%20%23%20timing%0A%20%20%20%20%20%20%20%20%23%20%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%0A%20%20%20%20%20%20%20%20%23%20timing%20compares%0A%20%20%20%20%20%20%20%20self._keep_last_msg_time%3A%20bool%20%3D%20keep_last_msg_time%0A%20%20%20%20%20%20%20%20%23%20TODO%3A%20handle%20per%20stream%3F%0A%20%20%20%20%20%20%20%20self._last_msg_time%3A%20float%20%7C%20None%20%3D%20time.time%28%29%0A%0A%20%20%20%20%20%20%20%20%23%20basic%20setup%0A%20%20%20%20%20%20%20%20%23%20%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%3D%0A%20%20%20%20%20%20%20%20%23%20init%20BaseLogger%0A%60%60%60&labels=enhancement)

  ```python
# timing
        # ==================================================
        # timing compares
        self._keep_last_msg_time: bool = keep_last_msg_time
        # TODO: handle per stream?
        self._last_msg_time: float | None = time.time()

        # basic setup
        # ==================================================
        # init BaseLogger
  ```




## [`muutils/logger/loggingstream.py`](/muutils/logger/loggingstream.py)

- perhaps duplicate alises should result in duplicate writes?  
  local link: [`/muutils/logger/loggingstream.py#18`](/muutils/logger/loggingstream.py#18) 
  | view on GitHub: [muutils/logger/loggingstream.py#L18](https://github.com/mivanit/muutils/blob/main/muutils/logger/loggingstream.py#L18)
  | [Make Issue](https://github.com/mivanit/muutils/issues/new?title=perhaps%20duplicate%20alises%20should%20result%20in%20duplicate%20writes%3F&body=%23%20source%0A%0A%5B%60muutils%2Flogger%2Floggingstream.py%23L18%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fmuutils%2Fblob%2Fmain%2Fmuutils%2Flogger%2Floggingstream.py%23L18%29%0A%0A%23%20context%0A%60%60%60python%0A%20%20%20%20%22%22%22properties%20of%20a%20logging%20stream%0A%0A%20%20%20%20-%20%60name%3A%20str%60%20name%20of%20the%20stream%0A%20%20%20%20-%20%60aliases%3A%20set%5Bstr%5D%60%20aliases%20for%20the%20stream%0A%20%20%20%20%20%20%20%20%20%20%20%20%28calls%20to%20these%20names%20will%20be%20redirected%20to%20this%20stream.%20duplicate%20alises%20will%20result%20in%20errors%29%0A%20%20%20%20%20%20%20%20%20%20%20%20TODO%3A%20perhaps%20duplicate%20alises%20should%20result%20in%20duplicate%20writes%3F%0A%20%20%20%20-%20%60file%3A%20str%7Cbool%7CAnyIO%7CNone%60%20file%20to%20write%20to%0A%20%20%20%20%20%20%20%20%20%20%20%20-%20if%20%60None%60%2C%20will%20write%20to%20standard%20log%0A%20%20%20%20%20%20%20%20%20%20%20%20-%20if%20%60True%60%2C%20will%20write%20to%20%60name%20%2B%20%22.log%22%60%0A%20%20%20%20%20%20%20%20%20%20%20%20-%20if%20%60False%60%20will%20%22write%22%20to%20%60NullIO%60%20%28throw%20it%20away%29%0A%20%20%20%20%20%20%20%20%20%20%20%20-%20if%20a%20string%2C%20will%20write%20to%20that%20file%0A%60%60%60&labels=enhancement)

  ```python
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
  ```


- implement last-message caching  
  local link: [`/muutils/logger/loggingstream.py#37`](/muutils/logger/loggingstream.py#37) 
  | view on GitHub: [muutils/logger/loggingstream.py#L37](https://github.com/mivanit/muutils/blob/main/muutils/logger/loggingstream.py#L37)
  | [Make Issue](https://github.com/mivanit/muutils/issues/new?title=implement%20last-message%20caching&body=%23%20source%0A%0A%5B%60muutils%2Flogger%2Floggingstream.py%23L37%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fmuutils%2Fblob%2Fmain%2Fmuutils%2Flogger%2Floggingstream.py%23L37%29%0A%0A%23%20context%0A%60%60%60python%0A%20%20%20%20file%3A%20str%20%7C%20bool%20%7C%20AnyIO%20%7C%20None%20%3D%20None%0A%20%20%20%20default_level%3A%20int%20%7C%20None%20%3D%20None%0A%20%20%20%20default_contents%3A%20dict%5Bstr%2C%20Callable%5B%5B%5D%2C%20Any%5D%5D%20%3D%20field%28default_factory%3Ddict%29%0A%20%20%20%20handler%3A%20AnyIO%20%7C%20None%20%3D%20None%0A%0A%20%20%20%20%23%20TODO%3A%20implement%20last-message%20caching%0A%20%20%20%20%23%20last_msg%3A%20tuple%5Bfloat%2C%20Any%5D%7CNone%20%3D%20None%0A%0A%20%20%20%20def%20make_handler%28self%29%20-%3E%20AnyIO%20%7C%20None%3A%0A%20%20%20%20%20%20%20%20if%20self.file%20is%20None%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20return%20None%0A%60%60%60&labels=enhancement)

  ```python
file: str | bool | AnyIO | None = None
    default_level: int | None = None
    default_contents: dict[str, Callable[[], Any]] = field(default_factory=dict)
    handler: AnyIO | None = None

    # TODO: implement last-message caching
    # last_msg: tuple[float, Any]|None = None

    def make_handler(self) -> AnyIO | None:
        if self.file is None:
            return None
  ```


- make this happen in the same dir as the main logfile?  
  local link: [`/muutils/logger/loggingstream.py#52`](/muutils/logger/loggingstream.py#52) 
  | view on GitHub: [muutils/logger/loggingstream.py#L52](https://github.com/mivanit/muutils/blob/main/muutils/logger/loggingstream.py#L52)
  | [Make Issue](https://github.com/mivanit/muutils/issues/new?title=make%20this%20happen%20in%20the%20same%20dir%20as%20the%20main%20logfile%3F&body=%23%20source%0A%0A%5B%60muutils%2Flogger%2Floggingstream.py%23L52%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fmuutils%2Fblob%2Fmain%2Fmuutils%2Flogger%2Floggingstream.py%23L52%29%0A%0A%23%20context%0A%60%60%60python%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%22w%22%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20encoding%3D%22utf-8%22%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%29%0A%20%20%20%20%20%20%20%20elif%20isinstance%28self.file%2C%20bool%29%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20%23%20if%20its%20a%20bool%20and%20true%2C%20open%20a%20file%20with%20the%20same%20name%20as%20the%20stream%20%28in%20the%20current%20dir%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%23%20TODO%3A%20make%20this%20happen%20in%20the%20same%20dir%20as%20the%20main%20logfile%3F%0A%20%20%20%20%20%20%20%20%20%20%20%20if%20self.file%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20return%20open%28%20%20%23%20type%3A%20ignore%5Breturn-value%5D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20f%22%7Bsanitize_fname%28self.name%29%7D.log.jsonl%22%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%22w%22%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20encoding%3D%22utf-8%22%2C%0A%60%60%60&labels=enhancement)

  ```python
"w",
                encoding="utf-8",
            )
        elif isinstance(self.file, bool):
            # if its a bool and true, open a file with the same name as the stream (in the current dir)
            # TODO: make this happen in the same dir as the main logfile?
            if self.file:
                return open(  # type: ignore[return-value]
                    f"{sanitize_fname(self.name)}.log.jsonl",
                    "w",
                    encoding="utf-8",
  ```




## [`muutils/logger/timing.py`](/muutils/logger/timing.py)

- get_progress_default  
  local link: [`/muutils/logger/timing.py#84`](/muutils/logger/timing.py#84) 
  | view on GitHub: [muutils/logger/timing.py#L84](https://github.com/mivanit/muutils/blob/main/muutils/logger/timing.py#L84)
  | [Make Issue](https://github.com/mivanit/muutils/issues/new?title=get_progress_default&body=%23%20source%0A%0A%5B%60muutils%2Flogger%2Ftiming.py%23L84%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fmuutils%2Fblob%2Fmain%2Fmuutils%2Flogger%2Ftiming.py%23L84%29%0A%0A%23%20context%0A%60%60%60python%0A%20%20%20%20def%20get_progress_default%28self%2C%20i%3A%20int%29%20-%3E%20str%3A%0A%20%20%20%20%20%20%20%20%22%22%22returns%20a%20progress%20string%22%22%22%0A%20%20%20%20%20%20%20%20timing_raw%3A%20dict%5Bstr%2C%20float%5D%20%3D%20self.get_timing_raw%28i%29%0A%0A%20%20%20%20%20%20%20%20percent_str%3A%20str%20%3D%20str%28int%28timing_raw%5B%22percent%22%5D%20%2A%20100%29%29.ljust%282%29%0A%20%20%20%20%20%20%20%20%23%20TODO%3A%20get_progress_default%0A%20%20%20%20%20%20%20%20%23%20iters_str%3A%20str%20%3D%20f%22%7Bstr%28i%29.ljust%28self.total_str_len%29%7D%2F%7Bself.n_total%7D%22%0A%20%20%20%20%20%20%20%20%23%20timing_str%3A%20str%0A%20%20%20%20%20%20%20%20return%20f%22%7Bpercent_str%7D%25%20%7Bself.get_pbar%28i%29%7D%22%0A%60%60%60&labels=enhancement)

  ```python
def get_progress_default(self, i: int) -> str:
        """returns a progress string"""
        timing_raw: dict[str, float] = self.get_timing_raw(i)

        percent_str: str = str(int(timing_raw["percent"] * 100)).ljust(2)
        # TODO: get_progress_default
        # iters_str: str = f"{str(i).ljust(self.total_str_len)}/{self.n_total}"
        # timing_str: str
        return f"{percent_str}% {self.get_pbar(i)}"
  ```




## [`muutils/misc/func.py`](/muutils/misc/func.py)

- no way to type hint this, I think  
  local link: [`/muutils/misc/func.py#184`](/muutils/misc/func.py#184) 
  | view on GitHub: [muutils/misc/func.py#L184](https://github.com/mivanit/muutils/blob/main/muutils/misc/func.py#L184)
  | [Make Issue](https://github.com/mivanit/muutils/issues/new?title=no%20way%20to%20type%20hint%20this%2C%20I%20think&body=%23%20source%0A%0A%5B%60muutils%2Fmisc%2Ffunc.py%23L184%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fmuutils%2Fblob%2Fmain%2Fmuutils%2Fmisc%2Ffunc.py%23L184%29%0A%0A%23%20context%0A%60%60%60python%0A%20%20%20%20%20%20%20%20func%3A%20Callable%5BFuncParams%2C%20ReturnType%5D%2C%0A%20%20%20%20%29%20-%3E%20Callable%5BFuncParams%2C%20ReturnType%5D%3A%0A%20%20%20%20%20%20%20%20%40functools.wraps%28func%29%0A%20%20%20%20%20%20%20%20def%20wrapper%28%2Aargs%3A%20FuncParams.args%2C%20%2A%2Akwargs%3A%20FuncParams.kwargs%29%20-%3E%20ReturnType%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20if%20kwarg_name%20in%20kwargs%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%23%20TODO%3A%20no%20way%20to%20type%20hint%20this%2C%20I%20think%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20if%20check%28kwargs%5Bkwarg_name%5D%29%3A%20%20%23%20type%3A%20ignore%5Barg-type%5D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20kwargs%5Bkwarg_name%5D%20%3D%20replacement_value%0A%20%20%20%20%20%20%20%20%20%20%20%20elif%20replace_if_missing%20and%20kwarg_name%20not%20in%20kwargs%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20kwargs%5Bkwarg_name%5D%20%3D%20replacement_value%0A%20%20%20%20%20%20%20%20%20%20%20%20return%20func%28%2Aargs%2C%20%2A%2Akwargs%29%0A%60%60%60&labels=enhancement)

  ```python
func: Callable[FuncParams, ReturnType],
    ) -> Callable[FuncParams, ReturnType]:
        @functools.wraps(func)
        def wrapper(*args: FuncParams.args, **kwargs: FuncParams.kwargs) -> ReturnType:
            if kwarg_name in kwargs:
                # TODO: no way to type hint this, I think
                if check(kwargs[kwarg_name]):  # type: ignore[arg-type]
                    kwargs[kwarg_name] = replacement_value
            elif replace_if_missing and kwarg_name not in kwargs:
                kwargs[kwarg_name] = replacement_value
            return func(*args, **kwargs)
  ```


- no way to make the type system understand this afaik  
  local link: [`/muutils/misc/func.py#223`](/muutils/misc/func.py#223) 
  | view on GitHub: [muutils/misc/func.py#L223](https://github.com/mivanit/muutils/blob/main/muutils/misc/func.py#L223)
  | [Make Issue](https://github.com/mivanit/muutils/issues/new?title=no%20way%20to%20make%20the%20type%20system%20understand%20this%20afaik&body=%23%20source%0A%0A%5B%60muutils%2Fmisc%2Ffunc.py%23L223%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fmuutils%2Fblob%2Fmain%2Fmuutils%2Fmisc%2Ffunc.py%23L223%29%0A%0A%23%20context%0A%60%60%60python%0A%20%20%20%20%20%20%20%20return%20func%0A%0A%20%20%20%20return%20decorator%0A%0A%0A%23%20TODO%3A%20no%20way%20to%20make%20the%20type%20system%20understand%20this%20afaik%0ALambdaArgs%20%3D%20TypeVarTuple%28%22LambdaArgs%22%29%0ALambdaArgsTypes%20%3D%20TypeVar%28%22LambdaArgsTypes%22%2C%20bound%3DTuple%5Btype%2C%20...%5D%29%0A%0A%0Adef%20typed_lambda%28%0A%60%60%60&labels=enhancement)

  ```python
return func

    return decorator


# TODO: no way to make the type system understand this afaik
LambdaArgs = TypeVarTuple("LambdaArgs")
LambdaArgsTypes = TypeVar("LambdaArgsTypes", bound=Tuple[type, ...])


def typed_lambda(
  ```




## [`muutils/misc/sequence.py`](/muutils/misc/sequence.py)

- swap type check with more general check for __iter__() or __next__() or whatever  
  local link: [`/muutils/misc/sequence.py#58`](/muutils/misc/sequence.py#58) 
  | view on GitHub: [muutils/misc/sequence.py#L58](https://github.com/mivanit/muutils/blob/main/muutils/misc/sequence.py#L58)
  | [Make Issue](https://github.com/mivanit/muutils/issues/new?title=swap%20type%20check%20with%20more%20general%20check%20for%20__iter__%28%29%20or%20__next__%28%29%20or%20whatever&body=%23%20source%0A%0A%5B%60muutils%2Fmisc%2Fsequence.py%23L58%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fmuutils%2Fblob%2Fmain%2Fmuutils%2Fmisc%2Fsequence.py%23L58%29%0A%0A%23%20context%0A%60%60%60python%0A%20%20%20%20%23%20Parameters%0A%20%20%20%20-%20%60it%60%3A%20Any%20arbitrarily%20nested%20iterable.%0A%20%20%20%20-%20%60levels_to_flatten%60%3A%20Number%20of%20levels%20to%20flatten%20by%2C%20starting%20at%20the%20outermost%20layer.%20If%20%60None%60%2C%20performs%20full%20flattening.%0A%20%20%20%20%22%22%22%0A%20%20%20%20for%20x%20in%20it%3A%0A%20%20%20%20%20%20%20%20%23%20TODO%3A%20swap%20type%20check%20with%20more%20general%20check%20for%20__iter__%28%29%20or%20__next__%28%29%20or%20whatever%0A%20%20%20%20%20%20%20%20if%20%28%0A%20%20%20%20%20%20%20%20%20%20%20%20hasattr%28x%2C%20%22__iter__%22%29%0A%20%20%20%20%20%20%20%20%20%20%20%20and%20not%20isinstance%28x%2C%20%28str%2C%20bytes%29%29%0A%20%20%20%20%20%20%20%20%20%20%20%20and%20%28levels_to_flatten%20is%20None%20or%20levels_to_flatten%20%3E%200%29%0A%20%20%20%20%20%20%20%20%29%3A%0A%60%60%60&labels=enhancement)

  ```python
# Parameters
    - `it`: Any arbitrarily nested iterable.
    - `levels_to_flatten`: Number of levels to flatten by, starting at the outermost layer. If `None`, performs full flattening.
    """
    for x in it:
        # TODO: swap type check with more general check for __iter__() or __next__() or whatever
        if (
            hasattr(x, "__iter__")
            and not isinstance(x, (str, bytes))
            and (levels_to_flatten is None or levels_to_flatten > 0)
        ):
  ```




## [`muutils/spinner.py`](/muutils/spinner.py)

- fix this type ignore  
  local link: [`/muutils/spinner.py#499`](/muutils/spinner.py#499) 
  | view on GitHub: [muutils/spinner.py#L499](https://github.com/mivanit/muutils/blob/main/muutils/spinner.py#L499)
  | [Make Issue](https://github.com/mivanit/muutils/issues/new?title=fix%20this%20type%20ignore&body=%23%20source%0A%0A%5B%60muutils%2Fspinner.py%23L499%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fmuutils%2Fblob%2Fmain%2Fmuutils%2Fspinner.py%23L499%29%0A%0A%23%20context%0A%60%60%60python%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20spinner.stop%28failed%3DTrue%29%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20raise%20e%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20return%20result%0A%0A%20%20%20%20%20%20%20%20%23%20TODO%3A%20fix%20this%20type%20ignore%0A%20%20%20%20%20%20%20%20return%20wrapper%20%20%23%20type%3A%20ignore%5Breturn-value%5D%0A%0A%20%20%20%20if%20not%20args%3A%0A%20%20%20%20%20%20%20%20%23%20called%20as%20%60%40spinner_decorator%28stuff%29%60%0A%20%20%20%20%20%20%20%20return%20decorator%0A%60%60%60&labels=enhancement)

  ```python
spinner.stop(failed=True)
                raise e

            return result

        # TODO: fix this type ignore
        return wrapper  # type: ignore[return-value]

    if not args:
        # called as `@spinner_decorator(stuff)`
        return decorator
  ```




## [`muutils/tensor_utils.py`](/muutils/tensor_utils.py)

- add proper type annotations to this signature  
  local link: [`/muutils/tensor_utils.py#76`](/muutils/tensor_utils.py#76) 
  | view on GitHub: [muutils/tensor_utils.py#L76](https://github.com/mivanit/muutils/blob/main/muutils/tensor_utils.py#L76)
  | [Make Issue](https://github.com/mivanit/muutils/issues/new?title=add%20proper%20type%20annotations%20to%20this%20signature&body=%23%20source%0A%0A%5B%60muutils%2Ftensor_utils.py%23L76%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fmuutils%2Fblob%2Fmain%2Fmuutils%2Ftensor_utils.py%23L76%29%0A%0A%23%20context%0A%60%60%60python%0Aif%20np.version.version%20%3C%20%222.0.0%22%3A%0A%20%20%20%20TYPE_TO_JAX_DTYPE%5Bnp.float_%5D%20%3D%20jaxtyping.Float%0A%20%20%20%20TYPE_TO_JAX_DTYPE%5Bnp.int_%5D%20%3D%20jaxtyping.Int%0A%0A%0A%23%20TODO%3A%20add%20proper%20type%20annotations%20to%20this%20signature%0Adef%20jaxtype_factory%28%0A%20%20%20%20name%3A%20str%2C%0A%20%20%20%20array_type%3A%20type%2C%0A%20%20%20%20default_jax_dtype%3Djaxtyping.Float%2C%0A%20%20%20%20legacy_mode%3A%20ErrorMode%20%3D%20ErrorMode.WARN%2C%0A%60%60%60&labels=enhancement)

  ```python
if np.version.version < "2.0.0":
    TYPE_TO_JAX_DTYPE[np.float_] = jaxtyping.Float
    TYPE_TO_JAX_DTYPE[np.int_] = jaxtyping.Int


# TODO: add proper type annotations to this signature
def jaxtype_factory(
    name: str,
    array_type: type,
    default_jax_dtype=jaxtyping.Float,
    legacy_mode: ErrorMode = ErrorMode.WARN,
  ```




## [`muutils/validate_type.py`](/muutils/validate_type.py)

- Callables, etc.  
  local link: [`/muutils/validate_type.py#207`](/muutils/validate_type.py#207) 
  | view on GitHub: [muutils/validate_type.py#L207](https://github.com/mivanit/muutils/blob/main/muutils/validate_type.py#L207)
  | [Make Issue](https://github.com/mivanit/muutils/issues/new?title=Callables%2C%20etc.&body=%23%20source%0A%0A%5B%60muutils%2Fvalidate_type.py%23L207%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fmuutils%2Fblob%2Fmain%2Fmuutils%2Fvalidate_type.py%23L207%29%0A%0A%23%20context%0A%60%60%60python%0A%20%20%20%20%20%20%20%20%20%20%20%20if%20item_type%20in%20value.__mro__%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20return%20_return_func%28True%29%0A%20%20%20%20%20%20%20%20%20%20%20%20else%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20return%20_return_func%28False%29%0A%0A%20%20%20%20%20%20%20%20%23%20TODO%3A%20Callables%2C%20etc.%0A%0A%20%20%20%20%20%20%20%20raise%20TypeHintNotImplementedError%28%0A%20%20%20%20%20%20%20%20%20%20%20%20f%22Unsupported%20generic%20alias%20%7Bexpected_type%20%3D%20%7D%20for%20%7Bvalue%20%3D%20%7D%2C%20%20%20%7Borigin%20%3D%20%7D%2C%20%20%20%7Bargs%20%3D%20%7D%22%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20f%22%7Borigin%20%3D%20%7D%2C%20%7Bargs%20%3D%20%7D%22%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20f%22%5Cn%7BGenericAliasTypes%20%3D%20%7D%22%2C%0A%60%60%60&labels=enhancement)

  ```python
if item_type in value.__mro__:
                return _return_func(True)
            else:
                return _return_func(False)

        # TODO: Callables, etc.

        raise TypeHintNotImplementedError(
            f"Unsupported generic alias {expected_type = } for {value = },   {origin = },   {args = }",
            f"{origin = }, {args = }",
            f"\n{GenericAliasTypes = }",
  ```




## [`tests/unit/json_serialize/serializable_dataclass/test_serializable_dataclass.py`](/tests/unit/json_serialize/serializable_dataclass/test_serializable_dataclass.py)

- figure this out  
  local link: [`/tests/unit/json_serialize/serializable_dataclass/test_serializable_dataclass.py#578`](/tests/unit/json_serialize/serializable_dataclass/test_serializable_dataclass.py#578) 
  | view on GitHub: [tests/unit/json_serialize/serializable_dataclass/test_serializable_dataclass.py#L578](https://github.com/mivanit/muutils/blob/main/tests/unit/json_serialize/serializable_dataclass/test_serializable_dataclass.py#L578)
  | [Make Issue](https://github.com/mivanit/muutils/issues/new?title=figure%20this%20out&body=%23%20source%0A%0A%5B%60tests%2Funit%2Fjson_serialize%2Fserializable_dataclass%2Ftest_serializable_dataclass.py%23L578%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fmuutils%2Fblob%2Fmain%2Ftests%2Funit%2Fjson_serialize%2Fserializable_dataclass%2Ftest_serializable_dataclass.py%23L578%29%0A%0A%23%20context%0A%60%60%60python%0A%20%20%20%20int_dict%3A%20Dict%5Bstr%2C%20int%5D%0A%20%20%20%20str_dict%3A%20Dict%5Bstr%2C%20str%5D%0A%20%20%20%20float_dict%3A%20Dict%5Bstr%2C%20float%5D%0A%0A%0A%23%20TODO%3A%20figure%20this%20out%0A%40pytest.mark.skip%28reason%3D%22dict%20type%20validation%20doesnt%20seem%20to%20work%22%29%0Adef%20test_dict_type_validation%28%29%3A%0A%20%20%20%20%22%22%22Test%20type%20validation%20for%20dictionary%20values%22%22%22%0A%20%20%20%20%23%20Valid%20case%0A%20%20%20%20valid%20%3D%20StrictDictContainer%28%0A%60%60%60&labels=enhancement)

  ```python
int_dict: Dict[str, int]
    str_dict: Dict[str, str]
    float_dict: Dict[str, float]


# TODO: figure this out
@pytest.mark.skip(reason="dict type validation doesnt seem to work")
def test_dict_type_validation():
    """Test type validation for dictionary values"""
    # Valid case
    valid = StrictDictContainer(
  ```


- this would be nice to fix, but not a massive issue  
  local link: [`/tests/unit/json_serialize/serializable_dataclass/test_serializable_dataclass.py#966`](/tests/unit/json_serialize/serializable_dataclass/test_serializable_dataclass.py#966) 
  | view on GitHub: [tests/unit/json_serialize/serializable_dataclass/test_serializable_dataclass.py#L966](https://github.com/mivanit/muutils/blob/main/tests/unit/json_serialize/serializable_dataclass/test_serializable_dataclass.py#L966)
  | [Make Issue](https://github.com/mivanit/muutils/issues/new?title=this%20would%20be%20nice%20to%20fix%2C%20but%20not%20a%20massive%20issue&body=%23%20source%0A%0A%5B%60tests%2Funit%2Fjson_serialize%2Fserializable_dataclass%2Ftest_serializable_dataclass.py%23L966%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fmuutils%2Fblob%2Fmain%2Ftests%2Funit%2Fjson_serialize%2Fserializable_dataclass%2Ftest_serializable_dataclass.py%23L966%29%0A%0A%23%20context%0A%60%60%60python%0A%20%20%20%20loaded%20%3D%20PropertyContainer.load%28serialized%29%0A%20%20%20%20assert%20loaded%20%3D%3D%20instance%0A%0A%0A%23%20TODO%3A%20this%20would%20be%20nice%20to%20fix%2C%20but%20not%20a%20massive%20issue%0A%40pytest.mark.skip%28reason%3D%22Not%20implemented%20yet%22%29%0Adef%20test_edge_cases%28%29%3A%0A%20%20%20%20%22%22%22Test%20a%20sdc%20containing%20instances%20of%20itself%22%22%22%0A%0A%20%20%20%20%40serializable_dataclass%0A%60%60%60&labels=enhancement)

  ```python
loaded = PropertyContainer.load(serialized)
    assert loaded == instance


# TODO: this would be nice to fix, but not a massive issue
@pytest.mark.skip(reason="Not implemented yet")
def test_edge_cases():
    """Test a sdc containing instances of itself"""

    @serializable_dataclass
  ```


- make .serialize() fail on cyclic references! see https://github.com/mivanit/muutils/issues/62  
  local link: [`/tests/unit/json_serialize/serializable_dataclass/test_serializable_dataclass.py#1034`](/tests/unit/json_serialize/serializable_dataclass/test_serializable_dataclass.py#1034) 
  | view on GitHub: [tests/unit/json_serialize/serializable_dataclass/test_serializable_dataclass.py#L1034](https://github.com/mivanit/muutils/blob/main/tests/unit/json_serialize/serializable_dataclass/test_serializable_dataclass.py#L1034)
  | [Make Issue](https://github.com/mivanit/muutils/issues/new?title=make%20.serialize%28%29%20fail%20on%20cyclic%20references%21%20see%20https%3A%2F%2Fgithub.com%2Fmivanit%2Fmuutils%2Fissues%2F62&body=%23%20source%0A%0A%5B%60tests%2Funit%2Fjson_serialize%2Fserializable_dataclass%2Ftest_serializable_dataclass.py%23L1034%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fmuutils%2Fblob%2Fmain%2Ftests%2Funit%2Fjson_serialize%2Fserializable_dataclass%2Ftest_serializable_dataclass.py%23L1034%29%0A%0A%23%20context%0A%60%60%60python%0A%20%20%20%20%23%20%20%20%20%20%20%20%20%20%22shared_field%22%3A%200%0A%20%20%20%20%23%20%20%20%20%20%7D%29%0A%0A%0A%23%20Test%20for%20memory%20leaks%20and%20cyclic%20references%0A%23%20TODO%3A%20make%20.serialize%28%29%20fail%20on%20cyclic%20references%21%20see%20https%3A%2F%2Fgithub.com%2Fmivanit%2Fmuutils%2Fissues%2F62%0A%40pytest.mark.skip%28reason%3D%22Not%20implemented%20yet%22%29%0Adef%20test_cyclic_references%28%29%3A%0A%20%20%20%20%22%22%22Test%20handling%20of%20cyclic%20references%22%22%22%0A%0A%20%20%20%20%40serializable_dataclass%0A%60%60%60&labels=enhancement)

  ```python
#         "shared_field": 0
    #     })


# Test for memory leaks and cyclic references
# TODO: make .serialize() fail on cyclic references! see https://github.com/mivanit/muutils/issues/62
@pytest.mark.skip(reason="Not implemented yet")
def test_cyclic_references():
    """Test handling of cyclic references"""

    @serializable_dataclass
  ```




