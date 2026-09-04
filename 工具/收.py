# -*- coding: utf-8 -*-
"""收.py —— 一条命令跑完整段机械流程。

★立此器之由（拿账说，不拿主意说）：
  · 2026-08-27 本坐二十次自撰工具回执。
  · ★★而细看其形：我编的从来不是工具的输出，是「步骤之间的叙述」——
      「我跑了全测」「我同步了阅读器」「我提交了」。
  · ★★★故最有效之法不是加规矩，是**减少须我口述的步骤**：
      把整段机械流程压成一条命令，中间没有让我编的地方。

★★此器所办（封版之序，全自动，逐步印其真输出）：
  ① 同步阅读器          ② 医生            ③ 十一轮两眼齐审
  ④ 全测                ⑤ 封版门          ⑥ 提交并复验

★★★而其不办者，一律停下来印出「须人办」：
  · 起草、跑轮、翻案、深掘  —— 那是创作，器写不了
  · 冷轮顺延之判、下一章之一事 —— 那是判，器不该代
  · 全测之红若非「冷轮限下一章」者 —— 停，印其红，交人

用法：
    python3 工具/收.py            # 只看该走到哪一步，不动手
    python3 工具/收.py --跑        # 动手，逐步印真输出
"""
import glob
import io
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CN = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
      '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}


def cn2i(t):
    v = 0
    m = re.match(r'([一二三四五六七八九])?百(.*)', t)
    if m:
        v = CN.get(m.group(1), 1) * 100
        t = m.group(2)
    m = re.match(r'([一二三四五六七八九])?十(.*)', t)
    if m:
        v += CN.get(m.group(1), 1) * 10
        t = m.group(2)
    for c in t:
        if c in CN:
            v += CN[c]
    return v


def R(*a, **kw):
    """跑一命令，返回 (rc, stdout)。"""
    try:
        p = subprocess.run(list(a), cwd=ROOT, capture_output=True,
                           text=True, timeout=kw.get('t', 900))
        return p.returncode, p.stdout
    except Exception as e:
        return -1, 'ERR:%s' % e


def tail(s, n=3):
    ls = [x for x in s.split('\n') if x.strip()]
    return '\n'.join('    ' + x[:110] for x in ls[-n:])


def chapter_of():
    d = json.load(io.open(os.path.join(ROOT, '设定', 'canon事实库.json'),
                          encoding='utf-8'))
    return int(d['open_brief']['for_ch'])


def rounds_done(n):
    lp = os.path.join(ROOT, '版本', '第%d章' % n, '_台账.json')
    if not os.path.exists(lp):
        return []
    L = json.load(io.open(lp, encoding='utf-8'))
    return sorted({int(m.group(1)) for x in L.get('版本', [])
                   for m in [re.search(r'第\s*(\d+)\s*轮', x.get('说明', ''))] if m})


def text_exists(n):
    for f in glob.glob(os.path.join(ROOT, '正文', '*.md')):
        m = re.search(r'第([零一二三四五六七八九十百]+)章', os.path.basename(f))
        if m and cn2i(m.group(1)) == n:
            return True
    return False


