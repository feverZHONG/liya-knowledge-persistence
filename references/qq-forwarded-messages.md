---
tier: T2  # T分级: T2=直接做 / T1=先请示 / T0=一律拒
---

# QQ 合并转发消息 · 处理实测（2026-07-31）

> 事件源：双生视界私服事件（Yricky/tiny-cafe）。验证了 QQ 合并消息的完整处理链路。

## 能力确认

- **合并转发可全量接收** — 发送者、消息内容、引用消息（关联消息）、图片附件全部解析不丢。实测 19 条 + 3 条补充，无遗漏
- **图片附件可下载（有时效）** — URL 为 `multimedia.nt.qq.com.cn/download?appid=1406&fileid=...&rkey=***&spec=0` 格式，`curl -sL` 可拉（2026-07-31 实测无需登录/cookie）
- ⚠️ **rkey 鉴权会过期（2026-09-03 实测）** — 转发出来的图片链接不是永久有效。失效返回 `{"retcode":-5503023,"retmsg":"appid is not match","retryflag":1}`（64 字节 JSON）。带 UA/Referer、换 spec 值（0/800/1000/2000）都救不回。**识别法：curl 下来 64 字节 JSON = 链接已死，别反复试，直接请用户重发原图**（MMX 识别走本地原图路径）
- ⚠️ **根因：合并转发文本里嵌的 URL 对 bot 永远无效（2026-09-03 深挖网关源码实测）** — 这些 `multimedia.nt.qq.com.cn` URL 是签发给**原群客户端会话**的，不是 bot 会话：裸 curl=`appid is not match`；带 bot access token（`Authorization: QQBot <token>`，token 从 `bots.qq.com/app/getAppAccessToken` 换，凭据 QQ_APP_ID/QQ_CLIENT_SECRET 在 <数据根>/.env）=HTTP 400；换 spec=`invalid spec or format`。**三条路全死，不是过期能救**。对照实测：同一张图 B1A3D778 走用户私聊消息（网关日志 attachment 下载成功、落 cache/images/），同一 fileid 的合并转发文本 URL 带 token 依然 400——**区别在通道：只有 QQ 消息事件推送的 attachment 才是 bot 合法下载权，转发文本里嵌的 URL 不是**
- **要图唯一姿势：请用户把关键图私聊发过来**（消息到达瞬间网关自动下载到 cache/images/，像正常收图一样处理）；合并转发文本里嵌的图一律当不存在，靠文字上下文还原（2026-09-03 用户指令）
- **下载后验证** — 对比文件大小与消息标注（如 78.4KB → 80270 bytes），基本吻合即成功；`file` 确认格式（容器内可能没有 file 命令，可用大小比对 + mmx 分析兜底）

## 标准链路

```bash
# 1. 下载图片到 <数据根>/images/
curl -sL --max-time 40 -o msgN_xxx.jpg "<附件URL>"

# 2. 看图（memory 铁律：收到图片第一反应 mmx vision describe）
mmx vision describe --image <数据根>/images/msgN_xxx.jpg --output json --quiet --prompt '详细描述这张图片'
```

## 第一手验证技巧（GitHub API）

聊天提到的人物/仓库，用 GitHub API 核实，不用猜：

```bash
curl -sL "https://api.github.com/users/<login>"          # 用户：company/location/followers/created_at
curl -sL "https://api.github.com/users/<login>/repos?sort=updated"  # 仓库：按更新时间倒序，看活跃度
curl -sL "https://api.github.com/repos/<user>/<repo>"     # 单仓库元数据
curl -sL "https://raw.githubusercontent.com/<user>/<repo>/main/README.md"  # README 原文
```

要点：
- `updated_at` 判断活跃度（刚更新=进行中项目）
- README 原文里找**非模板化细节**——真实业务取舍（如「不伪造已停服数据」）是判断作者水平/是否 AI 代工的关键证据
- 聊天中提到的技术点（如「OpenHarmony 是 arkTS」）可与仓库语言/书签等对照印证

## 双轨归档（写入位置）

| 轨 | 路径 | 内容 |
|:---|:-----|:-----|
| 完整档案 | `<档案目录>/YYYY-MM-DD-事件.md` | 聊天原文逐条 + 截图 mmx 描述 + API 实测数据 + 判断 |
| 轻量条目 | 记录类 skill（作者环境）/events/ + INDEX.md | ✅真/来源/事件/看点/后续 |

完整档案含敏感度评估：入库 git 前先扫 token/key 模式（见 knowledge-persistence SKILL.md）。

## 注意

- 归档用「自己判断」区分于「聊天内容」，不把别人观点当事实
- 日期用当天；验证状态标注清楚（GitHub 公开仓库=✅真 第一手来源）
