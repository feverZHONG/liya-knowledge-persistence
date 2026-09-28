---
tier: T2  # T分级: T2=直接做 / T1=先请示 / T0=一律拒
---

# 实体档案「一 id 一文件」模式（2026-08-02 QQ 群聊身份档案实例）

## 适用场景

持续积累的实体档案：成员名单、设备清单、收藏条目、身份映射——每个实体有独立状态和手工备注，会随事件增长。

## 结构

```
base/
├── index.json                    # 索引：只列 id（members: [...], groups: [...]），一眼看全
├── members/
│   └── <openid>.json             # 每实体一文件
└── groups/
    └── <group_openid>.json
```

## 成员文件字段

```json
{
  "openid": "xxx",
  "nickname": "群昵称",          // 手工备注优先；事件昵称仅在空时自动填入
  "qq_number": "",
  "first_seen": 时间戳,
  "last_seen": 时间戳,
  "seen_in": ["dm", "group:xxx"],
  "role_hint": null,
  "impression": "谁是谁/什么特征"
}
```

## 脚本纪律（幂等 --sync）

- `--sync` 扫数据源（如 state.db）自动登记，**可重复跑**
- `setdefault` 保证字段存在；**手工字段（nickname/group_name）脚本不覆盖**——只有空才自动填
- 时间轴用 `max/min` 更新 first_seen/last_seen
- 索引 index.json 每次重建（从已见 id 集合）

## 为什么一 id 一文件

- 单文件堆所有实体 → 编辑冲突、git diff 噪音大、加字段要改整个结构
- 一实体一文件 → 并行更新安全、diff 清晰、字段演进只动单文件
- 被纠正实例：roster.json 单文件 → 用户纠正「一个id对应一个文件」

## 昵称/名字数据源（QQ 群场景）

- 群事件 `author.username` → 适配器补丁 → session `origin_json.user_name`（**不是 display_name 列**）
- 群名：接口内邀白名单拿不到 → 分享链接 `busi_data` 参数 base64 解码 → groupCode=群号
- 详细排障见 qqbot-gateway-ops / group-chat-discipline（若 curator 可写时同步）
