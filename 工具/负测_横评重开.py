# -*- coding: utf-8 -*-
"""负测·横评之「重开」记因（2026-09-09·308封版之序·案席立）

★所治之伤：`跑轮.py::compare()` 逐版取 `r['soft']['净重']`，
  **而「重开」是一条记因，不是一版**——其 hard/soft 皆为空表，遇上它当场 KeyError；
  ★★其果：**`--十一轮 N` 之左眼整只瞎掉**，只印一句「跑轮侧总核未能运行：'净重'」，
  **而右眼照跑、总核照出结论**——这是 P32·假绿病之同族：**不是判错，是没有位。**
★★★其所以到 308 才犯：**「重开」这一记是本章之轮乱序跑才头一回大量出现的**（本章九条）；
  306／307 皆无一条，故此洞在两章封版之下一次也没有响过。

【本负测所验四项】
 ①以本章今日之台账回灌：**旧式抛 KeyError，新式跑得完**（证其非空跑）。
 ②去掉那九条「重开」之後：**二式所印之表逐字相同**（证新式只滤记因，不动任何一版）。
 ③把一版之净重改坏：**新式照旧在「逐项冠军」里点得出末版未持有其最优**（证它没被洗白）。
 ④一台账若只有「重开」而无一版带量项：**新式须报「没有一版带量项」而非崩**。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io, json, os, re, sys, tempfile, importlib.util as _u

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load(path):
    s = _u.spec_from_file_location('_pl_%d' % id(path), path)
    m = _u.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def _旧式(versions):
    """立此闸之前那一式：逐版直取 soft['净重']（原码之形，一字不改）。"""
    out = []
    for r in versions:
        s = r['soft']
        out.append('%s %d %d' % (r['版'], s['净重'], s['段数']))
    return out


def _跑(mod, n, led_obj, tmpdir):
    """把一份台账写进临时章目录，令 compare() 读它。"""
    d = os.path.join(tmpdir, '第%d章' % n)
    os.makedirs(d, exist_ok=True)
    io.open(os.path.join(d, '_台账.json'), 'w', encoding='utf-8').write(
        json.dumps(led_obj, ensure_ascii=False))
    old = mod.paths
    mod.paths = lambda k: (d, os.path.join(d, '_台账.json'))
    import contextlib
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            rc = mod.compare(n)
    finally:
        mod.paths = old
    return rc, buf.getvalue()


def main():
    过, 坏 = [], []

    def T(name, ok, why=''):
        (过 if ok else 坏).append(name)
        print('  %s %s%s' % ('✓' if ok else '⛔', name, ('　' + why) if why else ''))

    led = json.load(io.open(os.path.join(ROOT, '版本', '第308章', '_台账.json'),
                            encoding='utf-8'))
    vs = led['版本']
    记因 = [r for r in vs if not (r.get('soft') or {}).get('净重')]
    有量 = [r for r in vs if (r.get('soft') or {}).get('净重')]
    T('〇·本章台账确有「重开」记因（否则本负测係陪跑）', len(记因) >= 1,
      '记因 %d 条｜带量项之版 %d 个' % (len(记因), len(有量)))

    mod = _load(os.path.join(ROOT, '工具', '跑轮.py'))
    tmp = tempfile.mkdtemp(prefix='fuce_hp_')

    # ①旧式抛，新式跑得完
    旧崩 = False
    try:
        _旧式(vs)
    except KeyError:
        旧崩 = True
    T('①旧式（逐版直取 soft[净重]）对同一份台账抛 KeyError', 旧崩,
      '——旧式不崩即本负测係陪跑')
    rc, out = _跑(mod, 308, led, tmp)
    T('①之b 新式跑得完（rc=0 且印出横评之表）', rc == 0 and '量项走势' in out)
    T('①之c 且当场印出它滤掉了几条记因', ('不入横评' in out) and (str(len(记因)) in out))

    # ②去掉记因後，二式所印之版序逐字相同
    led2 = {'章': led.get('章', 308), '版本': 有量}
    rc2, out2 = _跑(mod, 308, led2, tmp)
    行1 = [l for l in out.splitlines() if re.match(r'^\s+v\d+\s', l)]
    行2 = [l for l in out2.splitlines() if re.match(r'^\s+v\d+\s', l)]
    # ★行数为 2×版数：一·硬项与二·量项走势两处各印一遍（本负测立时数错过一回，记之）
    T('②去掉那些记因之後，新式所印之逐版行逐字相同（证它只滤记因，不动任何一版）',
      行1 == 行2 and len(行1) == 2 * len(有量),
      '共 %d 行（＝2×%d 版）' % (len(行1), len(有量)))

    # ③把一版之净重改坏，须仍点得出末版未持有其最优
    import copy
    led3 = copy.deepcopy(led)
    坏了 = False
    坏版名 = ''
    for r in led3['版本']:
        if (r.get('soft') or {}).get('净重'):
            r['soft']['净重'] = 99999   # 头一版给一个不可能的最优
            坏版名 = r['版']
            坏了 = True
            break
    rc3, out3 = _跑(mod, 308, led3, tmp)
    # ★本负测立时头一式写作「须印『末版未持有』」——**而那一句只在「多数项之冠军不是末版」时才印**，
    #   改坏一项（七项之一）不足以翻转多数，故其式判得不对；
    #   ★★今改验一样更准的：**「净重」那一行之冠军须点名那个被改坏的版，而不是末版**。
    冠 = [l for l in out3.splitlines() if l.strip().startswith('净重') and '最优值' in l]
    被改 = 坏版名
    T('③一版之净重改坏，新式照旧把「净重」之冠军点在那一版上（未被洗白）',
      bool(冠) and ('99999' in 冠[0]) and (被改 in 冠[0]),
      冠[0].strip() if 冠 else '⛔未见净重之冠军行')

    # ④只有记因而无一版带量项：须报，不许崩
    led4 = {'章': 308, '版本': 记因 or [{'版': '重开', '说明': '记因', 'hard': {}, 'soft': {}}]}
    try:
        rc4, out4 = _跑(mod, 308, led4, tmp)
        ok4 = (rc4 == 1) and ('没有一版带量项' in out4)
    except Exception as e:
        ok4 = False
        out4 = str(e)
    T('④台账若只剩记因，新式须报「没有一版带量项」而非崩', ok4)

    _tot = len(过) + len(坏)
    # ★其末行须作「N/N 全通」式：`全测.py::_简测` 之壳取的正是这一式（本器立时漏了，全测当场报「未见其数」）
    print('\n★负测·横评重开 %d 项，过 %d，坏 %d —— %d/%d %s'
          % (_tot, len(过), len(坏), len(过), _tot, '全通' if not 坏 else '⛔未过'))
    return 1 if 坏 else 0


if __name__ == '__main__':
    sys.exit(main())
