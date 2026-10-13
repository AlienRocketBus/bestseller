#!/usr/bin/env python3
"""章料（1008 立·虫洞之律：机器能找的⛔让模型找）——零 token 汇一章之料，席只读此一档。

为何立：380 造式实测，三魂各席动手 57—146 回、取回 250—550KB，在圣经、canon、施工表、前文里自己搜；
每一回都把越来越长的上下文重发一遍——时与 token 花在「找」上（坑之账②④）。本器把「找」做完：
  开镜卡与预令（全）｜施工表「续写第 N 章前的硬门槛」｜余章总案之解歧之裁与本章前後之拍、本章之种｜
  前两章白文（全）｜开镜卡里点到之人之状态（取最新一章之态）｜涉本章之 canon 卡（有界之卡在前）｜
  悬线里钉在本章之行｜大师进化账末三十条｜叫绝之拍库「十条手艺」。
席之令：先读 `版本/第N章/_料.md`；料外只许 grep 核一处、上下三行；⛔自己搜料。

用法：
  python3 工具/章料.py N [出档]  → 写 版本/第N章/_料.md（或出档），印各节之大小
  python3 工具/章料.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, re, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from 对账预筛 import 章号  # 汉字章号 → int


def 读(p):
    p = os.path.join(ROOT, p) if not os.path.isabs(p) else p
    return open(p, encoding='utf-8').read() if os.path.exists(p) else ''


def 章档(n, root=ROOT):
    for f in glob.glob(os.path.join(root, '正文', '*.md')):
        if 章号(f) == n:
            return f
    return None


def 节(文, 头, 止=r'^## '):
    """取以「头」起之一节（至下一个同级之头止）。"""
    m = re.search(r'^' + re.escape(头) + r'.*$', 文, re.M)
    if not m:
        return ''
    rest = 文[m.end():]
    e = re.search(止, rest, re.M)
    return 文[m.start(): m.end() + (e.start() if e else len(rest))].strip()


def 本章之行(文, n, 邻=1):
    """总案、悬线里提到本章（及前後一章）之行。"""
    pat = re.compile(r'(?<!\d)(' + '|'.join(str(k) for k in range(n - 邻, n + 邻 + 1)) + r')(?!\d)')
    return [l for l in 文.split('\n') if pat.search(l)]


def 人物(卡文, 册):
    出 = []
    for p in 册.get('人物', []):
        名 = p.get('名', '')
        称 = [名] + [re.split(r'[（(]', a)[0] for a in p.get('别称', []) if a]
        if not any(c and len(c) >= 2 and c in 卡文 for c in 称):
            continue
        态键 = sorted([k for k in p if re.fullmatch(r'\d+态', k)], key=lambda k: int(k[:-1]))
        行 = ['### %s（%s·末见 %s）' % (名, p.get('生死', ''), p.get('末见章', '')),
             '- 身份：' + str(p.get('身份', ''))[:600],
             '- 知：' + '；'.join(p.get('知', []))[:600],
             '- 不知：' + '；'.join(p.get('不知', []))[:400]]
        if 态键:
            行.append('- %s：%s' % (态键[-1], str(p[态键[-1]])[:900]))
        出.append('\n'.join(行))
    return 出


def 全员(册):
    """★1009 坑⑬：料包须含「已定之细」——全员生死、末见、线、最新之态（一人一行）；开镜卡点到者另有全卡。"""
    出 = []
    for p in 册.get('人物', []):
        态键 = sorted([k for k in p if re.fullmatch(r'\d+态', k)], key=lambda k: int(k[:-1]))
        亡 = ('亡於 %s' % p.get('亡於章')) if p.get('亡於章') not in (None, '', 'None') else ''
        态 = ('｜%s：%s' % (态键[-1], str(p[态键[-1]])[:140])) if 态键 else ''
        出.append('- %s｜%s%s｜末见 %s｜%s%s' % (p.get('名', ''), p.get('生死', ''), ('·' + 亡) if 亡 else '',
                                            p.get('末见章', ''), p.get('线', ''), 态))
    return 出


限料 = 120 * 1024   # ★1009 坑③：档要短——章料逾此即红（380 实 102KB）


def canon卡(卡文, 库, n, 限=24000):
    有界, 名中 = [], []
    for f in 库.get('facts', []):
        if f.get('level') not in ('ERROR', 'WARN'):
            continue
        only = f.get('only_ch') or []
        frm = f.get('from_ch')
        if (only and n in only) or (frm and frm >= n - 10 and frm <= n):
            有界.append(f)
            continue
        idn = re.sub(r'^F\d+_', '', f.get('id', ''))
        if any(w and len(w) >= 2 and w in 卡文 for w in re.split(r'[与之和、]', idn)):
            名中.append(f)
    出, 计 = [], 0
    for f in 有界 + 名中:
        s = '- **%s**（%s）：%s' % (f['id'], f.get('level'), f.get('note', '')[:900])
        if 计 + len(s) > 限:
            出.append('- ……（另 %d 卡未列，限 %d 字）' % (len(有界) + len(名中) - len(出), 限)); break
        出.append(s); 计 += len(s)
    return 出


def 段案行(n, root=ROOT):
    """1013：设定/段案/<a>-<b>.md 之「## n」一节（重、魂路、叫绝之拍、种、知之变、物之动、日、钩）；无则空。"""
    for f in sorted(glob.glob(os.path.join(root, '设定', '段案', '[0-9]*-[0-9]*.md'))):
        t = open(f, encoding='utf-8').read()
        m = re.search(r'^## %d\s*$(.*?)(?=^## |\Z)' % n, t, re.M | re.S)
        if m:
            return '（%s）\n%s' % (os.path.relpath(f, root), m.group(1).strip())
    return ''


