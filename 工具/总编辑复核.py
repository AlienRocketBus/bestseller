# -*- coding: utf-8 -*-
"""总编辑复核——**规矩是死的，人是活的。总编辑逐条复核本仓之规：留、改、废，当场裁、当场生效。**

【其立之由（2026-09-25·作者令，逐字之意）】
  「你是总话事人，拥有对这本小说的至高决定权。规矩是死的，人是活的。之前设立的规则如果不利于这本小说写成
   中国第一，可以废除或修缮，完全由你自行决断，不需要我的指示。下面所有的东西都得听你的，由你来指导。
   把这个弄成一个机制，并且这个机制一定要行使起来。」
  ★本仓全测挂着近两百条规，**从来没有谁逐条问过一句：它让书更好了，还是在绑写的人的手？**

【唯一之问】对每一条规：**它护的是这本书的质量（让诸章合起来成中国第一），还是只在绑手、造数、逼刻意？**
  护质者留；护质而伤手者改；只绑手者废。**裁语须带实据**（它逮过哪一回真病／它逼出过哪一回凑字）。

【三路·机制之牙】
  甲·**须行使**：末一回裁在 48 小时之前 → 红。（一个不用的权，等於没有。）
  乙·**裁了须生效**：裁「废」之规，其名仍挂在全测里 → 红。（裁了不废，是纸上的裁。）
  丙·**进度**：印已复核几条／共几条，并印下三条待复核者——每一坐至少裁一条。

用法：
  python3 工具/总编辑复核.py                      # 印进度与下三条待复核
  python3 工具/总编辑复核.py --裁 <规名> 留|改|废 "<实据与其由>"
  python3 工具/总编辑复核.py --查                 # 甲乙两路（全测用）
  python3 工具/总编辑复核.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, re, sys, json, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
账档 = os.path.join(ROOT, '设定', '总编辑复核账.json')
须行使 = 48 * 3600


def 规之册():
    s = open(os.path.join(ROOT, '工具', '全测.py'), encoding='utf-8').read()
    # ★1017：并认起首之元组表（('检察官自测', chk_selftest) 一类八条——旧式只认 items.append，裁之亦不入册）
    名们 = re.findall(r"items\.append\(\('([^']+)'", s) + re.findall(r"\('([^']+)',\s*chk_\w+\)", s)
    seen, out = set(), []
    for n in 名们:
        if n not in seen:
            seen.add(n); out.append(n)
    return out


def 读账():
    try:
        return json.load(open(账档, encoding='utf-8'))
    except Exception:
        return {'裁': []}


def 写账(d):
    t = 账档 + '.tmp'
    json.dump(d, open(t, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    os.replace(t, 账档)


def 裁(名, 判, 由):
    if 判 not in ('留', '改', '废'):
        print('⛔判只许 留／改／废'); return False
    if len(由) < 12:
        print('⛔裁语须带实据（它逮过哪一回真病／逼出过哪一回凑字），不许一句空话'); return False
    d = 读账()
    d['裁'].append({'规': 名, '判': 判, '由': 由, '时': time.strftime('%Y-%m-%d %H:%M:%S')})
    写账(d)
    print('✓总编辑裁：「%s」→ %s｜%s' % (名, 判, 由))
    if 判 == '废':
        print('  ⛔裁了废，须当场从 全测.py 与其所挂之处撤下——否则 --查 乙路即红（裁了不废是纸上的裁）。')
    return True


def 查(印=True):
    d = 读账(); 坏 = []
    if not d['裁']:
        坏.append('甲·总编辑复核一条也没裁过——权不行使，等於没有')
    else:
        末 = max(time.mktime(time.strptime(x['时'], '%Y-%m-%d %H:%M:%S')) for x in d['裁'])
        if time.time() - 末 > 须行使:
            坏.append('甲·末一回裁在 %.0f 小时之前（>48）——总编辑之权须行使' % ((time.time() - 末) / 3600))
    现 = set(规之册())
    废了没撤 = [x['规'] for x in d['裁'] if x['判'] == '废' and x['规'] in 现]
    if 废了没撤:
        坏.append('乙·裁了「废」而仍挂在全测：%s' % '、'.join(废了没撤))
    if 印:
        for x in 坏:
            print('  ⛔ ' + x)
        if not 坏:
            print('  ✓ 总编辑复核：权在行使，裁皆生效。')
    return not 坏, 坏


def 进度():
    d = 读账(); 册 = 规之册()
    已 = {x['规'] for x in d['裁']}
    待 = [n for n in 册 if n not in 已]
    print('════ 总编辑复核 ════（规矩是死的，人是活的：留／改／废，由总编辑当场裁）')
    print('  已复核 %d 条｜全测挂规 %d 条｜待复核 %d 条' % (len(已 & set(册)), len(册), len(待)))
    for x in d['裁'][-3:]:
        print('  · 近裁：「%s」→ %s｜%s' % (x['规'], x['判'], x['由'][:60]))
    print('  ★下三条待复核（每一坐至少裁一条；只问：它护质，还是绑手？）：')
    for n in 待[:3]:
        print('     · %s' % n)
    查()


def 自测():
    import tempfile
    global 账档
    旧 = 账档
    账档 = os.path.join(tempfile.mkdtemp(), 'z.json')
    r = []
    r.append(('①空账即红（权不行使）', not 查(印=False)[0]))
    r.append(('②裁语太短不收', not 裁('x', '留', '好')))
    r.append(('③判只许留改废', not 裁('x', '毁', '这一条逼出过三回凑字，废之')))
    裁('爆窗', '留', '0924 逮过 363 之窗爆一回，护质')
    r.append(('④新裁之後甲路过', 查(印=False)[0]))
    裁('爆窗', '废', '假设之废，以验乙路：裁了废而仍挂全测')
    r.append(('⑤裁废而仍挂全测即红（裁须生效）', not 查(印=False)[0]))
    账档 = 旧
    for n, v in r:
        print(('  ✓ ' if v else '  ⛔ ') + n)
    print('负测·总编辑复核 %d/%d' % (sum(v for _, v in r), len(r)))
    return all(v for _, v in r)


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--自测' in a:
        sys.exit(0 if 自测() else 1)
    if '--查' in a:
        sys.exit(0 if 查()[0] else 1)
    if '--裁' in a:
        i = a.index('--裁')
        sys.exit(0 if 裁(a[i + 1], a[i + 2], a[i + 3]) else 1)
    进度()
