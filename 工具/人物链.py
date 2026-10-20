#!/usr/bin/env python3
"""人物链（1015 立·W34 换法·作者令「审人物要从头到尾；用脑子⛔蛮力；每个 token 发挥最大之效」）——零 token。

为何立：W34 初法（一人一席、各读其料）有二病——①⛔从头到尾：人物料逾 140KB 即舍，主角诸人舍六百至一千行，
  苏衍 317 章只到 116 章；②重读：十二席各取其章，同一章被读多回。1015 实量：全书白文 1,616,539 字，
  章记 12.6MB（比书本身大 2.6 倍）——**读白文一遍比读章记还省**。故换法：
  **全书白文只读一遍**（分段诸席，逐章记在场每人之「做、说、智、反智、记号、关系、变」，句带行号），
  本器把诸段之记**零 token 并成每人从第 1 章到末章之一条链**；审人之席只读其人之链（全程而薄），⛔再读书。
  链是永久之档：此後每章之记席只添本章之条（见 用法.md），**全书永不须为人物再通读**。
⛔限：只收、只验、只并、只抽样；⛔判。每条所引之句（line＋line_ln）机器逐条核於白文，不合者照实印、⛔入链。

用法：
  python3 工具/人物链.py --分 K [自 至]        # 按白文之字数把 自—至 分成 K 段（连续、字数相近）→ 印 JSON
  python3 工具/人物链.py --收 <journal.jsonl>   # 从工作流之 journal 收诸段读席之交 → 设定/全书记忆/人物链/_段/a-b.json
  python3 工具/人物链.py --验                   # 诸段之引句核於白文；章之覆盖（缺章照实印）
  python3 工具/人物链.py --并记                 # ★主法：自章记之「在场之人」零 token 并成每人之链（⛔读书）
  python3 工具/人物链.py --样 [每格N]           # 认声之样：照人×段分层抽其句 → 设定/_草/W34/声键.json、声题.json
  python3 工具/人物链.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, re, glob, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
链目 = os.path.join('设定', '全书记忆', '人物链')
段目 = os.path.join(链目, '_段')

# 正名：读席所交之 who → 链之名（别称归一）
正名 = {
    '我': '苏衍', '苏衍': '苏衍', '老头': '老头', '独眼老头': '老头', '钱满': '钱满', '刘二': '刘二',
    '东头': '东头', '东头那个汉子': '东头', '沈鸢': '沈鸢', '她': '沈鸢',
    '床上那人': '床上那人', '床上那个人': '床上那人', '阿禾': '床上那人',
    '坡下那汉子': '坡下那汉子', '搁柴之人': '坡下那汉子', '那孩子': '那孩子', '半大孩子': '那孩子',
    '霍钧': '霍钧', '黎东来': '黎东来', '赵阙': '赵阙', '门後之物': '赵阙', '门后之物': '赵阙',
    '测绘那个年轻人': '测绘那个年轻人', '测绘': '测绘那个年轻人',
}
主角诸人 = ['苏衍', '老头', '钱满', '刘二', '东头']


def 白文(n, root=ROOT):
    import 章料
    f = 章料.章档(n, root)
    if not f:
        return None
    t = open(f, encoding='utf-8').read()
    i = t.find('【本章亮点】')
    return t[:i] if i >= 0 else t


def 末章(root=ROOT):
    n = 1
    while 白文(n + 1, root) is not None:
        n += 1
    return n


def 分(K, 自=1, 至=None, root=ROOT):
    至 = 至 or 末章(root)
    长 = [(n, len(白文(n, root) or '')) for n in range(自, 至 + 1)]
    总 = sum(x for _, x in 长); 每 = 总 / K
    出 = []; 起 = 自; 累 = 0
    for n, x in 长:
        累 += x
        if 累 >= 每 * (len(出) + 1) and len(出) < K - 1 and n < 至:
            出.append([起, n]); 起 = n + 1
    出.append([起, 至])
    return 出


def 归名(w):
    w = (w or '').strip()
    if w in 正名:
        return 正名[w]
    for k, v in 正名.items():
        if len(k) >= 2 and k in w:
            return v
    return w


def 收(journal, root=ROOT):
    """journal 里读席（label 起「读·」）之 result → _段/a-b.json；→ [档]"""
    标 = {}; 出 = []
    os.makedirs(os.path.join(root, 段目), exist_ok=True)
    for l in open(journal, encoding='utf-8'):
        try:
            d = json.loads(l)
        except Exception:
            continue
        if d.get('type') == 'started':
            标[d.get('key')] = d.get('label') or ''
        elif d.get('type') == 'result' and 标.get(d.get('key'), '').startswith('读·'):
            r = d.get('result') or {}
            章们 = r.get('chapters') or []
            if not 章们:
                continue
            ns = [int(c.get('n')) for c in 章们 if str(c.get('n', '')).isdigit() or isinstance(c.get('n'), (int, float))]
            m = re.search(r'(\d+)—(\d+)', 标[d['key']])
            a, b = (int(m.group(1)), int(m.group(2))) if m else (min(ns), max(ns))
            p = os.path.join(root, 段目, '%d-%d.json' % (a, b))
            json.dump({'段': [a, b], '章们': 章们}, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            出.append(p)
    return 出


def 诸段(root=ROOT):
    出 = []
    for p in sorted(glob.glob(os.path.join(root, 段目, '*.json')), key=lambda x: int(re.search(r'(\d+)-', os.path.basename(x)).group(1))):
        出.append(json.load(open(p, encoding='utf-8')))
    return 出


def 核句(n, 句, 行, root=ROOT, 文=None):
    """引句在白文之第「行」行（±1 行，读席之行号偶差一行）→ (合否, 实在之行或 None)"""
    句 = re.sub(r'^[“「"]|[”」"]$', '', (句 or '').strip())
    if not 句:
        return True, None
    文 = 文 if 文 is not None else (白文(n, root) or '')
    L = 文.split('\n')
    核 = 句[:24]
    try:
        k = int(re.search(r'\d+', str(行)).group())
    except Exception:
        k = None
    if k:
        for j in (k, k - 1, k + 1):
            if 1 <= j <= len(L) and 核 in L[j - 1]:
                return True, j
    for j, l in enumerate(L, 1):
        if 核 in l:
            return False, j
    return False, None


def 验(root=ROOT, 印=True):
    段们 = 诸段(root)
    有 = set(); 错 = []; 计 = 0
    for s in 段们:
        for c in s['章们']:
            n = int(c.get('n')); 有.add(n); 文 = 白文(n, root) or ''
            for x in c.get('cast') or []:
                if x.get('line'):
                    计 += 1
                    合, 实 = 核句(n, x['line'], x.get('line_ln'), root, 文)
                    if not 合:
                        错.append('%d:%s %s「%s」%s' % (n, x.get('line_ln'), 归名(x.get('who')), x['line'][:20], ('实在 :%d' % 实) if 实 else '白文无此句'))
    末 = 末章(root)
    缺 = [n for n in range(1, 末 + 1) if n not in 有]
    if 印:
        print('人物链·验：段 %d、章 %d／%d、引句 %d（不合 %d）' % (len(段们), len(有), 末, 计, len(错)))
        for e in 错[:30]:
            print('  ⛔ ' + e)
        if 缺:
            print('  缺章 %d：%s' % (len(缺), _段(缺)))
    return 缺, 错, 计


def _段(ns):
    出 = []; i = 0
    while i < len(ns):
        j = i
        while j + 1 < len(ns) and ns[j + 1] == ns[j] + 1:
            j += 1
        出.append(str(ns[i]) if i == j else '%d—%d' % (ns[i], ns[j])); i = j + 1
    return '、'.join(出)


def 样(每格=6, root=ROOT, 出目=os.path.join('设定', '_草', 'W34')):
    """主角诸人（与测绘、黎东来、霍钧）× 四段，每格取至多「每格」句（≥4 字、各章均取）→ 键、题（题照字序乱之）"""
    人 = {}
    for s in 诸段(root):
        for c in s['章们']:
            n = int(c.get('n')); 文 = 白文(n, root) or ''
            for x in c.get('cast') or []:
                名 = 归名(x.get('who')); 句 = re.sub(r'^[“「"]|[”」"]$', '', (x.get('line') or '').strip())
                if 名 and len(句) >= 4 and 核句(n, 句, x.get('line_ln'), root, 文)[0]:
                    人.setdefault(名, []).append((n, x.get('line_ln'), 句))
    键 = []
    for 名 in 主角诸人 + ['测绘那个年轻人', '黎东来', '霍钧', '沈鸢']:
        for a, b in ((1, 100), (101, 200), (201, 300), (301, 10 ** 6)):
            格 = [x for x in 人.get(名, []) if a <= x[0] <= b]
            if not 格:
                continue
            步 = max(1, len(格) // 每格)
            for n, ln, 句 in 格[::步][:每格]:
                键.append({'章行': '%d:%s' % (n, ln), '说者': 名, '句': 句, '段': '%d—' % a})
    题 = sorted(range(len(键)), key=lambda i: (键[i]['句'], i))
    os.makedirs(os.path.join(root, 出目), exist_ok=True)
    json.dump(键, open(os.path.join(root, 出目, '声键.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    json.dump([{'号': k + 1, '句': 键[i]['句']} for k, i in enumerate(题)] + [{'序': 题}],
              open(os.path.join(root, 出目, '声题.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return 键, 题


# ★1015 W34 再换法：章记之「在场之人」本即逐章精读者所记（1—388 俱有，伤／所携／之状／所知……带行号），
#   人之链由此零 token 并成，⛔再读书；读席之试（369—388）只作对照：新读能否逮出章记所无之智、反智、记号。
留类 = ('之状', '所为', '所知', '所瞒', '不知', '不知／未到', '本章所追', '状')
舍类 = ('所携', '伤', '伤／身', '身', '伤／形', '所携／所用', '年')


def 记名(h):
    """章记「在场之人」条之粗体名 → 链之名；⛔立链者（提及而不在场、诸人与物）→ ''"""
    h = h.strip()
    if any(k in h for k in ('提及', '诸人与物', '不在场')) or h in ('其人',):
        return ''
    if '苏衍' in h or h.startswith('我'):
        return '苏衍'
    if '沈鸢' in h or h == '她' or h.startswith('她（') or h.startswith('她('):
        return '沈鸢'
    if '师父' in h:
        return '老头之师父' if '老头' in h else ''
    if '东头' in h and any(k in h for k in ('兄', '哥')):
        return '东头之兄'
    if '刘二' in h and any(k in h for k in ('妻', '婆娘', '家')):
        return '刘二之妻'
    if h.startswith('坡上下来那一个') or h.startswith('末一个窝跟前蹲着那一个'):     # 名之律：319、326、362 即老头（圣经 319 条、CHAR-362A）
        return '老头'
    for k, v in (('门后', '赵阙'), ('门後', '赵阙'), ('古尸', '古尸'), ('老头', '老头'), ('钱满', '钱满'), ('刘二', '刘二'), ('东头', '东头'), ('床上', '床上那人'), ('阿禾', '床上那人'),
                 ('搁柴', '坡下那汉子'), ('孩子', '那孩子'), ('霍钧', '霍钧'), ('黎东来', '黎东来'), ('测绘', '测绘那个年轻人'),
                 ('老周', '老周'), ('管粮', '老周'), ('寨老', '寨老'), ('陈砚', '陈砚')):
        if k in h:
            return v
    return re.sub(r'[（(].*$', '', h).strip('「」 ')[:12]


def 记条(体):
    """一条之文 → 只留之状、所知、所为、所瞒……（伤、所携⛔留）；无类标者全留"""
    段们 = re.split(r'(\*\*[^*：:]{1,6}\*\*[：:])', 体)
    if len(段们) < 3:
        return 体.strip()
    出 = [段们[0].strip()] if 段们[0].strip() else []
    for i in range(1, len(段们) - 1, 2):
        类 = re.sub(r'[*：:]', '', 段们[i])
        if 类 in 舍类:
            continue
        出.append(段们[i] + 段们[i + 1].strip())
    return ' '.join(x for x in 出 if x).strip()


def 在场块(t):
    """章记之「在场之人」块；首行可带括注（121、151 之式：「- 在场之人（行次：……）：」——1015 漏十四章之教）"""
    return re.search(r'^- 在场之人[^\n]*?[：:](.*?)(?=^- \S|^## |\Z)', t, re.M | re.S)


def 从记(root=ROOT):
    """→ {名: [(章, 线, 文)]}、无「在场之人」之章"""
    人 = {}; 无 = []
    for f in glob.glob(os.path.join(root, '设定', '全书记忆', '第*章.md')):
        n = int(re.search(r'第(\d+)章', f).group(1)); t = open(f, encoding='utf-8').read()
        线 = re.search(r'^- 线与日[：:]\s*\**([主暗][线]?)', t, re.M)
        线 = 线.group(1)[:1] if 线 else ''
        m = 在场块(t)
        if not m:
            无.append(n); continue
        for h, 体 in re.findall(r'^\s+- \*\*([^*]+)\*\*(.*?)(?=^\s+- \*\*|\Z)', m.group(1), re.M | re.S):
            名 = 记名(h)
            if not 名:
                continue
            文 = 记条(re.sub(r'\s*\n\s*', ' ', 体).lstrip('：: '))
            if 文:
                人.setdefault(名, []).append((n, 线, 文))
    for v in 人.values():
        v.sort()
    return 人, sorted(无)


def 并记(root=ROOT):
    人, 无 = 从记(root)
    os.makedirs(os.path.join(root, 链目), exist_ok=True)
    索 = ['# 人物链·索引（零 token 所并·工具/人物链.py --并记）', '',
          '> 每人从第 1 章到末章之链，并自各章记（设定/全书记忆/第N章.md）之「在场之人」——那是逐章精读者所记，'
          '此处只留其「之状、所知、所为、所瞒」（伤、所携⛔留，要者回章记取）。⛔再为人物通读全书；此後每章封版即重并。', '',
          '无「在场之人」之章（其人回章记之按拍取）：' + (_段(无) or '无'), '',
          '| 人 | 在场章数 | 首见 | 末见 | 千字 | 链 |', '|---|---|---|---|---|---|']
    for 名, 条 in sorted(人.items(), key=lambda kv: -len(kv[1])):
        ns = [n for n, _, _ in 条]; 字 = sum(len(x) for _, _, x in 条)
        if len(条) >= 2:
            档 = re.sub(r'[\\/:*?"<>|·\s]', '_', 名)[:30]
            体 = ['# 人物链·%s（第 %d—%d 章，在场 %d 章）' % (名, min(ns), max(ns), len(条)), '',
                  '> 一章一条，自章记「在场之人」并（之状、所知、所为、所瞒；L＝白文行号）。零 token；章记改则重并。', '']
            体 += ['- 〔%d·%s〕%s' % (n, 线, x) for n, 线, x in 条]
            open(os.path.join(root, 链目, '%s.md' % 档), 'w', encoding='utf-8').write('\n'.join(体) + '\n')
            链 = '`%s.md`' % 档
        else:
            链 = '（一章）'
        索.append('| %s | %d | %d | %d | %d | %s |' % (名, len(条), min(ns), max(ns), 字 // 1000, 链))
    open(os.path.join(root, 链目, '人物链.md'), 'w', encoding='utf-8').write('\n'.join(索) + '\n')
    return 人, 无


# ★1015 作者之议「人物链从头到尾所有角色、并每人之间之相互关系」——零 token：关系由章记「在场之人」里甲之条提到乙而得（虹吸：记席每章本就记，此只并）
关称 = (('苏衍', ('苏衍',)), ('老头', ('老头', '独眼')), ('钱满', ('钱满',)), ('刘二', ('刘二',)), ('东头', ('东头',)),
        ('沈鸢', ('沈鸢',)), ('床上那人', ('床上那', '阿禾')), ('坡下那汉子', ('搁柴', '她男人')), ('那孩子', ('那孩子', '半大孩子')),
        ('霍钧', ('霍钧', '师父')), ('黎东来', ('黎东来',)), ('测绘那个年轻人', ('测绘',)), ('寨老', ('寨老',)), ('陈砚', ('陈砚',)), ('老周', ('老周', '管粮')))


def 关系(人):
    """→ {(甲, 乙): [(章, 谁之条, 片)]}、同场之数 {(甲, 乙): n}"""
    对 = {}; 同 = {}
    名单 = [k for k, _ in 关称]
    在 = {}
    for 名, 条 in 人.items():
        for n, _, _ in 条:
            在.setdefault(n, set()).add(名)
    for n, s in 在.items():
        s = sorted(x for x in s if x in 名单)
        for i in range(len(s)):
            for j in range(i + 1, len(s)):
                同[(s[i], s[j])] = 同.get((s[i], s[j]), 0) + 1
    for 名, 条 in 人.items():
        if 名 not in 名单:
            continue
        for n, _, 文 in 条:
            句们 = re.split(r'(?<=[。；])', re.sub(r'\*\*', '', 文))
            for 乙, 称们 in 关称:
                if 乙 == 名:
                    continue
                if 乙 == '霍钧' and 名 != '沈鸢':      # 「师父」只在她之条里指霍钧
                    称们 = ('霍钧',)
                片 = [x.strip() for x in 句们 if any(c in x for c in 称们)]
                if 片:
                    k = tuple(sorted((名, 乙)))
                    对.setdefault(k, []).append((n, 名, ' '.join(片)[:160]))
    for v in 对.values():
        v.sort()
    return 对, 同


def 写关系(人, root=ROOT):
    对, 同 = 关系(人)
    目 = os.path.join(root, 链目, '关系')
    os.makedirs(目, exist_ok=True)
    for f in glob.glob(os.path.join(目, '*.md')):
        os.remove(f)
    主 = [k for k, _ in 关称][:11]
    索 = ['# 关系链·索引（零 token·工具/人物链.py --并记）', '',
          '> 每两人之间从头到尾之拍：甲之章记条里提到乙之句（带章号、L＝白文行号），按章序；同场之数＝两人同在一章之「在场之人」。'
          '⛔另读书；章记改则重并。此为索引——一对之全链在 `关系/甲—乙.md`。', '',
          '## 同场之数（主要诸人）', '', '| | ' + ' | '.join(主) + ' |', '|---|' + '---|' * len(主)]
    for a in 主:
        索.append('| %s | %s |' % (a, ' | '.join('—' if a == b else str(同.get(tuple(sorted((a, b))), '')) for b in 主)))
    索 += ['', '## 诸对（拍数≥3）', '', '| 对 | 拍数 | 首拍 | 末拍 | 链 |', '|---|---|---|---|---|']
    for k, v in sorted(对.items(), key=lambda kv: -len(kv[1])):
        if len(v) < 3:
            continue
        档 = '%s—%s.md' % k
        体 = ['# 关系链·%s—%s（%d 拍，第 %d—%d 章）' % (k[0], k[1], len(v), v[0][0], v[-1][0]), '',
              '> 甲之条提到乙之句，按章序（〔章·谁之条〕）。零 token 自章记「在场之人」并。', '']
        体 += ['- 〔%d·%s〕%s' % (n, 谁, 片) for n, 谁, 片 in v]
        open(os.path.join(目, 档), 'w', encoding='utf-8').write('\n'.join(体) + '\n')
        索.append('| %s—%s | %d | %d | %d | `关系/%s` |' % (k[0], k[1], len(v), v[0][0], v[-1][0], 档))
    open(os.path.join(root, 链目, '关系.md'), 'w', encoding='utf-8').write('\n'.join(索) + '\n')
    return 对, 同


def 自测():
    ok = 共 = 0
    共 += 1; ok += _段([1, 2, 3, 7, 9, 10]) == '1—3、7、9—10'
    共 += 1; ok += 归名('东头那个汉子') == '东头' and 归名('我') == '苏衍' and 归名('阿禾') == '床上那人'
    文 = '甲\n“找路。”我说。\n丙'
    共 += 1; ok += 核句(1, '找路。', 2, 文=文) == (True, 2) and 核句(1, '找路。', 3, 文=文) == (True, 2) and 核句(1, '找路。', 9, 文=文) == (False, 2)
    s = 分(4, 1, 40)
    共 += 1; ok += (s[0][0] == 1 and s[-1][1] == 40 and len(s) == 4 and all(s[i][1] + 1 == s[i + 1][0] for i in range(3)))
    共 += 1; ok += 记名('我（苏衍）') == '苏衍' and 记名('她（沈鸢；白文不书其名）') == '沈鸢' and 记名('提及而不在场') == '' and 记名('「他」（搁柴之人）') == '坡下那汉子'
    共 += 1; ok += 记条('**伤**：痛（L1）。**所携**：刀。**之状**：走（L2）。') == '**之状**：走（L2）。'
    对, 同 = 关系({'刘二': [(150, '主', '**之状**：「他行吗。」——问的是老头（L43）；递灯给钱满。')], '老头': [(150, '主', '咽了一下')]})
    共 += 1; ok += (('刘二', '老头') in 对 or ('老头', '刘二') in 对) and 同.get(('刘二', '老头')) == 1
    共 += 1; ok += bool(在场块('- 在场之人（行次：老头最前）：\n  - **老头**：走。\n- 物：')) and '**老头**' in 在场块('- 在场之人：\n  - **老头**：走。\n- 物：').group(1)
    t = 白文(386) or ''
    共 += 1; ok += 核句(386, '你们找什么？', 33, 文=t)[0]                    # 实章之引句核得着（W34 小样之键）
    print('人物链·自测 %d/%d' % (ok, 共))
    return ok == 共


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--自测']:
        sys.exit(0 if 自测() else 1)
    if a[:1] == ['--分']:
        K = int(a[1]); 自 = int(a[2]) if len(a) > 2 else 1; 至 = int(a[3]) if len(a) > 3 else None
        print(json.dumps(分(K, 自, 至))); sys.exit(0)
    if a[:1] == ['--收'] and len(a) == 2:
        ps = 收(a[1]); print('✓ 收 %d 段：%s' % (len(ps), '、'.join(os.path.basename(p) for p in ps))); sys.exit(0 if ps else 1)
    if a == ['--验']:
        缺, 错, 计 = 验(); sys.exit(0 if not 错 else 1)
    if a == ['--并记']:
        人, 无 = 并记(); 对, 同 = 写关系(人); print('关系：%d 对（≥3 拍 %d 对）' % (len(对), sum(1 for v in 对.values() if len(v) >= 3))); print('✓ 并记：%d 人（链 %d 条）→ %s/；无在场之人之章 %d' % (len(人), sum(1 for v in 人.values() if len(v) >= 2), 链目, len(无))); sys.exit(0)
    if a == ['--并']:   # ★1020 淘汰之律：旧法（段读之并）已删——跑之即以段之薄链覆主链（1020 实踩：12 链 1775 行被覆，git 还原）；主法 --并记
        print('⛔ --并 已删（旧法·段读之并，为 --并记 所代）：python3 工具/人物链.py --并记'); sys.exit(2)
    if a[:1] == ['--样']:
        键, 题 = 样(int(a[1]) if len(a) > 1 else 6); print('✓ 认声之样 %d 句' % len(键)); sys.exit(0)
    print(__doc__); sys.exit(2)
