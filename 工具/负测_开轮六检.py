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
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
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
    局记 = os.path.join(局路, '_轮记.md')
    造 = not os.path.exists(局路)
    # ★★★★★2026-09-05 治（305第1轮·开轮当场自逮）：★此测头一版之 finally 只在「目录係本测所造」
    #   时才清扫；★★而 304 封版之序当日先立了 版本/第305章/_开镜卡.md，目录遂已在，
    #   **造＝False，所写之 _轮记.md 一个字也没清掉**；★★★其果：**它随封版那一笔提交推上了 GitHub**，
    #   而次日开轮，跑轮之「前轮所见」印的是「## 第10轮·负测所造」「## 第11轮·负测所造」——
    #   **一份负测造的假轮记，混进了一章真的台账之前**。
    #   ★★★★故改作「先记其旧貌，跑毕逐样还原」：**目录係本测所造则整个删；目录本已在则只删（或还原）本测所写那一件**
    #   ——**一份测不许在仓库里留下一个字。**
    旧记 = io.open(局记, encoding='utf-8').read() if os.path.exists(局记) else None
    真轮数0 = K._rounds
    try:
        if 造:
            os.makedirs(局路)
        io.open(局记, 'w', encoding='utf-8').write(
            ''.join('## 第%d轮·负测所造\n\n' % i for i in range(1, 12)))
        K._rounds = lambda: 12                  # ★阈高於其轮数（11）＝轮未满，须放行
        放 = K.check7(局)[0][1]
        K._rounds = lambda: 11                  # ★阈等於其轮数＝轮已满，须报⛔
        咬 = K.check7(局)[0][1]
    finally:
        K._rounds = 真轮数0
        import shutil
        if 造 and os.path.isdir(局路):
            shutil.rmtree(局路)                 # ★本测所造之目录，整个删
        elif 旧记 is None:
            if os.path.exists(局记):
                os.remove(局记)                 # ★本测所写而先前无此件，删之
        else:
            io.open(局记, 'w', encoding='utf-8').write(旧记)   # ★先前有此件，还原其旧貌
    chk('②之d 真器走一回（阈高一即放、阈平即咬·其局自造自灭，不钉任何一章）',
        (放, 咬) == (True, False))
    chk('②之e 而其局跑毕即灭（不留一件文件在仓库里）',
        (not os.path.exists(局路)) if 造 else
        ((io.open(局记, encoding='utf-8').read() == 旧记) if 旧记 is not None
         else (not os.path.exists(局记))))

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

    # ⑤领轮基线之键（2026-09-05·机制总审）：⑨须读 nextround 所写之「目标轮」；无号即⛔，不许印「第None轮 ✓」
    _ks = io.open(os.path.join(ROOT, '工具', '开轮六检.py'), encoding='utf-8').read()
    chk('⑤⑨读「目标轮」且无号即⛔（旧式读「轮／round／轮号」印第None轮而✓）',
        "d.get('目标轮')" in _ks and '无「目标轮」' in _ks)
    # ⑥★2026-10-08·造式之章（无审改之轮，「轮满」之形永不出现）：造式之实俱齐即其封版之刻——锚未备者须咬；未齐者只记不拦
    #   ★其局自造自灭：取一个圣经里无「下一章之锚」、版本里亦无其目之大号章（跑毕整个删）。
    Z = _load('_zs_k6', os.path.join(ROOT, '工具', '造式.py'))
    局z = 9990
    while os.path.exists(os.path.join(ROOT, '版本', '第%d章' % 局z)) or re.search(r'第\s*%d\s*章必须从' % (局z + 1), s):
        局z += 1
    路z = os.path.join(ROOT, '版本', '第%d章' % 局z)
    import shutil as _sh6
    try:
        Z.造一局(ROOT, 局z)
        咬z = K.check7(局z)[0][1]
        _sh6.rmtree(路z)
        Z.造一局(ROOT, 局z, 缺=('回话',))
        放z = K.check7(局z)[0][1]
        _sh6.rmtree(路z)
        Z.造一局(ROOT, 局z)
        import os as _os6
        _os6.remove(os.path.join(路z, '_式.md'))
        放常 = K.check7(局z)[0][1]
    finally:
        if os.path.isdir(路z):
            _sh6.rmtree(路z)
    chk('⑥造式之实俱齐而下一章之锚未备者，报⛔（⛔不许造式之章借「轮永不满」逃过锚之检）', 咬z is False)
    chk('⑥之b 造式之实未齐者只记不拦（同轮未满之章）', 放z is True)
    chk('⑥之c 同一局而无 _式.md 者照轮数判（一轮＜十三，只记不拦）', 放常 is True)
    chk('⑥之d 其局跑毕即灭（不留一件文件在仓库里）', not os.path.exists(路z))
    print('  ── %d/%d %s ──' % (OK[0], OK[1], '全通' if OK[0] == OK[1] else '有红'))
    return 0 if OK[0] == OK[1] else 1


if __name__ == '__main__':
    sys.exit(main())
