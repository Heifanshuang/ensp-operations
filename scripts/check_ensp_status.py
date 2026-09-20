"""
检查 eNSP 相关进程状态的工具脚本。

用法：
    python check_ensp_status.py

返回：
    eNSP_Client.exe 是否运行
    eNSP_VBoxServer.exe 是否运行
    相关 VBox 进程数量
"""
import subprocess
import sys


def get_process_info(process_name):
    """查询指定进程是否运行，返回 (是否运行, 进程数)"""
    try:
        result = subprocess.run(
            ["tasklist", "/FI", f"IMAGENAME eq {process_name}", "/NH"],
            capture_output=True,
            text=True,
            encoding="gbk",
            errors="replace"
        )
        lines = [l for l in result.stdout.strip().split("\n") if l.strip() and process_name.lower() in l.lower()]
        return len(lines) > 0, len(lines)
    except Exception as e:
        return False, 0


def main():
    processes = [
        ("eNSP_Client.exe", "eNSP 客户端"),
        ("eNSP_VBoxServer.exe", "VBox 服务器"),
        ("VirtualBoxVM.exe", "VirtualBox 虚拟机"),
    ]

    print("=== eNSP 进程状态检查 ===")
    all_running = True
    for proc_name, desc in processes:
        running, count = get_process_info(proc_name)
        status = "运行中" if running else "未运行"
        print(f"  {desc:20s} ({proc_name:25s}): {status} ({count} 个进程)")
        if proc_name == "eNSP_Client.exe" and not running:
            all_running = False

    print()
    if all_running:
        print("✓ eNSP 客户端正在运行")
    else:
        print("✗ eNSP 客户端未运行")

    return 0 if all_running else 1


if __name__ == "__main__":
    sys.exit(main())
