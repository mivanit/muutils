class LazyExternalLoader:
    """lazy load np arrays or jsonl files, similar tp NpzFile from np.lib

    initialize with zipfile object and zanj metadata (for list of externals)
    """

    def __init__(
        self,
        zipf: zipfile.ZipFile,
        zanj_meta: dict,
        loaded_zanj: "LoadedZANJ",
    ):
        self._zipf: zipfile.ZipFile = zipf
        self._zanj_meta: JSONitem = zanj_meta
        # (path, item_type) pairs
        self._externals_types: dict[str, str] = {
            key: val["item_type"] for key, val in zanj_meta["externals_info"].items()
        }

        self._loaded_zanj: LoadedZANJ = loaded_zanj

        # validate by checking each external file exists
        for key, item_type in self._externals_types.items():
            if key not in zipf.namelist():
                raise ValueError(f"external file {key} not found in archive")

    def __getitem__(self, key: str) -> Any:
        if key in self._externals_types:
            item_type: str = self._externals_types[key]
            with self._zipf.open(key, "r") as fp:
                return GET_EXTERNAL_LOAD_FUNC(item_type)(self._loaded_zanj, fp)


# TODO: this needs to be refactored
class LoadedZANJ(typing.Mapping):
    """object loaded from ZANJ archive. acts like a dict."""

    def __init__(
        self,
        # config
        path: str | Path,
        zanj: _ZANJ_pre,
        loader_handlers: dict[str, LoaderHandler] | None = None,
        externals_mode: ExternalsLoadingMode = "lazy",
        format_error_mode: ErrorMode = "warn",
    ) -> None:
        # copy handlers
        self._loader_handlers: dict[str, LoaderHandler]
        if loader_handlers is not None:
            self._loader_handlers = loader_handlers
        else:
            self._loader_handlers = LOADER_MAP

        # path and zanj object
        self._path: str = str(path)
        self._zanj: _ZANJ_pre = zanj

        # config
        self._externals_mode: ExternalsLoadingMode = externals_mode
        self._format_error_mode: ErrorMode = format_error_mode

        # load zip file
        self._zipf: zipfile.ZipFile = zipfile.ZipFile(file=self._path, mode="r")

        # load data
        self._meta: dict = json.load(self._zipf.open(ZANJ_META, "r"))
        self._json_data: ZANJLoaderTreeNode = ZANJLoaderTreeNode(
            _parent=self,
            _data=json.load(self._zipf.open(ZANJ_MAIN, "r")),
        )

        # externals
        self._externals: LazyExternalLoader | dict
        if externals_mode == "lazy":
            self._externals = LazyExternalLoader(
                zipf=self._zipf,
                zanj_meta=self._meta,
                loaded_zanj=self,
            )
        elif externals_mode == "full":
            self._externals = dict()

            for fname, val in self._meta["externals_info"].items():
                item_type: str = val["item_type"]
                with self._zipf.open(fname, "r") as fp:
                    self._externals[fname] = GET_EXTERNAL_LOAD_FUNC(item_type)(self, fp)

    def __getitem__(self, key: str) -> Any:
        """get the value of the given key"""
        return self._json_data[key]

    def __iter__(self):
        return iter(self._json_data)

    def __len__(self):
        return len(self._json_data)
