#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""处方旗哨（2026-09-17 立·机制体检账 七十二之族）——
**一条处方里点名的那个「--旗」，那个器认不认得？**

★立此器之由（⛔**本坐今日自己栽的那一跤，逐字记在这儿**）：
  本坐要看 `跑轮.py --补存` 头一回拦在哪一条，遂敲了一行
  `python3 工具/跑轮.py --补存 340 "x" --dry-run`——
  ⛔**而 `--dry-run` 这个旗，本仓没有一个器认得它**；
  **於是那一行不是「看一眼」，是一次原原本本的写口调用**（`--补存` 是写口）。
  ★**那一回没写成，是闸恰好拦住了它，不是本坐当心**——**其得以不成祸，是运气不是本事。**

★★**其与 `死处方哨` 之分（二器同守一族而不同路，⛔不许合并）**：
  · `死处方哨`：**处方里点名的器，盘上有没有那个档**（其形之器名那一段在不在盘上）。
  · **本器**：**处方里点名的旗，那个器认不认得**（`--Y` 在不在那个器的码里）。
  ★**二者之害不同**：**器不在，跑起来当场报错，人看得见**；
  ⛔**而旗不认，多半不报错**——**那个器把它当作一个多余的字，照着它自己的默认路子走下去**；
  **默认那一条路要是写口，就落盘了。**

★★★**它认哪几样，⛔不认哪几样**：
  · **认**：`工具/*.py`、`工具/席/*.js`、`设定/*.md` 之文里，
    形如「python3 空格 工具/某器.py 空格 --某旗」者（旗须紧跟其器，中间只许空白）。
    ⛔**此处之器名与旗名皆不写成真形**——**写成真形，`死处方哨` 便把本器档首这几句
    当成真处方，去盘上找那个并不存在的器**（★**本坐 0917 立本器之日当场自栽一回，
    其红三处皆出自本档**；`死处方哨` 自己的档首早写死了这一条：**假名须当场拼出，不许写死**）。
  · ⛔**不认**：器不在盘上者（那一样归 `死处方哨` 管，⛔两器不许抢同一条红）。
  · ⛔**其判之法只一样**：**那个旗之字面在不在该器之码里**——
    ★**这是个宽判**：**码里提过即算认得**（注里提过也算）。
    ⛔**故本器只逮「一个字也没提过」那一种**——**宽而不漏，胜过严而误伤。**

★★★★**今日之实**：**处方里点名之旗 606 处，其器一字未提者 1 处**——
  `工具/席/一章.js` 之 `跑轮.py --help`。**本坐逐行读过其码，判其无害**：
  `跑轮.py` 主口之形係「`len(sys.argv) < 3` 即印 `__doc__` 并返 1」，
  **故 `--help` 落进那一条，印出来的正是其用法**——**其所为与处方所许者同**；
  ⚠**其唯一之瑕係返 1**（读退出码者会当它败了）。**本器报之而不拦。**

用法：
    python3 工具/处方旗哨.py          # 全盘
    python3 工具/处方旗哨.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import glob, io, json, os, re, sys

根 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
式 = re.compile(r'python3\s+(工具/[^\s`\'"]+\.py)\s+((?:--[\w一-龥]+[ \t]*)+)')


def 诸处方(根路=None):
    """自盘上诸档之文里，抽出「python3 空格 器 空格 旗」之形（⛔此处不写真形，见档首）。
    返回 [(见於何档, 其器, 其旗), ...]。⛔器不在盘上者不认（归 死处方哨 管）。"""
    R = 根路 or 根
    出 = []
    档 = (glob.glob(os.path.join(R, '工具', '*.py'))
          + glob.glob(os.path.join(R, '工具', '席', '*.js'))
          + glob.glob(os.path.join(R, '设定', '*.md')))
    for f in sorted(档):
        if os.path.basename(f) == os.path.basename(__file__):
            continue          # ⛔本器自己的档首写满了假旗，不认自己
        try:
            s = io.open(f, encoding='utf-8', errors='replace').read()
        except Exception:
            continue
        for m in 式.finditer(s):
            器 = os.path.join(R, m.group(1))
            if not os.path.exists(器):
                continue      # ⛔归 死处方哨
            for 旗 in m.group(2).split():
                出.append((os.path.relpath(f, R), m.group(1), 旗))
    return 出


def 旗之实(器路, 旗, 根路=None):
    """★宽判：那个旗之字面在不在该器之码里（注里提过也算）。"""
    R = 根路 or 根
    try:
        return 旗 in io.open(os.path.join(R, 器路), encoding='utf-8', errors='replace').read()
    except Exception:
        return True           # ⛔读不着即不报（「查不着」不是红之由）


def 废之旗(根路=None):
    """〔1120·W908 环7〕法用册「废」之去证以「无文」宣告某器已除之旗（如 连读重出：{无文: "--连读", 于: [工具/看官.py]}）——
    其旗之旧引俱係史录（裁、回执、圣经之史），⛔算「器不认之旗」：废之去证要器⛔含其字，本器要器认其字，二尺相抵，以废为准。→ [(器, 无文之式)]"""
    try:
        册 = json.load(io.open(os.path.join(根路 or 根, '设定', '法用册.json'), encoding='utf-8'))
    except Exception:
        return []
    出 = []
    for x in 册.get('废') or []:
        for c in x.get('去证') or [] if isinstance(x, dict) else []:
            if isinstance(c, dict) and isinstance(c.get('无文'), str) and c['无文'].startswith('--'):
                出 += [(t, c['无文']) for t in (c.get('于') or [])]
    return 出


