import time

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
