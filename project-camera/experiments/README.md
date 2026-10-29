# 摄像头实验记录 / Experiments

每次测试一个文件夹：`YYYY-MM-DD-主题/`（例如 `2026-11-02-rtsp-read/`），内含 `README.md` 与原始证据（日志、截图、短片段）。日期写测试实际进行的日期。

- 实验记录建立后只追加，不改写结论；后来的复核另起一次实验并互相链接。
- 视频文件 `.MOV/.mov` 自动走 Git LFS；大体积的 `.mp4` 等需要先在 `.gitattributes` 中加规则再提交。
- 记录中不写摄像头密码、内网凭据或个人路径。
- 实验完成后更新对应工作流和 [EVIDENCE](../../docs/EVIDENCE.md)。

## 记录模板

复制下面内容到新文件夹的 `README.md`：

```markdown
---
id: exp-YYYY-MM-DD-主题
type: experiment
workstream: ws-preroll-recording
roadmap_stage: 1
---

# YYYY-MM-DD · 主题

- 问题与假设：
- 设备与版本：摄像头型号/固件、ROCK 4C+ 系统、FFmpeg、控制程序版本、源码提交 SHA
- 条件：网络、PoE、硬盘、机位
- 输入/操作：完整命令或步骤（去掉凭据）
- 预期：
- 实际观察：
- 时间对齐：事件时间、接收时间、片段实际起止
- 失败、缺失与限制：断流、关键帧、磁盘状态等
- 证据路径：
- 可确认的个人贡献：（无法确认就留空）
- 下一步：
```
