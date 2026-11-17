---
name: knowledge-persistence
tier: T2  # T分级: T2=直接做 / T1=先请示 / T0=一律拒
description: 信息持久化规范——区分 memory/文件/skill 三层存储，确保重要信息不丢失。
---

# 知识持久化 · 信息该放哪

> 自己踩坑踩出来的：什么东西记哪里。
>
> **读者须知（落点名称）**：文中 `<记忆目录>`／`<档案目录>`／`<项目目录>`／<数据根> 都是**作者环境**的目录布局——
换环境照自己的目录理解即可（原则是「哪一层、为什么放那层」，不是具体路径）。表里出现的 skill 名
（记录类／日记类／知识库型那几个）是作者环境技能库的成员，**未单独公开**；实测日期读作「某次实测样本」。

## 什么时候用

- 发现环境信息/版本号/配置等可重现事实
- 被纠正「不只记在 memory 里」
- 需要判断一条信息该放 memory、文件还是 skill

## 三层存储

| 层级 | 容量 | 存活 | 用途 |
|:-----|:----:|:----:|:-----|
| **memory** | ~2KB | session间，但会被压缩 | 快速索引（「xxx 详情见 <记忆目录>/YYY.md」）|
| **文件** | 无限制 | 永久 | 环境快照、版本记录、工具状态、凭据清单 |
| **skill** | 无限制 | 永久 | 可复用的方法/流程/规范，不是单次记录 |

## 纪律
1. **memory 只是索引** — 不存放完整事实，只留一句指向文件的引用
2. **可重现的事实必须落文件** — 版本号、环境配置、工具状态、凭据位置 → `<记忆目录>/`
3. **方法进 skill，事实进文件** — 「怎么审计API」→ api-diagnostics skill；「当前装了什么」→ ENV.md
4. **技巧级经验进 skill references** — 调试发现的技术决策/踩坑/边界情况，按领域写进对应 skill 的 `references/`
5. **skill 资产登记** — 新增任何资产必须在 SKILL.md 登记（引用行/脚本清单段）｜A5
6. **git跟踪意识** — 建文件/目录前先 `git check-ignore -v`；被 ignore 的目录也是备份盲区｜A6

> **其余全文见 `references/纪律.md`**（整节逐字搬出，含判例、命令与例外）。
## 决策记录（拍板）规范

拍板/决策类记录落盘：**原话不加解读**、**必记「否掉了什么」**（方案+落选原因）、**被取代用新记录**；骨架 `## 拍板（原话）`／`## 否掉了什么（方案+原因）`／`## 影响/后果`；**归档冻结**｜详案 D1–D5

## 模式速查

| 模式/场景 | 规范在哪 |
|:---------|:---------|
| 记忆腾位置（逐条字数／合并候选／余量） | `bin/mem`（本 skill 的 `scripts/mem.py`，只读） |
| 归档目录（同类数据按时间累积） | `references/archive-pattern.md` |
| 实体档案「一 id 一文件」 | `references/entity-archive-pattern.md`（index.json + 每实体一文件） |
| 生活健康类观察归档 | `<记忆目录>/health-notes.md` + `references/health-verification.md` |
| 私人笔记/压缩包素材归档 | `references/private-note-archive.md` |
| 事件类双轨/三处落笔归档 | `references/event-dual-track.md`（完整档案+轻量条目+当日日记三处落笔，后续补充法） |
| 长案卷分层（一案一档：判词/过程账/证件/取证/第三方核查） | `references/case-archive-layout.md` |
| 目录纳入 git 前扫敏感信息 | 见下「敏感信息」节（凭据只走 .enc 不入库） |
| 知识库型 Skill（含**载体能力与边界实测**：linked_files 规格／别放 assets／60 阈值／CLI 耦合） | `references/knowledge-base-skill.md`（SKILL.md 导视 + 数据分类目录 + 防膨胀内建） |
| 旧时代/RAG遗留文件识别与处置（2026-09-05 双生实战） | `references/legacy-file-recognition.md`（胎记识别 + 母本不扔 + 原料成品并存） |
| 导视表拆独立 INDEX.md（2026-08-31 实战） | 见下「导视拆 INDEX」节 |
| 踩坑全录（20 条，用到才读） | `references/pitfalls.md` |
| 核实一段聊天记录是否真实存在／何时发生 | `references/session-history-verification.md`（state.db 直查 + 覆盖窗口 + FTS 空结果误读） |

