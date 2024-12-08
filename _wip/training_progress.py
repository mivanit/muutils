from pathlib import Path
from types import TracebackType
from typing import Literal, Mapping, Sequence, Type

from tqdm import tqdm

IntervalType = Literal["epochs", "batches", "samples"]


class TrainingProgress:
    def __init__(
        self,
        # required
        epochs: int,
        dataloader: "torch.utils.data.DataLoader",
        # saving:
        model: "zanj.torchutil.ConfiguredModel|None" = None,
        base_path: str | Path | None = None,
        zanj: "zanj.Zanj|None" = None,
        model_save_path_final: str | None = "model.final.zanj",
        model_save_path_except: str | None = "model.exception.zanj",
        # records
        model_records_key: str = "training_records",
        records_keys: Sequence[str] = ("loss", "accuracy", "grad_norm", "lr"),
        records_save_path_external: str = "training_records.json",
        # checkpoints
        model_save_path_checkpoint: str = "checkpoints/checkpoint-{checkpoint}.zanj",
        interval_checkpoint: str | tuple[int | None, IntervalType] = (None, "epochs"),
        # progress bar config
        fixed_width: int = 100,
        pbar_disable: bool = False,
        display_progress: IntervalType = "batches",
        display_keys: dict[str, str] = {"loss": "L", "accuracy": "A"},
    ):
        """progress bar and training records saving context manager

        given a number of epochs and dataloader, creates progress bars and stores training records
        - you should call `update` periodically for batches, passing the index of the batch (in the epoch) and a dict of records
        - you should call `next_epoch` at the end of each epoch

        # Parameters:
         - `epochs : int`
            number of epochs
         - `dataloader : torch.utils.data.DataLoader`
            dataloader to get the number of batches and samples per epoch
         - `model : zanj.torchutil.ConfiguredModel|None`
            optional model to save records to (primarily for use with `zanj`)
           (defaults to `None`)
         - `model_save_path_except : str | None`
            path to save the model to if an exception occurs
           (defaults to `"model.exception.zanj"`)
         - `model_records_key : str`
            key to save records to in the model (if `model` is not `None`)
           (defaults to `"training_records"` -- the default for a `zanj.torchutil.ConfiguredModel`)
         - `zanj : zanj.Zanj|None`
            optional configured `zanj` instance to save the model with, passed to `model.save()`
           (defaults to `None`)
         - `records_keys : Sequence[str]`
            keys to save records for -- records are `dict[str, dict[int, float]]` where outer dict has record names as keys, and inner dict has overall batch index as keys and record values as values
           (defaults to `("loss", "accuracy", "grad_norm", "lr")`)
         - `fixed_width : int`
            width of the progress bar
           (defaults to `100`)
         - `display_progress : Literal["epochs", "batches", "samples"]`
            how to display samples -- "epochs" means one progress bar, others mean a progress bar for each epoch
           (defaults to `"epochs"`)
         - `display_keys : _type_`
            record keys to display in the progress bar
           (defaults to `{"loss": "L", "accuracy": "A"}`)
        """
        # number of epochs, batches, and samples
        self.epochs_total: int = epochs
        self.batches_per_epoch: int = len(dataloader)
        self.batches_total: int = self.batches_per_epoch * epochs
        self.samples_per_epoch: int = len(dataloader.dataset)
        self.samples_total: int = self.samples_per_epoch * epochs

        # training records
        self.records: Mapping[str, dict[int, float]] = {
            key: dict() for key in records_keys
        }
        self.records_keys: Sequence[str] = records_keys
        self.model: "zanj.torchutil.ConfiguredModel|None" = model
        self.model_save_path_except: str | None = model_save_path_except
        self.zanj: "zanj.Zanj|None" = zanj

        # progress bar
        self.fixed_width: int = fixed_width
        self.current_epoch: int = 0
        self.current_batch_in_epoch: int = 0
        assert all(
            key in records_keys for key in display_keys
        ), f"all display_keys must be in records_keys, an element in '{display_keys}' not in '{records_keys}'"
        self.display_keys: Sequence[str] = display_keys
        assert (
            display_progress
            in (
                "epochs",
                "batches",
                "samples",
            )
        ), f"display_progress must be one of 'epochs', 'batches', or 'samples', got {display_progress}"
        self.display_progress: Literal["epochs", "batches", "samples"] = (
            display_progress
        )
        self.pbar: tqdm

        # single progress bar if over epochs, multiple otherwise
        self.multibar: bool = not (self.display_progress == "epochs")
        self.pbar_total: int = (
            self.batches_per_epoch
            if self.display_progress == "batches"
            else (
                self.samples_per_epoch
                if self.display_progress == "samples"
                else self.epochs_total
            )
        )

    def _get_desc(self) -> str:
        return f"Epoch {self.current_epoch+1}/{self.epochs_total}"

    def __enter__(self):
        self.pbar = tqdm(
            total=self.pbar_total,
            desc=self._get_desc(),
            position=0,
            leave=True,
            ncols=self.fixed_width,
            dynamic_ncols=False,
            disable=self.pbar_disable,
        )
        return self

    def __exit__(self, exc_type: Type, exc_val: Exception, exc_tb: TracebackType):
        # if the model was passed
        if self.model is not None:
            # add records
            if self.model_records_key is not None:
                # add records to model
                if getattr(self.model, self.model_records_key, None) is None:
                    # create a dict
                    setattr(self.model, self.model_records_key, self.records)
                elif isinstance(getattr(self.model, self.model_records_key), dict):
                    # add to existing dict
                    getattr(self.model, self.model_records_key).update(self.records)
                else:
                    # unexpected type
                    raise TypeError(
                        f"model_records_key '{self.model_records_key}' must be a dict, got {type(getattr(self.model, self.model_records_key))}"
                    )

            # if error
            if exc_type is not None:
                # add exception info
                getattr(self.model, self.model_records_key)["exception"] = dict(
                    type=str(exc_type),
                    value=str(exc_val),
                    traceback=str(exc_tb),
                )
                # save the model
                self.model.save(self.model_save_path_except, zanj=self.zanj)

        # close the progress bar
        self.pbar.close()

    def update(self, batch_in_epoch_idx: int, records: Mapping[str, float]) -> None:
        """update records and progress bar, call once a batch is complete"""
        # update records
        for key in records:
            self.records[key][
                self.current_epoch * self.batches_per_epoch + batch_in_epoch_idx
            ] = records[key]

        self.pbar.set_postfix({key: records[key] for key in self.display_keys})
        self.pbar.update(batch_in_epoch_idx - self.current_batch_in_epoch)
        self.current_batch_in_epoch = batch_in_epoch_idx

    def next_epoch(self) -> None:
        """call at the end of each epoch"""
        self.current_epoch += 1
        self.current_batch_in_epoch = 0
        if self.multibar:
            self.pbar.close()
            self.pbar = tqdm(
                total=self.pbar_total,
                desc=self._get_desc(),
                position=0,
                leave=True,
                ncols=self.fixed_width,
                dynamic_ncols=False,
                disable=self.pbar_disable,
            )
        else:
            self.pbar.set_description(self._get_desc())
