from exectools import ExecExport


if __name__ == '__main__':
    ExecExport("~/Desktop/test_exec_tools_empty.xlsx").to_excel([dict(No=111, display_name="123")])