def 引之原句(文, root=ROOT, 限=80):
    """1013（坑⑬复踩之治）：开镜卡、段案、预令所引之「章:行」（如 380:69）与「总纲:行」逐一展开为原句。
    ⛔其由：381 之料只带章号不带原句（318:33、327:29 之掰口等），五稿三稿各撞坏一处已定之细（掰口写反、空钉、床位）。
    行号逾其章之行数者（如 380:2572 是净重，不是行）⛔展；空行⛔展。"""
    出, 见, 档 = [], set(), {}
    纲 = os.path.join(root, '设定', '02_余章之势_总纲.md')
    for m in re.finditer(r'(?<![\d:])(总纲|\d{3}):(\d{1,4})(?!\d)', 文):
        k = m.group(0)
        if k in 见:
            continue
        见.add(k)
        f = 纲 if m.group(1) == '总纲' else 章档(int(m.group(1)), root)
        if not f or not os.path.exists(f):
            continue
        if f not in 档:
            档[f] = open(f, encoding='utf-8').read().split('\n')
        i = int(m.group(2))
        if 1 <= i <= len(档[f]) and 档[f][i - 1].strip():
            出.append('- %s　%s' % (k, 档[f][i - 1].strip()[:400]))
        if len(出) >= 限:
            break
    return 出


