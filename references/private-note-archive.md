# 私人笔记/压缩包素材归档（2026-08-24 实战）

> 触发：用户甩「手机笔记 App 的副本压缩包」/私人来源的角色设定素材，要求收录登记。

## 手机笔记副本压缩包格式

- 笔记 App「以副本形式分享」→ 自动打包成 zip
- zip 内含：`idNNN_note.txt`（**可读文本，笔记全文**）+ `.NNN.note`（二进制 protobuf，非 utf-8，不用解析）
- **直接读 txt 即可**，别在 .note 上浪费时间
- 无 unzip 命令时用 python：
  ```python
  import zipfile; zipfile.ZipFile('x.zip').extractall('dir')
  ```

## 查无公开来源的素材建档

1. **先多轮搜索确认作品归属**（mmx search 多角度关键词）；查无 → 不硬猜作品、不编造来源
2. 建档 `<项目目录>/references/characters/<角色名>-角色设定.md`：按 chara-profile 五节整理（基础/背景/性格/关系/深层），信息不足的字段留原文、不编造
3. frontmatter 标 `来源=私人笔记`、`作品=查无` —— 公开角色规范的「不写来源标注」对原创设定**破例**，来源是必要信息
4. **原文全文存档**：私人笔记无外部备份，正文末尾必须留原文全文，防丢
5. 更新角色库 INDEX.md + git 提交

## 实例：见习天使伊娃（2026-08-24）

「见习天使伊娃 / EVO大陆 / 无垢之翼 / 伊始天使 / Genesis Angel」多轮搜索查无公开作品来源；撞名干扰：EVA Genesis Angel、坎公骑冠剑骑士团长伊娃、空洞骑士丝之歌伊娃、EROLABS 伊娃第二使徒（后者就是「不太好多说什么」的部分）。已建档 `<项目目录>/references/characters/见习天使伊娃-角色设定.md`，INDEX.md 登记。
