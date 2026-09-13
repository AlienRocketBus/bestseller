# -*- coding: utf-8 -*-
"""负测 · FS闸之「裁过的不许再催」（2026-09-13 立）

⛔其事：本器自 0913 起逐坐印「改期逾二回者 3 根——须由人当场裁」，
   而 0913 本坐当场裁毕（三根俱不废，逐根改挂到它走得到的线上）——**裁完了它照旧每坐催一回**。
★**一道催过之後还催的闸，下一坐只会学着不看它**（与「一盏从 08-27 没灭过的灯」同骨）。

★★本测两路，缺一即假：
   一·**裁过的须认得出**（同一根＋同一个限，其裁之档上都写着）；
   二·⛔**而牙不许拔掉**——**限一改，其裁即作废，照旧催**；**没有裁档的根，照旧催**；
      **只写了根名而没写这个限的档，不算裁过。**
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib
FS = importlib.import_module('FS闸')


def chk_fs_caiguo():
    R = []
    # 一·盘上真局：三根之今限，其裁之档上都写着
    for 根, 限 in (('FS01', 330), ('FS03', 331), ('FS05', 332)):
        R.append(('①%s 限%d·裁过须认得出' % (根, 限), FS.裁过(根, 限) is True))
    # 二·⛔牙·限一改，其裁即作废（那几个限，裁档上没有）
    for 根, 限 in (('FS01', 999), ('FS03', 888), ('FS05', 777)):
        R.append(('②%s 限%d·限一改即作废，照旧催' % (根, 限), FS.裁过(根, 限) is False))
    # 三·⛔牙·没裁过的根照旧催（FS06／FS16／FS17 皆无裁档）
    for 根, 限 in (('FS06', 408), ('FS16', 448), ('FS17', 448)):
        R.append(('③%s 未裁过者照旧催' % 根, FS.裁过(根, 限) is False))
    # 四·⛔牙·器印里，已裁与未裁须分作两行（不许合成一句）
    码 = io.open(os.path.join(FS.ROOT, '工具', 'FS闸.py'), encoding='utf-8').read()
    R.append(('④器印分两行（已裁一行／未裁一行）',
              '已当场裁过者' in 码 and '须由人当场裁' in 码))
    坏 = [n for n, ok in R if not ok]
    print('════ 负测·FS裁过 ════ %d/%d %s'
          % (len(R) - len(坏), len(R), '全通' if not 坏 else '有败'))
    for n, ok in R:
        print('  %s%s' % ('✓' if ok else '⛔', n))
    return (not 坏), ''


if __name__ == '__main__':
    ok, _ = chk_fs_caiguo()
    sys.exit(0 if ok else 1)