def 量(根路=None):
    出 = 诸处方(根路)
    免 = 废之旗(根路)
    红 = [(f, t, g) for f, t, g in 出 if not 旗之实(t, g, 根路)
          and not any(t.endswith(器) and (g == 式 or re.fullmatch(式, g)) for 器, 式 in 免)]
    return 出, 红


def 跑(报=True):
    出, 红 = 量()
    if 报:
        print('════ 处方旗哨 ════（守：处方里点名的旗，那个器须认得它）')
        print('  处方里点名之旗 %d 处｜⛔其器一字未提者 %d 处' % (len(出), len(红)))
        见 = set()
        for f, t, g in 红:
            if (t, g) in 见:
                continue
            见.add((t, g))
            print('  ⛔ %s 之 %s ← 见於 %s' % (t, g, f))
        if not 红:
            print('  ✓ 处方里点名的旗，器器皆认得。')
        print('  ★本器只报不拦：**旗不认之害在「它不报错而照默认路走」**，'
              '其轻重须人读那一条默认路方判得出。')
    return 红


def 自测():
    import shutil, tempfile
    R = []
    出, 红 = 量()
    R.append(('①盘上抽得出处方之旗（≥200 处）', len(出) >= 200))
    R.append(('②今日其器未提者 ≤2 处', len(红) <= 2))
    tmp = tempfile.mkdtemp(prefix='处方旗哨_')
    try:
        os.makedirs(os.path.join(tmp, '工具', '席'))
        os.makedirs(os.path.join(tmp, '设定'))
        真 = '--' + '真' + '旗'
        假 = '--' + '假' + '旗'
        甲 = '甲' + '器.py'          # ⛔当场拼出，不许写死（见档首）
        乙 = '乙' + '器.py'
        io.open(os.path.join(tmp, '工具', 甲), 'w', encoding='utf-8').write(
            "if sys.argv[1] == '%s': pass\n" % 真)
        io.open(os.path.join(tmp, '设定', '令.md'), 'w', encoding='utf-8').write(
            '照此跑：python3 工具/%s %s\n并及：python3 工具/%s %s\n'
            '并及一个不在盘上的器：python3 工具/%s %s\n' % (甲, 真, 甲, 假, 乙, 假))
        出2, 红2 = 量(tmp)
        R.append(('③认得出真旗与假旗（其处 ＝2，⛔器不在者不认）', len(出2) == 2))
        R.append(('④逮得出假旗，且只逮那一个', len(红2) == 1 and 红2[0][2] == 假))
        R.append(('⑤真旗不误伤', all(x[2] != 真 for x in 红2)))
        # ⑥⛔器不在盘上者归 死处方哨，本器一字不报
        R.append(('⑥器不在盘上者本器不认（⛔不与 死处方哨 抢同一条红）',
                  all(t.endswith(甲) for _, t, _ in 出2)))
        # ⑦⛔宽判之守：旗只在注里提过，亦算认得
        io.open(os.path.join(tmp, '工具', 甲), 'a', encoding='utf-8').write(
            '# 其旗 %s 亦认\n' % 假)
        _, 红3 = 量(tmp)
        R.append(('⑦宽判：旗只在注里提过亦算认得（其红归零）', 红3 == []))
        # ⑨〔1120〕废之去证以「无文」宣告已除之旗 → 其旧引免红（废与本器相抵·以废为准）
        t9 = tempfile.mkdtemp(prefix='处方旗哨九_')
        try:
            os.makedirs(os.path.join(t9, '工具')); os.makedirs(os.path.join(t9, '设定'))
            io.open(os.path.join(t9, '工具', 甲), 'w', encoding='utf-8').write('pass\n')
            io.open(os.path.join(t9, '设定', '令.md'), 'w', encoding='utf-8').write('旧：python3 工具/%s %s\n' % (甲, 假))
            _, 红9a = 量(t9)
            io.open(os.path.join(t9, '设定', '法用册.json'), 'w', encoding='utf-8').write(
                json.dumps({'废': [{'id': 'x', '去证': [{'无文': 假, '于': ['工具/' + 甲]}]}]}, ensure_ascii=False))
            _, 红9b = 量(t9)
            R.append(('⑨废之去证「无文」所宣已除之旗：其旧引免红（无废则红）', len(红9a) == 1 and 红9b == []))
        finally:
            shutil.rmtree(t9, ignore_errors=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    # ⑧⛔本器不许认自己（其档首写满了假旗）
    R.append(('⑧本器不认自己之档', all(not f.endswith('处方旗哨.py') for f, _, _ in 出)))
    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    print('  自测 %d/%d' % (sum(1 for _, o in R if o), len(R)))
    return all(o for _, o in R)


if __name__ == '__main__':
    if '--自测' in sys.argv:
        sys.exit(0 if 自测() else 1)
    跑()
    sys.exit(0)   # ⛔只报不拦
