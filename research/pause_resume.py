"""暂停/恢复指定 PID 的进程(Windows NtSuspendProcess)。

用法: python pause_resume.py suspend 4148   /   python pause_resume.py resume 4148
"""

import ctypes
import sys


def main():
    action, pid = sys.argv[1], int(sys.argv[2])
    PROCESS_ALL_ACCESS = 0x1F0FFF
    h = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if not h:
        raise SystemExit(f"OpenProcess({pid}) 失败,权限不足或进程已退出")
    fn = ctypes.windll.ntdll.NtSuspendProcess if action == "suspend" else ctypes.windll.ntdll.NtResumeProcess
    status = fn(h)
    ctypes.windll.kernel32.CloseHandle(h)
    if status != 0:
        raise SystemExit(f"{action} 失败,NTSTATUS=0x{status & 0xFFFFFFFF:08X}")
    print(f"已{'暂停' if action == 'suspend' else '恢复'}进程 {pid}")


if __name__ == "__main__":
    main()
