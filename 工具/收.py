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
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
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
    # ★2026-09-05·机制总审：轮号之式与 跑轮._round_of 同源（re.match 锚句首；「回补·第6轮镜头之补」不算第6轮）
    return sorted({int(m.group(1)) for x in L.get('版本', [])
                   for m in [re.match(r'\s*第\s*(\d+)\s*轮', x.get('说明', ''))] if m})


def _造式判(n):
    """→ (是造式, 所缺)；判据在 工具/造式.py（⛔不另抄）。挂 _式.md 而判据取不到者，判「缺」。"""
    if not os.path.exists(os.path.join(ROOT, '版本', '第%d章' % n, '_式.md')):
        return False, []
    try:
        import importlib.util as _u
        _sp = _u.spec_from_file_location('_zaoshi_shou', os.path.join(ROOT, '工具', '造式.py'))
        _m = _u.module_from_spec(_sp)
        _sp.loader.exec_module(_m)
        return _m.判(n, ROOT)
    except Exception as _e:
        return True, ['造式之判跑不起来（%s）' % _e]


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
    # ★2026-10-08·造式之章（`版本/第N章/_式.md`·判在 `工具/造式.py`）：⛔审改之轮，「真轮 13/13」永不出现——
    #   ⛔不许叫它去「跑轮」（那正是作者 1008 所禁）；改以造式之实俱齐为封版之刻，缺者照印其缺而停。
    造, 造缺 = _造式判(n)
    if 造 and 造缺:
        print('▶ 本章係造式之章（⛔审改之轮）：造式之实缺 %d 样——%s' % (len(造缺), '｜'.join(造缺[:4])))
        print('【须人办】缺哪一席之档，派那一席补（⛔以跑轮补）。全看：python3 工具/造式.py %d' % n)
        return
    if len(rs) < 13 and not 造:
        nxt = (max(rs) + 1) if rs else 1
        print('▶ 真轮 %d/13，下一轮：第%d轮。' % (len(rs), nxt))
        print('【须人办】跑轮——器跑不了。先 python3 工具/跑轮.py --下一轮 %d' % n)
        return

    print('▶ %s → 封版之序（六步，器全办）' % ('造式之实俱齐（造式之章·无审改之轮）' if 造 else '真轮 13/13 已满'))
    if not go:
        print('')
        print('（只看。要动手，跑 python3 工具/收.py --跑）')
        return

    # ── ⓪ 回执（须在同步之前；无回执则末章判为前一章，进位必报红）──
    import glob as _g
    # ⛔认三种，不只认作业单（限360·其详在 全测.py::_已封版）
    _r=[f for k in ('作业单','案席','封版席')
          for f in _g.glob(os.path.join(ROOT,'设定','回执_*_第%d章%s.md'%(n,k)))]
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
    # ★2026-09-05·机制总审（八路·流程之缝审第8条）：旧式 `'通过' in o` 被左眼「【尽力查·通过】」满足而恒放行；今只认总核之印。
    if '【总核·通过】' not in o:
        print('【停】十一轮未过（无「【总核·通过】」之印）——其硬项须人修。器不猜。')
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
    _rc = glob.glob(os.path.join(ROOT, '设定', '回执_*第%d章*.md' % n))
    # ★★★★★2026-09-23·限359（自 `负测_销立门::④之c` 回灌所逮·354／356 二章同形）：
    #   ⛔**闸之式比它的负测还粗**——**负测已於 2026-09-18 为 346 补了「说式之界」，而闸本身一格没补**；
    #     ★**令九·③之反面**：**法变成了闸才生效，而这一回是「测变了闸没变」——更坏，因为账面看着绿。**
    #   ★**今把负测那一判整个搬进来，并补一格新的：自指不作销。**
    #     ①**数字之界 `(?<!\d)`**（「1章冷眼轮」係「101章冷眼轮」之尾）；
    #     ②**句之界**（句号与换行同时断），**句中带「须书／一无干涉」之类者係说式，不作销**；
    #     ③⛔**新补·自指不作销**：**「第N章冷眼轮」之 N 即本章之号者，係 `_cold_done` 所读的那个记号本身**，
    #       **不是「销了别章一笔冷轮」**——**354 之回执逐字说的正是这一件**：
    #       「**本席知道 `_cold_done` 读的正是「第354章冷眼轮」这六个字，而本席不拿这六个字去销一笔并不存在的账**」。
    #       ★**其非陪跑之凭**：**平写之「289章冷眼轮」（跨章）照旧作销，一格未放松**（见同日负测⑥之b）。
    #   ⛔★★★★★**并及一件，须当面说明，免後坐把本条读成一纸赦书**（同日 `空头签` 之报所逼）：
    #     **本条只判一件事——「那六个字不是一笔销」**；⛔**它一格也没说「那六个字写得对」。**
    #     ★**`空头签` 同日正把这两份回执判红**，其由是另一样：
    #       **`_cold_done(354)` 会把「第354章冷眼轮」读作「COLD-354 已执」，那一笔遂在立成之日自销。**
    #     ★★**二判不相抵，係两道闸各守各的**：**销立门问「销了没立新没有」，空头签问「这一签签得着签不着」。**
    #     ⛔**故本条不许被引来免那两份回执之治**——**其治照 `空头签` 所书：那六字里的 N 写被执者之号，
    #       须引旧文者以〈本章之号〉代之**；**今挂在限 359，待大审收庭後落笔。**
    _说式 = r'须书|一无干涉|不是本章之号|非本章之号|〈本章之号〉|销不掉|之判读的是|其六字里那个'
    _销 = False
    for _f in _rc:
        _tx0 = io.open(_f, encoding='utf-8', errors='replace').read()
        for _m in re.finditer(r'(?<!\d)(\d+)章冷眼轮', _tx0):
            if int(_m.group(1)) == n:          # ③自指
                continue
            _b = max(_tx0.rfind('。', 0, _m.start()), _tx0.rfind('\n', 0, _m.start())) + 1
            _en = [x for x in (_tx0.find('。', _m.end()), _tx0.find('\n', _m.end())) if x > 0]
            if not re.search(_说式, _tx0[_b:(min(_en) if _en else len(_tx0))]):
                _销 = True
                break
        if _销:
            break
    _立 = glob.glob(os.path.join(ROOT, '设定', '冷轮_COLD%d_*.md' % n))
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
    for _f in glob.glob(os.path.join(ROOT, '设定', '冷轮_COLD*.md')):
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
    # ★2026-09-05·机制总审（八路·流程之缝审第15条）：封版不清扫轮务状态——55 份 _领轮.json 与 3 份 _拦停.json 留在已封版之章。
    #   今封版之前：旗在则拒封（其因须人看一眼再销）；_领轮.json 随封版删去（定案／回修之存版不再需其基线）。
    _flag = os.path.join(ROOT, '版本', '第%d章' % n, '_拦停.json')
    if os.path.exists(_flag):
        print('【停】第%d章拦停旗未销（%s）——封版之前须先修其因或以一次成功之补存销旗。' % (n, io.open(_flag, encoding='utf-8').read()[:120].replace('\n', ' ')))
        return
    _ling = os.path.join(ROOT, '版本', '第%d章' % n, '_领轮.json')
    if os.path.exists(_ling):
        os.remove(_ling)
        print('    ✓已清扫 _领轮.json（封版之章不再需领轮基线）')

    # ── ⑥之二·open_brief 须已推到下一章（2026-09-23·限362 立）────────────
    # ⛔**其所由来**：**361 封版席自己交上来的第⑦条红**，逐字：
    #   「**`open_brief` 第六回靠人记得·盘上四把器无一把写它**（355／357／358／359／360／361）
    #    ——⛔**须立一把器去写它**」。
    # ★**而本坐查过盘上之实，判它所指之处为真，而其所求之治不可取**：
    #   ★**一把「自己去写」的器不可立**：`open_brief` 五格之中只有 `for_ch` 是机械的，
    #     **`接写自`／`required_state_cards`／`位`／`批次` 四格皆係判**；
    #     ⛔**若器把 `for_ch` 自己推上去而那四格照旧是上一章的**，
    #     **闸当场转绿而料是旧的**——**那比没有这道闸更坏**（`书级体检::check_loss` 之鉴：
    #     **一个看不见的器，比一个不存在的器更坏：它每跑一回都在替一件办过的事作证说没办**）。
    # ★★**而那道闸其实早已有**：`小说检察官.py:4733` 逐字
    #   「**第%d章开拍状态卡批次未指向（open_brief.for_ch≠%d）**」，且 `--doctor` 每跑必查。
    #   ⛔**其真正的缝在「几时查」**：**它只在下一章开跑之时才出声**——
    #   **於是这一笔永远落在下一坐头上，而封这一章的人「记得」与否，盘上无人问。**
    # ★★★**故本坐所立者不是一把写它的器，是把那一条已有之令挪到它该咬住的那一刻**：
    #   **封版之前问一句**——⛔**推不上去就不许封**。
    #   **这一改令闸更硬，不更软**：**它不放过任何一章，而从前它只逮下一章之始。**
    try:
        _cb = os.path.join(ROOT, '设定', 'canon事实库.json')
        _ob = (json.load(io.open(_cb, encoding='utf-8')).get('open_brief') or {})
        _for = int(_ob.get('for_ch') or 0)
        if _for != n + 1:
            print('【停】open_brief.for_ch＝%s，而本章係第%d章——封版之前须先把它推到 %d。'
                  % (_ob.get('for_ch'), n, n + 1))
            print('    ⛔**而不是只改那一个数**：`接写自`／`required_state_cards`／`位`／`批次`'
                  '四格皆係判，须一并写过——⛔**只推数不换料，闸转绿而料是旧的，比不推更坏。**')
            print('    ★其法照上一章之例（`设定/canon事实库.json::open_brief` 末一块自书其取法）。')
            return
        print('    ✓open_brief 已推到第%d章（封版之前当场问过）' % (n + 1))
    except Exception as _e:
        print('【停】open_brief 读不出来（%s）——⛔不许当作「已推」，须人看一眼。' % _e)
        return
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

    # ── ⑦ 双备份（0910·310封版席立·作者亲令「最好是双备份保存……而且一定要严格的去实施」）──
    # ★立此步之由（对位闸 2026-09-10 实印）：`工具/存底.py`／`工具/云端验.py`／`工具/心跳.py`／`工具/续跑.py`
    #   四件**俱係孤器**——「码在仓库里，今日之路上一步也走不到」；
    #   ★★而作者之令是「严格地去实施」，一件靠人记得跑的备份不是机制，是习惯；
    #   ★★★故把它焊进封版之序：**推毕即存、即标、即演、即验、即跑账**。
    #   ★**而 `--演` 是真去克隆一份下来逐档比**——**没有演过的备份不算备份**。
    print('── ⑦ 双备份（存·标·演·验·账）──')
    for _cmd, _t in ((['python3', '工具/存底.py', '--存', '第%d章封版' % n], 300),
                     (['python3', '工具/存底.py', '--标', str(n)], 300),
                     (['python3', '工具/存底.py', '--演', str(n)], 600),
                     (['python3', '工具/云端验.py'], 900),
                     (['python3', '工具/跑账.py'], 300)):
        _rc, _o = R(*_cmd, t=_t)
        print('    %s → %s' % (' '.join(_cmd[1:]), tail(_o, 1).strip()[:90] or ('rc=%d' % _rc)))
        if _rc != 0:
            print('    ⛔ 这一条不过——**照实交上，不许说「已封版」**（主枝推成了不等於保住了）。')
    # ★★★★而心跳与续跑二件同在此路上（`工具/心跳.py` 记一次心跳｜`工具/续跑.py` 记一步续跑）：
    #   **`工具/存底.py --存` 一条顶三样：东西上云端＋记一步续跑＋续一次心跳**（其码自记）。

    print('')
    print('════ 第%d章封版毕 ════' % n)
    print('【须人办·下一章】①定其一事与形向 ②补执到期之冷轮 ③起草')
    print('　　先跑 python3 工具/一坐.py 看该修者。')


if __name__ == '__main__':
    main()
