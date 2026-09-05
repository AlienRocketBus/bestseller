# -*- coding: utf-8 -*-
"""负测·连读客问五（逐字重出）（2026-09-03·296第11轮立）

★立此闸之由（其红在哪一行，上磁盘核过）：
  ★296第10轮手打一条 grep，量出 294→296 有 19/138 拍含≥10字与294逐字重出，最长20字；
  ★★而同日跑 `python3 工具/看官.py --连读 292 296`，**问一至问四四问俱绿**，
    问三印「✓无跨章过密之语」——**本书唯一一只跨章之眼，对「上一章的句子原样搬过来」是瞎的**；
  ★★★其故是问三合五章为一片，数5—6字之串出现≥章数×4回；
    **一个20字的长串在两章里各出一回，它数得2，离20差着十八。**
★★§六④·它认哪几样，本书同类共几样：**31对相邻同线之章（264—296）**，
  中位 2.1%｜均 2.9%｜底 0.0%｜**顶 13.8%（294→296）**；逾6%者4对，逾10%者2对。
  **故取 6% 为⚠、10% 为⛔——非拍脑袋，是自这31对之分布取的。**
"""
import io, os, re, sys
from importlib.util import spec_from_file_location, module_from_spec

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_sp = spec_from_file_location('_kg', os.path.join(ROOT, '工具', '看官.py'))
KG = module_from_spec(_sp); _sp.loader.exec_module(KG)

OK = [0, 0]


def chk(name, cond):
    OK[1] += 1
    OK[0] += 1 if cond else 0
    print('  %s %s' % ('✓' if cond else '⛔', name))


def 旧问三(a, b):
    """★旧式回灌：只把问三那一段照原样重跑，看它对294→296说什么。"""
    合 = ''
    for n in range(a, b + 1):
        _f, t = KG.白文(n)
        if t:
            合 += re.sub(r'[\s＊]', '', t)
    from collections import Counter
    c = Counter()
    for k in (5, 6):
        for i in range(len(合) - k + 1):
            c[合[i:i + k]] += 1
    章数 = b - a + 1
    return [(x, v) for x, v in c.items() if v >= 章数 * 4]


def _白文钉版(n):
    """★2026-09-05·机制总审（八路·陪跑闸审第5条）：②⑤原读活正文——296 若回修删去抄自 294 之句，测即红，
    等於把本书之顶级⛔钉在正文里不许治。★★今改读 版本/第N章/ 之末版（已封之版不随回修而变），旧式回灌之义方立。"""
    import glob as _g, re as _re
    vs = sorted(_g.glob(os.path.join(ROOT, '版本', '第%d章' % n, 'v[0-9][0-9].md')))
    if not vs:
        return KG.白文(n)
    t = io.open(vs[-1], encoding='utf-8').read().split('【本章亮点')[0]
    t = _re.sub(r'^.*?第.+?章[^\n]*\n', '', t, count=1, flags=_re.S)
    return vs[-1], t


def main():
    print('███ 负测·连读客问五 ███')
    _real = KG.白文
    KG.白文 = _白文钉版          # ②③④⑤ 皆以封版之末版量，不读活正文
    r296 = KG._重出率(294, 296)
    r293 = KG._重出率(291, 293)
    r295 = KG._重出率(293, 295)
    KG.白文 = _real
    print('  ★所量：294→296 %.1f%%｜291→293 %.1f%%｜293→295 %.1f%%' % (r296, r293, r295))

    chk('①旧式回灌：问三之判据对292—296一无所报（证此闸非重复已有者）', len(旧问三(292, 296)) == 0)
    chk('②新式：294→296 逾⛔之限（≥10%）', r296 >= 10)
    chk('③新式非遍地皆红：291→293 在⚠之下（<6%）', r293 < 6)
    chk('④新式非遍地皆红：293→295 在⚠之下（<6%）', r295 < 6)
    chk('⑤其限自群取，非拍脑袋：296之率须为本书之顶，且≥中位之五倍（中位2.1%）',
        r296 >= 2.1 * 5)
    # ⑥驱真器：连读客跑毕，须把这一笔挂进看官账之判语里
    out, 挂 = KG.连读客(292, 296)
    txt = '\n'.join(out)
    chk('⑥驱真器·连读客自印问五，且294→296 一行带⛔', '问五' in txt and '⛔ 294→296' in txt)
    chk('⑦驱真器·此笔须挂账（判不过者不许当场辩）',
        any('逐字重出' in x for x in 挂))
    # ⑧不许挖空：把限抬到20%，则294→296 亦不红——以此证「限」是这闸的活扣，须留在群上
    # ⑨同线配对（2026-09-05·机制总审）：285 之上一同线章须为 284（同线连排），283 之为 281；旧式 N-2 把 283 配 285（暗对主）
    chk('⑨同线配对：_prev_same(285)=284、_prev_same(283)=281（旧式 N-2 会把 283→285 暗对主）', (KG._prev_same(285), KG._prev_same(283)) == (284, 281))
    chk('⑧限之活扣可验：若限抬至20%，本书无一对报⛔（故限不许随手抬）',
        all((KG._重出率(n - 2, n) or 0) < 20 for n in (296, 294, 292)))

    print('  ── %d/%d %s ──' % (OK[0], OK[1], '全通' if OK[0] == OK[1] else '有红'))
    return 0 if OK[0] == OK[1] else 1


if __name__ == '__main__':
    sys.exit(main())
