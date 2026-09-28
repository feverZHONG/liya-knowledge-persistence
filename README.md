# 知识持久化 · 什么信息该放哪

> 给 agent 作者的一层规范：**一条信息该放「记忆层」「项目文件」还是「技能库」**——三层各管一段，混着放必丢。
> 附：记录完整性（原文不改 · 勘误回指 · 拍板留痕）、语料减法、会话史溯源、归档模式一览。

## 三层存储

| 层级 | 容量 | 存活 | 用途 |
|:-----|:----:|:----:|:-----|
| **记忆层** | 很小（~2KB） | 跨会话，但会被压缩 | 只放**快速索引**（「xxx 详情见 <档案目录>/YYY.md」） |
| **文件** | 无限制 | 永久 | 环境快照、版本记录、工具状态、凭据位置 |
| **技能库** | 无限制 | 永久 | 可复用的方法／流程／规范，不是单次记录 |

一句话：**memory 只是索引，事实落文件，方法进技能库。**

## 纪律（节选）

1. **可重现的事实必须落文件**——版本号、环境配置、工具状态、凭据位置
2. **技巧级经验进技能库的 references**——按领域归档，别堆在入口文件里
3. **记忆层满时先删索引**——删指向已存在文件的引用，不挤掉重要信息
4. **收到纠正→写进对应文件，不只存记忆层**；判据是「要在本会话之外生效吗」
5. **新事实推翻旧前提时，去改那处文件**——grep 依赖处，加「YYYY-MM-DD 更新」并回指
6. **登记「事件+推断」分层落笔**——事实层／推断层／原话栏／待核栏，四栏分开写
7. **同一结论反复改口：留痕不抹**——原文不动 ＋ 勘误块回指 ＋ 末节写终稿
8. **收录原文：换行是结构，不是排版**——原文整段用代码块包住；收完跑逐行 diff
9. **素材归位：一件东西一「家」**——混合体裁先拆；他处只挂链，不复制正文
10. **跨实例共享的硬设定＝设定层档案**——被多处共用且必须一致的事实，立正本、逐条挂出处；写新实例前先读它

完整 32 条（含每条背后的实测判例）见 `references/`，入口文件只留可执行的那一条。

## 模式速查

| 场景 | 规范在哪 |
|:-----|:---------|
| 归档目录（同类数据按时间累积） | `references/archive-pattern.md` |
| 实体档案「一 id 一文件」 | `references/entity-archive-pattern.md` |
| 生活健康类观察归档 | `references/health-verification.md` |
| 私人笔记／压缩包素材归档 | `references/private-note-archive.md` |
| 事件类双轨／三处落笔归档 | `references/event-dual-track.md` |
| 知识库型技能（导视 + 数据分类 + 防膨胀） | `references/knowledge-base-skill.md` |
| 旧时代／RAG 遗留文件识别与处置 | `references/legacy-file-recognition.md` |
| 核实「一段聊天记录是否真实存在／何时发生」 | `references/session-history-verification.md` |
| 语料长胖了做减法 | `references/corpus-slimming.md` |
| 记忆层瘦身（先验尸再删） | `references/memory-debloat.md` |
| 记录完整性（原文／勘误／拍板） | `references/record-integrity.md` |
| 归位判例集（哪条规则适用哪种场景） | `references/routing-cases.md` |
| 踩坑全录 | `references/pitfalls.md` |
| 平台转发消息类事件的调查法 | `references/qq-forwarded-messages.md` |

## 决策记录（拍板）规范

拍板／决策类记录落盘：**原话不加解读**、**必记「否掉了什么」**（方案 + 落选原因）、被取代用新记录。
骨架：`## 拍板（原话）` ／ `## 否掉了什么（方案+原因）` ／ `## 影响/后果`；归档冻结。

## 敏感信息

把 gitignore 掉的目录纳入版本管理前，先全目录扫敏感模式（`ghp_`／`gho_`／`sk-`／api key／token／password／secret／bearer），确认干净再放行。**凭据类永远只走加密文件，不入库。**

## 读者须知

文中 `<记忆目录>`／`<档案目录>`／`<项目目录>`／`<数据根>` 都是**作者环境**的目录布局——照自己的目录理解即可，重要的是「哪一层、为什么放那层」，不是具体路径。表里出现的技能名（记录类／日记类／知识库型那几个）是作者环境技能库的成员，**未单独公开**；实测日期读作「某次实测样本」。

## 姊妹仓库

- [liya-dev-workflow](https://github.com/feverZHONG/liya-dev-workflow) · [liya-subtraction-skill](https://github.com/feverZHONG/liya-subtraction-skill) —— 开发流程 / 技能库做减法
- [liya-persona-authoring](https://github.com/feverZHONG/liya-persona-authoring) —— 给 AI agent 写它自己的身份文件（本仓管「信息放哪」，它管「身份文件怎么瘦」）
- [liya-delegation-and-verification](https://github.com/feverZHONG/liya-delegation-and-verification) —— 委派与验收：把「自报」验成事实
- [liya-news-verification](https://github.com/feverZHONG/liya-news-verification) —— 验证伞：核查与链接安全
- [liya-prose-quality-metrics](https://github.com/feverZHONG/liya-prose-quality-metrics) · [liya-story-revision-plan](https://github.com/feverZHONG/liya-story-revision-plan) · [liya-corpus-line-mining](https://github.com/feverZHONG/liya-corpus-line-mining) —— 写作三件
- [liya-sillytavern-cards](https://github.com/feverZHONG/liya-sillytavern-cards) · [liya-tavern-card-refinement](https://github.com/feverZHONG/liya-tavern-card-refinement) · [liya-sillytavern-worldbook](https://github.com/feverZHONG/liya-sillytavern-worldbook) —— 酒馆角色卡三件
- [liya-vision-recognition-traps](https://github.com/feverZHONG/liya-vision-recognition-traps) —— 视觉模型识图陷阱
- [liya-chat-game-referee](https://github.com/feverZHONG/liya-chat-game-referee) · [liya-spy-game](https://github.com/feverZHONG/liya-spy-game) · [liya-sea-turtle-soup](https://github.com/feverZHONG/liya-sea-turtle-soup) —— 聊天里能玩的三件
- [liya-ruozhiba-wordbank](https://github.com/feverZHONG/liya-ruozhiba-wordbank) —— 弱智吧题防御手册
- [liya-subtitle-proofreading](https://github.com/feverZHONG/liya-subtitle-proofreading) —— 字幕校对/重建/外挂 SRT

## 提思路 / 提修正

- 你的分层口径、归档模式、踩过的丢信息坑 → 开 [Issue](https://github.com/feverZHONG/liya-knowledge-persistence/issues)
- 想直接改 → Fork + PR

## 许可

**双许可**——文档与代码分开：

- **代码**（`scripts/` 下的文件）：**MIT** —— 拿去用、改、再发，保留版权声明即可。
- **文档**（`SKILL.md`、`references/`、本 README 的正文）：**[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)** —— 可以自由使用、改编、连商用都行，**但要署名**（莉娅 / [@feverZHONG](https://github.com/feverZHONG)）并注明来源。

本仓当前是**纯文档仓**（无 `scripts/`），`LICENSE` 留作后续脚本的默认许可。两份全文：`LICENSE`（MIT）／`LICENSE-DOCS`（CC BY 4.0）。

---

*莉娅（[@feverZHONG](https://github.com/feverZHONG)）· 宇宙美好记录官*
