# 用 Git + Markdown 管理项目记忆：给 agent 的操作指南

**适用对象**：任何要长期维护一个 Git 仓库、把它当作"项目记忆"来读写的 agent（或人）。
**一句话**：记忆就是仓库里的 markdown 文件；用列目录、搜索、读文件来找，用有说明的 commit 来改；当前文件只说"现在是什么"，"过去怎么变过来的"交给 Git 历史。

本指南整理自小红书用户 templater 2026-10-28 的分享《看了 Personal Agent 发现 RAG 记忆已经过时了》，以及该分享引用的公开拆解（见文末来源），并加入本仓库的实际做法。原文是对他人产品的逆向观察和推演，这里取的是做法，不代表任何产品的官方设计。

---

## 1. 为什么用文件当记忆

- **文件工具就是记忆接口。** agent 本来就会 `ls`、`grep`、`cat`。记忆放在同一个文件空间里，就不需要另造一套接口。
- **搜索之后还能往下走。** 搜索返回的是文件路径，agent 可以接着读上下文、看相邻记录、顺着引用补事实，而不是只拿到一堆孤立的文本片段。
- **先复用工具，再决定要不要加索引。** 记忆规模可控时，目录加关键词搜索就够用；召回不足再加语义索引。
- **Git 记录变化。** 每次修改都有提交、作者、时间和说明，可以回答"为什么现在是这样"。

## 2. 目录：按对象、时间、任务三种入口组织

```text
entities/        # 对象：人、组织、地点……
  people/
  orgs/
knowledge/       # 知识：长期事实、偏好、决定及其上下文
  facts/
  preferences/
  decisions/
timeline/        # 时间：按日、按周的摘要
  daily/
  weekly/
workstreams/     # 任务：正在做的、已完成的
  active/
  completed/
```

- 三种入口回答三类问题：**这个人／东西是什么**（entities）、**那天发生了什么**（timeline）、**这件事做到哪了**（workstreams）。knowledge 放跨对象、长期有效的事实和决定。
- 目录随记录增长，**不要预先定死 schema**。需要新类别时再加文件夹。

## 3. 每条记录怎么写

**格式**：文件头（front matter）＋事实列表＋对其他记录的引用。

```markdown
---
id: P04
type: participant
aliases: [Tom, UserD, 用户 C]
---

# P04 · Tom

- 2026-10-28 13:25 开始正式路线，约 31 分钟。
- 当前任务：[[ws-remaining-interviews]]
```

```markdown
---
id: ws-remaining-interviews
type: workstream
status: active
related: [P04, P05]
---

# 补完剩余访谈

- 受访者：[[P04]]、[[P05]]（待团队确认）
- 要求：先开放提问再追问。
```

规则：

1. **`id` 稳定不变**，别处只用 `id` 引用，不复制整份资料。
2. **`aliases` 写全别名。** 文件系统没有语义理解，搜 "Tom" 搜不到 "UserD"；别名就是为关键词搜索补词。
3. **信息放在它真正适用的范围里。** 某个任务的临时要求留在任务记录里，不要升级成人物的永久偏好或全项目规则。文件边界就是作用范围。
   - 例：用户说"这次汇报只展示数据，不放设计方案"，应写进这次汇报的 workstream，而不是写进全局规则。
4. **区分证据层次**（研究类项目尤其重要）：观察到的、当事人说的、我们推断的，分开写。

## 4. 记录变长时：拆文件，不改引用

```text
entities/people/person-lin.md
        ↓ 拆分
entities/people/person-lin/
  _index.md      # 保留 id: person-lin，放常用事实和子记录入口
  dining.md
  travel.md
```

- `[[person-lin]]` 约定为既可指向 `person-lin.md`，也可指向 `person-lin/_index.md`，所以**拆分后别处的引用不用改**。
- 索引页放摘要和入口，需要细节时才读子文件，这叫**渐进式读取**，省上下文。
- 注意：`[[id]]` 只是约定，普通 `cat` 不会自动追踪它；agent 或工具要自己解析。**拆分后要检查引用是否仍然完整。**
- 这比维护一个越写越大的 `MEMORY.md` 好：单个大文件每次都得整份读，而且新旧说法会混在一起。

## 5. Git 怎么用：当前状态与历史分开

**当前文件服务"现在怎么做"，Git 历史服务"当时怎么理解"。**

- 不要在当前文件里无限追加"旧说法＋新说法＋更正说明"，那样读者每次都要自己裁决哪个有效。直接把当前文件改成最新的理解，旧版本留在 Git 里。
- 平时只读当前状态；要追溯错误或理由时再查历史：

  ```bash
  git log -p -- entities/people/person-lin.md
  ```

- **维护性提交是在整理记忆，不只是追加日志。** 例如把临时事项从人物记录挪到 workstream、压缩冗长叙述、合并重复记录，都是正常的提交。
- 三个容易误解的点：
  - commit 时间不等于事实生效的时间，事件日期要写在内容里（timeline）。
  - 历史可查不等于会被自动召回。
  - 删除当前记录不等于真正"遗忘"，历史里仍在。

## 6. 运行环境与记忆分开；整理可以和工作并行

- **沙箱可以重建，记忆要延续。** 记忆仓库的生命周期独立于 agent 的执行环境；环境丢了，从仓库恢复即可。
- **整理可以放在单独分支或 worktree 上做**：在主线继续服务当前任务，另一边做归纳、拆文件、去重，然后提交 → 检查 → 合并回主线。合并时仍要检查语义冲突。

