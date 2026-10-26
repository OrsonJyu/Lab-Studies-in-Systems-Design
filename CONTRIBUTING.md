# 维护与协作约定 / Contributing

本仓库同时服务访客、项目合作者和 agents。更新时保留材料来源、结论适用范围及前后变化。

1. 先阅读 [AGENTS.md](AGENTS.md) 和[当前状态](docs/STATUS.md)，确认课程与项目边界。
2. 新资料按用途归档：项目成果放 `project-camera/`，课堂实验放 `activities/`，解释与过程记录放 `docs/`，旧版放 `archive/`。原始文件保持内容不变。
3. 每项实验记录日期、设备/软件版本、方法、输入、观察结果、原始证据、失败与限制、贡献人（仅在可确认时填写）。
4. 决定发生变化时追加决定记录，说明替代了什么及依据。同步维护状态与知识网，不把建议写成已接受决定。
5. 使用清晰的提交标题，例如 `docs: update recording workflow decision`。新成果通过分支与 PR 评审；初始归档可直接建立已授权的仓库基线。
6. 修改后执行 `python3 scripts/validate_repository.py --hash`；涉及大文件时执行 `git lfs fsck` 并核对上传结果。
7. 更新 `CHANGELOG.md` 和 `VERSION`，为阶段里程碑建立同名 Git 标签。课程作业内容是否提交，应另留可核实记录。

不要上传账号凭据、摄像头密码或 API token。第三方资料保持原有归属；需要对外公开时先核实材料可分享范围。