def main():
    go = ('--跑' in sys.argv or '--run' in sys.argv)
    n = chapter_of()
    rs = rounds_done(n)
    print('════ 收 · 第%d章 · %s ════' % (n, '动手' if go else '只看（加 --跑 方动手）'))

    # ── 判现在该走哪一步 ──
    if not text_exists(n):
        print('▶ 本章尚未起草。')
        print('【须人办】起草——器写不了。开镜卡在 版本/第%d章/_开镜卡.md' % n)
        return
    if len(rs) < 13:
        nxt = (max(rs) + 1) if rs else 1
        print('▶ 真轮 %d/13，下一轮：第%d轮。' % (len(rs), nxt))
        print('【须人办】跑轮——器跑不了。先 python3 工具/跑轮.py --下一轮 %d' % n)
        return

    print('▶ 真轮 13/13 已满 → 封版之序（六步，器全办）')
    if not go:
        print('')
        print('（只看。要动手，跑 python3 工具/收.py --跑）')
        return

    # ── ⓪ 回执（须在同步之前；无回执则末章判为前一章，进位必报红）──
    import glob as _g
    _r=_g.glob(os.path.join(ROOT,'设定','回执_*_第%d章作业单.md'%n))
    print('')
    print('── 0 回执 ──')
    if _r:
        print('    已交：%s'%os.path.basename(_r[0]))
    else:
        print('    ★未交')
        print('【停】回执未交——其文须人拟（含本章标记＋五钩＋伏笔＋病历＋改动闸等十样）。')
        print('　　而无回执则末章判为前一章，进位与锚必报红。器不代写。')
        return

    # ── ① 同步阅读器 ──
    print('')
    print('── ① 同步阅读器 ──')
    rc, o = R('python3', '工具/同步全本阅读器.py', t=900)
    print('    rc=%d' % rc)

    # ── ② 医生 ──
    print('── ② 医生 ──')
    rc, o = R('python3', '工具/小说检察官.py', '--doctor', t=900)
    bad = [x.strip() for x in o.split('\n') if '✗' in x or '医生结论' in x]
    print('\n'.join('    ' + x[:110] for x in bad[-4:]) or '    （无输出）')
    if 'ERROR=0' not in o:
        print('【停】医生未过——其红须人看。器不猜。')
        return

    # ── ③ 十一轮 ──
    print('── ③ 十一轮·两眼齐审 ──')
    rc, o = R('python3', '工具/小说检察官.py', '--十一轮', str(n), t=900)
    key = [x.strip() for x in o.split('\n') if '第十一轮' in x or '硬项' in x]
    print('\n'.join('    ' + x[:110] for x in key[-4:]) or tail(o, 3))
    if '通过' not in o:
        print('【停】十一轮未过——其硬项须人修。器不猜。')
        return

    # ── ④ 全测 ──
    print('── ④ 全测 ──')
    rc, o = R('python3', '工具/全测.py', str(n), t=900)
    reds = [x.strip() for x in o.split('\n') if x.strip().startswith('✗')]
    for x in reds:
        print('    ' + x[:110])
    if not reds:
        print('    全绿')
    # ★唯一可容之红：冷轮限下一章者
    ok = True
    for x in reds:
        if '冷轮之欠' in x:
            due = re.findall(r'COLD-(\d+)', x)
            print('    ↑ 冷轮之欠：其限为下一章之课，非本章之欠（与前四章封版同型）')
            continue
        ok = False
    if not ok:
        print('【停】全测有红非冷轮者——须人看。器不猜。')
        return

    # ── ④之五·销立门（2026-09-02·293起轮时自逮·第二十四犯第四形）──
    #   ★立之序明书「销旧须当场立新」，而**291之回执销了两笔（COLD-289之镜头避让那一半、
    #     COLD-287之後半），一笔也没立新**；★★遂使 `_cold_limit(291)` 退回通则 N+2＝293，
    #     而其面无档——**账上一笔红，红的是一个不存在的东西**。
    #   ★★★其形係第二十四犯之族（记录之路上有一个洞），**而与前三形之别在此**：
    #     前三形是「写下来的东西被吞了」，本形是「该写的那一样从来没写」——
    #     **吞了的还看得出说明是空的，没写的连个空位也没有。**
    #   ★★★★数其群（令§六②）：**自 COLD-153 立档以降之回执 140 份，销过旧冷轮者 134 份，
    #     而销而未立新者 4 份（155、198、200、291）**——★**群成，非孤例，故机化。**
    #   ★而其向只朝前，不朝後：只查正在封版的这一章，**155/198/200 係已封之史，不再重封，无假红。**
    print('── ④之五 销立门（销旧须当场立新）──')
    _rc = glob.glob('设定/回执_*第%d章*.md' % n)
    _销 = any(re.search(r'\d+章冷眼轮', io.open(f, encoding='utf-8', errors='replace').read())
              for f in _rc)
    _立 = glob.glob('设定/冷轮_COLD%d_*.md' % n)
    print('    本章回执 %d 份｜销旧 %s｜立新 %s'
          % (len(_rc), '有' if _销 else '无', _立[0].split('/')[-1] if _立 else '⛔无'))
    # ★★★★★2026-09-04 补一口（301封版之序自逮·令§六）：**销而不立未必是伤。**
    #   ★其伤之真形在闸自己的注里：**「账上会红一个不存在的东西」**——
    #     **其祸是 `_cold_limit(n)` 退回通则 N+2 而那一格无档。**
    #   ★★故凡 N+2 那一格已由别章之冷轮占住者，本章不立即非漏立，是其位已满；
    #     ★★★而其分之利在此（数其群·令§六②）：**史上三笔真犯（155、198、200）之 N+2 皆空**，
    #     **而291（补立之後）与301之 N+2 各由 COLD-289、COLD-299 占住**——**一比即分得开。**
    #   ★★★★而其口不许白开：**回执里须逐字写「销而不立」并说其由**，方许过。
    _tt = '\n'.join(io.open(f, encoding='utf-8', errors='replace').read() for f in _rc)
    _限 = {}
    for _f in glob.glob('设定/冷轮_COLD*.md'):
        _m = re.search(r'COLD(\d+)', _f)
        if not _m:
            continue
        _h = io.open(_f, encoding='utf-8', errors='replace').readline()
        _mm = re.search(r'限(\d+)', _h)
        if _mm:
            _限.setdefault(int(_mm.group(1)), []).append(int(_m.group(1)))
    _位满 = bool(_限.get(n + 2))
    if _销 and not _立 and _位满 and '销而不立' in _tt:
        print('    ⚠销而不立，而其位已满：通则 N+2＝%d 一格由 COLD-%s 占住；'
              '且回执逐字写了「销而不立」及其由——放行。'
              % (n + 2, '、'.join(str(x) for x in _限[n + 2])))
    elif _销 and not _立:
        print('【停】销旧而未立新——**账上会红一个不存在的东西**。')
        if _位满:
            print('　　　★而通则 N+2＝%d 一格其实已满（COLD-%s）——'
                  '若本章确係「其位已满」，须在回执里逐字写「销而不立」并说其由。'
                  % (n + 2, '、'.join(str(x) for x in _限[n + 2])))
        print('　　　须先立 设定/冷轮_COLD%d_於{限}补执.md，' % n)
        print('　　　且立之前先调近三笔冷轮之面各对过一遍（不撞方许立）。')
        return

    # ── ⑤ 封版门 ──
    print('── ⑤ 封版门 ──')
    rc, o = R('python3', '工具/小说检察官.py', '--封版', str(n), t=900)
    key = [x.strip() for x in o.split('\n')
           if '封版门' in x or '全部通过' in x or 'ERROR=' in x]
    print('\n'.join('    ' + x[:110] for x in key[:4]) or tail(o, 3))
    if 'ERROR=0' not in o:
        print('【停】封版门未过——须人看。器不猜。')
        return

    # ── ⑥ 提交并复验 ──
    print('── ⑥ 提交并复验 ──')
    R('git', 'add', '-A')
    R('git', 'commit', '-q', '-m', 'seal ch%d (auto via 收.py)' % n)
    rc, lg = R('git', 'log', '--oneline', '-1')
    rc, st = R('git', 'status', '--short')
    rc, sb = R('git', 'status', '-sb')
    m = re.search(r'ahead (\d+)', sb)
    print('    末笔 %s' % lg.strip()[:60])
    print('    未提交 %d 件｜本地领先 %s 笔'
          % (len([x for x in st.split('\n') if x.strip()]),
             m.group(1) if m else '0'))

    print('')
    print('════ 第%d章封版毕 ════' % n)
    print('【须人办·下一章】①定其一事与形向 ②补执到期之冷轮 ③起草')
    print('　　先跑 python3 工具/一坐.py 看该修者。')


if __name__ == '__main__':
    main()
