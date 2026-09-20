---
name: ensp-operations
description: "华为 eNSP (Enterprise Network Simulation Platform) 网络仿真平台的桌面操作 Skill。用于启动 eNSP 客户端、打开/新建拓扑文件、启动/停止网络设备、打开设备 CLI 命令行界面、保存拓扑以及关闭 eNSP。当用户提到 eNSP、华为网络仿真、ensp 拓扑、ensp 实验、ensp 设备操作等场景时使用此 Skill。基于 computer_use_tool plane='cu' 进行 GUI 自动化操作。"
---

# eNSP 网络仿真平台操作

## 概述

本 Skill 用于在 Windows 桌面上操作华为 eNSP 网络仿真软件，完成从启动软件、加载拓扑、控制设备到关闭软件的完整流程。

**软件路径**：`E:\eNSP\eNSP_Client.exe`（主程序）
**VBox 服务器**：`E:\eNSP\vboxserver\eNSP_VBoxServer.exe`
**示例拓扑目录**：`E:\eNSP\examples\`

## 核心操作流程

所有 GUI 操作均通过 `computer_use_tool` 的 `plane="cu"` 完成。每次关键操作前必须截图观察当前界面状态，再根据截图定位坐标。

### 1. 启动 eNSP

**前置条件**：确认 eNSP 未在运行。

```python
import seed_computer_use as cu

# 方式一：通过 list_apps + launch_app 启动（推荐）
apps = cu.list_apps()
ensp_apps = [a for a in apps if "ensp" in a.name.casefold()]
print("找到的 eNSP 应用:", ensp_apps)
if ensp_apps:
    cu.launch_app(ensp_apps[0].name)
else:
    # 方式二：直接通过可执行文件路径启动
    import subprocess
    subprocess.Popen(r"E:\eNSP\eNSP_Client.exe")

# 等待启动完成并截图确认
cu.wait(5)
cu.screenshot()
```

**注意**：eNSP 启动较慢，首次加载可能需要 10-30 秒。启动后应看到主窗口，左侧为设备树，右侧为拓扑编辑区。

### 2. 打开拓扑文件

支持两种方式：

**方式 A：通过菜单打开**
1. 点击菜单栏「文件」→「打开」（或 Ctrl+O）
2. 在文件对话框中导航到目标 `.topo` 文件
3. 选中并点击「打开」

**方式 B：直接双击打开**
1. 在资源管理器中找到 `.topo` 文件
2. 双击即可用 eNSP 打开

**常用示例拓扑路径**：
- 单区域 OSPF：`E:\eNSP\examples\2-1Single-Area OSPF\`
- BGP 基础：`E:\eNSP\examples\3-1BGP&EBGP\`
- 校园网：`E:\eNSP\examples\Campus_Network\`
- HCNA 实验：`E:\eNSP\examples\HCNA2.0 Lab\`

### 3. 设备操作

#### 启动设备
- **单个设备**：右键点击拓扑中的设备图标 → 选择「启动」
- **全部设备**：菜单栏「设备」→「全部启动」，或点击工具栏的绿色启动按钮

#### 停止设备
- **单个设备**：右键点击设备图标 → 选择「停止」
- **全部设备**：菜单栏「设备」→「全部停止」

#### 打开设备 CLI
- **双击设备图标**：直接打开该设备的 CLI 命令行窗口
- 或右键设备 → 选择「CLI」

**注意**：设备必须先启动完成（图标变绿/状态灯正常），CLI 才能正常进入。启动过程中设备图标会闪烁。

### 4. 保存拓扑

- 快捷键：`Ctrl + S`
- 或菜单栏「文件」→「保存」
- 首次保存需选择保存路径和文件名（.topo 格式）

**关键坑：另存为对话框里 cu.type() 不生效，必须用剪贴板粘贴**

eNSP 的"另存为"对话框使用特殊输入控件，`cu.type()` 直接打字完全无效（光标在但字进不去）。**唯一可靠的方法是用剪贴板粘贴**：

```python
import seed_computer_use as cu

# 1. 按 Ctrl+S 触发另存为
cu.hotkey("ctrl", "s")
cu.wait(2)  # 等待对话框弹出

# 2. 点击文件名输入框确保焦点（对话框底部，文件名(N): 右侧）
cu.click(495, 630)
cu.wait(0.5)

# 3. 用剪贴板粘贴文件名（不要用 cu.type()，对这个对话框无效！）
cu.set_clipboard("my-lab.topo")
cu.wait(0.3)
cu.hotkey("ctrl", "v")
cu.wait(1)

# 4. 点击"保存(S)"按钮（对话框右下角）
cu.click(620, 638)
cu.wait(2)
```

> 坐标基于 1920×1080 分辨率，实际使用前必须截图校准。

### 5. 关闭 eNSP

1. 先停止所有运行中的设备（避免 VBox 进程残留）
2. 关闭 eNSP 主窗口（Alt+F4 或点击关闭按钮）
3. 确认 VBox 服务器进程已退出

**验证关闭**：
```python
import subprocess
result = subprocess.run(["tasklist", "/FI", "IMAGENAME eq eNSP_Client.exe"], 
                       capture_output=True, text=True)
