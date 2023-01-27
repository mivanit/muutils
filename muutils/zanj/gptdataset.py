import os
import abc
from functools import cached_property
from typing import Any, Callable, Generic, Literal, NamedTuple, Sequence, TypeVar, Union
from dataclasses import dataclass, field

import numpy as np
import torch
from torch.utils.data import Dataset
from muutils.tensor_utils import ATensor, NDArray, DTYPE_MAP, lpad_array, lpad_tensor

@dataclass(kw_only=True)
class GPTDatasetConfig(metaclass=abc.ABCMeta):
	"""base config class"""
	name: str
	device: torch.device = field(
		default_factory = lambda: torch.device("cuda" if torch.cuda.is_available() else "cpu")
	)
	dtype: torch.dtype|np.dtype = field(default_factory=lambda : torch.int16)
	seq_len_min: int|None
	seq_len_max: int|None
	
	@abc.abstractmethod
	def token_arr(self) -> list[str]:
		raise NotImplementedError()

	@abc.abstractmethod
	def padding_token_idx(self) -> int:
		raise NotImplementedError()

	def tokenizer_map(self) -> dict[str, int]:
		"""map from token to index"""
		return {
			t: i
			for i, t in enumerate(self.token_arr)
		}

	@classmethod
	@abc.abstractmethod
	def _dataset_class(cls) -> type:
		raise NotImplementedError("this should be implemented by subclasses!")

	def gpt_config_kwargs(self) -> dict:
		"""gpt model config with vocab size, context size, and padding token"""
		return dict(
			vocab_size = len(self.token_arr),
			n_positions = self.seq_len_max,
			pad_token_id = self.padding_token_idx(), # The id of the _padding_ token.
			bos_token_id = self.padding_token_idx(), # The id of the _beginning-of-stream_ token.
			eos_token_id = self.padding_token_idx(), # The id of the _end-of-stream_ token.
		)

	def tokenize_seq(self, seq: list[str]) -> ATensor:
		"""tokenize sequence"""
		return torch.tensor(
			[ self.tokenizer_map[t] for t in seq ], 
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
	def load(cls, data: dict) -> "DatasetConfig":
		# TODO: how to handle inheritance for loaders?
		raise NotImplementedError()


	def update_max_seq_len(self, slm: int):
		"""update max seq len if needed"""
		if self.seq_len_max is None:
			self.seq_len_max = slm
		elif slm < self.seq_len_max:
			self.seq_len_max = slm


	def pad_sequence(self, seq: ATensor):
		"""process TOKENIZED sequence into tensor, padding or truncating as needed"""
		if seq.shape[0] > self.seq_len_max:
			return seq[:self.seq_len_max]
		else:
			return np.concatenate([
				np.full((self.seq_len_max - seq.shape[0],), self.padding_token_idx(), dtype=seq.dtype),
				seq,
			])


@dataclass(kw_only=True)
class IndexedArray(metaclass=abc.ABCMeta):
	"""join a list of arrays into a single big one with indices
	
	mainly for allowing __getitem__ to work nice for datasets"""
	arr: ATensor
	idxs: ATensor

	def get_len(self, idx: int) -> int:
		return self.idxs[idx+1] - self.idxs[idx]

	def get_all_lengths(self) -> ATensor:
		return torch.cat([
			self.idxs[1:] - self.idxs[:-1],
			torch.tensor([self.arr.shape[0] - self.idxs[-1]], dtype=self.idxs.dtype, device=self.idxs.device),
		])

	@classmethod
	@abc.abstractclassmethod
	def from_sequences(cls, data: list[ATensor[("tokens")]]) -> "IndexedArray":
		"""process many sequences into a single array, keeping track of sequence start indices
		
		example:
		f( [[a,b,c], [d,e]] ) -> IndexedArray(
			arr = [a,b,c,d,e],
			idxs = [0,3],
		)
		"""
		arr: ATensor = torch.cat(data)
		idxs: ATensor = torch.cumsum( torch.tensor([ 0, *map(len, data) ]), dim = 0 )[:-1]
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



