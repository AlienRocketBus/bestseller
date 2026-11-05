#!/usr/bin/env python3
"""裁之生效 —— 做了的决定必须生效（2026-09-24 作者当面令立）。

★作者原话之意：「我们已经做出来的决定一定要去执行，有很多决定没有生效——
  那做这件事的意义是什么？浪费时间和资源吗？」

★本器只问一件，判得死：**`设定/裁_*.md` 每一份裁，须点名至少一样守它的器
  （`工具/xxx.py` 或 `工具/席/xxx.js`），且那一样器须真在盘上、且真接在 `全测.py` 里
  （或它本身是 `全测.py`／`自走.py` 每跑必调之器）。**
  ——只写在纸上、没有一样器在守的裁，就是「做了而没生效」的那一种。

★旧裁以棘轮守（同 `进化链.py`）：**未生效之裁数只许降、不许升**；
  0924（含）以後所立之裁，一份也不许未生效——立裁之日须同日配器。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io, os, re, sys, glob, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
棘轮档 = os.path.join(ROOT, '设定', '裁之生效_棘轮.json')
新令起 = '0924'   # ★此日（含）以後之裁：一份也不许未生效


def _src(rel):
    p = os.path.join(ROOT, rel)
    return io.open(p, encoding='utf-8', errors='replace').read() if os.path.exists(p) else ''


def _在役():
    """全测／自走／诸席所调之器之名（档名）。"""
    s = _src('工具/全测.py') + _src('工具/自走.py') + ''.join(
        _src(os.path.relpath(f, ROOT)) for f in glob.glob(os.path.join(ROOT, '工具', '席', '*.js')))
    return s


def 守器(裁文):
    """裁文里点名之器：`工具/xxx.py`、`xxx.py`、`工具/席/xxx.js`。"""
    names = set(re.findall(r'([\w一-鿿]+\.py)', 裁文)) | set(re.findall(r'(席/[\w一-鿿]+\.js)', 裁文))
    return {n for n in names if os.path.exists(os.path.join(ROOT, '工具', n))}


def 查(档们=None, 在役=None):
    """→ [(裁名, 由)]：未生效之裁。"""
    档们 = 档们 if 档们 is not None else sorted(glob.glob(os.path.join(ROOT, '设定', '裁_*.md')))
    在役 = _在役() if 在役 is None else 在役
    坏 = []
    for f in 档们:
        名 = os.path.basename(f)
        器 = 守器(io.open(f, encoding='utf-8', errors='replace').read())
        if not 器:
            坏.append((名, '无一样器守它'))
            continue
        活 = [x for x in 器 if x in ('全测.py', '自走.py') or os.path.basename(x) in 在役 or x in 在役]
        if not 活:
            坏.append((名, '所点之器（%s）未接进全测／自走／诸席' % '、'.join(sorted(器))))
    return 坏


def _日(名):
    m = re.match(r'裁_(\d{4})', 名)
    return m.group(1) if m else '0000'


def 报():
    坏 = 查()
    新坏 = [x for x in 坏 if _日(x[0]) >= 新令起]
    旧坏 = [x for x in 坏 if _日(x[0]) < 新令起]
    底 = None
    if os.path.exists(棘轮档):
        try:
            底 = json.load(io.open(棘轮档, encoding='utf-8')).get('旧裁未生效之底')
        except Exception:
            底 = None
    ok = True
    print('════ 裁之生效 ════（做了的决定须有器守、且那器真在跑）')
    if 新坏:
        ok = False
        print('  ⛔0924 以後之裁未生效 %d 份（⛔立裁同日须配器）：' % len(新坏))
        for n, why in 新坏:
            print('     · %s：%s' % (n, why))
    if 底 is None:
        json.dump({'旧裁未生效之底': len(旧坏)}, io.open(棘轮档, 'w', encoding='utf-8'), ensure_ascii=False)
        底 = len(旧坏)
        print('  ℹ棘轮初立：旧裁未生效 %d 份（此後只许降）' % 底)
    elif len(旧坏) > 底:
        ok = False
        print('  ⛔棘轮红：旧裁未生效 %d 份 ＞ 其底 %d' % (len(旧坏), 底))
    else:
        if len(旧坏) < 底:
            json.dump({'旧裁未生效之底': len(旧坏)}, io.open(棘轮档, 'w', encoding='utf-8'), ensure_ascii=False)
        print('  ✓旧裁未生效 %d 份（其底 %d·只许降）' % (len(旧坏), 底))
    if ok and not 新坏:
        print('  ✓0924 以後之裁，份份有器在守。')
    return ok


def 自测():
    import tempfile, shutil
    d = tempfile.mkdtemp()
    R = []
    try:
        a = os.path.join(d, '裁_0999_空.md'); io.open(a, 'w', encoding='utf-8').write('只写了一句话。')
        b = os.path.join(d, '裁_0999_有器不在役.md'); io.open(b, 'w', encoding='utf-8').write('由 `工具/分量闸.py` 守。')
        c = os.path.join(d, '裁_0999_有器在役.md'); io.open(c, 'w', encoding='utf-8').write('由 `工具/分量闸.py` 守。')
        R.append(('①无器之裁判未生效', 查([a], 在役='')[0][1] == '无一样器守它'))
        R.append(('②有器而未接进全测者判未生效', bool(查([b], 在役=''))))
        R.append(('③有器且在役者过', 查([c], 在役='工具/分量闸.py') == []))
        e = os.path.join(d, '裁_0999_假名.md'); io.open(e, 'w', encoding='utf-8').write('由 `工具/并不存在之器.py` 守。')
        R.append(('④点名不存在之器不算（⛔不许写个假名混过）',
                  查([e], 在役='并不存在之器.py') == [('裁_0999_假名.md', '无一样器守它')]))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    for n, o in R:
        print('  %s %s' % ('✓' if o else '⛔', n))
    k = sum(1 for _, o in R if o)
    print('  ── 裁之生效·自测 %d/%d %s ──' % (k, len(R), '全通' if k == len(R) else '⛔未过'))
    return k == len(R)


if __name__ == '__main__':
    if '--自测' in sys.argv:
        sys.exit(0 if 自测() else 1)
    sys.exit(0 if 报() else 1)
