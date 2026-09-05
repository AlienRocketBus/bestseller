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

    # ★★★★★2026-09-05 再订（304第13轮当日·**同日第二犯，故并入原号**）：
    #   ★此二条原钉在 304 之现轮记上（「今有 N 个标题，10≤N<13」）——★★而 304 那一日正在跑轮，
    #     **当晚它就跑满了十三轮，此条随即失效**；★★★**而我前一轮（304第10轮）才为 `负测_销立门` ④之d
    #     立过一条法：「凡负测之断言指到一个具体章号者，先问一句『这一章会不会被治好』——会被治好的，
    #     就不许拿它当断言的身」**——**立法之後一轮，同一个手病再犯一回。**
    #   ★★★★故改以合成之数验之，不取任何一章之现状：**造一个「轮数落在 [10, ROUNDS) 而锚未备」之局**，
    #     **旧阈须咬，新阈须放**——**此局不随磁盘变，故它守的是那个不变量，不是那一天的磁盘。**
    合成 = 11                                  # ★十轮已满而十三轮未满之任一数
    chk('②合成之局在旧新二阈之间（10 ≤ %d < %d）' % (合成, R), 10 <= 合成 < R)
    chk('②之b 旧阈（10）咬它：报⛔（此即那个早了三轮的拦，故此改非陪跑）',
        (合成 >= 10) is True)
    chk('②之c 新阈（ROUNDS）放它：不咬', (合成 >= R) is False)

    # ②之d 而其咬与放，须由真器走一回，不许只算数。
    #   ★★★★★2026-09-05 再订（304封版之序当日·**同日第三犯**）：★此局原取 304，
    #     ★★而 304 封版之序当日备了第305章之锚，check7 遂走「锚之长」那一路，此局落空；
    #     ★★★故改造一个自带自灭之局：**在下一未写之章之位上临时写一份轮记**（其锚必未备），
    #       **跑毕即删**——★**此局不随任何一章之治而变**，**而它走的是真器，不是算式**。
    局 = 304
    while os.path.exists(os.path.join(ROOT, '版本', '第%d章' % (局 + 1), '_轮记.md')):
        局 += 1
    局 += 1                                     # ★下一未写之章：其「下一章之锚」必未备
    局路 = os.path.join(ROOT, '版本', '第%d章' % 局)
    造 = not os.path.exists(局路)
    真轮数0 = K._rounds
    try:
        if 造:
            os.makedirs(局路)
        io.open(os.path.join(局路, '_轮记.md'), 'w', encoding='utf-8').write(
            ''.join('## 第%d轮·负测所造\n\n' % i for i in range(1, 12)))
        K._rounds = lambda: 12                  # ★阈高於其轮数（11）＝轮未满，须放行
        放 = K.check7(局)[0][1]
        K._rounds = lambda: 11                  # ★阈等於其轮数＝轮已满，须报⛔
        咬 = K.check7(局)[0][1]
    finally:
        K._rounds = 真轮数0
        import shutil
        if 造 and os.path.isdir(局路):
            shutil.rmtree(局路)
        elif os.path.exists(os.path.join(局路, '_轮记.md')) and 造:
            os.remove(os.path.join(局路, '_轮记.md'))
    chk('②之d 真器走一回（阈高一即放、阈平即咬·其局自造自灭，不钉任何一章）',
        (放, 咬) == (True, False))
    chk('②之e 而其局跑毕即灭（不留一件文件在仓库里）', not os.path.exists(局路) or not 造)

    # ③新式未挖空：上之「咬」那一半即是——轮已满而锚未备者，新式照旧报⛔。
    chk('③新式仍咬：轮已满而锚未备者，报⛔（不是挖空闸，是挪回它该出声的那一刻）',
        咬 is False)

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
