from typing import Callable, Type, Mapping, Sequence, Literal

from tqdm import tqdm

class TrainingProgress:
    def __init__(
            self, 
            epochs: int,
            dataloader: "torch.utils.data.DataLoader",
            fixed_width: int = 100,
            display_progress: Literal["epochs", "batches", "samples"] = "epochs",
            records_keys: Sequence[str] = ("loss", "accuracy", "grad_norm", "lr"),
            display_keys: Sequence[str] = ("loss", "accuracy"),
        ):
        """records stored per-batch"""
        # number of epochs, batches, and samples
        self.epochs_total: int = epochs
        self.batches_per_epoch: int = len(dataloader)
        self.batches_total: int = self.batches_per_epoch * epochs
        self.samples_per_epoch: int = len(dataloader.dataset)
        self.samples_total: int = self.samples_per_epoch * epochs

        # training records
        self.records: Mapping[str, dict[int, float]] = {key: dict() for key in records_keys}
        self.records_keys: Sequence[str] = records_keys
        
        # progress bar
        self.fixed_width: int = fixed_width
        self.current_epoch: int = 0
        assert all(key in records_keys for key in display_keys), f"all display_keys must be in records_keys, an element in '{display_keys}' not in '{records_keys}'"
        self.display_keys: Sequence[str] = display_keys
        assert display_progress in ("epochs", "batches", "samples"), f"display_progress must be one of 'epochs', 'batches', or 'samples', got {display_progress}"
        self.display_progress: Literal["epochs", "batches", "samples"] = display_progress
        self.pbar: tqdm

        # single progress bar if over epochs, multiple otherwise
        self.multibar: bool = not (self.display_progress == "epochs")
        self.pbar_total: int = (
            self.batches_per_epoch if self.display_progress == "batches" else
            self.samples_per_epoch if self.display_progress == "samples" else
            self.epochs_total
        )

    def _get_desc(self) -> str:
        if self.multibar:
            return f"Epoch {self.current_epoch+1}/{self.epochs_total}"
        else:
            return f"Training"

    def __enter__(self):
        self.pbar = tqdm(
            total=self.pbar_total,
            desc=self._get_desc(),
            position=0,
            leave=True,
            ncols=self.fixed_width,
            dynamic_ncols=False,
        )
        return self

    def __exit__(self, exc_type: Type, exc_val: Exception, exc_tb: "TracebackType"):
        # TODO: write to training records?
        self.pbar.close()

    def update(self, batch_idx: int, records: Mapping[str, float]) -> None:
        """update records and progress bar"""
        # update records
        for key in self.records_keys:

        self.pbar.set_postfix({"loss": f"{loss:.3f}", "accuracy": f"{accuracy:.3f}"}, refresh=False)
        self.pbar.update(1)

    def next_epoch(self):
        self.current_epoch += 1
        self.pbar.close()
        self.pbar = tqdm(total=self.num_batches, desc=f"Epoch {self.current_epoch+1}/{self.num_epochs}", position=0, leave=True, ncols=self.fixed_width, dynamic_ncols=False)