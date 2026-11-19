# 文件库清单

本文件是现状文档，直接改写。文件库是仓库外的一个文件夹，在仓库里以 `library/` 出现，不进 Git。规则见 [项目记忆规范](https://github.com/OrsonJyu/project-standards/blob/main/STANDARD.md) 5.1 节。

- 路径用代码格式写，例如 `library/localfiles/footage/`，不要写成链接：被忽略的文件在 GitHub 上打不开，校验也会报断链。
- `localdata/` 只写类别、数量和用途，不写受访者姓名等敏感信息。

## 文件库在哪

本机桌面上的 `Lab Studies in Systems Design` 文件夹，在本地磁盘上，**目前没有云盘或其他备份**（用户 2026-11-19 决定，以后要备份时再说）。`localdata/` 只有这一份，丢了无法从 GitHub 找回。

2026-11-19 按 5.1 节整理：已在仓库里的课件、PDF、Tutorial 文本、课堂活动照片与视频（含 Git LFS 对象，已核对远端存在）从文件库删除；失效的旧 worktree、旧仓库副本、停用的 `live-preview/` 脚本和 8 GB 解压镜像也已删除，代码都能从 GitHub 取回。

## localfiles：大文件

| 路径 | 内容 | 来源 / 怎么重新获得 |
|---|---|---|
| `library/localfiles/rock-4c-plus_bookworm_kde_r2.output_512.img.xz` | ROCK 4C+ Debian 12 bookworm KDE 系统镜像（1.4 GB），要刷卡时 `xz -dk` 解压 | Radxa 官方下载，见 [home 指南](guides/HOME_HARDWARE_AND_EXPERIMENT_GUIDE.md) |
| `library/localfiles/home_硬件连接与程序实验复现指南.md` | home 复现指南 v1.2.1 的导出版（链接改为绝对地址） | 仓库 tag `v1.2.1` 的 `docs/guides/HOME_HARDWARE_AND_EXPERIMENT_GUIDE.md` |

## localdata：调研数据和敏感资料

| 路径 | 内容 | 来源 | 备份在哪 |
|---|---|---|---|
| `library/localdata/Video_SD5531/SD5531-Demo/` | 正在使用的录制 Demo：`code/demo-installer` 分支 `demo.py` 的副本 + 4 个双击 `.command`；`recordings`、`.local/wired-lab.json` 是指向同组文件夹的相对软链接 | 分支 `code/demo-installer`（`dfc2147`） | 无 |
| `library/localdata/Video_SD5531/.local/` | 私有网络配置（`wired-lab.json`、摄像头源配置）和 home/school 网络检查记录，8 个 | 本机生成 | 无 |
| `library/localdata/Video_SD5531/recordings/` | 录制程序转存的事件片段与 JSON（2026-11 测试，约 170 个 MP4，可能拍到房间和人物），即 [D015](DECISIONS.md) 的 `Video_SD5531/recordings/` | 录制程序 | 无 |
| `library/localdata/Video_SD5531/recovery/` | 2026-11-05 SD 卡网络修复的备份（含私有 Wi-Fi 配置、rootfs 元数据镜像）和修复脚本 | [恢复实验](../project-camera/experiments/2026-11-05-home-wired-recovery/README.md) | 无 |
| `library/localdata/Video_SD5531/experiments/` | 4 个 2026-10-30 实验原始运行目录中未入库的部分（school 60 秒原片、预览图、含私有参数的脚本和日志） | [实验索引](../project-camera/experiments/README.md) | 无 |
| `library/localdata/presentation-raw/Photos-Videos/` | Assignment 3 实拍装置照片与视频，12 个（3.3 GB），可能拍到同学和校园 | 用户手机 | 无 |
| `library/localdata/presentation-raw/confluence-only/` | 只放在 Confluence 的两段演示视频，其中一段拍到同学 | 剪辑自上一项 | 无 |

## 只在文件库里的产出

超过 50 MB、没进仓库 `outcomes/` 的产出。

| 路径 | 内容 |
|---|---|
| `library/outcomes/SD5531 Assignment3.pdf` | Assignment 3 小组展示导出 PDF（54 MB） |
