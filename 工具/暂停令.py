#!/usr/bin/env python3
"""暂停令（1009 立·治「作者之暂停令只在文里、不在盘上」）——诸器认作者之暂停，一处判、处处用。

为何立：1008 作者令「380 封版之後即暂停，⛔开写 381、⛔开耗 token 之工作流，待下週 token 重置、作者令下再开」。
此令只写在四入口档里，盘上无据：①接力闸照旧判「断流」，全测红、推被拦；②新一坐依律先跑 `自走.py`，
它不知有暂停，会印「派下一席」——**正好违令**（D6 之教训：一週之资源一事无成）。
本器把暂停令放到盘上（`设定/暂停令.json`），接力与自走只问它一句：暂停令在不在。

待（1023 立·作者令「写完第410章，然后大审完之後，先暂停」）：令可带 `"待": {"大审至": N}`——大审之册至第 N 章
（非空模子）成之前令「待」而不在（诸器照常走到那一步），成即自在（自走印【判】停、会话之守拦开会话、段序之守拦开庭开写）；
⛔凭某坐记得到点去立令（409、410 与大审俱由接力之会话自跑，无人盯）。

防滥（⛔拿一个旗把闸关掉）：令须引作者原话（「令」含「作者令」），其「据」须指到入口档里真有「暂停令」三字之那一行；
二者缺一即不认，诸闸照旧。解令只一条路：`--解 "<作者之言>"`，记其时与其言，⛔删档。

用法：
  python3 工具/暂停令.py --查                  # 在不在、立於何时、令之原文、其据
  python3 工具/暂停令.py --解 "作者令：……"      # 作者令下方解；记时与言
  python3 工具/暂停令.py --例外 W18 "作者令：……"  # 暂停之中作者亲令一件：只许此一件开一回（记时与言；用即销），其余照停
  python3 工具/暂停令.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, re, json, time, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
档 = os.path.join('设定', '暂停令.json')


def 读令(root=ROOT):
    p = os.path.join(root, 档)
    try:
        return json.load(open(p, encoding='utf-8'))
    except Exception:
        return None


def 据之行(据, root=ROOT):
    m = re.fullmatch(r'(.+):(\d+)', 据 or '')
    if not m:
        return ''
    p = os.path.join(root, m.group(1))
    try:
        return open(p, encoding='utf-8').read().split('\n')[int(m.group(2)) - 1]
    except Exception:
        return ''


def 在(root=ROOT):
    """返回 (在否, 由)。在＝有令、未解、令引作者原话、据之行真有「暂停令」。"""
    d = 读令(root)
    if not d:
        return False, '无暂停令'
    if d.get('解'):
        return False, '已解（%s）' % str(d['解'].get('时', ''))
    if '作者令' not in str(d.get('令', '')):
        return False, '⛔令不引作者原话——不认'
    if '暂停令' not in 据之行(d.get('据', ''), root):
        return False, '⛔其据（%s）之行无「暂停令」——不认' % d.get('据', '')
    待 = d.get('待')
    if isinstance(待, dict) and 待.get('大审至') is not None:
        try:
            至 = int(待['大审至'])
        except (TypeError, ValueError):
            return False, '⛔待之「大审至」非章号——不认'
        if not 审至(至, root):
            return False, '待：大审之册至第%d章成即停（未到·诸器照常）——%s' % (至, str(d.get('令', ''))[:100])
    return True, '暂停令在（立 %s·据 %s）：%s' % (d.get('立', ''), d.get('据', ''), str(d.get('令', ''))[:160])


def 审至(至, root=ROOT):
    """大审之册至第「至」章（或其後）已成否（空模子⛔算）。"""
    import glob
    try:
        import 大审
        空 = 大审.空模子
    except Exception:
        空 = lambda p: False
    for p in glob.glob(os.path.join(root, '设定', '大审_至第*章.md')):
        m = re.search(r'大审_至第(\d+)章\.md$', p)
        if m and int(m.group(1)) >= 至 and not 空(p):
            return True
    return False


def 许(件, root=ROOT):
    """暂停之中，此件有作者亲令之例外而未用否。"""
    d = 读令(root) or {}
    return any(x.get('件') == 件 and not x.get('用') for x in d.get('例外', []))


def 例外(件, 言, root=ROOT):
    d = 读令(root)
    if not d or d.get('解'):
        print('⛔ 无未解之暂停令，无须例外'); return False
    if '作者' not in 言:
        print('⛔ 例外须引作者之言（「作者令：……」）'); return False
    d.setdefault('例外', []).append({'件': 件, '时': time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime()), '言': 言, '用': False})
    json.dump(d, open(os.path.join(root, 档), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('✓ 暂停令之例外：%s（只许开一回）——%s' % (件, 言[:80]))
    return True


def 销(件, root=ROOT):
    d = 读令(root)
    for x in (d or {}).get('例外', []):
        if x.get('件') == 件 and not x.get('用'):
            x['用'] = time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())
            json.dump(d, open(os.path.join(root, 档), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            return True
    return False


def 解(言, root=ROOT):
    d = 读令(root)
    if not d or d.get('解'):
        print('⛔ 无未解之暂停令'); return False
    if '作者' not in 言:
        print('⛔ 解令须引作者之言（「作者令：……」）'); return False
    d['解'] = {'时': time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime()), '言': 言}
    json.dump(d, open(os.path.join(root, 档), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('✓ 暂停令已解（%s）：%s' % (d['解']['时'], 言))
    if root == ROOT:                    # 1022：停锁换空锁——守书三十分後见停写即派，书自续（自测之临时仓⛔动云端）
        try:
            import 心跳, 自走
            rc, m = 心跳.解停(自走.末章() + 1)
            print('  心跳：%s' % ('停锁已解，交第%d章之棒' % (自走.末章() + 1) if rc == 0 and not m else (m or '解停未推')))
        except Exception as e:
            print('  ⚠ 解停锁未成（%s）——跑 `python3 工具/心跳.py --收`' % e)
    return True


def 自测():
    ok = 共 = 0
    t = tempfile.mkdtemp()
    try:
        os.makedirs(os.path.join(t, '设定'))
        open(os.path.join(t, '设定', '交.md'), 'w', encoding='utf-8').write('甲\n> ⏸ 暂停令（作者令）\n')
        w = lambda d: json.dump(d, open(os.path.join(t, 档), 'w', encoding='utf-8'), ensure_ascii=False)
        共 += 1; ok += 在(t)[0] is False                                   # 无令
        w({'立': 'x', '令': '作者令：暂停', '据': '设定/交.md:2', '解': None})
        共 += 1; ok += 在(t)[0] is True                                    # 有令、有据
        w({'立': 'x', '令': '暂停', '据': '设定/交.md:2', '解': None})
        共 += 1; ok += 在(t)[0] is False                                   # 不引作者
        w({'立': 'x', '令': '作者令：暂停', '据': '设定/交.md:1', '解': None})
        共 += 1; ok += 在(t)[0] is False                                   # 据之行无「暂停令」
        w({'立': 'x', '令': '作者令：暂停', '据': '设定/交.md:2', '解': None})
        import io, contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            r1 = 解('随便', t); r2 = 解('作者令：开', t)
        共 += 1; ok += (r1 is False and r2 is True and 在(t)[0] is False)     # 解须引作者；解後不在
        w({'立': 'x', '令': '作者令：暂停', '据': '设定/交.md:2', '解': None})
        with contextlib.redirect_stdout(io.StringIO()):
            e1 = 例外('W9', '随便', t); e2 = 例外('W9', '作者令：此件可开', t)
        a1 = 许('W9', t); a2 = 许('W8', t); 销('W9', t); a3 = 许('W9', t)
        共 += 1; ok += (e1 is False and e2 is True and a1 and not a2 and not a3 and 在(t)[0] is True)   # 例外只许其件、用即销、令仍在
        # 1023 待：大审之册至第 N 章成之前不在（诸器照常），成即在；解之即不在
        w({'立': 'x', '令': '作者令：审完即停', '据': '设定/交.md:2', '解': None, '待': {'大审至': 410}})
        p7 = os.path.join(t, '设定', '大审_至第407章.md')
        open(p7, 'w', encoding='utf-8').write('册')
        r待 = 在(t)
        p10 = os.path.join(t, '设定', '大审_至第410章.md')
        import 大审 as _大
        原空 = _大.空模子
        _大.空模子 = lambda p: '空' in open(p, encoding='utf-8').read()
        try:
            open(p10, 'w', encoding='utf-8').write('空')
            r空 = 在(t)
            open(p10, 'w', encoding='utf-8').write('满')
            r成 = 在(t)
        finally:
            _大.空模子 = 原空
        共 += 1; ok += (r待[0] is False and '待' in r待[1] and r空[0] is False and r成[0] is True)   # 待：407 册在、410 空模子⛔算、410 成即在
        w({'立': 'x', '令': '作者令：审完即停', '据': '设定/交.md:2', '解': None, '待': {'大审至': 'x'}})
        共 += 1; ok += 在(t)[0] is False                                   # 待之章号坏⛔认（⛔误停）
    finally:
        shutil.rmtree(t)
    print('暂停令·自测 %d/%d' % (ok, 共))
    return ok == 共


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--自测']:
        sys.exit(0 if 自测() else 1)
    if a == ['--查']:
        print(在()[1]); sys.exit(0)
    if a[:1] == ['--例外'] and len(a) == 3:
        sys.exit(0 if 例外(a[1], a[2]) else 1)
    if a[:1] == ['--解'] and len(a) == 2:
        sys.exit(0 if 解(a[1]) else 1)
    print(__doc__); sys.exit(2)
