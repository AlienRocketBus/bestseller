# -*- coding: utf-8 -*-
"""负测 · 重出之趋（2026-09-13 立）

⛔其事：`看官.py --连读` 逐对报其数，而「这一对高不高」与「它在往哪儿走」是两个问题
   ——0913 头一回跑：300—324 中位 2.1%（逾10%者一章）→ 325:14.4｜326:10.0｜327:24.1。
★★本测两路，缺一即假：
   一·**其算须真**（全抄近百、两不相干近零、只比 n−2 不比 n−1）；
   二·⛔**牙不许拔**：**逾界而册上无一行裁者，全测那一格须红**；
      **而其认须紧——「其章之号在册上出现过三个数字」不算，须带「第N章」或「N·」之形。**
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io, os, sys, importlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
趋 = importlib.import_module('重出趋')


def chk_chongchu():
    R = []
    甲 = '＊' + '＊'.join(['她把柴一根一根摆进圈里，掰口朝里' for _ in range(5)])
    乙 = '＊' + '＊'.join(['今天门口空着，她把罐抱到缸边去量了一回' for _ in range(5)])
    R.append(('①全抄者近百', 趋.率(甲, 甲) > 90))
    R.append(('②⛔牙·两不相干近零', 趋.率(甲, 乙) < 5))
    R.append(('③逾界之章须报', len(趋.判({10: 甲, 12: 甲}, 起=10)[1]) == 1))
    R.append(('④⛔牙·不相干者不报', not 趋.判({10: 甲, 12: 乙}, 起=10)[1]))
    R.append(('⑤⛔牙·只比 n−2 不比 n−1',
              abs(趋.判({10: 乙, 11: 甲, 12: 甲}, 起=12)[0][0][1] - round(趋.率(乙, 甲), 1)) < 0.05))
    # ⑥⛔牙·全测那一格之认须紧：拿一个「册上只有其三个数字」之局回灌
    码 = io.open(os.path.join(趋.ROOT, '工具', '全测.py'), encoding='utf-8').read()
    # ⛔只看「真在判的那几行」，不看注与文——**注里提得起旧式，判里不许用旧式**
    #   （★本格立日即自栽一回：其时拿整档去找那一串，而我自己刚把它写进注里。）
    判行 = [ln for ln in 码.splitlines()
            if ('裁文' in ln or '章.get(n' in ln)
            and ln.lstrip().startswith(('if ', 'or ', 'and ', '    or', '    and'))]
    判文 = '\n'.join(判行)
    R.append(('⑥全测之判须带「第N章」或「N·」之形（⛔判里不许用 str(n)）',
              bool(判文) and 'str(n)' not in 判文 and "'第%d章' % n" in 判文))
    # ⑦盘上真局：三章逾界，且三章皆已有裁在册
    出, 逾 = 趋.判()
    裁 = ''
    import glob as _g
    for f in _g.glob(os.path.join(趋.ROOT, '设定', '*裁*重出*.md')):
        裁 += io.open(f, encoding='utf-8', errors='replace').read()
    缺 = [n for n, r in 逾 if ('第%d章' % n) not in 裁 and ('%d·' % n) not in 裁
          and ('**%d**' % n) not in 裁]
    R.append(('⑦盘上逾界 %d 章皆已有裁在册（缺 %s）' % (len(逾), 缺 or '零'), not 缺))
    坏 = [n for n, ok in R if not ok]
    print('════ 负测·重出之趋 ════ %d/%d %s'
          % (len(R) - len(坏), len(R), '全通' if not 坏 else '有败'))
    for n, ok in R:
        print('  %s%s' % ('✓' if ok else '⛔', n))
    return (not 坏), ''


if __name__ == '__main__':
    ok, _ = chk_chongchu()
    sys.exit(0 if ok else 1)
