# -*- coding: utf-8 -*-
"""负测·回执对账闸（2026-09-01 立·全书审计第二层 2-4）

★立此测之由：287回执自书「净重2,951（起草）→2,796…十三轮共减155字」，
　★★而台账逐版明印 v01=2,529 → 峰 v08=2,951 → v15=2,796，**是净增 267**⛔。
★★★而令§十一曰：留底之档里的错因，会被下一坐当成场。
★★★★本测之要害只一条：**把那处旧错灌回去，闸须当场红，且须说出「峰不是起草」**。
　★一道灌回旧错而不红的闸，就是陪跑。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io, os, sys, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_R = os.path.join(ROOT, '设定', '回执_20260901_第287章作业单.md')
# ★2026-09-01 改·回修补三拍之後回执首节之数已变（v15 2,796 → v16 2,861），
#   ★★而本测所锚者只须是「那个被称作起草的数」——故改锚为「2,529（起草v01）」一段，
#     ★★★如此回执之其余诸数再变，本测亦不必跟着改（一份天天要改的测，早晚没人改）。
_今 = '2,529（起草v01）'
_旧 = '2,951（起草）'


def _器():
    spec = importlib.util.spec_from_file_location('对账', os.path.join(ROOT, '工具', '回执对账.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def 跑():
    m = _器()
    坏 = []
    # ①今日之全书须零章红
    if m.全书(quiet=True):
        坏.append('今日全书有章报红——此闸开得太宽（其伤在闸不在文）')
    # ②灌回旧错，须红且须点出「峰不是起草」
    if not os.path.exists(_R):
        坏.append('取不到287之回执，无从回灌')
    else:
        orig = io.open(_R, encoding='utf-8').read()
        if _今 not in orig:
            坏.append('287回执之今文与本测所记不符，回灌之据已陈')
        else:
            try:
                io.open(_R, 'w', encoding='utf-8').write(orig.replace(_今, _旧))
                st, _, _, 语 = m.查(287)
                if st != '红':
                    坏.append('★灌回旧错而闸不红——陪跑之闸')
                elif not any('峰' in x and '422' in x for x in 语):
                    坏.append('闸红了而说不出其形（须点明「峰不是起草」且差422）：%s' % 语)
            finally:
                io.open(_R, 'w', encoding='utf-8').write(orig)
    # ③276之形（台账缺起草版）须判「缺起草版」而非判回执之错
    st276 = m.查(276)
    if st276 and st276[0] == '红':
        坏.append('★276被判红——而其 v01 说明为「第1轮」，是台账缺起草版，不是回执之错')
    if 坏:
        print('✗ 负测·回执对账 %d/3' % (3 - len(坏)))
        for x in 坏:
            print('   ⛔ ' + x)
        return 1
    print('✓ 负测·回执对账 3/3 全通（今日全书零章红；灌回旧错即红且点出峰非起草差422；276判缺起草版不判回执）')
    return 0


if __name__ == '__main__':
    sys.exit(跑())
