# -*- coding: utf-8 -*-
"""负测·器物点名（2026-09-03 立·与其闸同日）

★令§六③：改闸／立闸必同日立负测，且须以旧式回灌验；★★一个只会说「零」的闸没有价值。
★★★故本测逐条回灌，每一条都拿「真犯过此项之原物」去撞它（令§十四③）：
  ①今日之册须绿（其基线）
  ②删一格「出」即红——**这正是295第6轮逮出的那一伤**（笔与那一点东西原皆无「出」）
  ③把「用」之拍号改成一个没有该器物之名的拍即红——**295第7轮之坐头一版册即栽在此**
    （本子·用=拍8，而拍8之白文是「递到一半，他伸手接了」，无「本子」二字）
  ④拍号逾全章拍数即红
  ⑤册不在即红
  ⑥旧式回灌：**若判据只数「册上有没有这一行」而不验其拍**，②③④三条俱过——
    **一份在旧式下也全过的测就是陪跑**（令§六③）。
"""
import importlib.util as iu, io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, '版本', '第295章', '_器物.md')


def _mod():
    sp = iu.spec_from_file_location('_qw', os.path.join(ROOT, '工具', '器物点名.py'))
    m = iu.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def _跑(m, 文):
    io.open(P, 'w', encoding='utf-8').write(文)
    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = m.跑(295)
    return rc, buf.getvalue()


def 跑():
    if not os.path.exists(P):
        print('✗ 负测·器物点名 ⛔前置不在：%s' % P)
        return 1
    原 = io.open(P, encoding='utf-8').read()
    m = _mod()
    坏 = []
    try:
        rc, _ = _跑(m, 原)
        if rc != 0:
            坏.append('★①今日之册本该绿，而它红了（rc=%d）' % rc)
        # ②删一格「出」
        rc, o = _跑(m, re.sub(r'｜出=\d+', '', 原, count=1))
        if rc == 0 or '缺「出」' not in o:
            坏.append('★②删一格「出」而它没红——正是295第6轮那一伤（笔与那一点东西原皆无出）')
        # ③拍号指到无其名之拍
        rc, o = _跑(m, 原.replace('本子｜入=6｜用=92', '本子｜入=6｜用=8'))
        if rc == 0 or '无其名' not in o:
            坏.append('★③「用=拍8」而拍8之白文无「本子」二字，它没红——拍号是抄的它也认')
        # ④拍号逾全章
        rc, o = _跑(m, 原.replace('用=92', '用=9999'))
        if rc == 0 or '不在' not in o:
            坏.append('★④拍号 9999 逾全章而它没红')
        # ⑤册不在
        os.remove(P)
        rc, o = _跑2 = (None, None)
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = m.跑(295)
        if rc == 0 or '器物册不在' not in buf.getvalue():
            坏.append('★⑤册不在而它没红')
        # ⑥旧式回灌（只数行数，不验拍）
        rows = [l for l in 原.split('\n') if '｜' in l and not l.startswith('#')]
        旧式过 = 0
        for 变 in (re.sub(r'｜出=\d+', '', 原, count=1),
                   原.replace('用=92', '用=8'),
                   原.replace('用=92', '用=9999')):
            n = len([l for l in 变.split('\n') if '｜' in l and not l.startswith('#')])
            if n == len(rows):
                旧式过 += 1
        if 旧式过 != 3:
            坏.append('★⑥旧式回灌本该三条全过（故新式非陪跑），而它过了 %d 条' % 旧式过)
    finally:
        io.open(P, 'w', encoding='utf-8').write(原)
    # ★还原毕须与测前逐字相同（第二十八犯之处方）
    if io.open(P, encoding='utf-8').read() != 原:
        坏.append('★⑦还原毕之册与测前不同——本测改坏了它所读的盘')
    if 坏:
        print('✗ 负测·器物点名 %d/7 ⛔未过' % (7 - len(坏)))
        for x in 坏:
            print('   ⛔ ' + x)
        return 1
    print('✓ 负测·器物点名 7/7 全通（②③④三条在旧式「只数行数」之下俱过，故本测非陪跑）')
    return 0


if __name__ == '__main__':
    sys.exit(跑())
