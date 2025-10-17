#%%
import torch
import numpy as np
from muutils.dbg import dbg_tensor

# Different shapes
scalar = torch.tensor(42.0)
dbg_tensor(scalar)

vector = torch.randn(10)
dbg_tensor(vector)

matrix = torch.randn(5, 8)
dbg_tensor(matrix)

# With NaN values
nan_tensor = torch.randn(100, 100)
nan_tensor[0:20, 0:20] = float('nan')
dbg_tensor(nan_tensor)

# with Inf values
inf_tensor = torch.randn(100, 100)
inf_tensor[0:20, 0:20] = float('inf')
dbg_tensor(inf_tensor)

# Different dtypes
bool_tensor = torch.rand(50, 50) > 0.5
dbg_tensor(bool_tensor)

int_tensor = torch.randint(-1000, 1000, (50, 50), dtype=torch.int32)
dbg_tensor(int_tensor)

# CUDA if available
if torch.cuda.is_available():
    cuda_tensor = torch.randn(50, 50).cuda()
    dbg_tensor(cuda_tensor)

# NumPy
np_array = np.random.randn(50, 50)
dbg_tensor(np_array)

# With gradients
grad_tensor = torch.randn(50, 50, requires_grad=True)
dbg_tensor(grad_tensor)