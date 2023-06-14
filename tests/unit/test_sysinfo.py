from muutils.sysinfo import SysInfo


def test_sysinfo():
    sysinfo = SysInfo.get_all()
    # we can't test the output because it's different on every machine
    print(sysinfo)
    