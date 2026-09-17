#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""负测 · 冷轮之「盖过」之口（2026-09-17 立·其裁在 `设定/裁_0917_COLD336_书把它走过去了.md`）

★**本器所守者一句**：**一份废档要盖过一份 `於N补执` 之档，须逐样写明四件**——
  ①**「盖过」二字与其所盖之档名**（⛔须指名）｜②**其物在哪儿、本书还回不回那个地方**｜
  ③**其魂移到哪一样还在手边的物上**｜④**裁者与其由**。
⛔**四件缺一，照旧判欠。**

★★**其所以要开这个口**（⛔旧式之向是反的）：
  **旧式一句「有 `於N补执` 之档即不许废」**——**而凡有人试过而没执成的冷轮，都会留下这么一份档**；
  ★**於是「人试过而执不成」的那一种永远废不掉**，**而那一种正是最可能真该废的。**
★★★**而其所以要四件**：**要废得难，不要废得易**——
  **旧式之所以焊死，是怕有人拿一份空档把账抹掉**；**四件正是把那一条怕落成可数之物。**

用法：
    python3 工具/负测_冷轮盖过.py
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import importlib.util as _iu
import io, os, shutil, sys, tempfile

根 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _器(盘):
    sp = _iu.spec_from_file_location('_lz6_盖', os.path.join(根, '工具', '开轮六检.py'))
    m = _iu.module_from_spec(sp)
    sp.loader.exec_module(m)
    m.ROOT = 盘
    return m


def _摆(tmp, n, 补执=True, 废之文=None):
    d = os.path.join(tmp, '设定')
    os.makedirs(d, exist_ok=True)
    if 补执:
        io.open(os.path.join(d, '冷轮_COLD%d_於%d补执.md' % (n, n + 5)), 'w',
                encoding='utf-8').write('# 其面在此\n')
    if 废之文 is not None:
        io.open(os.path.join(d, '冷轮_COLD%d_废_20260917.md' % n), 'w',
                encoding='utf-8').write(废之文)


def _judged(n, 补执=True, 废之文=None):
    tmp = tempfile.mkdtemp(prefix='负测_冷轮盖过_')
    try:
        _摆(tmp, n, 补执, 废之文)
        return _器(tmp)._cold_void(n)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def 跑():
    N = 700                                   # ⛔当场取一个盘上没有的号，不写死真号
    全 = ('盖过 `冷轮_COLD%d_於%d补执.md`\n'
          '其物在那一站的屋里，本书还回不回那个地方：不回（总纲逐段读过）\n'
          '其魂移到棱外头那一道印子上\n'
          '裁者：本坐\n其由：书把它走过去了\n' % (N, N + 5))
    局 = []
    局.append(('①四件俱全者，判其已废', _judged(N, True, 全) is True))
    局.append(('②⛔一份空废档盖不过补执之档（旧式之怕，今照旧拦）',
               _judged(N, True, '# 废\n') is False))
    for 缺, 名 in ((('盖过 `冷轮_COLD%d_於%d补执.md`' % (N, N + 5)), '①指名'),
                   ('还回不回', '②其物在哪儿'),
                   ('其魂移', '③其魂移到哪一样'),
                   ('裁者', '④裁者')):
        文 = '\n'.join(l for l in 全.split('\n') if 缺 not in l)
        局.append(('③⛔缺「%s」一件即照旧判欠' % 名, _judged(N, True, 文) is False))
    # ⑦★头一个口未动：从未立过面者（无补执之档），旧式之判据照旧认
    局.append(('④头一个口未动：无补执之档而其废档带裁与其由者，照旧认',
               _judged(N, False, '裁者：本坐\n其由：从来没有立过面\n') is True))
    # ⑧⛔盖过之名须指其真号，不许拿别号之档名混过去
    混 = 全.replace('COLD%d' % N, 'COLD%d' % (N + 1))
    局.append(('⑤⛔所盖之档名须係其本号（拿别号之名混不过去）',
               _judged(N, True, 混) is False))

    print('════ 负测 · 冷轮之「盖过」之口 ════（守：要废得难，不要废得易）')
    过 = 0
    for 名, ok in 局:
        print(('  ✓ ' if ok else '  ⛔ ') + 名)
        过 += 1 if ok else 0
    print('  %d/%d %s' % (过, len(局), '全通' if 过 == len(局) else '未全通'))
    return 过 == len(局)


if __name__ == '__main__':
    sys.exit(0 if 跑() else 1)
