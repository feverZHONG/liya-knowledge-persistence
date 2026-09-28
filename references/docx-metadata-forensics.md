# docx 元数据取证 · 作者归属验证

> 2026-09-03 電學.docx 归属验证实战（qq-neighbor-watch 电视案例）。用途：收到 docx 想知道「谁写的/几个人写的/什么时候写的/能不能证明某段是谁写的」。

## 快速命令（python3 zipfile，无第三方依赖）

```python
import zipfile, re
z = zipfile.ZipFile('文件.docx')

# 1. 作者与时间线
print(z.read('docProps/core.xml').decode('utf-8', errors='replace'))
# dc:creator / cp:lastModifiedBy / cp:revision / dcterms:created / dcterms:modified

# 2. 修订痕迹（多人协作会留 author 属性）
doc = z.read('word/document.xml').decode('utf-8', errors='replace')
authors = set(re.findall(r'w:author="([^"]+)"', doc))   # 修订作者
print('修订作者:', authors if authors else '无')
print('插入次数:', doc.count('<w:ins '), '删除次数:', doc.count('<w:del '))
```

另有 `docProps/app.xml`：Pages/Words/TotalTime（编辑总时长，可佐证投入度）/AppVersion。

## 解读要点

- **creator ≠ 内容作者的可能**：creator 是 Word 账户名（微软账号），可能是作者的罗马音/账户名而非显示昵称（实战：電學.docx creator=Aika Sakai = 群内 Sakai Aika = 坂井小愛佳，同一人三形态；对不上时先找「罗马音↔昵称」映射，别急着下「作者另有其人」）
- **无修订痕迹 = 单人成稿**：没有 w:ins/w:del、没有多 author = 文档本体单人写成——**能证「不是多人修订」，但证不了「每段是谁写的」**（段落归属需要修订模式痕迹/当事人证词，文件层给不了）
- **created/modified 时间线是行为证据**：创建到定稿跨多久、revision 次数——实战发现電學 2023-12 创建 2024-09 定稿修订 17 次 = 跨 9 个月持续观察编码，本身就是「行为模式跨两年稳定」的判型级佐证
- **附录信息要和人确认**：段落级归属争议（「这段是不是 X 写的」）文件层无解时，直接问知情者/当事人，别用「无修订痕迹」硬推

## 边界

- 只能读 OOXML 包装的 docx；.doc（老格式）需先转换
- 无修订痕迹 ≠ 无多人参与——可能先口头/他处写好再粘贴（实战教训：条目疑似他人手笔，文件层无法验证，最终靠当事人确认「非他人手笔」收尾）
