#!/usr/bin/env python3
"""费哨（1021 立·作者问「七成的 token 竟然没有用来写书……为什么都耗费了这么多 token，你都没有做出一个及时的措施」）。

为何立：诸复盘只比「同类之上回」——每件都比上回同类省，而非写书之件越开越多，没有一处看全局之钱落在哪。
本哨零 token：读 设定/费账.json（费审.py --记／--记主 所写），按件分「写书」（一章、造剧情）与「非写书」，
看末 N 件（默认 10 件，以 W 号计）写书之占；⛔低於七成即红（裁_1021_省律 三之1「七三之律」）。
跑口：工作流账.py 印（每回会话开头先跑）之首行；工作流账 --开 一件非写书之件而哨红者拒开，
      除非有效之据写明「挡路：」（挡下一章之料或闸）或「读者可见：」（读者读得到之病）及其由。
用法：
  python3 工具/费哨.py            # 印末十件之占；红则 rc=1
  python3 工具/费哨.py --件 20    # 看末二十件
  python3 工具/费哨.py --章       # 开章之检（自走.py 每回首印之）
  python3 工具/费哨.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, re, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
界 = 0.70
写书类 = ('一章', '造剧情')
写书词 = re.compile(r'造式|二代|第\d+章|剧情庭|段案|余章总案|造剧情')
例外式 = re.compile(r'(挡路|读者可见)[：:]\s*(?:\S\s*){4,}')   # 由须四字以上（空白不计）


def 类表(root=ROOT):
    """W 号 → 复盘所书之类（「- 类：一章（…）」取括号前）。"""
    表 = {}
    for p in glob.glob(os.path.join(root, '设定', '复盘', '*.md')):
        m = re.search(r'_(W\d+)_', os.path.basename(p))
        if not m:
            continue
        try:
            t = open(p, encoding='utf-8').read()
        except Exception:
            continue
        k = re.search(r'^- 类：\s*([^（(\n]+)', t, re.M)
        if k:
            表[m.group(1)] = k.group(1).strip()
    return 表


def 判类(名, 表):
    """返（W 号或 None, 是否写书）。"""
    m = re.match(r'(W\d+)', 名 or '')
    w = m.group(1) if m else None
    if w and w in 表:
        return w, 表[w] in 写书类
    return w, bool(写书词.search(名 or ''))


def 算(行, 表, 件=10):
    """行：费账之行；只计 wf_、子席:、主环: 三种（主会话: 係其总，⛔重加）。返 (写, 非, 诸件)。"""
    按件 = {}
    for r in 行:
        键 = str(r.get('键', ''))
        if 键.startswith('主会话'):
            continue
        w, 写 = 判类(r.get('名', ''), 表)
        if not w:
            continue
        a = 按件.setdefault(w, {'名': r.get('名', ''), '美元': 0.0, '写': 写})
        a['美元'] += float(r.get('美元') or 0)
    末 = sorted(按件, key=lambda x: int(x[1:]))[-件:]
    写 = sum(按件[w]['美元'] for w in 末 if 按件[w]['写'])
    非 = sum(按件[w]['美元'] for w in 末 if not 按件[w]['写'])
    return 写, 非, [(w, 按件[w]) for w in 末]


def 判(root=ROOT, 件=10):
    """返 (红否, 一行之述, 诸件)。"""
    try:
        行 = json.load(open(os.path.join(root, '设定', '费账.json'), encoding='utf-8'))['行']
    except Exception as e:
        return False, '费哨：费账读不得（%s）——只报不拦' % e, []
    写, 非, 诸 = 算(行, 类表(root), 件)
    共 = 写 + 非
    if 共 <= 0:
        return False, '费哨：末 %d 件无费可计' % 件, 诸
    占 = 写 / 共
    红 = 占 < 界
    述 = '%s 费哨：末 %d 件（%s—%s）写书 $%.0f／非写书 $%.0f——写书之占 %.0f%%（界 ≥%.0f%%·裁_1021_省律）%s' % (
        '⛔' if 红 else '✓', len(诸), 诸[0][0] if 诸 else '', 诸[-1][0] if 诸 else '', 写, 非, 占 * 100, 界 * 100,
        '：非写书之件只许「挡路：」「读者可见：」二种方开' if 红 else '')
    return 红, 述, 诸


def 许开(名, 有效之据, root=ROOT):
    """工作流账 --开 所调：返 (许否, 由)。写书之件恒许；非写书之件於哨红时须带例外之由。"""
    _, 写 = 判类(名, 类表(root))
    if 写:
        return True, ''
    红, 述, _ = 判(root)
    if not 红:
        return True, ''
    if 例外式.search(有效之据 or ''):
        return True, '费哨红而有例外之由：' + 例外式.search(有效之据).group(0)
    return False, 述 + '——此件非写书，有效之据须写「挡路：<挡哪一章之料或闸>」或「读者可见：<哪一处之病>」'


def 章检(root=ROOT):
    """★1021 作者令「每一章只要一开始就看看原来的方法还行不行……一想能想出来，⛔过度消耗」：零 token 印数行——
    末五章之费与其势、主环之占、写书之占、账限之欠，并三问（章末简式复盘照答）。返 [行]。"""
    L = ['── 开章之检（零 token·省律）──']
    try:
        行 = json.load(open(os.path.join(root, '设定', '费账.json'), encoding='utf-8'))['行']
    except Exception:
        行 = []
    表 = 类表(root)
    章费 = {}
    for r in 行:
        if str(r.get('键', '')).startswith('主会话'):
            continue
        w, 写 = 判类(r.get('名', ''), 表)
        if not w or not re.search(r'第?\d{3}章?造式|二代', r.get('名', '')):
            continue
        a = 章费.setdefault(w, {'名': r.get('名', ''), '席': 0.0, '主': 0.0})
        a['主' if str(r.get('键', '')).startswith('主环') else '席'] += float(r.get('美元') or 0)
    末 = sorted(章费, key=lambda x: int(x[1:]))[-5:]
    if 末:
        L.append('  末五章：' + '｜'.join('%s $%.0f（主环 %.0f%%）' % (re.sub(r'^W\d+·', '', 章费[w]['名'])[:8], 章费[w]['席'] + 章费[w]['主'],
                 100 * 章费[w]['主'] / max(0.01, 章费[w]['席'] + 章费[w]['主'])) for w in 末))
        均 = sum(章费[w]['席'] + 章费[w]['主'] for w in 末) / len(末)
        L.append('  每章均 $%.0f；的 ≤$30、主环 ≤$5（裁_1021_省律）' % 均)
    L.append('  ' + 判(root)[1])
    try:
        import 账限哨
        L.append('  ' + 账限哨.印(root)[1][0])
    except Exception:
        pass
    L.append('  三问（章末 `复盘.py W 题 runs --简` 一句一答）：法行否｜最贵之席值否｜进化（入账 X 号或已行或无）')
    return L


def 自测():
    r = []
    def T(名, 条):
        r.append((名, bool(条)))
        print(('  ✓ ' if 条 else '  ✗ ') + 名)
    表 = {'W1': '一章', 'W2': '治器设计', 'W3': '造剧情', 'W4': '核验'}
    行 = [{'键': 'wf_a', '名': 'W1·写', '美元': 30}, {'键': '主环:x', '名': 'W1·写', '美元': 10},
          {'键': 'wf_b', '名': 'W2·器', '美元': 50}, {'键': 'wf_c', '名': 'W3·段', '美元': 20},
          {'键': '主会话:z', '名': 'W1·写', '美元': 999}, {'键': 'wf_d', '名': 'W4·审', '美元': 10}]
    写, 非, 诸 = 算(行, 表, 10)
    T('①写书＝一章＋造剧情（30+10+20）', 写 == 60)
    T('②非写书＝治器＋核验（50+10）', 非 == 60)
    T('③主会话之行⛔重加', all(x[1]['美元'] < 999 for x in 诸))
    写2, 非2, 诸2 = 算(行, 表, 2)
    T('④末 N 件以 W 号之序取（末二件 W3、W4）', [w for w, _ in 诸2] == ['W3', 'W4'] and 写2 == 20 and 非2 == 10)
    T('⑤无复盘之件以名判：「W9·第401章造式」写书', 判类('W9·第401章造式', 表)[1] is True)
    T('⑥无复盘之件以名判：「W9·D1之备」非写书', 判类('W9·D1之备', 表)[1] is False)
    T('⑦例外之由须四字以上', 例外式.search('挡路：401 之料缺此') and not 例外式.search('挡路：无'))
    # ⑧许开：以 tempdir 造一局红账
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, '设定', '复盘'))
        json.dump({'行': [{'键': 'wf_a', '名': 'W1·器', '美元': 90}, {'键': 'wf_b', '名': 'W2·第9章造式', '美元': 10}]},
                  open(os.path.join(d, '设定', '费账.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        红, 述, _ = 判(d)
        T('⑧写书 10%＜七成即红', 红)
        T('⑨哨红：非写书之件无例外拒开', 许开('W3·治器三批', '据', d)[0] is False)
        T('⑩哨红：非写书之件带「挡路：」许开', 许开('W3·治器三批', '挡路：401 之料缺远引', d)[0] is True)
        T('⑪哨红：写书之件恒许', 许开('W3·第10章造式', '', d)[0] is True)
    ok = sum(v for _, v in r)
    print('费哨·自测 %d/%d%s' % (ok, len(r), ' 全通' if ok == len(r) else ' 未过'))
    return ok == len(r)


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--自测' in a:
        sys.exit(0 if 自测() else 1)
    if '--章' in a:
        print('\n'.join(章检())); sys.exit(0)
    n = int(a[a.index('--件') + 1]) if '--件' in a else 10
    红, 述, 诸 = 判(ROOT, n)
    print(述)
    for w, x in 诸:
        print('  %s %-28s $%7.2f %s' % (w, x['名'][:28], x['美元'], '写书' if x['写'] else '非写书'))
    sys.exit(1 if 红 else 0)
