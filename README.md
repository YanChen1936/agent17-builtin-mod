# Agent17 内置修改器（Cheat Menu）

> 📖 **第一次用？先看 [使用说明.md](使用说明.md)（保姆级步骤，5 分钟装好）。**

适用于 Ren'Py 游戏 **Agent17 0.26.10** 的独立内置修改器，单文件实现，不依赖任何第三方库或游戏本体改动。

- 当前版本：**v7.4.5**
- 引擎：Ren'Py 8.5.2
- 入口：主界面「修改器」按钮，或 **F9** 全局开关
- 关闭：右上角 **X** / **Esc**

## 文件清单

| 文件 | 说明 |
|---|---|
| `game/script/ActorScript/cheat_menu.rpy` | 修改器主源码（全部 UI + 逻辑） |
| `game/script/Menu/homemenu.rpy` | 游戏主界面入口（`if g_cheat_open: use cheat_menu_main`） |
| `renpy/audio/audio.py` | 引擎补丁：WASAPI 初始化失败时按 directsound → winmm → dummy 重试，避免“无声音 + 动画变静态” |

> 其余游戏资源（archive.rpa、图片、视频、lib、renpy 主体）不在仓库内，见 `.gitignore`。

## 安装

1. 把 `game/script/ActorScript/cheat_menu.rpy` 覆盖到游戏对应路径；
2. 删除同目录下旧的 `cheat_menu.rpyc`（游戏会自动重新编译）；
3. 如需修复音频/动画问题：用仓库里的 `renpy/audio/audio.py` 覆盖游戏同名文件；
4. 启动游戏，主界面点「修改器」或按 `F9`。

回滚：用 `git checkout <tag>` 取对应版本，或恢复 `_backup_20261107/` 下的备份。

## 功能

- **快捷页（默认）**：金币 +1万 / 拉满、银行卡、全角色好感/胁迫/友谊/心情/认识、全技能满级、解锁全图鉴、解除角色锁定、时间 +1 天、天气晴、快照存档、自动存档、常用入口。
- **金钱 / 玩家 / 角色 / 技能 / 物品 / 其他 / 任务 / 每日 / 图鉴 / 房间 / 变量 / 快照** 12 个分类页。
- **角色页**：左侧角色列表（可搜索），右侧好感 / 胁迫 / 友谊 / 心情 / 身体数值 / 状态标记 / H 计数；底部「全角色批量」面板。
- **全局搜索**（顶部）：角色、任务、物品、房间、变量、书籍、图片、贴纸、音乐、卡片、日记；点击结果跳转到对应页。
- **操作反馈**：执行后底部弹出结果提示；空结果有明确引导。
- **安全网**：一键快照 / 自动存档；引导层提示“改大数值前先快照”。

## 已知限制

- Ren'Py 输入框对**中文输入法组字**支持很差：英文/数字可直接输入，中文请复制后 `Ctrl+V` 粘贴（所有输入框已开启 `copypaste`）。
- 物品页只搜索“物品”；书籍/菜谱/图片等请用顶部「全局搜索」。
- 0.26.10 资源包本身缺失 34 个被脚本引用的动画，对应场景会显示静态图，与修改器无关。

## 验证流程

```powershell
# 1) 静态检查
.\Agent17.exe "<游戏目录>" lint

# 2) 隔离预览（另建临时工程，仅复制 cheat_menu.rpy）
#    show screen cheat_menu_main + renpy.screenshot，目视核对布局

# 3) 真机启动，确认无 traceback.txt / errors.txt
```

最近一次验证：lint 通过（862 menus / 173 images / 469 screens），真机启动无报错，`cheat_menu.rpyc` 正常重编译。

## 版本历史

| 版本 | 内容 |
|---|---|
| v7.4.5 | 输入框可点击区域改为整框；开启 Ctrl+V 粘贴；新增「显示全部」物品浏览 |
| v7.4.4 | 搜索重做：物品/全局搜索支持中文译名，全局搜索覆盖书籍等图鉴，结果浮层可见，空结果反馈 |
| v7.4.3 | 字体放大加粗；输入框套可见外框；X/? 居中；导航滚动条联动 |
| v7.4.2 | 角色页列表固定高度 + 底部批量面板；滚动条真实联动、内容不足自动隐藏 |
| v7.4.1 | 显式按钮文字样式，修复继承游戏 `button_text` 导致的文字溢出 |
| v7.4 | 快捷页改双栏仪表盘，等宽瓦片栅格 |
| v7.3 | 「Aurora」视觉重制（石墨黑 + 琥珀金） |
| v7.2 | 新手引导、快捷页、分组导航、F9 热键、操作反馈 |
| v7.1 | 启动崩溃修复（style 属性 / 自检误报） |

## 相关开源项目（参考，非本仓库）

- [DiaDia9889/auto-cheat-renpy](https://github.com/DiaDia9889/auto-cheat-renpy) — 自动分析 Ren'Py 代码并在选项中提示数值变化。
- [kmertkun/renpy-tr-yama-hile](https://github.com/kmertkun/renpy-tr-yama-hile) — 针对个别游戏的土耳其语补丁/作弊菜单。
- [Tao6634/slg_commander66](https://github.com/Tao6634/slg_commander66) — Agent17 的**外部存档修改器**（非内置菜单）。
- [ricardol96/renpy_save_editor](https://github.com/ricardol96/renpy_save_editor) — 通用 Ren'Py 存档编辑器。
