# 来源与校验 / Provenance

[source-manifest.json](source-manifest.json) 记录归档输入，每条含来源组、组内相对路径、仓库路径、字节数、SHA-256 和 `git` / `git-lfs` 存储类型。来源间相同文件可对应同一个仓库路径；不同内容不能共享同一路径。

此表用于核对原始输入，不包含本次新编写的说明、知识网或导航页。讨论导出各自带 thread/turn ID；Figma 快照带抓取日期与节点 ID。

在取回 LFS 原件后运行：

```sh
python3 scripts/validate_repository.py --hash
git lfs fsck
```

校验通过只证明档案文件与清单一致，不证明其中的技术主张、实验方法或课程提交已经重新验证。