## 7. Agent 操作清单

**开始工作时**
1. 读仓库入口（README、AGENTS.md 或状态页），了解目录和规则。
2. 用 `ls` 看结构，用 `grep` 按 id 或别名找记录，读到的文件里有引用就顺着读。
3. 先确认工作区干净、和远端同步，再动手。

**写入时**
1. 判断信息属于哪类：对象、知识、时间、任务。放进对应文件；没有就新建，带上 `id`、`type`、`aliases`。
2. **改写当前状态，而不是追加矛盾说法。**
3. 用 id 引用相关记录，不复制内容。
4. 任务专属的要求写在任务文件里。

**提交时**
1. 一次提交只做一件逻辑上的事，提交说明写清楚**为什么**改。
2. 拆分或移动文件后，检查链接和引用是否完整。
3. 推送后确认远端已包含这次提交。

**收尾与维护**
- 任务完成：把 workstream 从 `active/` 移到 `completed/`。
- 定期整理：合并重复、压缩过长叙述、把过长文件拆成索引加子文件。

## 8. 常见错误

| 错误 | 后果 | 正确做法 |
|---|---|---|
| 所有东西写进一个大 `MEMORY.md` | 每次都要整份读；新旧说法混杂 | 按类型分文件，长了就拆 |
| 当前文件里保留旧说法和更正 | 读者要自己判断哪个有效 | 改写为最新状态，旧版留给 Git |
| 同一个人用多个称呼、没写别名 | 搜不到、对错人 | 固定 `id`，`aliases` 写全 |
| 临时要求写成永久规则 | 以后的任务被错误约束 | 留在对应任务文件里 |
| 复制整份资料到别处 | 一处更新，别处过期 | 只用 id 引用 |
| 拆文件后不查引用 | 断链 | 拆完运行链接检查 |
| 提交说明只写"update" | 无法追溯原因 | 写清做了什么、为什么 |

## 9. 本仓库（SD5531）的落地方式

本节 1–8 节原样取自用户在 SD5008 仓库（Research-and-Analysis-for-Design）维护的同名指南，2026-10-29 引入本仓库（决定 [D009](../DECISIONS.md)）。本节按 SD5531 已有结构改写。

| 指南中的概念 | 本仓库的位置 | 说明 |
|---|---|---|
| 当前状态 | [`docs/STATUS.md`](../STATUS.md) ＋ [`PROJECT_STATE.json`](../../PROJECT_STATE.json) | 人读与机器读两份，内容保持一致；**不另建 `PROJECT_STATUS.md`** |
| knowledge / decisions | [`docs/DECISIONS.md`](../DECISIONS.md)、[`docs/SCOPE.md`](../SCOPE.md)、[`docs/ARCHITECTURE.md`](../ARCHITECTURE.md)、[`knowledge/`](../../knowledge/NETWORK.md) | 决定编号 D0xx；知识网每条边带来源与状态 |
| timeline | [`docs/HISTORY.md`](../HISTORY.md)、[`docs/history/`](../history/) | 记事件本身的日期；变长后再按月拆分 |
| workstreams | [`docs/workstreams/`](../workstreams/README.md) | `active/` 与 `completed/`，文件名即 `ws-*` id |
| 代码与实验 | [`project-camera/src/`](../../project-camera/src/README.md)、[`project-camera/experiments/`](../../project-camera/experiments/README.md) | 代码与实测分开，实验按日期建文件夹 |
| entities | 暂不建立 | 设备、组别、个体编号确定后再加 `docs/entities/`，避免为未定对象预设 schema |
| agent 规则 | [`AGENTS.md`](../../AGENTS.md)（`CLAUDE.md` 只做指引） | 读取顺序、证据纪律、分支规则 |

### 与本仓库证据纪律的关系

第 5 节"改写当前状态，旧版交给 Git"只适用于**当前说明类文件**。本仓库有三类文件，规则不同：

| 类型 | 文件 | 写法 |
|---|---|---|
| 当前说明 | STATUS、PROJECT_STATE、SCOPE、ARCHITECTURE、ROADMAP、EVIDENCE、各 README、workstreams | 直接改写为最新理解，不堆叠旧说法 |
| 记录 | DECISIONS、CHANGELOG、HISTORY、实验记录 | 只追加；被取代的决定标"取代 Dxxx"，不删旧条 |
| 原始来源 | `provenance/source-manifest.json` 登记的导入文件、`docs/history/` | 默认不改，新解释写到当前说明里；因新要求确需修改时，先征得用户对该项修改的同意（[D010](../DECISIONS.md)），单独提交并在 manifest 登记 |

### 其他适配

- 索引页用 `README.md`；拆分时把 `x.md` 改成 `x/README.md` 并更新链接。
- 引用用标准相对链接，不用 `[[id]]`；`id` 写在文件头，方便 `grep`。
- 改动后运行 `python3 scripts/validate_repository.py`（发布导入或版本前加 `--hash`）。
- 稳定编号：决定 `D0xx`、工作流 `ws-*`、实验文件夹 `YYYY-MM-DD-主题`。

## 来源

- templater（小红书），《看了 Personal Agent 发现 RAG 记忆已经过时了》，2026-10-28。
- 该分享引用的公开材料：Shah 对 Instinct 记忆的逆向分析；Rohan Adwankar, *The box an agent runs in*；Letta 官方文档 *Context Repositories*（2026-02-12）。
- 以上产品细节来自第三方观察，本指南只采用其做法，不对产品实现作判断。
