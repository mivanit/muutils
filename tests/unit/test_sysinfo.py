import pytest

from muutils.sysinfo import SysInfo


@pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning")
def test_sysinfo():
    sysinfo = SysInfo.get_all()
    # we can't test the output because it's different on every machine
    print(sysinfo)