def 汇(n, root=ROOT, 出=None):
    d = os.path.join(root, '版本', '第%d章' % n)
    卡 = 读(os.path.join(d, '_开镜卡.md'))
    if not 卡:
        raise SystemExit('⛔ 无开镜卡：版本/第%d章/_开镜卡.md' % n)
    预 = 读(os.path.join(d, '_总编辑预令.md'))
    施 = 读(os.path.join(root, '设定', '01_镇冢秘术_逐章施工与伏笔回收表.md'))
    案 = 读(os.path.join(root, '设定', '剧情庭题', '余章总案.md'))
    悬 = 读(os.path.join(root, '设定', '全书记忆', '悬线.md'))
    进 = 读(os.path.join(root, '设定', '大师进化账.md'))
    拍 = 读(os.path.join(root, '设定', '叫绝之拍库.md'))
    册 = json.loads(读(os.path.join(root, '设定', '人物状态册.json')) or '{}')
    库 = json.loads(读(os.path.join(root, '设定', 'canon事实库.json')) or '{}')
    段 = []
    段.append(('开镜卡', 卡))
    案行 = 段案行(n, root)
    if 案行:
        段.append(('段案·本章之行（重、魂路、叫绝之拍、种——上游之设计，执笔照此造）', 案行))
    if 预:
        段.append(('总编辑预令', 预))
    引 = 引之原句(卡 + '\n' + 案行 + '\n' + 预, root)
    if 引:
        段.append(('开镜卡、段案所引之原句（章:行 逐一展开——写已定之细只照此，⛔凭章号猜）', '\n'.join(引)))
    门 = 节(施, '## 四、续写第 %d 章前的硬门槛' % n)
    if 门:
        段.append(('施工表·续写本章前之硬门槛', 门))
    if 案:
        段.append(('余章总案·解歧之裁', 节(案, '## 二、')))
        段.append(('余章总案·本章前後之行（%d±1）' % n, '\n'.join(本章之行(案, n))))
    for k in (n - 1, n - 2):
        f = 章档(k, root)
        if f:
            段.append(('前文·第%d章白文（全）' % k, open(f, encoding='utf-8').read()))
    人 = 人物(卡 + 预, 册)
    if 人:
        段.append(('人物之态（开镜卡点到者）', '\n\n'.join(人)))
    全 = 全员(册)
    if 全:
        段.append(('全员之账（生死、末见、线、最新之态）', '\n'.join(全)))
    c = canon卡(卡 + 预, 库, n)
    if c:
        段.append(('canon 卡（有界在前，名中在後）', '\n'.join(c)))
    悬行 = 本章之行(悬, n, 0)
    if 悬行:
        段.append(('悬线·钉在本章之行', '\n'.join(悬行)))
    教 = [l for l in 进.split('\n') if l.startswith('- ')][-30:]
    if 教:
        段.append(('大师进化账·末三十条', '\n'.join(教)))
    手 = 节(拍, '## 十条手艺') or 节(拍, '## 十')
    if 手:
        段.append(('叫绝之拍库·十条手艺', 手))
    文 = ['# 第%d章·章料（工具/章料.py 零 token 汇；席只读此档，料外只许 grep 核一处、上下三行）\n' % n]
    for 名, t in 段:
        文.append('## 〔%s〕\n\n%s\n' % (名, t.strip()))
    出 = 出 or os.path.join(d, '_料.md')
    open(出, 'w', encoding='utf-8').write('\n'.join(文))
    for 名, t in 段:
        print('  %-28s %6d 字节' % (名, len(t.encode())))
    大 = os.path.getsize(出)
    print('✓ 写 %s（%d KB）' % (os.path.relpath(出, root), 大 // 1024))
    if 大 > 限料:
        print('⛔ 章料 %d KB 逾限 %d KB（坑③：档要短——每席每回都背它）：先瘦开镜卡与预令，⛔删全员之账与 canon' % (大 // 1024, 限料 // 1024))
        return None
    return 出


def 自测():
    ok = 共 = 0
    共 += 1; ok += 本章之行('a 380 b\nc 3801 d\ne 379 f\ng 12', 380) == ['a 380 b', 'e 379 f']
    文 = '# t\n## 一、甲\nx\n## 二、乙\ny\nz\n## 三、丙\nw'
    共 += 1; ok += 节(文, '## 二、') == '## 二、乙\ny\nz'
    册 = {'人物': [{'名': '老头', '别称': ['樗里闩（终局方许）'], '生死': '存', '知': ['甲'], '不知': [], '379态': '新', '377态': '旧'}]}
    r = 人物('老头站着', 册)
    共 += 1; ok += (len(r) == 1 and '379态：新' in r[0])
    库 = {'facts': [{'id': 'F1_老头之眼', 'level': 'ERROR', 'note': 'n1'}, {'id': 'F2_别的', 'level': 'ERROR', 'note': 'n2', 'only_ch': [380]},
                    {'id': 'F3_无关', 'level': 'ERROR', 'note': 'n3'}, {'id': 'F4_债词', 'level': 'FYI', 'note': 'n4', 'only_ch': [380]}]}
    c = canon卡('老头站着', 库, 380)
    共 += 1; ok += (len(c) == 2 and 'F2_别的' in c[0] and 'F1_老头之眼' in c[1])
    全 = 全员({'人物': [{'名': '甲', '生死': '亡', '亡於章': 300, '末见章': 300, '线': '主线', '299态': '旧', '300态': '倒'},
                        {'名': '乙', '生死': '存', '亡於章': None, '末见章': 380, '线': '暗线'}]})
    共 += 1; ok += (len(全) == 2 and '亡於 300' in 全[0] and '300态：倒' in 全[0] and '亡於' not in 全[1])
    共 += 1; ok += (限料 == 120 * 1024)
    共 += 1; ok += ('魂路：翻个儿｜物证｜不说' in 段案行(386) and 段案行(999) == '')
    _f = 章档(380); _行 = open(_f, encoding='utf-8').read().split('\n') if _f else ['']
    _引 = 引之原句('见 380:1 又 380:1，又 380:2572（净重）、总纲:1、9380:1', ROOT)
    共 += 1; ok += (len(_引) == 2 and _引[0] == '- 380:1　' + _行[0].strip()[:400] and _引[1].startswith('- 总纲:1　'))
    print('章料·自测 %d/%d' % (ok, 共))
    return ok == 共


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--自测']:
        sys.exit(0 if 自测() else 1)
    if len(a) not in (1, 2) or not a[0].isdigit():
        print(__doc__); sys.exit(2)
    sys.exit(0 if 汇(int(a[0]), 出=a[1] if len(a) == 2 else None) else 1)
