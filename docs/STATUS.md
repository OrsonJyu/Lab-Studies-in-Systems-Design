# 当前状态 / Current status

核对日期：**2026-10-30，香港**。已有 **home** 短录基线与后续 **school** 网络/预览记录（[D011 / D013](DECISIONS.md)）。最新用户选择为学校全有线预览。课堂历史、home 录像与学校网络结果分别记录。

## 项目基线与本次进展

| 项目 | 当前状态 | 依据 |
| --- | --- | --- |
| 课程与目标 | SD5531；豹纹守宫观察、记录与学习支持，完整范围未缩小 | [SCOPE](SCOPE.md) |
| 主机 | ROCK 4C+，Debian 12 bookworm、aarch64，已通过 SSH 操作 | [home 环境](../project-camera/environments/home/README.md) |
| 项目存储方向 | SATA 机械硬盘仍保留；本阶段按用户要求先测试系统 microSD（D012） | [DECISIONS](DECISIONS.md) |
| 摄像头与供电 | 实物标称 4MP / 2.8mm / PoE 48V 4W；普通交换机配独立 PoE 供电器；ONVIF 读取及 RTSP/TCP 接收成功 | [home 实物记录](../project-camera/environments/home/hardware-observations.json) |
| 系统卡基础保存 | 60 秒合成片段保存、读回及完整软件解码通过 | [系统卡实验](../project-camera/experiments/2026-10-30-home-system-card/README.md) |
| 实物短录像 | 60.001 秒，H.264，2560 × 1440，约 20 fps；1201 帧，完整解码通过，末段可见手进入画面 | [真实录像实验](../project-camera/experiments/2026-10-30-home-camera-recording/README.md) |
| home Mac 实时预览 | ROCK 转发到 Mac 本机，FFplay 动态画面由用户确认；延迟未量测 | [home 预览实验](../project-camera/experiments/2026-10-30-home-live-preview/README.md) |
| 时间与持续部署 | OSD 日期不正确、存在包时间戳/DTS 警告；网络辅助地址未持久化；尚无完整服务部署 | [录像限制](../project-camera/experiments/2026-10-30-home-camera-recording/README.md) |
| 分段缓存、事件和预录制 | 尚未实现/验收；SATA、长期及故障恢复均未通过本次测试 | [当前工作流](workstreams/active/ws-preroll-recording.md) |
| school 最终有线预览 | 摄像头 → 交换机 → Mac / IINA；TCP 端口、2560 × 1440 H.264 / 报告 20 fps、三秒解码及用户预览确认通过；Mac 线协商为 100 Mbps 全双工 | [school 实验](../project-camera/experiments/2026-10-30-school-network-preview/README.md) |
| school 板卡管理 | 阶段中有线/无线 SSH 曾成功；末次固定有线 IPv4/SSH 未恢复，IPv6 只有 ICMP 回应；保存的静态配置为手动启用 | [school 档案](../project-camera/environments/school/README.md) |
| school 热点与校园网 | ROCK AP 无线 SSH 由用户确认；iPhone/IINA 预览可见但用户报告网络差；电脑热点 FFplay 黑屏不记成功；macOS 拒绝 802.1X 来源共享，未证明校园全局隔离 | [school 分变体记录](../project-camera/environments/school/README.md) |
| school 录像与持续性 | 没有学校新录像；SATA、预录制、时钟、长期性能和重启恢复未验收；通用 hotspot 环境仍预留 | [学校配置与恢复指南](guides/SCHOOL_NETWORK_AND_PREVIEW_GUIDE.md) |
| 热阵列、定位/识别、行为信息、跨组接口 | 规划/探索，性能与责任需验证或共同确认；数据库和消息栈仍待选择 | [完整范围](SCOPE.md) |

每项结果只适用于各自记录的环境与变体。home 的短录不能替代学校录像；Mac 直接有线预览成功也不证明 ROCK 的管理已恢复。短检查不等于全天稳定、预录制完成或事件时间准确；既往超时/黑屏没有确定的唯一原因。

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
