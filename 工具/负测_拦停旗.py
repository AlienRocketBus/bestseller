# -*- coding: utf-8 -*-
"""负测·拦停旗自失其义（2026-09-04·299第6轮立·与其闸同日）

★所治之伤（其形上磁盘核过·本轮亲犯）：**一轮存过版之後再存一回**——
  ★`--存版 299` 不带说明，v08 落盘（说明为空）；★★带着说明再存，空轮闸判「正文与末版逐字相同」→ 拦 → 落旗；
  ★★★而销旗之路只有一条「一次成功的存版／补存」，那一条路正被空轮闸堵着——
  **旗落下去就再也拿不掉，而它拦的是其後一切轮务**（第二十四犯之族：记录之路上有一个洞）。

★★本测所验者为不变量，非快照：
  ①**空轮闸之旗**＋台账上已有那一轮之真说明 → **失其义，销**（其事不成立）；
  ②空轮闸之旗＋台账上没有那一轮之版 → **不销**（那一轮真没存上）；
  ③**因非空轮闸者（棘轮回退／趋阈闸／硬项／闸八）** → **一面也不销**，纵台账上有那一版
    （**那几样是「存坏了」，账上有没有那一版都不改其为伤**）；
  ④空轮闸之旗而说明报不出轮号 → **不销**（认不出它拦的是哪一轮）；
  ⑤台账上那一轮之说明是占位或空 → **不销**（一行说不出自己跑了什么的账，不算「有身」）；
  ⑥**旧式回灌**：旧式（无此查）在①之下照旧拒——**故本测非陪跑**（令§六③）。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io, os, sys, json, shutil, tempfile, importlib.util as iu

_D = os.path.dirname(os.path.abspath(__file__))
_R = os.path.dirname(_D)
案 = []


def chk(名, 得, 期):
    案.append((名, 得 == 期, '得%r 期%r' % (得, 期)))


def _mod(root):
    sp = iu.spec_from_file_location('_pl_%d' % id(root), os.path.join(_D, '跑轮.py'))
    m = iu.module_from_spec(sp)
    sp.loader.exec_module(m)
    m.ROOT = root
    m.JJ_DIR = os.path.join(root, '版本')
    return m


占位 = '（本轮说明未填，须在回执补记开庭与真伤级别）'


def 造(root, 说明):
    vd = os.path.join(root, '版本', '第999章')
    os.makedirs(vd, exist_ok=True)
    io.open(os.path.join(vd, '_台账.json'), 'w', encoding='utf-8').write(json.dumps(
        {'章': 999, '版本': [{'版': 'v08', '说明': 说明, 'hard': {}, 'soft': {}}]},
        ensure_ascii=False, indent=1))
    return vd


def 跑():
    tmp = tempfile.mkdtemp()
    try:
        m = _mod(tmp)
        # ①空轮闸之旗＋账上有那一轮之真说明 → 销
        造(tmp, '第6轮·资源庭·器物逐件点名：所改何事')
        m.raise_flag(999, '⛔空轮闸：正文与末版逐字相同，本轮零改动。', '第6轮·资源庭·器物逐件点名·补存')
        chk('①旗在（前置）', os.path.exists(m._flag_path(999)), True)
        失, 由 = m._flag_stale(999, m.read_flag(999))
        chk('①空轮闸之旗＋账上有那一轮之真说明 → 失其义', 失, True)
        chk('①之b 且说得出其事何以不成立', 'v08' in 由 and '第6轮' in 由, True)
        chk('①之c 而 flag_block 不再拒', m.flag_block(999, '发轮'), False)
        chk('①之d 且旗当场销去', os.path.exists(m._flag_path(999)), False)

        # ⑥旧式回灌：旧式（无此查）在①之下照旧拒
        造(tmp, '第6轮·资源庭·器物逐件点名：所改何事')
        m.raise_flag(999, '⛔空轮闸：正文与末版逐字相同，本轮零改动。', '第6轮·资源庭·器物逐件点名·补存')
        旧式拒 = bool(m.read_flag(999))          # 旧式只问「旗在不在」
        chk('⑥旧式（只问旗在不在）在①之下照旧拒 → 故本测非陪跑', 旧式拒, True)
        m.clear_flag(999)

        # ②账上没有那一轮之版 → 不销
        造(tmp, '第5轮·在场庭：所改何事')
        m.raise_flag(999, '⛔空轮闸：正文与末版逐字相同，本轮零改动。', '第6轮·资源庭·补存')
        chk('②账上没有第6轮之版 → 不销', m._flag_stale(999, m.read_flag(999))[0], False)
        chk('②之b 且 flag_block 照旧拒', m.flag_block(999, '发轮'), True)
        m.clear_flag(999)

        # ③因非空轮闸 → 一面也不销
        for 因 in ('⛔棘轮闸：四字串三现 9→20 回退',
                   '趋阈闸：某数勉强跨过一条有名之限而说明未自证',
                   '⛔硬项：破折号 ×2',
                   '⛔闸八·领轮基线不符：起轮时正文已偏'):
            造(tmp, '第6轮·资源庭·器物逐件点名：所改何事')
            m.raise_flag(999, 因, '第6轮·资源庭·补存')
            chk('③「%s…」之旗不失义' % 因[:8], m._flag_stale(999, m.read_flag(999))[0], False)
            chk('③之b 「%s…」flag_block 照旧拒' % 因[:8], m.flag_block(999, '发轮'), True)
            m.clear_flag(999)

        # ④说明报不出轮号 → 不销
        造(tmp, '第6轮·资源庭：所改何事')
        m.raise_flag(999, '⛔空轮闸：正文与末版逐字相同，本轮零改动。', '资源庭·补存')
        chk('④旗之说明报不出轮号 → 不销', m._flag_stale(999, m.read_flag(999))[0], False)
        m.clear_flag(999)

        # ⑤账上那一轮之说明是占位／空 → 不销
        for 说明 in (占位, ''):
            造(tmp, 说明)
            m.raise_flag(999, '⛔空轮闸：正文与末版逐字相同，本轮零改动。', '第6轮·资源庭·补存')
            chk('⑤账上那一行说明是「%s」 → 不销' % (说明[:6] or '（空）'),
                m._flag_stale(999, m.read_flag(999))[0], False)
            m.clear_flag(999)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ⑥封版留旗（2026-09-05·机制总审）：以「已封版而留旗」之形回灌 全测._留旗之章 须报其章；无回执者不报（旧式：全测无此检，三章留旗二十余日无人见）
    try:
        import importlib.util as _iu, tempfile as _tf, json as _js
        _sp = _iu.spec_from_file_location('quance', os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '工具', '全测.py'))
        _q = _iu.module_from_spec(_sp); _sp.loader.exec_module(_q)
        _t = _tf.mkdtemp(prefix='zm_flag_')
        _d = os.path.join(_t, '第7章'); os.makedirs(_d)
        _js.dump({'因': 'x'}, open(os.path.join(_d, '_拦停.json'), 'w'))
        chk('⑥已封版而留旗 → 报其章', _q._留旗之章([(7, _d)], lambda n: True), [7])
        chk('⑥之b 未封版而留旗 → 不报（旗尚有义）', _q._留旗之章([(7, _d)], lambda n: False), [])
        shutil.rmtree(_t, ignore_errors=True)
    except Exception as e:
        chk('⑥封版留旗之验运行', str(e), '')
    坏 = [x for x in 案 if not x[1]]
    for 名, 过, 详 in 案:
        print('  %s %s%s' % ('✓' if 过 else '✗', 名, '' if 过 else '　（%s）' % 详))
    print('\n★负测 %d 项，过 %d，坏 %d' % (len(案), len(案) - len(坏), len(坏)))
    return 1 if 坏 else 0


if __name__ == '__main__':
    sys.exit(跑())
