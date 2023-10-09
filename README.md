# Lovemilk Minecraft China Mainland Login Fix Tools
* 从 [Minecraft CN Login Fix Tool](https://github.com/SkyDynamic/MinecraftCNLoginFixTool) 重构 UI 而来, 与原作者无关 <br>
~~实际上就用了下 ip_data.py, 参考了下 UI, 其他全部重写(xd~~
* 一个基于修改 Hosts 让中国大陆用户登录 Minecraft 国际版(Java / 基岩) 不再困难的软件


## 如何使用
* ### Windows 用户
  1. 通过 [Releases](/../../releases) 下载最新发行版, 解压运行
  2. 打开软件后, 单击上方的延时测试
  3. 单击 下方表格中延时最小的一项左侧显示 IP 的按钮
  4. 享受畅快登录的快感
* ### Linux 用户(需要 root 权限) / MacOS 用户(未经测试)
  > 如果您是 Linux 或 MacOS 用户, 我们默认您已经掌握了如何安装 Python3.11 和 git
  1. 安装 [Python3.11](https://www.python.org/downloads/release/python-311/)
  2. 克隆本仓库 (运行 `git clone <仓库地址>`, <> 内代表必填内容, 运行时无需携带该符号) <br>
  如果显示 `git` 命令没有找到, 请先[安装 `git`](https://git-scm.com/)
  1. 如果 `git` 您不会安装, 可以单击界面右上角绿色的 `Code` 按钮, 选择 `Download ZIP` 后将下载下了的 zip 压缩包解压并安装所需库: 运行如下指令 `pip install -r requirements.txt` <br>
  (**如果下载过慢, 可以使用清华大学的 pypi 源**, 运行如下指令 `pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`)
  1. 注意: 建议您使用 venv 以获得干净的全局 Python 环境
  2. 安装后, 使用 Python3.11 运行 `main.py`
  3. 待 UI 窗口出现后, 单击上方的延时测试
  4. 单击 下方表格中延时最小的一项左侧显示 IP 的按钮
  5. 享受畅快登录的快感

### 当你不想要这些之后可以点击 "删除已改 Hosts" 清理本软件添加的hosts

> [!NOTICE]
> 温馨提示: 本软件支持向下兼容删除使用 `Minecraft CN Login Fix Tool` 所修改的 Hosts, 您可以无需在上述软件内清除 Hosts 后方可使用本软件