## 敏感信息

把 gitignored 目录（diary/、<项目目录>/）纳入版本管理前，先全目录扫敏感模式（ghp_/gho_/sk-/api key/token/password/secret/bearer），确认干净再改 .gitignore 放行。凭据类永远只走加密文件（.enc），不入库。

## 导视拆 INDEX（2026-08-31 internet-memes-reference 实战）

知识库型 skill 的导视表是最大重复块 → **拆到 skill 根独立 「INDEX.md」**（依赖分析→建 INDEX.md→SKILL.md 换一行指引→全库引用同步→实测验证）；**装饰 emoji 端走**（用户拍板）｜详案 K1

## 参考资料

| 文件 | 内容 |
|:-----|:-----|
| `references/pitfalls.md` | 踩坑全录 20 条（根目录死文件/收录要全量/一id一文件/workspace散货/委派收尾三查/gitignore 误伤等） |
| `references/qq-forwarded-messages.md` | QQ 转发消息事件调查（GitHub API 第一手核实） |
| `references/docx-metadata-forensics.md` | docx 作者归属验证（creator/修订痕迹/时间线取证） |
| `references/archive-pattern.md` / `references/entity-archive-pattern.md` / `references/health-verification.md` / `references/private-note-archive.md` / `references/knowledge-base-skill.md` | 各归档/知识库模式详规 |
| `references/session-history-verification.md` | 会话史溯源（state.db 直查／覆盖窗口／空结果≠不存在） |

## 登记口径 · 做被要求的事，产出即时落档

- 登记**只做被要求的事**——用户没点名的不自作主张建条（小事别抢着存档）。
- 但**任务内的产出要即时落档，别问「要不要留」**：问了＝把判断推回给用户。该不该留按本 skill 的归位规则自己判，判完直接写。
- **查证类提问开工前先翻本地档**——「X 现在怎么样了」也算，不只是用户说「更新档案」时：`search_files` 扫 `skills/` 与 `<档案目录>`／`<记忆目录>`＋`bin/kb search`，命中就接着写。全盘 `grep -r` 大目录会超时，按窄路径分头搜。
- **「这个应该能更新本地的档案」＝先找同主题的既有长期档，不是只建一条事件条目**：`grep -ril <关键词> <记忆目录> <档案目录> skills/*/references` 摧机制笔记／本机账／技术速查——新事实按「新增一节」补进去（旧结论不改），同时改 `INDEX.md` 那行的描述；事件条目与日记照旧。判据：只写轻量条目＝那份长期档还是缺的，用户下次会再指一遍同一个缺口｜详 `references/event-dual-track.md`「主题档优先」
- **同一事实只留一处正文**：答完才发现 skill/档案已有同一节时，撤掉新件、在 `INDEX.md` 留一行指针指过去（「→ 见 skill … §xxx」）。两处并存必分叉，后一个读的人不知道该信哪份。
- **结论型产出（判型／评级／评估）要把结论回填到它的源档**：新产出（案例、报告）落盘后，回原档把「未做／待补」那行改成已做＋一句结论＋产物路径，并在承载 skill 的源件区加一行指针。两个数一旦分了叉，下次只找得到产物找不到归属，或原档还挂着「未做」让人重做一遍——回填是收尾动作，不是可选项。

## 拆分记录

- 2026-11-10 二轮（8K 线）：「纪律」整节逐字搬 `references/纪律.md`；本文 8640 → 4020 字符，守恒 0 缺失。

> 2026-09-22 拆薄（规矩留、案例搬，**一条未删**，原文逐字进 references）：31.6KB → 9.5KB。A5–A28→`references/routing-cases.md`；B14→`references/feedback-and-persistence.md`；C20→`references/memory-debloat.md`；D18–D27＋决策记录规范→`references/record-integrity.md`；E15–E24→`references/daily-log-and-registration.md`；F29→`references/corpus-slimming.md`；G30→`references/interpreting-user-work.md`；D21b→并入 `references/session-history-verification.md`；导视拆 INDEX 节→并入 `references/knowledge-base-skill.md`。
