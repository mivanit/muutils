import abc
import os
from dataclasses import dataclass, field
from typing import Sequence

import jaxtyping
import numpy as np
import torch
from torch.utils.data import Dataset


# "error: Only concrete class can be given where Type[Abstract] is expected"
# this is a mypy issue, see
# https://github.com/python/mypy/issues/5374
# https://github.com/python/mypy/issues/4717
@dataclass(kw_only=True)  # type: ignore
class GPTDatasetConfig(metaclass=abc.ABCMeta):
    """base config class"""

    name: str
    device: torch.device = field(
        default_factory=lambda: torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )
    )
    dtype: torch.dtype = field(default_factory=lambda: torch.int16)
    seq_len_min: int | None
    seq_len_max: int | None

    @abc.abstractmethod
    def token_arr(self) -> list[str]:
        raise NotImplementedError()

    @abc.abstractmethod
    def padding_token_idx(self) -> int:
        raise NotImplementedError()

    def tokenizer_map(self) -> dict[str, int]:
        """map from token to index"""
        return {t: i for i, t in enumerate(self.token_arr())}

    @classmethod
    @abc.abstractmethod
    def _dataset_class(cls) -> type:
        raise NotImplementedError("this should be implemented by subclasses!")

    def gpt_config_kwargs(self) -> dict:
        """gpt model config with vocab size, context size, and padding token"""
        return dict(
            vocab_size=len(self.token_arr()),
            n_positions=self.seq_len_max,
            pad_token_id=self.padding_token_idx(),  # The id of the _padding_ token.
            bos_token_id=self.padding_token_idx(),  # The id of the _beginning-of-stream_ token.
            eos_token_id=self.padding_token_idx(),  # The id of the _end-of-stream_ token.
        )

    def tokenize_seq(self, seq: list[str]) -> jaxtyping.Int[torch.Tensor, "n_tokens"]:
        """tokenize sequence"""
        return torch.tensor(
            [self.tokenizer_map()[t] for t in seq],
            dtype=self.dtype,
            device="cpu",
        )

    def serialize(self) -> dict:
        """serialize config to dict

        TODO: make it clear that this should be an abstract method
        """
        return {
            "name": self.name,
            "device": str(self.device),
            "dtype": str(self.dtype),
            "seq_len_min": self.seq_len_min,
            "seq_len_max": self.seq_len_max,
        }

    @classmethod
    @abc.abstractclassmethod
    def load(cls, data: dict) -> "GPTDatasetConfig":
        # TODO: how to handle inheritance for loaders?
        raise NotImplementedError()

    def update_max_seq_len(self, slm: int):
        """update max seq len if needed"""
        if self.seq_len_max is None:
            self.seq_len_max = slm
        elif slm < self.seq_len_max:
            self.seq_len_max = slm

    def pad_sequence(self, seq: jaxtyping.Int[torch.Tensor, "n_tokens"]):
        """process TOKENIZED sequence into tensor, padding or truncating as needed"""
        assert (
            len(seq.shape) == 1
        ), f"sequence to be padded should be 1d, got {seq.shape = }"
        # even with this assert, mypy still complains about the shape of seq

        if seq.shape[0] > self.seq_len_max:  # type: ignore[operator]
            return seq[: self.seq_len_max]
        else:
            # no idea why mypy complains about the signature of np.full here
            return np.concatenate(
                [
                    np.full(  # type: ignore[call-overload]
                        (self.seq_len_max - seq.shape[0],),  # type: ignore[operator]
                        self.padding_token_idx(),
                        dtype=seq.dtype,
                    ),
                    seq,
                ]
            )


@dataclass(kw_only=True)
class IndexedArray(metaclass=abc.ABCMeta):
    """join a list of arrays into a single big one with indices

    mainly for allowing __getitem__ to work nice for datasets"""

    arr: torch.Tensor
    idxs: jaxtyping.Int[torch.Tensor, "n_seqs"]

    def get_len(self, idx: int) -> int:
        return (self.idxs[idx + 1] - self.idxs[idx]).item()  # type: ignore[return-value]

    def get_all_lengths(self) -> torch.Tensor:
        return torch.cat(
            [
                self.idxs[1:] - self.idxs[:-1],
                torch.tensor(
                    [self.arr.shape[0] - self.idxs[-1]],
                    dtype=self.idxs.dtype,
                    device=self.idxs.device,
                ),
            ]
        )

    @classmethod
    @abc.abstractclassmethod
    def from_sequences(cls, data: Sequence[torch.Tensor]) -> "IndexedArray":
        """process many sequences into a single array, keeping track of sequence start indices

        example:
        f( [[a,b,c], [d,e]] ) -> IndexedArray(
                arr = [a,b,c,d,e],
                idxs = [0,3],
        )
        """
        arr: torch.Tensor = torch.cat(tuple(data))
        idxs: torch.Tensor = torch.cumsum(torch.tensor([0, *map(len, data)]), dim=0)[
            :-1
        ]
        return cls(arr=arr, idxs=idxs)


class GPTDataset(Dataset, metaclass=abc.ABCMeta):
    """wrapper for torch dataset with some extra functionality

    (meaning the functionality should be inherited in downstream classes)
    """

    def __init__(self, config: GPTDatasetConfig):
        self.config = config

    @abc.abstractmethod
    def get_all_lengths(self) -> list[int]:
        """get the lengths of all sequences"""
        raise NotImplementedError()

    @abc.abstractmethod
    def save(self, path: str):
        """save dataset to path"""
        raise NotImplementedError()

    def save_named(self, basepath: str):
        """save dataset to path with name"""
        self.save(os.path.join(basepath, self.config.name))