print(result.stdout)
```

## 操作注意事项

1. **截图优先**：每次点击前必须截图确认界面状态，eNSP 的工具栏和菜单位置可能因窗口大小变化而偏移。
2. **等待设备启动**：AR 路由器设备启动通常需要 30-60 秒，期间不要重复点击。
3. **坐标基准**：cu 使用 0-1000 相对坐标，根据截图中元素位置换算。
4. **多窗口处理**：打开 CLI 后会弹出新窗口，需要重新截图定位新窗口中的操作区域。
5. **保存习惯**：修改拓扑后及时保存，避免意外丢失。

## 常见问题

| 问题 | 解决方案 |
|------|----------|
| eNSP 启动后设备无法启动 | 检查 VirtualBox 是否正常运行，eNSP_VBoxServer.exe 是否启动 |
| CLI 窗口打不开 | 确认设备已完全启动（状态灯变绿），再双击设备 |
| 拓扑文件打开失败 | 确认文件路径正确，且 eNSP 版本兼容该拓扑文件 |
| 设备启动卡住 | 停止设备后重新启动，或重启 VBox 服务器 |

---

## 实操踩坑记录（必看！）
### 1. USG6000V 防火墙登录避坑
- **默认账号密码**：admin / Admin@123
- **首次登录必须修改密码**：要求大写+小写+数字+特殊字符，新密码如 `Huawei@123`
- **绝对不要选n拒绝改密码**：输入n会直接超时退回登录界面，必须输入y修改
- **登录后等待3-5秒**，再按回车进入命令行

### 2. CLI 命令输入技巧
- **先点击CLI窗口激活焦点**，再用 `cu.type()` 整段输入命令，不要分多次按按键
- **cu.press() 不支持 "-" 横杠按键**，所有带横杠的命令（如 `int gigabitethernet 1/0/0`）直接整段type就行
- 每条命令输完后自动加回车，不要单独按enter

### 3. 拓扑连线技巧
- 用左侧Auto闪电图标连线最方便：先点第一个设备→选对应接口→再点第二个设备→选对应接口，自动完成链路
- 连线完成后，必须**点击工具栏上的白色箭头选择工具**退出连线模式，否则双击设备打不开配置窗口

### 4. PC 终端配置避坑
- 双击PC打开图形配置窗口，**不要依赖Tab键跳转输入框**，Tab顺序不可控，容易跳到MAC地址或其他无关位置
- 每个IP输入框先点击激活，按Ctrl+A全选原有内容，再输入新数字
- 输入顺序：IP地址4个段 → 子网掩码4个段 → 网关4个段，全部输完点"应用"按钮
- 中文输入在PC配置框和保存对话框中可能失效，优先用英文文件名

### 5. 保存拓扑避坑（实测验证）
- **【核心坑】cu.type() 在另存为对话框里完全无效**——光标看起来在输入框里，但打什么字都进不去。这是 eNSP 对话框的特殊输入控件导致的。
- **唯一可靠方法：剪贴板粘贴**：`cu.set_clipboard("文件名.topo")` 然后 `cu.hotkey("ctrl", "v")`，实测 100% 成功。
- 中文文件名同样可以通过剪贴板粘贴输入（如果系统输入法支持），但建议优先用英文文件名避免编码问题。
- 导航到目标路径太慢时，直接在文件名输入框输入**完整绝对路径**（如 `C:\Users\xxx\Desktop\fw-lab.topo`），系统会自动识别。
- 关闭 eNSP 时会弹出"是否保存"提示，选"否"则未保存的拓扑会丢失，记得先存盘。

---

## 完整实验示例：USG6000V双PC防火墙实验
### 拓扑结构
```
PC1 (内网) ──── FW1 (GE1/0/0)  FW1 (GE1/0/1) ──── PC2 (外网)
```

### 配置步骤
1. 拖入1台USG6000V + 2台PC，Auto连线
2. 启动FW1，等待2-3分钟加载完成
3. 双击FW1打开CLI，登录并改密码
4. 进入系统视图，执行以下配置：
```
sysname FW1
interface GigabitEthernet 1/0/0
 ip address 192.168.1.1 24
 quit
interface GigabitEthernet 1/0/1
 ip address 10.0.0.1 24
 quit
firewall zone trust
 add interface GigabitEthernet 1/0/0
 quit
firewall zone untrust
 add interface GigabitEthernet 1/0/1
 quit
security-policy
 rule name permit_trust_untrust
  source-zone trust
  destination-zone untrust
  action permit
  quit
 quit
```
5. 配置PC1：IP=192.168.1.10/24，网关=192.168.1.1
6. 配置PC2：IP=10.0.0.10/24，网关=10.0.0.1
7. PC1 ping PC2 验证连通性

## 参考资源

- 示例拓扑目录：`E:\eNSP\examples\`
- 帮助文档：`E:\eNSP\help\eNSP 帮助.chm`
