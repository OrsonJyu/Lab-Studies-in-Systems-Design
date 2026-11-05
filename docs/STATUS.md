# 当前状态 / Current status

核对日期：**2026-11-05，香港**。[D014](DECISIONS.md)明确 home/school 共用有线配置；场地标签仍分别记录结果。完整接续见[上下文](handoffs/2026-11-05-shared-wired-baseline.md)。

| 项目 | 当前状态 | 依据 |
| --- | --- | --- |
| 课程与完整范围 | SD5531；豹纹守宫视频、热阵列、存储/访问、定位/识别探索和跨组对齐 | [SCOPE](SCOPE.md) |
| 主机与存储 | ROCK 4C+ / Debian 12 / aarch64；测试用系统 microSD；录像核对后移到 Mac 的 `recordings/`，ROCK 只暂存（D015）；SATA 仍未验收 | D002 / D012 / D015 |
| 共用网络 | 三个数据端接独立交换机；Mac Wi-Fi 仅外网；同一私有 JSON、同一 lab-wired，自动连接/优先级 100、有线无默认路由 | [统一指南](guides/SHARED_WIRED_NETWORK_GUIDE.md) |
| 旧配置整理 | 保留有线 UUID/地址；school-camera 改名 lab-wired；三份旧无线 profile 保留为手动，没有关闭全局射频 | [恢复实验](../project-camera/experiments/2026-11-05-home-wired-recovery/README.md) |
| home 开机恢复 | SD 检查发现有线不自启和待恢复日志；完成备份、恢复、单行修改；装卡启动及统一后正常重启均自动恢复 SSH | [结构化结果](../project-camera/experiments/2026-11-05-home-wired-recovery/result.json) |
| home 当前链路 | 主机密钥、静态地址/路由、端口和远端状态检查通过；重启后三秒解码 60 帧，无错误，未保存新录像 | [health](../project-camera/experiments/2026-11-05-home-wired-recovery/health-check.json) · [video](../project-camera/experiments/2026-11-05-home-wired-recovery/video-check.json) |
| 历史 home 媒体 | 合成基础保存、真实约 60 秒录像与完整解码，FFplay 动态画面由用户确认 | [实验索引](../project-camera/experiments/README.md) |
| school 后续短录 | 10-30 较早网络/预览后恢复板卡管理，17:40 起完成 60.001 秒、1200 帧、完整解码及复制哈希核对；JSON 已补录，原片本地保留 | [school 录像](../project-camera/experiments/2026-10-30-school-camera-recording/README.md) |
| school 新基线 | 2026-11-05 学校现场只读检查 9 项通过，录制程序连续运行约 2.5 小时保存 86 个完整事件；板卡中途失联一次、重插电恢复，原因未明（[记录](../project-camera/experiments/2026-11-05-school-recorder-first-run/README.md)）；旧热点/802.1X 观察不作为全部校园隔离证明 | [school](../project-camera/environments/school/README.md) |
| 码流与接口 | 主/子码流 2560×1440 / 800×448、20 fps，关键帧间隔实测 2 秒；ONVIF 公告运动事件（PullPoint），没有录像/回放服务；子码流解码约占 6 核 3.6% | [只读探测](../project-camera/experiments/2026-11-05-home-stream-probe/README.md) |
| 时间与录制服务 | ROCK 已于 2026-11-05 按 Mac 时间校准（偏差约 10 毫秒，重启后保持未验证）；摄像头时间已于同日按 ROCK 设置为手动时间（原慢约 28 天，修改后差 0.3 秒，[记录](../project-camera/experiments/2026-11-05-home-camera-clock-set/README.md)），断电后**不能保持**（学校现场断电后回到 NTP、慢约 8 小时），漂移未测；包时间戳/DTS、事件边界仍待核；通用持久录制服务未实现 | [当前工作流](workstreams/active/ws-preroll-recording.md) |
| 延迟 | 拍摄到 ROCK 约 0.23 秒（中位）；触发后才录会丢开头约 0.4 秒以上，需滚动缓存；预览显示与检测延迟未测 | [延迟实验](../project-camera/experiments/2026-11-05-home-latency/README.md) |
| 事件录制 | recorder 0.2：内存盘 2 秒分段缓存 + 子码流帧差运动检测（也可手动触发）；home 手挥动四个事件均自动录制，手出现前保留 3.7–4.65 秒，检测延迟约 0.5–0.65 秒；守宫场景阈值、断流恢复、长期运行未做 | [手挥动](../project-camera/experiments/2026-11-05-home-motion-hand-test/README.md) · [手动](../project-camera/experiments/2026-11-05-home-recorder-manual-trigger/README.md) · [代码](../project-camera/src/recorder/README.md) |
| 网页 | recorder 0.3 的局域网页面：实时画面、录制状态、带时间戳标记的时间轴和片段回放；无登录，只绑定隔离实验网；2026-11-05 用户在自己浏览器中确认可用（同期 6 个运动事件均保存成功，无断流或进程退出记录） | [说明](../project-camera/src/recorder/README.md) |
| 下一项实验 | 手部模拟运动触发、静止 n 秒结束、前段完整性和延迟；网站为后续可选，n/预录长度未定 | [接续上下文](handoffs/2026-11-05-shared-wired-baseline.md) |
| 尚未验收 | 预录制、SATA、长期/异常断电恢复、所有 Wi-Fi 兼容、热阵列/行为性能和跨组接口 | [ROADMAP](ROADMAP.md) |

确认了网络不自启的缺陷，同时也恢复了文件系统日志；未用单变量实验确定唯一根因。一次冷启动和一次正常重启不等于异常断电或持续服务恢复。共用配置不取消场地复测，也不等于已自动识别/切换任意 Wi-Fi。

## 已保存的成果

- 27 页展示 PDF、原始 PPTX、1 页跨组合作计划。
- 两份会议机器转录、AI 中文纪要与项目讲解；这些材料不是已由老师确认的纪要。
- Figma 2026-10-26 文字/节点快照及26 份有内容的顶层架构图 PNG；原设计仍含旧硬件及云端方案。
- In-Class Activity 6 的 8 题独立源码、ZIP、历史编译记录、串口图片与视频。
- 电路、焊接原始影像；未据文件存在推断课程提交或评分结果。
- 早期编程实现、模拟测试代码、板卡诊断程序和采集原始帧。

## 编程实验：需要保留的差异

原 README / HARDWARE_PROGRESS 记录八题编译通过和串口实机结果，但当时 Task 8 的手机动作画面缺失。本次在 Documents 工作目录另找到 **IMG_1320.MOV**；抽样画面可见板卡、手部和屏幕。现应记录为“已有补拍文件，完整短/长按覆盖待逐段复核”，不能继续说文件不存在，也不能仅凭抽样宣称验收完成。

Task 7 另有两份 `Real_Light.MOV`；Tasks 4/5 另有 `SerialMonitor2.mov`。原始说明保持不变，新增证据见 [EVIDENCE](EVIDENCE.md)。Task 1 仍未找到包含首次 `1500ms` 输出的新增截图，先保留待补/待复核状态。

课程平台提交：**未知**。历史助手仅准备文件，用户曾明确自行上传；没有收集到提交回执，不把旧“未上传”报告直接当作今天的事实。

## 下一步

参见 [ROADMAP](ROADMAP.md)。仓库导入完成度与项目实现完成度分开；具体文件覆盖及缺失源文件见 [SYNC_REPORT](SYNC_REPORT.md)。
