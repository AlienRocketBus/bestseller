# -*- coding: utf-8 -*-
"""负测·开轮六检（2026-09-05·304第10轮所立·清 DEBT-297E）

★其所验者只一样：**check7（下一章之锚）之阈**。
★★其红在哪一行（令§十三②·上磁盘核）：
  ·**旧阈写死作 10**，而码注自陈「十轮已满」——**係十轮制之遗**；
  ·★而本系统十三轮（`跑轮.py::ROUNDS=13`），**而锚之备係封版之事，封版在第13轮之後**；
  ·★★故此拦在第10轮即出声，**早了三轮**，且它一出声便拦住往後每一轮之推；
  ·★★★**297第10轮实逮，304第10轮再逮**——同形第二次，故今结清。
★★★而其治不是把 10 改写成 13，是**去问跑轮它自己有几轮**（`_rounds()`）——一改全改。
★★★★而此测之头一项，即令§六④那一行：**它认哪几样，本书同类共几样。**
"""
import io, os, re, sys, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


K = _load('_k6', os.path.join(ROOT, '工具', '开轮六检.py'))

OK = [0, 0]


def chk(name, cond):
    OK[1] += 1
    OK[0] += 1 if cond else 0
    print('  %s %s' % ('✓' if cond else '⛔', name))


def _轮数(c):
    fp = os.path.join(ROOT, '版本', '第%d章' % c, '_轮记.md')
    if not os.path.exists(fp):
        return 0
    tx = io.open(fp, encoding='utf-8').read()
    return len(set(re.findall(r'^## 第(\d+)轮', tx, re.M)))


def _旧式(cur, 阈=10):
    """★旧式之 check7：其阈写死作 10（此即 DEBT-297E 之本身）。"""
    p = os.path.join(ROOT, '设定', '00_镇冢秘术_唯一总圣经.md')
    s = io.open(p, encoding='utf-8', errors='replace').read()
    nx = cur + 1
    if re.search(r'第\s*%d\s*章必须从([^\n]*?)接写' % nx, s):
        return True          # 锚已备，不在本测之内
    return _轮数(cur) < 阈    # True＝放行


def main():
    print('███ 负测·开轮六检（check7 之阈） ███')

    # ①令§六④·它认哪几样，本书同类共几样
    R = K._rounds()
    print('  ★§六④·它认哪几样，本书同类共几样：')
    print('     本系统之轮 %d（取自 跑轮.py::ROUNDS）｜锚之备在封版，封版在第 %d 轮之後' % (R, R))
    print('     旧阈 10｜新阈 %d｜其差 %d 轮——即此闸从前早出声的那几轮' % (R, R - 10))
    chk('①新阈取自跑轮之 ROUNDS，非写死（今 %d）' % R, R == 13)
    chk('①之b 而其取法容得下日後再扩（跑轮改 ROUNDS 即随之改）',
        '_rounds' in io.open(os.path.join(ROOT, '工具', '开轮六检.py'),
                             encoding='utf-8').read())

    # ②旧式回灌：拿 304 之现轮记（十轮已满而十三轮未满）灌进旧阈，须报⛔
    n304 = _轮数(304)
    chk('②304之轮记今有 %d 个「## 第N轮」标题（10≤N<%d）' % (n304, R),
        10 <= n304 < R)
    chk('②之b 旧式回灌304：报⛔（此即那个早了三轮的拦，故此改非陪跑）',
        _旧式(304) is False)
    chk('②之c 新式跑304：放行',
        K.check7(304)[0][1] is True)

    # ③新式未挖空：满轮而无锚者，照旧须报⛔
    class _桩(object):
        pass

    真轮数 = K._rounds
    try:
        K._rounds = lambda: 1          # ★把阈压到 1，即模拟「轮已满」
        chk('③新式仍咬：轮已满而锚未备者，报⛔（不是挖空闸，是挪回它该出声的那一刻）',
            K.check7(304)[0][1] is False)
    finally:
        K._rounds = 真轮数

    # ④其判据只动阈，不动别处：锚已备之章照旧走「锚之长」那一路
    s = io.open(os.path.join(ROOT, '设定', '00_镇冢秘术_唯一总圣经.md'),
                encoding='utf-8', errors='replace').read()
    有锚 = bool(re.search(r'第\s*304\s*章必须从([^\n]*?)接写', s))
    chk('④第304章之锚在圣经里（证「锚已备」那一路本测未动它）', 有锚)
    r = K.check7(303)
    chk('④之b 而以303跑之，走的是「锚之长」那一路（其名带「之长」二字）',
        '之长' in r[0][0])

    print('  ── %d/%d %s ──' % (OK[0], OK[1], '全通' if OK[0] == OK[1] else '有红'))
    return 0 if OK[0] == OK[1] else 1


if __name__ == '__main__':
    sys.exit(main())
