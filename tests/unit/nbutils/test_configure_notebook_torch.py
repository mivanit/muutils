import torch

from muutils.nbutils.configure_notebook import configure_notebook


def test_configure_notebook():
    """Test configure_notebook which returns a torch.device."""
    device = configure_notebook(seed=42, plot_mode="ignore")
    assert isinstance(device, torch.device)
