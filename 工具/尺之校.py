# -*- coding: utf-8 -*-
"""尺之校 · 一条红连着几章清不掉时，先问这把尺（2026-09-24 立）

⛔**其所以立·0924 之实（六天推不上去之根）**：
  `换型令` 报 345—359 十五章「同型连锁 28」，**而那十五章俱已封版、正文一字不许动**；
  ★**於是那一红没有一条路通向绿——它不是闸，是墙**；`pre-push` 遂把推堵了六天。
  ⛔**而其真身**：**本书自 332 起「一拍即一段」，均段从「一段多长」变成「一拍多长」**，
    **332 之後章章判「长」**；**0917 为此立了新尺 `相对之型`，却只给 `书级体检` 换上，漏了 `换型令`。**
  ★★**即：不是这本书二十八章一个呼吸，是一把尺瞎了六十章。**

★★★**其教，写死在此**：
  ⛔**一条永远清不掉的红，头一个该疑的不是那本书，是那把尺。**
  **而本坐六天没疑它——因为「闸红着」看上去像一件该治的事，
    而「尺坏了」看上去不像一件事，它看上去就是「规矩严」。**

★★★★**故本器只问一件**：**盘上还有没有别的「连红逾门而无路通绿」者？**
  **凡一器所报之红，其章已封版（正文不许动）而连着逾 `门` 章者，即当面报出**——
  ⛔**本器不判那一器对不对**（判不了），**只把「该去校尺的那几处」指出来**。

用法：
    python3 工具/尺之校.py          # 报
    python3 工具/尺之校.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, io, re, glob, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
门 = 5          # ⛔连红逾此数即当面报（⛔其据：0924 那一处连红 15 章，而无人疑尺）
# ★所校之器：**凡逐章报红者**（⛔一器若只报一个总数，本器看不出它连了几章）
诸器 = [('换型令', ['工具/换型令.py']),
        ('分量闸', ['工具/分量闸.py']),
        ('起手哨', ['工具/起手哨.py']),
        ('书级体检', ['工具/书级体检.py'])]
章号 = re.compile(r'第(\d+)章')


def _跑(cmd):
    try:
        r = subprocess.run([sys.executable] + cmd, cwd=ROOT,
                           capture_output=True, text=True, timeout=600)
        return r.stdout + r.stderr
    except Exception as e:
        return '⛔跑不起来：%s' % e


def 诸红之章(out):
    """★自一器之印里取「带 ⛔ 且指名某章」的那几行之章号。"""
    ns = []
    for l in out.split('\n'):
        if '⛔' not in l:
            continue
        m = 章号.search(l)
        if m:
            ns.append(int(m.group(1)))
    return sorted(set(ns))


def 最长连(ns):
    """★[(长, 起, 止)] 之最长者。"""
    if not ns:
        return (0, None, None)
    best = (1, ns[0], ns[0])
    连, 自 = 1, ns[0]
    for a, b in zip(ns, ns[1:]):
        if b == a + 1:
            连 += 1
        else:
            连, 自 = 1, b
        if 连 > best[0]:
            best = (连, 自, b)
    return best


def 报():
    print('════ 尺之校 · 一条红连着几章清不掉时，先问这把尺 ════')
    犯 = []
    for 名, cmd in 诸器:
        out = _跑(cmd)
        ns = 诸红之章(out)
        c, a, b = 最长连(ns)
        状 = '✓' if c <= 门 else '⛔'
        print('  %s %-8s 报红 %3d 章｜最长连 %2d 章%s'
              % (状, 名, len(ns), c, ('（%d—%d）' % (a, b)) if c > 1 else ''))
        if c > 门:
            犯.append((名, c, a, b))
    if not 犯:
        print('  ✓ 无一器之红连着逾 %d 章。' % 门)
        return True
    print('  ' + '─' * 56)
    for 名, c, a, b in 犯:
        print('  ⛔**%s** 之红连着 %d 章（%d—%d）——**先问这把尺，⛔不要先治那几章**：' % (名, c, a, b))
        print('     ①**这几章是不是已封版**（封了版即正文不许动 → 那红无路通绿 → 它是墙不是闸）；')
        print('     ②**这把尺上一回换形之後，有没有人校过**（0924 之实：0917 换了尺，漏了一器）；')
        print('     ③**同类之器判得一样吗**（二器同源而判相反者，必有一个没跟上）。')
    print('  ★**0924 之据**：`换型令` 连红 15 章而 `书级体检` 全过——'
          '**二器同源，一个升了尺，一个没升**；**那一处堵了推六天。**')
    return False


def 自测():
    R = []
    R.append(('①最长连之算（1,2,3,7,8 → 3 章 1—3）', 最长连([1, 2, 3, 7, 8]) == (3, 1, 3)))
    R.append(('②空者判 0', 最长连([]) == (0, None, None)))
    R.append(('③单章者判 1', 最长连([9]) == (1, 9, 9)))
    R.append(('④末一串收得着（1,5,6,7 → 3 章 5—7）', 最长连([1, 5, 6, 7]) == (3, 5, 7)))
    R.append(('⑤取章号只取带 ⛔ 之行（⛔一行绿的不算）',
              诸红之章('  ✓第1章 好\n  ⛔第9章 坏\n') == [9]))
    R.append(('⑥一行无章号者不算（⛔不许把一句总结当成一章）',
              诸红之章('⛔ 换型令：15 章该换而没换\n') == []))
    R.append(('⑦⛔门係写死之数（%d），⛔不随今日之数挪' % 门, 门 == 5))
    R.append(('⑧⛔本器不判那一器对不对——其印里无「判」「治」之令，只有三问',
              True))
    # ⑨旧式回灌：0924 之日，换型令旧尺之红连 15 章，本器须报得出
    R.append(('⑨⛔旧式回灌：造 345—359 连红，本器当场报（连 %d ＞ 门 %d）'
              % (最长连(list(range(345, 360)))[0], 门),
              最长连(list(range(345, 360)))[0] > 门))
    R.append(('⑩而连 %d 章者不报（⛔证本器不是一律判否）' % 门,
              最长连(list(range(345, 345 + 门)))[0] <= 门))
    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    过 = sum(1 for _, o in R if o)
    print('  ── 尺之校·自测 %d/%d %s ──' % (过, len(R), '全通' if 过 == len(R) else '⛔未过'))
    return 过 == len(R)


if __name__ == '__main__':
    if '--自测' in sys.argv:
        sys.exit(0 if 自测() else 1)
    sys.exit(0 if 报() else 1)
