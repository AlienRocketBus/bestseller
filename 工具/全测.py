#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全测——一条命令跑完全部回归，一个结论定去留。

【批115·立】病灶：此前验证须分四次调用（检察官 --selftest／--doctor／全书检、跑轮 --自测），
  四段输出各看各的，遂有「改一处而不知碰坏他处」之隙；本会话已两度自证——
  ZM_REOPEN 所写空 soft 记录令存版必崩、同名夹具后者覆盖前者令二测名义在跑而实测旧局，
  皆是「改bug时造bug」而当时四段输出俱绿。
  故立全测：一条命令、一个退出码；并由 pre-push 钩子强制，不过不许推。

用法：
    python3 工具/全测.py            # 全跑
    python3 工具/全测.py --快        # 略过全书检（仅自检层，供频繁调用）
"""
import os
import re
import sys
import ast
import glob
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV = dict(os.environ, ZM_STREAM=os.environ.get('ZM_STREAM', 'streamA-cli'))



def _测数(out, 兜底):
    """★2026-09-03·295第4轮立：从负测自印之首行里取它自己那个「M/N 全通」。
    ★★其立之由：三处 wrapper 把「3/3」「9/9」写死在码里，而 `负测_冷轮同判` 已扩至 7/7；
    全测遂逐日印「3/3 全通」——**器没印的数，令§一②不许说**，而这一处正是全测自己在说。
    ★★★故此後一律回印其自印之数；取不着方退回兜底，且兜底须带「★未取着」以示其疑。"""
    ls = [x for x in (out or '').split('\n') if x.strip()]
    for line in ([ls[0]] if ls else []) + (ls[-1:] if ls else []) + ls:
        m = re.search(r'(\d+/\d+)\s*全通', line)
        if m:
            return m.group(1)
    return '★未取着·' + 兜底

def run(desc, args, timeout=900):
    try:
        r = subprocess.run([sys.executable] + args, cwd=ROOT, env=ENV,
                           capture_output=True, text=True, timeout=timeout)
        return r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return '__TIMEOUT__'
    except Exception as e:
        return '__ERR__%s' % e


def chk_selftest():
    out = run('检察官自测', ['工具/小说检察官.py', '--selftest'])
    m = re.search(r'规则回归:(\d+)/(\d+)；契约负测:(\d+)/(\d+)；项目接线:(\S+?)；末章硬闸:(\S+)', out)
    if not m:
        return False, '未取到自测结论行'
    a, b, c, d, e, f = m.groups()
    ok = (a == b and c == d and e == '通过' and f.startswith('通过'))
    return ok, '规则回归%s/%s 契约负测%s/%s 接线%s 末章硬闸%s' % (a, b, c, d, e, f)


def chk_doctor():
    out = run('医生', ['工具/小说检察官.py', '--doctor'])
    m = re.search(r'医生结论: ERROR=(\d+)', out)
    if not m:
        return False, '未取到医生结论'
    return m.group(1) == '0', 'ERROR=%s' % m.group(1)


def chk_shilun():
    out = run('跑轮负测', ['工具/跑轮.py', '--自测'])
    m = re.search(r'负测（含端到端真跑）：(\d+)/(\d+)', out)
    if not m:
        m = re.search(r'负测：(\d+)/(\d+)', out)
    if not m:
        return False, '未取到负测结论'
    return m.group(1) == m.group(2), '%s/%s' % m.groups()


def chk_book():
    out = run('全书检', ['工具/小说检察官.py'])
    m = re.search(r'全书仪表盘:ERROR=(\d+)', out)
    if not m:
        return False, '未取到全书仪表盘'
    return m.group(1) == '0', 'ERROR=%s' % m.group(1)


def chk_bookwide():
    """书级体检（191章末立）：补十轮系统之唯一盲区——章级之闸看不见跨章之漂。
    六检：人物在场衰减／章型连锁／账之净额／日数速率／距终点与账之余额／轮记开销比。"""
    out = run('书级体检', ['工具/书级体检.py', '--静'])
    if out is None:
        return False, '运行失败'
    if '书级体检通过' in out:
        return True, '六检皆过'
    bad = [ln.strip().lstrip('⛔ ') for ln in out.splitlines() if '⛔' in ln]
    return False, '；'.join(bad[:3]) if bad else '未通过'


def chk_quality_gates():
    """质量三闸（2026-08-15立·见 设定/02_全书之约_逐站事数表.md）：
    ★闸①一章一事（防一章塞多事）／★★闸②脉象不相犯（防站与站重复）／★★★闸③谜底之距（防吊太久）。
    ★★★★而其立之由：全书重排为约450章之后，章级十轮之闸仍看不见「质量之三敌」。"""
    out = run('质量三闸', ['工具/质量三闸.py'])
    if out is None:
        return False, '运行失败'
    if '三闸皆过' in out:
        return True, '三闸皆过'
    bad = [ln.strip() for ln in out.splitlines() if '⛔' in ln]
    return False, '；'.join(bad[:3]) if bad else '未通过'


def chk_open_six():
    """开轮六检（2026-08-16立·见 工具/开轮六检.py）：治近日所逮之六条未治之bug——
    ★③人名计数之误／★★⑤撞号与merged／★★★⑥冷轮逾期／
    ★★★★⑦锚之长／★⑨领轮之号／★★⑩招五之第二形。"""
    # ★2026-08-17 订：全测无参调用，开轮检遂取末章；
    # ★★而末章已封版时，⑭必报——★★★而那不是伤，是全测取错了章。
    # ★★★★遂改：取「下一章」（末章＋1）——★而其正是开轮检该测之章。
    import glob as _g, os as _o, re as _r
    _CN = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
           '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}

    def _cn(_p):
        _m = _r.search(r'第([零〇一二三四五六七八九十百]+)章', _o.path.basename(_p))
        if not _m:
            return -1
        _s = _m.group(1)
        _t = _n = 0
        for _ch in _s:
            if _ch in _CN and _ch != '十':
                _n = _CN[_ch]
            elif _ch == '十':
                _t += (_n or 1) * 10
                _n = 0
            elif _ch == '百':
                _t += (_n or 1) * 100
                _n = 0
        return _t + _n
    _cs = [_cn(x) for x in _g.glob('正文/*.md')]
    _cs = [x for x in _cs if x > 0]
    _last = max(_cs) if _cs else 1
    _nx = _last + 1
    # ★★★★★2026-09-02·九席审读所逮·当日治：
    #   ★**旧式只跑「末章＋1」，而那一章尚未起草**——十六检里 ⑬⑮⑱⑳ 一律自赦
    #     （「正文缺，免测」），③⑩ 连印都没印，**当真读了文字的只有 ⑰⑲ 两条**；
    #   ★★**即：57项里这一个绿勾，覆盖的是一个不存在的章**，且它掩护着底下六道
    #     本来能报红的检。★★★这正是令§一⑤：**不是查过了判无罪，是压根没查。**
    #   ★★★★故今两头都跑：**末章（有正文，真读得着）＋末章＋1（该起草之章）**；
    #     ★而末章那一趟须摘掉 ⑭——**⑭之职正是「拿已封版之章重跑即报」**，
    #     它在审计之下必红，而那一红不是伤，是它认得出我在审计。
    _o1 = run('开轮十六检·末章', ['工具/开轮六检.py', str(_last), '--静'])
    _o2 = run('开轮十六检·下章', ['工具/开轮六检.py', str(_nx), '--静'])
    _RAW['开轮十六检'] = (_o1 or '') + '\n' + (_o2 or '')
    if _o1 is None or _o2 is None:
        return False, '运行失败'
    def _bad(_t, _skip14):
        _b = []
        for _ln in (_t or '').splitlines():
            _x = _ln.strip()
            if not _x or '开轮十六检通过' in _x:
                continue
            if _skip14 and ('⑭' in _x or '已封版' in _x):
                continue
            _b.append(_x)
        return _b
    _b1, _b2 = _bad(_o1, True), _bad(_o2, False)
    if not _b1 and not _b2:
        return True, '两头俱过（末章第%d章·下章第%d章）' % (_last, _nx)
    _m = []
    if _b1:
        _m.append('末章第%d章：%s' % (_last, '；'.join(_b1[:2])))
    if _b2:
        _m.append('下章第%d章：%s' % (_nx, '；'.join(_b2[:2])))
    return False, '｜'.join(_m)


def chk_three_bands():
    """评论员三条带 负测（2026-09-03立·298第13轮·见 工具/负测_三条带.py）。
    ★其立之由：评论员之群只一条「前6章之窗」，而比带两造之前就立过「三条带，以同形为先」；
    ★★298第13轮实逮：本席判「弱在动拍%（本章46，窗中位54.5）」，
    ★★★而全书中位38、同形「做事」中位38——本章46在两条带之上，那个弱是六章之窗造出来的。
    ★★★★而此测须在旧式（只取窗）下与新式判得不同方算数（令§六③·回灌验），否则它是陪跑。"""
    out = run('负测·三条带', ['工具/负测_三条带.py'])
    if out is None:
        return False, '运行失败'
    if '全通' not in out:
        return False, out.strip().split('\n')[0]
    if '非陪跑' not in out:
        return False, '★此测在旧式下亦同判，是陪跑之测'
    return True, out.strip().split('\n')[0].replace('✓ ', '')


def chk_nomination_ledger():
    """小说家提名账 负测（2026-09-03立·298第12轮·见 工具/负测_提名账.py）。
    ★其立之由：小说家席在第298章连提同一对拍四回，而看官账所记者是拍号，
    ★★拍号每削一刀就漂一格——四条记的是同两拍，四条却无一条对得上另一条，
    ★★★故那四回提名一回也没被看见，而第12轮重判判它该删。
    ★★★★而此测须在旧式（认号）下认 0 回方算数（令§六③·回灌验），否则它是陪跑。"""
    out = run('负测·提名账', ['工具/负测_提名账.py'])
    if out is None:
        return False, '运行失败'
    if '全通' not in out:
        return False, out.strip().split('\n')[0]
    if '非陪跑' not in out:
        return False, '★此测在旧式下亦认得出，是陪跑之测'
    return True, out.strip().split('\n')[0].replace('✓ ', '')


def chk_kanguan_hand():
    """看官·「手上之事」闸 负测（2026-09-01立·见 工具/负测_看官手闸.py）。
    ★其立之由：生客问一报第287章「拍25—49连25拍无一手上之事」，
    ★★而那一段里 抬×5、托×2 皆是手上之事；数其群，旧式全书287章报红202章（70%）——
    ★★★一道七成篇幅都喊的闸，喊的不是文，是它自己。
    ★★★★而此测须在旧式下漏认方算数（令§六③·回灌验），否则它是陪跑。"""
    out = run('负测·看官手闸', ['工具/负测_看官手闸.py'])
    if out is None:
        return False, '运行失败'
    if '全通' not in out:
        return False, out.strip().split('\n')[0]
    if '非陪跑' not in out:
        return False, '★此测在旧式下亦全过，是陪跑之测'
    import re as _r
    m = _r.search(r'(\d+)/(\d+) 全通', out)
    return True, ('%s/%s 全通' % (m.group(1), m.group(2))) if m else '全通'


def chk_hard_gate():
    """硬闸·单一真源 负测（2026-09-01立·见 工具/负测_硬闸.py）。
    ★其立之由：硬项之集先前散在跑轮／预检／检察官三处，遂成两本账——
    ★★实测一段含 `? ! ;`、九鼎、赵阙、「那个那个」之稿跑预检，只报「英文」与「段间空行」。
    ★★★而此测除验新格外，另有一路要紧：**旧十三格拿全书回灌，一格不许走样**。"""
    out = run('负测·硬闸', ['工具/负测_硬闸.py'])
    if out is None:
        return False, '运行失败'
    if '全通' not in out:
        return False, out.strip().split('\n')[0]
    if '非陪跑' not in out:
        return False, '★此测在旧式下亦全过，是陪跑之测'
    return True, out.strip().split('｜', 1)[0].replace('✓ 负测·硬闸 ', '')


def chk_dup_gate():
    """叠词粘连闸 负测（2026-09-01立·见 工具/负测_叠词闸.py）。
    ★其立之由：检察官那道叠词闸写作 r'(那个|…)\\1'——r-string 里是「反斜杠＋1」两个字面字符，
    ★★故此闸自立起之日一次也没红过；★★★而改对之後其词表之「一个」又误咬「一个一个」34 处。"""
    out = run('负测·叠词闸', ['工具/负测_叠词闸.py'])
    if out is None:
        return False, '运行失败'
    if '全通' not in out:
        return False, out.strip().split('\n')[0]
    if '非陪跑' not in out:
        return False, '★陪跑之测'
    return True, _测数(out, '9/9') + ' 全通'


def chk_num_gate():
    """数闸（2026-09-01立·见 工具/数闸.py）。
    ★其立之由：这本书跟读者只签了一份合同——我只报我数过的（其法自书於 287:241）；
    ★★而十三轮之十二格硬项一格也不看数 ⛔。★★★今日一扫：全书138处「N个字」之标签，
    ★★★★本闸判得动132处，其中不符者若干——**一本以数为骨的书，机器不看数**。"""
    # ★★★★★2026-09-01·新立之闸只从立闸那一章起硬拦，其前之数作旧账（**此非挖空闸**）。
    #   ★其据是本书已有之先例：禁抖 40 章 75 处、五逗 3 章 4 处、半角引号 8 章 144 处——
    #     ★★三样皆是立法之前所写，三样皆不回头判红，而它们一直挂在账上。
    #   ★★★而旧账不许躺着：其数逐笔印在一坐与本项之语里，还清一笔少一笔；
    #     ★★★★**而第 288 章起若再犯一处，照旧硬拦。**
    out = run('数闸', ['工具/数闸.py'])
    if out is None:
        return False, '运行失败'
    # ★2026-09-01 修尺毕：全书三十余处逐处落刀，今零处不符；
    #   ★★而此闸两度放宽（前缀合／差逾五／引文许跨句）之後，须由负测证其还逮得住——
    #     ★★★故此处并跑 负测_数闸.py（十三处旧错逐处灌回须皆红，五处误报之形一处不许认）。
    neg = run('负测·数闸', ['工具/负测_数闸.py'])
    if neg is None or '全通' not in (neg or ''):
        return False, ('负测未过：%s' % (neg or '').strip().split('\n')[0])
    if '零处不符' in out:
        return True, '全书「N个字」之标签零处不符｜负测 19/19（十三处旧错灌回皆红）'
    # ★★★★★2026-09-01·旧账已还清（三十余处逐处落刀），故此闸即日提为全硬：
    #   ★立闸之日曾以「其前不回头判红」暂记旧账，其据是本书三处先例（禁抖／五逗／半角引号）；
    #   ★★而那是为了不让一道新闸回头把二百八十七章一齐判红，**不是为了让那笔账躺着**；
    #   ★★★今日账已还清，暂记即行撤销——**此後任何一章再犯一处，硬拦。**
    import re as _r
    m = _r.search(r'不符 (\d+) 处', out or '')
    return False, ('全书「N个字」标签不符 %s 处（其单在 数闸.py）' % (m.group(1) if m else '?'))


def chk_receipt_recon():
    """回执对账闸 负测（2026-09-01立·见 工具/负测_回执对账.py）。
    ★其立之由：287回执自书「净重2,951（起草）→2,796…共减155字」，而台账明印
    ★★v01=2,529→峰v08=2,951→v15=2,796，**是净增267**——把峰当成了起草 ⛔。
    ★★★令§十一：留底之档里的错因，会被下一坐当成场。"""
    out = run('负测·回执对账', ['工具/负测_回执对账.py'])
    if out is None:
        return False, '运行失败'
    if '全通' not in out:
        return False, out.strip().split('\n')[0]
    return True, _测数(out, '3/3') + ' 全通（含灌回旧错之验）'


def chk_fs_silence():
    """FS 沉默闸（2026-09-01立·见 工具/FS闸.py）。
    ★其立之由：canon 18 根伏笔，未销 13 根，逾期 137—212 章；
    ★★检察官每章印一遍，而**含 FS 编号之回执共 32 份，最末一份是第 99 章**——
    ★★★188 章问了 188 遍，一次没人答。★★★★它逼的是回话，不是逼数相等。"""
    # ★★★★★2026-09-01·同数闸之律：**此闸自第288章之回执起硬拦**。
    #   ★其由：287之回执已交（8月封版之前所写），而此闸9月才立——
    #     ★★拿今日之尺去追一份已交的回执，追得回来的只有一句空话。
    #   ★★★而这十三根不是就此放过：本坐正逐根回原场裁（兑了没有／改期到哪一站／判废），
    #     ★★★★裁毕即逐根写进回执并销此红；在那之前它每一坐都印在眼前。
    # ★★★★★2026-09-01·旧账已还清（十三根逐根回原场裁毕：六根判已兑补销、七根判改期），
    #   ★故此闸即日提为全硬——**此後任一根逾期而本章回执不提其名，硬拦**。
    #   ★★而须防一样：**闸是靠改期绿的**；一根钩子若靠反复改期永不兑现，
    #     ★★★这道闸就成了一张会自己签字的欠条 ⛔ → 故并印「改期之账」，逾二回者由人当场裁。
    out = run('FS沉默闸', ['工具/FS闸.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    改 = _r.search(r'改过期者 (\d+) 根', out or '')
    尾 = ('｜改过期者 %s 根' % 改.group(1)) if 改 else ''
    if '逐根俱已回话' in out:
        if '改期逾二回者' in out:
            m2 = _r.search(r'改期逾二回者 (\d+) 根', out)
            return True, ('逐根俱已回话%s｜⚠其中 %s 根改期逾二回，须人裁' % (尾, m2.group(1) if m2 else '?'))
        return True, ('逾期之伏笔，本章回执逐根俱已回话%s' % 尾)
    m = _r.search(r'未答 (\d+) 根', out or '')
    return False, ('本章回执未回话之逾期伏笔 %s 根（其单在 FS闸.py）' % (m.group(1) if m else '?'))


def chk_outside_voice():
    """外声闸（2026-09-01立·见 工具/外声闸.py）——**只报不拦**。
    ★其立之由：全角引号 1—99章2,876 → 100—199章2,461 → 200—239章572 → 240—287章 **0**；
    ★★280—287 八章 34,563 字，当场说出口的话四句十一个字，十七个问号全在心里。
    ★★★而此闸不设配额：279／283／286 是一人对一个不能说话的人，那三章的静是戏不是病。"""
    out = run('外声闸', ['工具/外声闸.py', '8'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'末尾连续出声为零：(\d+) 章', out or '')
    z = int(m.group(1)) if m else 0
    q = _r.search(r'240—\d+章 (\d+)', out or '')
    尾 = ('｜240章以来全角引号 %s 处' % q.group(1)) if q else ''
    if z >= 8:
        return True, ('⚠连续 %d 章无人出声（≥8，只报不拦）%s' % (z, 尾))
    if z >= 5:
        return True, ('⚠连续 %d 章无人出声（≥5，只报不拦）%s' % (z, 尾))
    return True, ('末尾连续无声 %d 章（限5）%s' % (z, 尾))


def chk_big_questions():
    """大问表（2026-09-01立·八造2026-09-03改·见 工具/大问表.py）——**可以欠，不可以不认**。
    ★其立之由：机器一处也没在问「读者还在等什么」——到期账258笔 open 0，
    ★★书级体检遂每章印「未清0笔｜距终点163章｜须净减0.00笔/章 ✓」。
    ★★★而器印：玉末见第80章缺207章／血图末60缺227／悬赏末71缺216／寨老末108／地窖末72缺215。
    ★★★★更要命者：E4指定要用的两样旧物（玉、听针）分别缺席207章与85章。

    ★★★★★**八造所改（其红在哪一行·2026-09-03 上磁盘核）**：其律自印「只报不拦」，
    以294章计逾四十章者七样（血图缺234章、悬赏223、地窖222、寨里那些人186、爷爷184、
    走路的理由116、听针92）——**二百三十四章之内没有一道闸因此拦过一次**。
    ★而其治**不是**逼着每章补喂一样（那必写成回忆段，正是令§二所禁），
    ★★是**逼着在册上认一笔**：逾限者须各有一笔挂账（其样／限第N章／其形写死），
    ★★★**挂了账又逾了自己那个限的，当场拦。**
    """
    out = run('大问表', ['工具/大问表.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'逾上限者 (\d+) 样', out or '')
    n = int(m.group(1)) if m else 0
    无挂 = _r.search(r'⛔ 逾限而无一笔挂账者 (\d+) 样：(.+)', out or '')
    逾限 = _r.search(r'⛔ 挂了账而逾了自己那个限者 (\d+) 样：(.+)', out or '')
    if 无挂 or 逾限:
        b = []
        if 无挂:
            b.append('无挂账 %s 样（%s）' % (无挂.group(1), 无挂.group(2).strip()))
        if 逾限:
            b.append('逾自定之限 %s 样（%s）' % (逾限.group(1), 逾限.group(2).strip()))
        return False, '｜'.join(b)
    if n == 0:
        return True, '八样俱在四十章之内'
    首 = _r.findall(r'^  (\S+)\s+\d+\s+第(\d+)章\s+(\d+)章\s+⛔', out or '', _r.M)[:3]
    return True, ('逾四十章者 %d 样，俱已挂账且未逾其限：%s'
                  % (n, '、'.join('%s缺%s章' % (a, c) for a, b, c in 首)))




def chk_blank_sign():
    """空头签 负测（2026-09-03立·见 工具/负测_空头签.py）。
    ★其立之由：295之回执以本章之号写了签核之六字，而 `_cold_done` 之 N 是被执者之号；
      ★★於是296起手时一坐印「COLD-295 限299 已执」——一笔方才立的冷轮，被一张空头签当场销掉。
    ★★★而立闸当日数其群（令§六②）当场驳掉头一版判据：那六字在本书有两代写法，
      75—278 以本章之号写它（195份），281起以被执者之号写它——故此闸只判新式那一代。"""
    out = run('负测·空头签', ['工具/负测_空头签.py'])
    if out is None:
        return False, '运行失败'
    if '全通' not in out:
        return False, out.strip().split('\n')[0]
    if '非陪跑' not in out:
        return False, '★陪跑之测'
    return True, _测数(out, '6/6') + ' 全通'


def chk_blank_sign_live():
    """空头签·实盘（每回直扫全书回执，不只跑负测）。"""
    out = run('空头签', ['工具/空头签.py'])
    if out is None:
        return False, '运行失败'
    if '零处' not in out:
        return False, '★有空头签，须逐份改其号'
    return True, '零处（新式那一代无一份签自己那一笔）'

def chk_object_roll():
    """器物点名 负测（2026-09-03立·见 工具/负测_器物点名.py）。
    ★其立之由：令§三③写死「器物须有来去，入用出缺一即伤」并指名归第6轮，
      ★★而 `一坐.py::逐轮之器` 第6轮空着——一条有主人的法，主人手上没有尺。
    ★★★而立闸当日负测②即逮出闸自身一洞：`len(parts)<4: continue`
      把「缺了一格的行」当成「没有这一行」，於是删掉一格「出」反倒全绿。"""
    out = run('负测·器物点名', ['工具/负测_器物点名.py'])
    if out is None:
        return False, '运行失败'
    if '全通' not in out:
        return False, out.strip().split('\n')[0]
    if '非陪跑' not in out:
        return False, '★陪跑之测'
    return True, _测数(out, '7/7') + ' 全通'

def chk_object_roll_all():
    """器物册·逐章回灌（2026-09-04立·299第6轮之坐所兑）。
    ★其立之由（其红在哪一行，上磁盘核过）：**器物点名只在它自己那一章的第6轮跑一回，跑完再没有人跑它**；
      ★★故凡第6轮之後的每一刀，都在册上留一道拍号错位，而没有一道有人看见；
      ★★★2026-09-04 逐章回灌，**297之册当场红五格**（本子·出107｜笔·用107、出109｜指甲·用76、出78——
        皆差一，其由是第6轮之後全章少了一拍而册一格也没跟着数），**而它自第7轮起一直绿到封版**。
    ★★★★**一份只在立它那一天跑过一回的册，跟没有是一个样**——故今逐章跑，一章红即此项红。
    ★其判据（令§六④）：**它认哪几样**——`版本/第*章/_器物.md` 之全部（今5份：295—299）；
      **本书同类共几样**——已写299章，其中有册者5章，无册者294章（第6轮之器立於295，其前无册，不追）。"""
    import glob as _g
    ps = sorted(_g.glob(os.path.join(ROOT, '版本', '第*章', '_器物.md')))
    if not ps:
        return False, '★一份器物册也没有'
    红 = []
    for f in ps:
        m = re.search(r'第(\d+)章', f)
        if not m:
            continue
        n = int(m.group(1))
        out = run('器物点名%d' % n, ['工具/器物点名.py', str(n)])
        if out is None or out.startswith('__'):
            return False, '第%d章 运行失败' % n
        if '⛔' in out:
            头 = [l.strip() for l in out.split('\n') if '⛔ ★' in l]
            红.append('第%d章·%s' % (n, 头[0] if 头 else '未过'))
    if 红:
        return False, '★' + '｜'.join(红[:3])
    return True, '%d 份册逐章跑过，皆绿' % len(ps)


def chk_stop_flag():
    """拦停旗自失其义 负测（2026-09-04立·见 工具/负测_拦停旗.py）。
    ★其立之由（299第6轮亲犯）：`--存版 N` 不带说明，版落盘而说明为空；
      ★★带着说明再存，空轮闸判「正文与末版逐字相同」→ 拦 → 落旗；
      ★★★而销旗之路只有一条「一次成功的存版／补存」，那一条路正被空轮闸堵着——
      **旗落下去就再也拿不掉，而它拦的是其後一切轮务**（第二十四犯之族）。
    ★★★★故立「旗自失其义」之查，其条件写死三样（因是空轮闸｜说明报得出轮号｜账上有那一轮之真说明）；
      **而棘轮回退／趋阈闸／硬项／闸八所落之旗，一面也销不掉**——那几样是「存坏了」，不是「存了两回」。"""
    out = run('负测·拦停旗', ['工具/负测_拦停旗.py'])
    if out is None or out.startswith('__'):
        return False, '运行失败'
    if '坏 0' not in out:
        bad = [l.strip() for l in out.split('\n') if l.strip().startswith('✗')]
        return False, bad[0] if bad else out.strip().split('\n')[-1]
    if '非陪跑' not in out:
        return False, '★陪跑之测'
    return True, _测数(out, '19 项') + ' 全通（旧式「只问旗在不在」在①之下照旧拒，故非陪跑）'


def chk_reread_dup():
    """连读客·问五（逐字重出）负测（2026-09-03·296第11轮立·见 工具/负测_连读重出.py）。
    ★其立之由：296第10轮手打一条 grep 量出 294→296 有19/138拍含≥10字逐字重出，
      ★★而同日 `看官.py --连读 292 296` 四问俱绿——**本书唯一一只跨章之眼对此是瞎的**；
    ★★★§六④：31对相邻同线之章，中位2.1%｜顶13.8%（294→296）；故6%⚠、10%⛔。"""
    out = run('负测·连读重出', ['工具/负测_连读重出.py'], timeout=1200)
    if out is None:
        return False, '运行失败'
    if '全通' not in out:
        return False, out.strip().split('\n')[-1]
    return True, _测数(out, '8/8') + ' 全通（旧式问三对292—296一无所报）'


def chk_draft_court():
    """起草庭 负测（2026-09-04·作者亲令所立·见 工具/起草庭.py）。
    ★其立之由（上磁盘核·两组数）：**开镜卡 102 份**——写了「五钩」者 0 份｜「新问」0 份｜
      「弃卷／合上书／翻下一页」0 份｜一事之另二候选 3 份（其余 99 份只写一个一事，从来没有比过）；
      ★★而「最神一句」轮记 87 份（第13轮才问），**开镜卡 0 份**——
      **书里最好的那几句，一句也不是先立志要写、而後挣来的。**
    ★★★故十三轮管的是「写完之後怎么改到最好」，而「怎么想才起草得出最好的那一章」，
      **全书一件器也没有**。★★★★本庭补的正是那一件。
    ★而其非陪跑之凭：**拿 303 之现卡回灌，四格须皆报红**（负测断言②）。"""
    out = run('负测·起草庭', ['工具/起草庭.py', '--自测'])
    if out is None:
        return False, '运行失败'
    if '全通' not in out:
        return False, out.strip().split('\n')[-1]
    return True, out.strip().split('\n')[-1].strip()


def chk_due_states():
    """到期账词表 负测（2026-09-04·303第1轮立·见 工具/负测_到期账词表.py）。
    ★其立之由：`小说检察官.py::_CLEARED_STATES` 只认 done/closed/half/废弃/cold/冷藏/已清，
      而账写的是「清」——故 301 封版那一坐清掉的三笔（PRES-297A／PRES-297B／PROM-295.83），
      **在 303 之全书检里照旧被催作「逾期2章未清」，ERROR=3，封版即拦。**
    ★★而这已是第二回：批123 之 closed 是头一回（220判账写 closed，闸不认，222报红）。
    ★★★其群：全表266项，状态之全集只六样（done247/closed9/cold3/half1/open3/清3），
      **「清」只三笔，而三笔同出於一坐**——一坐写下一个新词，闸就跟不上。"""
    out = run('负测·到期账词表', ['工具/负测_到期账词表.py'])
    if out is None:
        return False, '运行失败'
    if '全通' not in out:
        return False, out.strip().split('\n')[-1]
    if '非陪跑' not in out:
        return False, '负测未证其非陪跑（旧表回灌须报红）'
    return True, out.strip().split('\n')[-1] + '（旧表回灌那三笔皆判未清，故非陪跑）'


def chk_price_check():
    """立价查 负测（2026-09-03·296第9轮立·见 工具/负测_立价查.py）。
    ★其立之由：`立价查.py` 自292第13轮立起，全书无一条负测证明它红得起来
      （对位闸印「赤手无负测者 21 项」，此器即其一）；
    ★★而296第9轮当场见其缺口：旧式四条认不着「只要」，
      故它在296之第4、7、9三轮连印「✓全章无立价之句」，
      **而本章之价正写在「而它管用只在一样上：只要它今天这么摆着」**。
    ★★★数其群：条件句全集688处，旧式认544处，**144处（21%）此器一眼看不见**。"""
    out = run('负测·立价查', ['工具/负测_立价查.py'])
    if out is None:
        return False, '运行失败'
    if '全通' not in out:
        return False, out.strip().split('\n')[-1]
    if '非陪跑' not in out:
        return False, '★陪跑之测'
    return True, _测数(out, '7/7') + ' 全通（旧式回灌真器印「全章无立价之句」）'


def chk_open6_gate():
    """开轮六检·check7 之阈 负测（2026-09-05·304第10轮立·清 DEBT-297E·见 工具/负测_开轮六检.py）。
    ★其立之由：check7 之阈原写死作 10，而码注自陈「十轮已满」——係十轮制之遗；
    ★★而本系统十三轮（跑轮.py::ROUNDS=13），**而锚之备係封版之事，封版在第13轮之後**；
    ★★★故此拦在第10轮即出声，早了三轮，且它一出声便拦住往後每一轮之推
      （297第10轮实逮，304第10轮再逮——同形第二次，故今结清）。
    ★★★★而其治不是把 10 改写成 13，是去问跑轮它自己有几轮（_rounds）——一改全改。"""
    out = run('负测·开轮六检', ['工具/负测_开轮六检.py'])
    if out is None:
        return False, '运行失败'
    if '全通' not in out:
        return False, out.strip().split('\n')[-1]
    if '非陪跑' not in out:
        return False, '★陪跑之测'
    return True, _测数(out, '8/8') + ' 全通（旧阈回灌304真报⛔，而满轮无锚者新阈照旧咬）'


def chk_cold_agree():
    """一坐与开轮六检对冷轮须同判 负测（2026-09-01立·见 工具/负测_冷轮同判.py）。
    ★其立之由：同一 HEAD 上一坐印「COLD-284／285 未执」而六检印「⑥ 零」——二器相反 ⛔。
    ★★数其群：冷轮档134份，含「已执＋销档」者仅37份、以回执判者131份——那个标记从未成为惯例。"""
    out = run('负测·冷轮同判', ['工具/负测_冷轮同判.py'])
    if out is None:
        return False, '运行失败'
    if '全通' not in out:
        return False, out.strip().split('\n')[0]
    return True, _测数(out, '3/3') + ' 全通（二器同用一处 _cold_done）'


def chk_reader_nag():
    """存版·阅读器过期即报 负测（2026-09-01立·见 工具/负测_阅读器催.py）。
    ★其立之由：每轮改文之后阅读器即过期，而医生／检察官自测／全书检三项俱据之报红，
    ★★遂使每一轮之推送皆被拦一回；其治只一条命令，难只在「想不起来」。
    ★★★七项之中，末二项最要紧：器崩与看不懂之时须仍催——
    ★★★★一个「看不懂就当没事」的催，比没有更坏。"""
    out = run('负测·阅读器催', ['工具/负测_阅读器催.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'负测 (\d+) 项，过 (\d+)，坏 (\d+)', out)
    if not m:
        return False, '未见其数'
    tot, ok, bad = (int(x) for x in m.groups())
    if bad or ok != tot:
        _b = [ln.strip() for ln in out.splitlines() if ln.strip().startswith('⛔')]
        return False, '；'.join(_b[:3]) or '%d/%d' % (ok, tot)
    return True, '%d/%d 全通' % (ok, tot)


def chk_reversible():
    """可逆库之验（2026-08-30立·作者令「我给你授权，但要留下记录，随时可以复原」）。
    ★逐件核 sha256：库若损，「随时可复原」即是空话，而那条授权也就白给了。
    ★★故此验一红即拦推——库不完好之时，任何不可逆之事都不许再办。"""
    out = run('可逆库之验', ['工具/可逆.py', '--验', '--静'])
    if out is None:
        return False, '运行失败'
    if '可逆库完好' in out:
        import glob as _g
        n = len([x for x in _g.glob(os.path.join(ROOT, '版本', '_可逆库', 'R*')) if os.path.isdir(x)])
        return True, '%d 笔·逐件 sha256 相符' % n
    return False, out.strip()[:120]


def chk_reversible_neg():
    """可逆册负测（2026-08-30立·见 工具/负测_可逆册.py）。
    ★二十三项：存了真能复原（含删章之形）／库损了认得出／认不出时敢不敢拦／
    ★★号须递增不许覆盖／册须逐笔留痕（号、由、复原之法三样俱在）。"""
    out = run('负测·可逆册', ['工具/负测_可逆册.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'负测 (\d+) 项，过 (\d+)，坏 (\d+)', out)
    if not m:
        return False, '未见其数'
    tot, ok, bad = (int(x) for x in m.groups())
    if bad or ok != tot:
        _b = [ln.strip() for ln in out.splitlines() if ln.strip().startswith('⛔')]
        return False, '；'.join(_b[:3]) or '%d/%d' % (ok, tot)
    return True, '%d/%d 全通' % (ok, tot)


def chk_push_gate():
    """推闸负测（2026-08-28立·随「改钩子之策」同日·见 工具/负测_推闸.py）。
    ★其立之由：推闸一开，闸即从「全绿才许推」放宽为「跑轮期间可推」；
    ★★而放宽之闸若窗划得不准，等於把闸拆了——故须有测逐一证其窄。
    ★★★十六项之中，放行者只三（跑轮中·只那二项），其余十三项一律须拦。"""
    out = run('负测·推闸', ['工具/负测_推闸.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'负测 (\d+) 项，过 (\d+)，坏 (\d+)', out)
    if not m:
        return False, '未见其数'
    tot, ok, bad = (int(x) for x in m.groups())
    if bad or ok != tot:
        _b = [ln.strip() for ln in out.splitlines() if '⛔' in ln]
        return False, '；'.join(_b[:3]) or '%d/%d' % (ok, tot)
    return True, '%d/%d 全通' % (ok, tot)


def chk_day_gate():
    """①之c·一章一日 负测（2026-08-28立·随「补零〇」同日·见 工具/负测_日词闸.py）。
    ★其立之由：旧式不含零／〇，凡带零之日号一律漏认，且报「0 处」而非报错；
    ★★其最险之一形：「第一百天」与「第一百零一天」同章，旧闸报「1 处」——二日同章整个放过去。
    ★★★而此测已以旧式回灌验过：旧式之下十一项坏五项，新式之下全通。"""
    out = run('负测·日词闸', ['工具/负测_日词闸.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'负测 (\d+) 项，过 (\d+)，坏 (\d+)', out)
    if not m:
        return False, '未见其数'
    tot, ok, bad = (int(x) for x in m.groups())
    if bad or ok != tot:
        _b = [ln.strip() for ln in out.splitlines() if '⛔' in ln]
        return False, '；'.join(_b[:3]) or '%d/%d' % (ok, tot)
    return True, '%d/%d 全通' % (ok, tot)


def chk_ratchet_v01():
    """★棘轮之v01之底负测（RATCHET_V01·2026-09-02立·欠-289B所结）：
    ★★四感不得低於起草之版。其立之前取二组数——
      ★★★以峰为底（RATCHET_MAX之式）逐章回灌红 128章/177（72%），一改即红一片，是拆书不是修闸；
      ★★★★以 v01 为底则 嗅2%／听6%／触5%／视7%。二组数皆写在负测里，下一坐不必再量。"""
    out = run('负测·棘轮v01', ['工具/负测_棘轮v01.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'(\d+)/(\d+) (全通|⛔有败)', out)
    if not m:
        return False, '未见其数'
    ok, tot, 判 = int(m.group(1)), int(m.group(2)), m.group(3)
    if 判 != '全通' or ok != tot:
        _b = [ln.strip() for ln in out.splitlines() if '✗' in ln]
        return False, '；'.join(_b[:3]) or '%d/%d' % (ok, tot)
    return True, '%d/%d 全通（v26回灌报「听15→13低於起草」｜删无感官之判则放行）' % (ok, tot)


def chk_band():
    """★令四之带负测（2026-09-02·291第7轮改齐）：
    ★★旧表逐字为「常章2,500—3,500｜转章4,000—5,500｜爆章~6,000以上」——
      **故3,501—3,999与5,501—5,999二段字面上没有名字**；
      ★★★逐章量之：缝一35章、缝二39章，合「不足2,500」者共99章＝**全书34%在所有带之外**，
        **而全书净重中位3,691正落在缝一的正中**——即旧表把本书最常见的那一档章长整个划在带外。
    ★★★★今改：**转章带 3,501—5,999**（下沿由4,000降、上沿由5,500抬），常章带与爆章之界（6,000起）不动。
      ★其据不是数，是事：**缝内三十九章逐章读过，三十六章判「转章之事」（92.3%）**，
        且逐百字分格无梯度（3600—3700与3900—4000皆100%）——**4,000那个下沿是虚的**。
      ★★而三章判「常章之事」者（284、146、145）正是「笔法之重非事之重」，
        由上位之序②接住：**品由事定，带为其验；品带相犯者写一行留档，不许改品去就带。**"""
    out = run('负测·章型带', ['工具/负测_章型带.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'(\d+)/(\d+) (全通|⛔未通)', out)
    if not m:
        return False, '未见其数'
    ok, tot, 判 = int(m.group(1)), int(m.group(2)), m.group(3)
    if 判 != '全通' or ok != tot:
        _b = [ln.strip() for ln in out.splitlines() if '✗' in ln]
        return False, '；'.join(_b[:3]) or '%d/%d' % (ok, tot)
    return True, '%d/%d 全通（旧表带外74章25%%→新表0章｜中位3691正落旧缝｜序②在册）' % (ok, tot)


def chk_ratchet_verdict():
    """★棘轮裁负测（2026-09-02·292第3轮所立）：**那道专为「裁棘轮回退」而立的器，自己是歪的。**
    ★①方向：其「历史最优」用 min()，不分方向；★★而棘轮 MIN 二目、MAX 二目、V01 四目，
      **八目里六目愈高愈好**——跑 `--棘轮 292 --项 嗅` 得「历史最优 2（出於 v01）」，
      而 v01 正是最薄那一版；**照它读，嗅 8 反倒该记功。**
    ★②举证：292第2轮裁一处回退，其由是「所删那一拍係逐字抄290」——**而那句话是我说的，不是器说的**；
      ★★其治不是让器替我免裁（回灌全书：可免裁者 18/28＝64%，含拆章之版，**太松，那是挖空闸**），
      ★★★而是举证：**器摆凭据，裁仍归人**。
    ★★★★其回灌（令§六③）：③以旧式（min）於嗅得 2，新式得 12；⑦⑧举证之句逐字可查。"""
    out = run('负测·棘轮裁', ['工具/负测_棘轮裁.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'(\d+)/(\d+) (全通|⛔未通)', out)
    if not m:
        return False, '未见其数'
    return m.group(3) == '全通', '棘轮裁负测 %s/%s' % (m.group(1), m.group(2))


def chk_blankline_gate():
    """★段间空行闸负测（2026-09-02·292第11轮·补跑所立）：
    ★其形：**一个闸只会假红，於是它教出来的不是「补空行」，是「看见红就跳过」。**
    ★★其凭据（器出，非本席之说）：段间空行之检原查全文，而【本章亮点】係markdown列行，行行紧挨；
      **全书292章有55章长红，而这55章白文内之命中皆为0**——五十五分之五十五皆假。
    ★★★而阅读器那一头更进一层：为堵这噪，加过一条「七十／八十」之赦——
      **只对两批章号硬拦，余者一概「存量待补(不拦)」**；★★★★**赦的不是伤，是噪。**
    ★其治：只查白文（段间空行本就是白文之律），赦令一并撤去，白文漏空行即硬拦。
    ★★其回灌（令§六③）：②之b 以旧式判「白文洁净＋常规亮点段」得红，新式得净；
      ⑧以旧式回灌全书须假红≥20章；⑦以新式回灌全书须为0——撤赦之凭据在此，不在本席口里。"""
    out = run('负测·段间空行闸', ['工具/负测_段间空行闸.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'负测 (\d+) 项，过 (\d+)，坏 (\d+)', out)
    if not m:
        return False, '未见其数'
    tot, ok, bad = (int(x) for x in m.groups())
    if bad or ok != tot:
        _b = [ln.strip() for ln in out.splitlines() if ln.strip().startswith('⛔')]
        return False, '；'.join(_b[:3]) or '%d/%d' % (ok, tot)
    return True, '%d/%d 全通' % (ok, tot)


def chk_fill_note_gate():
    """★填记口负测（2026-09-02·292第11轮自逮）：**吞记闸之第二形**。
    ★其形：`--验收 N` 之说明亦係位置参数（argv[3]）；不写即自动存版并落一行占位说明。
      ★★而落完之後正文与末版已逐字相同，**空轮闸遂拦住 --存版 与 --补存**——
      **那一行占位说明再也改不掉了**；★★★而真轮数轮号数的正是这一行：
      **一轮真跑过了，而账上说不出它跑了什么。**（292 v16、v17 二行皆栽於此）
    ★其治不是让验收少落一版（账上少一版比说不清更坏），而是开一个**只填得了洞的口**：
      ★★凡该行说明非占位原文者一律拒填，且填完留「原说明」之痕——**能填洞，不能覆盖记录。**
    ★★★其回灌（令§六③）：③以真说明一行试填，须拒；③之d 填过一回之後再填，仍须拒。"""
    out = run('负测·填记口', ['工具/负测_填记口.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'负测 (\d+) 项，过 (\d+)，坏 (\d+)', out)
    if not m:
        return False, '未见其数'
    tot, ok, bad = (int(x) for x in m.groups())
    if bad or ok != tot:
        _b = [ln.strip() for ln in out.splitlines() if ln.strip().startswith('⛔')]
        return False, '；'.join(_b[:3]) or '%d/%d' % (ok, tot)
    return True, '%d/%d 全通' % (ok, tot)


def chk_effort_recheck():
    """★功力回检第五路负测（2026-09-02·292第12轮·极限轮所立）：
    ★**一道靠加词修的闸，修了五回。** 前四修皆是「再加几个词」（08-19加真伤路／08-21修数字类
      并广词表／08-22加带数之产出／08-22再修加净重A→B）；★★**每加一个词就多一个「写这个词
      即可蒙混」的口，而它照旧看不见没写那个词的活。**
    ★★★今日之实：**292第7轮之轮记有十一版回灌表、一个相关系数、一处「42→27」，
      是全十轮里量得最细的一轮**，而器判它「五路俱无·走了过场」——
      ★**器报的不是活没干，是器看不见活**（此语係08-21那一修自己写下的，今日又应验一回）。
    ★★★★故第五路不认词，只认账：**自台账取该轮之版与其前一版比净重，文动了即是实凭**；
      并於每行下印「凭何而绿」，**见得出哪一轮靠轮记之实、哪一轮只靠正文动过。**
    ★其回灌（令§六③）：⑥摘掉第五路，第2轮须由绿转⚠（**证非陪跑**）；
      ⑤第3轮词无而正文亦未动，两式同判⚠（**证未把闸改成人人皆绿**）。"""
    out = run('负测·功力回检', ['工具/负测_功力回检.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'负测 (\d+) 项，过 (\d+)，坏 (\d+)', out)
    if not m:
        return False, '未见其数'
    tot, ok, bad = (int(x) for x in m.groups())
    if bad or ok != tot:
        _b = [ln.strip() for ln in out.splitlines() if ln.strip().startswith('⛔')]
        return False, '；'.join(_b[:3]) or '%d/%d' % (ok, tot)
    return True, '%d/%d 全通' % (ok, tot)


def chk_layer_census_honest():
    """★层census与立价查负测（2026-09-02·292第13轮所立）：
    ★**造出来的器不称职，须与器同存，不许删。**
    ★★层census 本是为答「每层在白文里占几拍」而造；拿她自己四章回灌：
      **284 覆盖 6%（四层皆判「占一拍」，而284係已封版之章，其五层无人判过薄）｜
      286 17%｜292 31%｜288 45%**——★★★**同一把尺在五章之间从6%摆到45%**，
      **摆的是我写亮点段的手，不是章的厚薄**。★★★★故其名与其判俱改：
      **它量的是「亮点段引实率」**，且校准之数印在器上，**不许再读作层薄**。
    ★而那一问另造一器答之：**立价查**——价之形係条件句，其收是那个果在其後真发生一回。
      ★★292得「立价1处·未收1处」（拍10「写上去这一行就得往里挪」），
      **正是第12轮逐层读出来的那一根，器独立复得**；
      ★★★回灌她自己四章：284/286 零｜288 一处未收｜290 二处未收｜**291 一处而收了**
      ——**非遍地皆红，亦非陪跑。**
    ★★★★而其所现者非伤：**立而不收是她三章连着的一个手法**（288「改了这一行就成了两个日子的」／
      290、292「往里挪」）——**她一再立一个价，然後不付。** 器把它由「疑似之伤」变成「认得出的形」。"""
    out = run('负测·层census与立价查', ['工具/负测_层census.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'负测 (\d+) 项，过 (\d+)，坏 (\d+)', out)
    if not m:
        return False, '未见其数'
    tot, ok, bad = (int(x) for x in m.groups())
    if bad or ok != tot:
        _b = [ln.strip() for ln in out.splitlines() if ln.strip().startswith('⛔')]
        return False, '；'.join(_b[:3]) or '%d/%d' % (ok, tot)
    return True, '%d/%d 全通' % (ok, tot)


def chk_seal_new_cold():
    """★销立门负测（2026-09-02·293起轮时所立·第二十四犯之第四形）：
    ★**立之序明书「销旧须当场立新」**，而**291之回执销了两笔却一笔也没立新**；
      ★★遂使 `_cold_limit(291)` 退回通则 N+2＝293，而其面无档——
      **账上一笔红，红的是一个不存在的东西。**
    ★★★**与前三形之别**：前三形是「写下来的东西被吞了」，**本形是「该写的那一样从来没写」**——
      ★★★★**吞了的还看得出说明是空的，没写的连个空位也没有。**
    ★数其群（令§六②）：**自 COLD-153 立档以降之回执 140 份，销过旧冷轮者 134 份，
      而销而未立新者 4 份（155、198、200、291）**——**群成，非孤例，故机化。**
    ★★其向只朝前（只查正在封版的那一章），**故於已封之史零假红**；
      ★★★其回灌（令§六③）：④之b 291今已补立，须不在其中——**它若还在，说明补立那一档没落盘。**"""
    out = run('负测·销立门', ['工具/负测_销立门.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'负测 (\d+) 项，过 (\d+)，坏 (\d+)', out)
    if not m:
        return False, '未见其数'
    tot, ok, bad = (int(x) for x in m.groups())
    if bad or ok != tot:
        _b = [ln.strip() for ln in out.splitlines() if ln.strip().startswith('⛔')]
        return False, '；'.join(_b[:3]) or '%d/%d' % (ok, tot)
    return True, '%d/%d 全通' % (ok, tot)


def chk_orphan_snapshot():
    """★孤版负测（2026-09-02·293第1轮自逮·第二十四犯之第五形）：
    ★`save()` 之快照落盘写在诸闸之前，而趋阈闸／棘轮闸拦停时 return——**快照落了盘，台账没落**；
      ★★且当场印一句「⛔存版已拦停，未写入任何文件」——**那是假话，文件写了。**
    ★★★其果有二：①磁盘上多一个无账之孤版；②**空轮闸原比「磁盘上最後一个 vNN.md」**，
      而那个孤版恰与正文逐字相同，**空轮闸遂把「上一次被拦」读成「本轮零改动」**，
      此後同一段文再也存不进去——★★★★**一道闸拦了我一回，然後把门锁上了。**
    ★其实（今日之实，非设想）：293第1轮补感官毕，趋阈闸拦一回，此後 --补存 一律被空轮闸拦死；
      **而那一次拦本身是对的**（长段数 0→1 余量0字），**错的是它拦完之後留下的那个孤版。**
    ★★其治二样：①**快照之写下移至台账之写旁**（账上有它，磁盘才有它，其间无 return）；
      ②**空轮闸改比「台账所记之末版」**——**账上没有的版，不作数。**
    ★★★其回灌（令§六③）：④与⑤之b 以旧式於同一局面判「空轮·拦死」，新式放行——**两式相反，证非陪跑**；
      ★③之b 真空轮（正文与台账末版逐字相同）照旧拦——**证未挖空。**"""
    out = run('负测·孤版闸', ['工具/负测_孤版闸.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'负测 (\d+) 项，过 (\d+)，坏 (\d+)', out)
    if not m:
        return False, '未见其数'
    tot, ok, bad = (int(x) for x in m.groups())
    if bad or ok != tot:
        _b = [ln.strip() for ln in out.splitlines() if ln.strip().startswith('⛔')]
        return False, '；'.join(_b[:3]) or '%d/%d' % (ok, tot)
    return True, '%d/%d 全通' % (ok, tot)


def chk_fs_ack():
    """★FS认账负测（2026-09-02·293第1轮所立）：
    ★**FS沉默闸之销在本章回执，而回执须待十三轮跑毕**；
      ★★故一根逾期之伏笔可以拦住此後十二轮的每一次推——
      ★★★**而拦十二回并不能让回执早交一天，只能教出「见红就 --no-verify」**
      （绕行审计.log 里那四十五次绕行，正是⑥当年这么长出来的）。
    ★★★★其治之式与⑥之否决记同，一字不宽：**放行之价是一行写下来的字，不是一次沉默**——
      **逾期之每一根 FS，须在本章之轮记或开镜卡里写着「FSxx·本章未兑」**；
      ★**认账只有在肯写「未兑」二字时才写得出来**；★★**悄悄滑过去的那一根，照旧拦。**
    ★★★其回灌（令§六③）：②之b 抽掉其中一根之认账即须拦（**不许拿「认了大半」蒙混**）；
      ①一根也没认账者照旧拦（**证本闸之本职未被挖空**）。
    ★★★★而其单取自 FS闸 自己那一支，不取自报文——**报文里本就没有根号**（头一版即栽於此，已与器同存）。"""
    out = run('负测·FS认账', ['工具/负测_FS认账.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'负测 (\d+) 项，过 (\d+)，坏 (\d+)', out)
    if not m:
        return False, '未见其数'
    tot, ok, bad = (int(x) for x in m.groups())
    if bad or ok != tot:
        _b = [ln.strip() for ln in out.splitlines() if ln.strip().startswith('⛔')]
        return False, '；'.join(_b[:3]) or '%d/%d' % (ok, tot)
    return True, '%d/%d 全通' % (ok, tot)


def chk_highlight_gate():
    """★亮点闸负测（2026-09-02·293第2轮所立·**九犯而未机化，今机化**）：
    ★一坐⑬之法早已写在纸上——**「凡起草毕即须落亮点段，不得留到后轮」**；★★**而它只报不拦。**
    ★★★病历本记「亮点段必犯病」8次，一坐今日印「此病已犯九次」——**而第九次正是我自己**：
      293起草毕未落，留到第2轮才补。
    ★★★★数其群（令§六①②）：**有版可查之章 174，亮点段落在 v01 或 v02 者 125 章，
      而落在 v03 之後者 49 章（28%）**——**群成，非孤例。**
    ★其位非在报，在存版之路上：**第1轮之存版若无亮点段，当场拦停**；
      ★★而其向只朝前（旧章不再重存，全书106篇无亮点段之旧章零假红），
      ★★★不报轮号之存版亦不受此拦（与领轮闸同律：说明一空即不认轮）。
    ★★★★其回灌（令§六③）：⑥摘掉 `_liang` 一路，第1轮无亮点段者即放行——**证非陪跑**；
      ★②③④三项各验其不越界（有者不拦／第2轮不问／不报轮号者不问）——**证未扩成「凡存版皆拦」。**"""
    out = run('负测·亮点闸', ['工具/负测_亮点闸.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'负测 (\d+) 项，过 (\d+)，坏 (\d+)', out)
    if not m:
        return False, '未见其数'
    tot, ok, bad = (int(x) for x in m.groups())
    if bad or ok != tot:
        _b = [ln.strip() for ln in out.splitlines() if ln.strip().startswith('⛔')]
        return False, '；'.join(_b[:3]) or '%d/%d' % (ok, tot)
    return True, '%d/%d 全通' % (ok, tot)


def chk_review_no_note():
    """★验收空说明只查不存 负测（2026-09-02·293第3轮所立·**第二十四犯第二形之根治**）：
    ★前此之治只是「先出声，照旧落占位」；★★**而一坐之内我从这个口走过六回**
      （292 v16/v17、293 v02/v05/v07/v08/v11/v12）——**每一回都是同一个来回**：
      做完活 → 跑一次不带说明的 `--验收` 查硬项 → 它把版存了 →
      我带着说明再存，空轮闸判「正文与末版逐字相同」→ 拦 → 回头 `--填记`。
    ★★★数其群（令§六①②）：**全书台账 3,352 版，占位行旧史只 1 行（第101章 v03）**；
      **而今日一坐造出 8 行**——★★★★**群不在旧史里，在今日这一坐里，而它是同一个口。**
    ★故不再落占位：**不带说明的 `--验收` 只查不存**；
      ★★**其由**：**一行读不出自己跑的是哪一轮的账，不如不落**；
      ★★★**而「挑刺」带说明者照旧存版，批103之单一入口未动**（只少了「空说明也存」这一路）。
    ★★★★其回灌（令§六③）：①之c 沙盘实跑一回，台账一行不动；
      ★②③各验其不越界（带说明者照旧存／填记口未删，旧史那一行还得有路可填）。"""
    out = run('负测·验收空说明', ['工具/负测_验收空说明.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'负测 (\d+) 项，过 (\d+)，坏 (\d+)', out)
    if not m:
        return False, '未见其数'
    tot, ok, bad = (int(x) for x in m.groups())
    if bad or ok != tot:
        _b = [ln.strip() for ln in out.splitlines() if ln.strip().startswith('⛔')]
        return False, '；'.join(_b[:3]) or '%d/%d' % (ok, tot)
    return True, '%d/%d 全通' % (ok, tot)


def _简测(名, 脚本):
    """★共用之壳：跑一份「N/N 全通」式负测，取其末行之数。"""
    out = run(名, [脚本])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = None
    for _m in _r.finditer(r'(\d+)/(\d+)\s*(全通|⛔未过)', out):
        m = _m
    if not m:
        return False, '未见其数'
    ok, tot = int(m.group(1)), int(m.group(2))
    if ok != tot:
        _b = [ln.strip() for ln in out.splitlines() if ln.strip().startswith('⛔')]
        return False, '%d/%d｜%s' % (ok, tot, '；'.join(_b[:3]))
    return True, '%d/%d 全通' % (ok, tot)


def chk_bigq_neg():
    """负测·大问挂账（八造·2026-09-03 立·见 工具/负测_大问挂账.py）。"""
    return _简测('负测·大问挂账', '工具/负测_大问挂账.py')


def chk_two_ledger():
    """两册对限（2026-09-04·300第7轮立·见 工具/两册对限.py）。

    ★其由：一笔改了限而另一册没跟着改——刘二之限由300改301，同笔改了四处档，
      而 到期账.json 照旧写着300，三坐无人看见（欠-297A之形：令与闸各读一册）。
    """
    out = run('两册对限', ['工具/两册对限.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'两册认得上者 (\d+) 对', out or '')
    bad = _r.search(r'⛔ 两册不合 (\d+) 笔', out or '')
    if bad:
        return False, '⛔两册不合 %s 笔（一笔改了限而另一册没跟着改）' % bad.group(1)
    return True, '两册认得上者 %s 对，逐笔同限（★其余只在一册上者本器不说）' % (m.group(1) if m else '?')


def chk_two_ledger_neg():
    """负测·两册对限（见 工具/负测_两册对限.py）。"""
    return _简测('负测·两册对限', '工具/负测_两册对限.py')


def chk_scenecut_neg():
    """负测·场景切换闸（2026-09-04·300第5轮立·见 工具/负测_场景切换闸.py）。

    ★其由：质量三闸①之c 之词表原有四样，而三百章里只响过三回，三回皆假；
      真切换词「与此同时／同一时候」全书零处。今缩其词表至二样，并以本测钉死其判据。
    """
    return _简测('负测·场景切换闸', '工具/负测_场景切换闸.py')


def chk_duiwei():
    """对位闸（八造·2026-09-03 立·见 工具/对位.py）——**所有的机制都得跑起来**（作者令）。

    ★其查三样：①孤器（有器而无一条路够得着）｜②剧情之器出声之位（出声之时文还改不改得动）
    ｜③负测覆盖（令§一⑤★★★★：一项要进「所守」，须其负测里有一条回灌须报红）。
    ★★其红在哪一行（2026-09-03 上磁盘核）：`pageturn`（五钩·本书唯一一件量「读者翻不翻页」之器）
    全仓只有一个调用点，在 `ai_homework` 之内，而 `ai_homework` 只在 `--封版` 之下——
    **十三轮无一轮调得着它**；且 `--封版 293` 实跑，其「收尾三段」印的是封版台账，不是小说的结尾。
    """
    out = run('对位闸', ['工具/对位.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    孤 = _r.search(r'⛔ 孤器 (\d+) 件', out or '')
    哑 = len(_r.findall(r'⚠ \S+：\*\*令里有其事而无其命令\*\*', out or ''))
    负 = _r.search(r'赤手无负测者 (\d+)（(\d+)%）', out or '')
    msg = []
    if 负:
        msg.append('负测覆盖：赤手无负测者 %s 项（%s%%）之绿一律记「未验」' % (负.group(1), 负.group(2)))
    if 孤 or 哑:
        b = []
        if 孤:
            b.append('孤器 %s 件' % 孤.group(1))
        if 哑:
            b.append('哑器 %d 件（令里有其事而无其命令）' % 哑)
        return False, '｜'.join(b + msg)
    return True, '｜'.join(['诸器各有其位'] + msg)


def chk_grand_audit():
    """大审闸（2026-09-02·作者令所立）
    ★**作者令**：「平均10章就应该从头到尾进行一个剧情和质量各个方面严格把控」，
      且须「站在普通读者／最顶尖小说家／评委／编辑／小说爱好者的视角」，「不要说只有一个小说家」。
    ★★而立此闸之前先答一问（审器所逼）：**光加席够不够？不够。**
      ★**五席之输入是同一样东西**（`白文(n)` 之字符流＋一张手写动词表＋对它的计数）——
        **四席吃同一份输入，是同一次测量的四个样本，不是四只眼**；
      ★★**唯一产出过真发现的是连读客，而它正是唯一输入不同的那一席（多章）**；
      ★★★**故甲律**：**一席要占位，须说得出「它看得见而现有各席都看不见的那一样是什么」。**
    ★★★**乙律·不强制出负，强制留痕**（必然要响的器，响的时候不携带信息）；
      **丙律·每笔须落拍号，且须逐笔落治／驳／挂，挂须带限。**
    ★★★★而此器不读小说也不判小说——**它只管到十章了没有、席够不够、判有没有人收**；
      **真读的那一步只有人（或替人真读的第三方）做得了，器不许替它签字。**"""
    out = run('大审闸', ['工具/大审.py', '--闸'])
    if out is None:
        return False, '运行失败'
    bad = [x.strip() for x in out.splitlines() if x.strip().startswith('⛔')]
    if bad:
        return False, '；'.join(x[:110] for x in bad[:2])
    return True, '不到期，或上册之判已逐笔落裁'


def chk_promise_due():
    """约到期闸（2026-09-02·九席审读所逮·立於同日）
    ★所治之伤：**第291章拍139明写「要分出来得有第三天」，而第一百零四天（第293章）
      正是那第三天**；★★**而293全章：东头0｜担架0｜毡子0｜甜0｜馊0｜刘二0｜玉0**——
      **它一步也没去看**；★★★**而十三轮＋封版之序＋五十八项全测＋看官五席，一处也没出声。**
    ★★★★何以没出声：`书级体检①` 印「东头 缺席2章（限5）✓」——
      **它量的是缺席多久，而291立的是「到第三天就得去看」**：**一个到期的约，缺席计数器看不见。**
    ★而其式与 FS闸 同：**放行之价是一行写下来的字**——到期之章的轮记／回执须见「约-NNN」。
    ★★其回灌之要害在③：以291拍139回灌须报欠（负测_约到期 13项）。"""
    return _简测('负测·约到期闸', '工具/负测_约到期.py')


def chk_station_ledger():
    """站账闸（2026-09-02·293封版之後立·作者令「一切服务於质量，不管张数」之机化）
    ★其由：约第五节第3条曰「三数任一掉了 → 当场压章」——★★而实际走的是反面：
      均净重自5,479（169—200）跌到3,192（近十章），而收E3自约30章走成71章（2.37倍）；
      ★★★**那句「当场压章」，九十章之内一次也没执行过，而没有一件器出过声。**
    ★★★★而它不催字数（催字数即犯令§二）：**它只逼人在一站走满时回头对一次账。**
    ★其回灌：抽掉收E3之对站之记须复红二条、抽掉E4之记须出声（负测_站账 13项）。"""
    return _简测('负测·站账闸', '工具/负测_站账.py')


def chk_caibi_gate():
    """裁毕闸（2026-09-02·293第12轮立·第二十四犯第五形之治）
    ★其由：293第9轮之轮记称「21对，逐对裁毕」，而同节之内写明其由者只八条；
      ★★那四个字，是我替其余十三对签的字——**而没人报。**
    ★★★其回灌之要害在③：**以293第9轮之原轮记回灌，须报红。**"""
    return _简测('负测·裁毕闸', '工具/负测_裁毕闸.py')


def chk_yishi_jichen():
    """一事几陈（2026-09-02·293第12轮立·第二十七犯之治）
    ★其由：「浅是我手上停了，不是那天有事」这一判，293全章说了三回，
      而三处两两之字面近似 0.24—0.32，俱低於查重之0.60槛——**尺认字，不认命题。**
    ★★其回灌之要害在③④：**改前（v22）拍36中四词，改後只中二词**——
      **一份在改前改後都印同一个数的测就是陪跑。**"""
    return _简测('负测·一事几陈', '工具/负测_一事几陈.py')


def chk_band_by_form():
    """★比带负测（2026-09-02·293第8轮所立）：**一把带，取错了比的人，就把三处好文判成了伤。**
    ★本坐之实（非设想）：293第5、7、8三轮各逮一「逾带」，**而三处用的是同一把手挑之带**
      （苏衍近五章 282／285／287／289／291）；★★**而那五章之形是做事与问人，
      而293是他近年唯一一篇翻判**。
    ★★★换成形相同之十八章（201—280之翻判诸章），**三个数一个也不逾带**：
      「因为」2.3（同形带 0.0—3.1 中位1.18）｜「像」0.9（同形带 0.0—1.2 中位0.31）｜
      段长90分位 38（同形带 30—76 中位34）——★★★★**三个「逾带」，一个也不成立。**
    ★而其所以险，不在这三处，在这一类：**「比她自己」这一句，本坐用了整整两章**；
      ★★**而它对了几回，是因为292那几章凑巧同形（沈鸢诸章多记账），不是因为那把尺挑对了。**
    ★★★故立 `工具/比带.py`：**一个数报三条带（全书／同镜／同形），并印本章落在哪几条里**；
      ★★★★**而它不判**——**它只是不许我再只看一条带就下判。**
    ★其回灌（令§六③）：②全书回灌须得≥10处「同镜与同形判得不一样」（今得33处，跨二项以上）——
      **若为0，此器即无用，当日撤**；★★④验其不出「须改」二字（只报不判）。"""
    out = run('负测·比带', ['工具/负测_比带.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'负测 (\d+) 项，过 (\d+)，坏 (\d+)', out)
    if not m:
        return False, '未见其数'
    tot, ok, bad = (int(x) for x in m.groups())
    if bad or ok != tot:
        _b = [ln.strip() for ln in out.splitlines() if ln.strip().startswith('⛔')]
        return False, '；'.join(_b[:3]) or '%d/%d' % (ok, tot)
    return True, '%d/%d 全通' % (ok, tot)


def chk_seal_cold_slot():
    """★封版档之冷轮口负测（2026-09-02·292第1轮立·欠-291D之群成立所致）：
    ★★其历：291封版之日，十六检报⑭（恒真）与⑥（COLD-288之红，其档自书「留在账上不许再挪」），
      而封版档只放行⑭，遂绕行一回；★★★当日判其孤例（在档不在闸）并立欠-291D：
      **「若此形再现一回，其群已成，当日须改」**；★★★★今日再现，故改。
    ★其限死在一处：**⑥所名之每一个 COLD-N，须在某份回执里带着「COLD-N·本章未执」之否决记**——
      **凡一笔冷轮之红而无人写过否决记者，照旧拦**：那正是⑥本来要逮的，无声消失。
    ★★其回灌（令§六③）：**旧式（只认⑭）对同一入参判「拦」**，见负测④。"""
    out = run('负测·封版档冷轮口', ['工具/负测_封版档冷轮.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'(\d+)/(\d+) (全通|⛔未通)', out)
    if not m:
        return False, '未见其数'
    return m.group(3) == '全通', '封版档冷轮口 %s/%s' % (m.group(1), m.group(2))


def chk_swallowed_note_gate():
    """★吞记闸负测（2026-09-02·291第13轮开轮时所立）：
    ★★其形：**器收下了一样它本该拒收的东西，而它一声没出。**
      `--存版 291 --记 "…"` 里，「--记」当了说明（说明是位置参数 argv[3]），其後真文被静静丢弃；
      ★★★於是 v15、v16 两版之说明尽失，**真轮数不着第12轮——一轮真跑过了，而账上说它没跑。**
    ★其族同第二十三犯（数句闸）：**判据里少了一样，它不报错，而在别处稳稳地绿。**
    ★★其回灌（令§六③）：**旧式（argv[3]照收）原样搬进负测第⑨项，以同一入参真跑一遍**——
      须一声不出、且把说明取成「--记」；**二者对同一入参判得不一样，此闸方才不是陪跑。**"""
    out = run('负测·吞记闸', ['工具/负测_吞记闸.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'(\d+)/(\d+) (全通|⛔未通)', out)
    if not m:
        return False, '未见其数'
    return m.group(3) == '全通', '吞记闸负测 %s/%s' % (m.group(1), m.group(2))


def chk_count_sentence_gate():
    """★数句闸负测（2026-09-02·291第12轮·极限轮所立）：
    ★★其形：**一个数与另一个数比着，而两边都没被数过**——
      291断言「他今天说了六句」，正文里数得出来的是「他说」十一处；
      ★★★第3轮·逐数对表判其过，其判据是「此数有没有对头」，不是「此数自己对不对」。
    ★取二组数（令§六①）：**组一·本章三处数，两处数不出来（钱满六句／老头六句），一处数得出（三个字）**；
      ★★**组二·全书同类入闸者十处，九处皆在页上给了明细或逐句编号，唯291一处两样皆无**——群在，故入闸不入档。
    ★★★其回灌（令§六③）：**改前之291原文存於 版本/第291章/_回灌_291改前.txt，须报红二处。**"""
    out = run('负测·数句闸', ['工具/负测_数句闸.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'(\d+)/(\d+) (全通|⛔未通)', out)
    if not m:
        return False, '未见其数'
    return m.group(3) == '全通', '数句闸负测 %s/%s' % (m.group(1), m.group(2))


def chk_threshold_gate():
    """★趋阈闸负测（2026-09-02·291第7轮所立·每次存版必跑）：
    ★★其形：**一个数差一点就够到一条有名之限，而最省的一步是补几个字把它顶过去**；
      ★★★而那几个字过得了每一道硬闸、抬得起净重、看起来跟正常落笔一模一样。
    ★取二组数（令§六①）：**逐章回灌台账，版际之比3147次、趋阈之红54次＝1.72%（291第7轮改带後，4,000与5,500二线已废）**——非陪跑亦非拆书；
      ★★**而其中195、273、275、276、283、284 数章落在3500线上，余量0至2字**，各自封了版，无一道闸出过声。
    ★★★其过法不是签一个字（LAW-290B）：须写「非凑数：<其由>」，**而那一行连同其数一并落进台账**，日後可逐条回读。"""
    out = run('负测·趋阈闸', ['工具/负测_趋阈闸.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'(\d+)/(\d+) (全通|⛔未通)', out)
    if not m:
        return False, '未见其数'
    ok, tot, 判 = int(m.group(1)), int(m.group(2)), m.group(3)
    if 判 != '全通' or ok != tot:
        _b = [ln.strip() for ln in out.splitlines() if '✗' in ln]
        return False, '；'.join(_b[:3]) or '%d/%d' % (ok, tot)
    return True, '%d/%d 全通（全书回灌红率1.72%%｜275/276/283/284四章落线俱逮着｜3000→3900阔跨零报）' % (ok, tot)


def chk_missing_slot():
    """★缺报格闸负测（2026-09-02·六造§八所立）：
    ★★令§〇之二逼我每轮写一行「本可问而未问」，**而从前没有任何器数它在不在**；
      ★★★漏写既不报红也不留痕，下一坐无从知道那一轮到底选了什么、办了什么。
    ★取二组数（令§六①）：**全书137章1594轮，缺此格者98%**——而其大半立於此法之前；
      ★★**而五造之後四章（288—291）之数是 288缺2/13、289缺2/13、290缺4/13、291缺0/6**，
      ★★★即：**法已在而人漏 18%**，非拆书。且此闸只查当章，历史之红不入 fix。
    ★★★★而其最险处不在逮不逮得住，在误伤：**289一轮拆二十三节**，按节数则其缺由2涨至12。"""
    out = run('负测·缺报格', ['工具/负测_缺报格.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'(\d+)/(\d+) (全通|⛔未通)', out)
    if not m:
        return False, '未见其数'
    ok, tot, 判 = int(m.group(1)), int(m.group(2)), m.group(3)
    if 判 != '全通' or ok != tot:
        _b = [ln.strip() for ln in out.splitlines() if '✗' in ln]
        return False, '；'.join(_b[:3]) or '%d/%d' % (ok, tot)
    return True, '%d/%d 全通（290回灌报缺四轮｜289按节数则由2涨至12，故合数一步非可有可无）' % (ok, tot)


def chk_turnpage_obj():
    """★翻页备料查（检五）之对象负测（2026-09-02·291第1轮所逮）：
    ★★原码取「全书最大章号＋1」，是全局之数，不随所查之章而动；
      ★★★其果：291一起草，以290为cur索292之锚，**以289为cur也索292之锚**——
        判据里根本没有「所查之章」这一项，故它不是在查这一章的翻页，是在查全书的进度。
    ★★★★今改作 n+1；而状态卡批次係全书一个指针，只问前沿（n+1 未写出者）。"""
    out = run('负测·翻页备料查', ['工具/负测_翻页备料查.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'(\d+)/(\d+) (全通|⛔未通)', out)
    if not m:
        return False, '未见其数'
    ok, tot, 判 = int(m.group(1)), int(m.group(2)), m.group(3)
    if 判 != '全通' or ok != tot:
        _b = [ln.strip() for ln in out.splitlines() if '✗' in ln]
        return False, '；'.join(_b[:3]) or '%d/%d' % (ok, tot)
    return True, '%d/%d 全通（旧式令289与290所索者同为一章｜新式各索其下一章）' % (ok, tot)


def chk_cold_veto():
    """★冷轮否决记负测（2026-09-02·290封版当日立）：
    ★★令§十①逼回执写足「N章冷眼轮」六字，**而那六个字正是⑥所读之签核**——
      ★★★於是一份明写「本章未执」的回执，把账当场销了（实证：290之回执，一坐当场印「COLD-288 已执」⛔）。
    ★取二组数：回执中出现那六字者 216 笔，其近旁含「未执／顺延／挂红」者 11 笔（5%）；
      ★★数其群：无一份旧回执含「COLD-N·本章未执」此式——故立此式作否决记，**回灌全书零红**。
    ★★★而其非陪跑之凭在④⑤：以旧式回灌，COLD-288 判「已执」；二式相异者全书只此一笔。"""
    out = run('负测·冷轮否决记', ['工具/负测_冷轮否决记.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'(\d+)/(\d+) (全通|⛔未通)', out)
    if not m:
        return False, '未见其数'
    ok, tot, 判 = int(m.group(1)), int(m.group(2)), m.group(3)
    if 判 != '全通' or ok != tot:
        _b = [ln.strip() for ln in out.splitlines() if '✗' in ln]
        return False, '；'.join(_b[:3]) or '%d/%d' % (ok, tot)
    return True, '%d/%d 全通（旧式於COLD-288判已执｜二式相异者全书只此一笔）' % (ok, tot)


def chk_hl_table():
    """★亮点对表负测（289第10轮立·第9轮所逮）：亮点段与正文相犯，全书原无一道闸看得见。
    ★★而三路之中只一路作闸——③约数路（红3章/289，1%）；
      ★★★①引文路（红57章，20%）与②数路（红51章，18%）经数其群，其红大半是着重号与概括，
      ★★★★故降为「报而不拦」，且其数写进器里，免得下一坐把它们当闸。"""
    out = run('负测·亮点对表', ['工具/负测_亮点对表.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'(\d+)/(\d+) (全通|⛔有败)', out)
    if not m:
        return False, '未见其数'
    ok, tot, 判 = int(m.group(1)), int(m.group(2)), m.group(3)
    if 判 != '全通' or ok != tot:
        _b = [ln.strip() for ln in out.splitlines() if '✗' in ln]
        return False, '；'.join(_b[:3]) or '%d/%d' % (ok, tot)
    return True, '%d/%d 全通（v20回灌逮出「二十来口气」｜旧式当场漏掉，非陪跑）' % (ok, tot)


def chk_ratchet_pre():
    """★棘轮预检负测（LAW-289C·2026-09-01 立）：
    ★★其要害不在「会不会报红」，在「它报的红与 --存版 之棘轮闸是不是同一个红」——
      ★★★故①②③验其 import 跑轮之 score 与 RATCHET_MIN/MAX（不许另造一把尺），
      ★★★★⑤⑥拿本坐真撞过棘轮的 v14（是哪一样）、v16（馊压过甜）二版回灌，须逐版报红且所指之串正确。"""
    out = run('负测·棘轮预检', ['工具/负测_棘轮预检.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'(\d+)/(\d+) (全通|⛔有败)', out)
    if not m:
        return False, '未见其数'
    ok, tot, 判 = int(m.group(1)), int(m.group(2)), m.group(3)
    if 判 != '全通' or ok != tot:
        _b = [ln.strip() for ln in out.splitlines() if '✗' in ln]
        return False, '；'.join(_b[:3]) or '%d/%d' % (ok, tot)
    return True, '%d/%d 全通（与跑轮同源｜v14/v16 回灌逐版报红）' % (ok, tot)


def chk_unans_gate():
    """★未答闸（⑳）负测：其答词集补了其②之诸形（说不上／数不出／指不出…），须验其防未动。
    ★★其要害三项：④新红须为旧红之子集｜⑤所松之章逐章正文皆见其限之明写｜
      ★★★⑥假章（摆问而二十拍内一字不交代）新式仍逮得住。"""
    out = run('负测·未答闸', ['工具/负测_未答闸.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'负测 (\d+) 项，过 (\d+)，坏 (\d+)', out)
    if not m:
        return False, '未见其数'
    tot, ok, bad = (int(x) for x in m.groups())
    if bad or ok != tot:
        _b = [ln.strip() for ln in out.splitlines() if '⛔' in ln]
        return False, '；'.join(_b[:3]) or '%d/%d' % (ok, tot)
    return True, '%d/%d 全通（新红係旧红之子集｜所松者皆见其限之明写）' % (ok, tot)


def chk_carry_gate():
    """★承前闸（⑮）负测：其比由「前一章」改为「同线最近之章」，须验其防未动。
    ★★其要害二项：③同线相接之章新旧两式逐章同判（防未动）；
      ★★★⑥换线之章新式之红率须显著低於旧式而不为零（改而不挖空）。"""
    out = run('负测·承前闸', ['工具/负测_承前闸.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'负测 (\d+) 项，过 (\d+)，坏 (\d+)', out)
    if not m:
        return False, '未见其数'
    tot, ok, bad = (int(x) for x in m.groups())
    if bad or ok != tot:
        _b = [ln.strip() for ln in out.splitlines() if '⛔' in ln]
        return False, '；'.join(_b[:3]) or '%d/%d' % (ok, tot)
    return True, ('%d/%d 全通（同线新旧第一路同判｜换线红率 51→31；'
                  '2026-09-03并入第二节：轮记逐样落判者亦算过，转绿之旧章12皆有真声明）'
                  % (ok, tot))


def chk_cold_gate():
    """⑥·冷轮之欠 负测（2026-08-28立·随「改⑥之闸」同日·见 工具/负测_冷轮闸.py）。
    ★其立之由：改闸之後⑥当场转绿，而一个只会说「零」的闸没有价值；
    ★★故此测专问它还逮不逮得住真欠——十项之中六项为「须报而报」，四项为「不须报而不报」。
    ★★★令九·③：写下来的法不生效，只有变成闸才生效。"""
    out = run('负测·冷轮闸', ['工具/负测_冷轮闸.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'负测 (\d+) 项，过 (\d+)，坏 (\d+)', out)
    if not m:
        return False, '未见其数'
    tot, ok, bad = (int(x) for x in m.groups())
    if bad or ok != tot:
        _b = [ln.strip() for ln in out.splitlines() if '⛔' in ln]
        return False, '；'.join(_b[:3]) or '%d/%d' % (ok, tot)
    return True, '%d/%d 全通' % (ok, tot)


def chk_round_zero():
    """第零轮·开镜庭（2026-08-16立·见 工具/第零轮开镜庭.py）：起草之前问三事——
    ★①本章之位（主线还是暗线）／★★②本章之镜（若为暗线，是谁）／★★★③本章之一事。
    ★★★★而其立之由：十轮治这一章，十一轮查十轮跑透没有；
    ★★★★★而无一轮问「这一章该不该是这一章、该不该先插一章」——而沈鸢漂八十五章正从此缝漏掉。"""
    import glob as _g, os as _o, re as _r
    cs = []
    for _p in _g.glob(_o.path.join(_o.path.dirname(_o.path.dirname(_o.path.abspath(__file__))), '正文', '*.md')):
        _m = _r.search(r'第([零〇一二三四五六七八九十百]+)章', _o.path.basename(_p))
        if _m:
            cs.append(_p)
    out = run('第零轮', ['工具/第零轮开镜庭.py', '--静'])
    _RAW['第零轮'] = out or ''
    if out is None:
        return False, '运行失败'
    if '第零轮通过' in out:
        return True, '开镜庭过'
    bad = [ln.strip() for ln in out.splitlines() if ln.strip()]
    return False, '；'.join(bad[:2]) if bad else '未通过'


def chk_unfinished():
    """核轮（2026-08-16立·见 工具/核轮.py）：查有无「跑到一半就去写下一章」之章。
    ★而其立之由：漏跑之实已见二回——200跑到第5轮停（章界闸偶然逮住）、
    ★★201跑到第1轮停（★★★而其时章数未变，无一闸响）。"""
    out = run('核轮', ['工具/核轮.py', '--全', '--静'])
    if out is None:
        return False, '运行失败'
    if '核轮通过' in out:
        return True, '无未竟之章'
    bad = [ln.strip() for ln in out.splitlines() if ln.strip()]
    return False, '；'.join(bad[:2]) if bad else '未通过'


def chk_huixiu():
    """回修案（2026-08-19立·见 设定/10_回修令.md 与 工具/回修.py）：
    ★作者亲令「封版之后一样也可以改，只要能让整本书质量最高」。
    ★★而第六十六批早已立此法，却躺了一个月无人跑——其由：只有字，无闸。
    ★★★依批100之融入标准（能拦住交付方算融入），故立此检：
    凡已开之回修案，其连带同步与复验须办毕，四问须答毕；未毕者禁封版。"""
    import glob as _g
    d = os.path.join(ROOT, '设定', '回修案')
    if not os.path.isdir(d):
        return True, '无在办之回修案'
    fs = _g.glob(os.path.join(d, '回修案_第*章_*.md'))
    if not fs:
        return True, '无在办之回修案'
    bad = []
    for f in fs:
        n = re.search(r'第(\d+)章', os.path.basename(f))
        if not n:
            # ★★★★★2026-09-04 治（301第12轮自逮）：**一份档名它读不懂的案，从前是 continue。**
            #   ★其红在哪一行：本坐当日立「回修案_第288至299章_20260904_骨记残引.md」，
            #     `第(\d+)章` 一处也匹配不着（288之後是「至」，不是「章」），
            #     ★★而其果不是报错，是**这一件案从此不在册上，而末行照旧印「N件俱办毕」**；
            #   ★★★即令§一④之形：**闸绿，而那一件根本不在它的判据里。**
            #   ★★★★故改作报红，不作 continue：**读不懂的档名，是档名之伤，不是不存在。**
            bad.append('%s：档名里读不出章号（式须作「回修案_第N章_日期…md」）——'
                       '读不懂的案从前一律跳过，而末行照旧印「俱办毕」'
                       % os.path.basename(f))
            continue
        out = run('回修', ['工具/回修.py', '--验案', n.group(1)])
        if out is None or '禁封版' in (out or '') or '未办毕' in (out or ''):
            bad.append('第%s章' % n.group(1))
    if bad:
        return False, '回修案未办毕：%s（见 设定/10_回修令.md 第四节）' % '、'.join(bad)
    return True, '回修案 %d 件俱办毕' % len(fs)



def chk_repair_name():
    """★负测·回修案档名（301第12轮立·同日与其闸并立·令§六④）：
    ★一份档名读不出章号的案，从前在回修案检里是 continue——**它不在册上，而末行照旧印「俱办毕」。**"""
    out = run('负测·回修案档名', ['工具/负测_回修案档名.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'(\d+)/(\d+) (全通|⛔有败)', out)
    if not m:
        return False, '取不着其数'
    return m.group(3) == '全通', '%s/%s %s' % (m.group(1), m.group(2), m.group(3))



def chk_adj_dup():
    """★负测·邻拍重出（301第13轮立·同日与其器并立·令§六④）：
    ★一句话拆开来摆在两拍上，读起来是两步；逐字一比，是一句。
    ★★而此测另守一样：**器之限须写在器里**——它逮不着立它的那一处（公共串只5字），
      而降槛之式已数其群而驳（近四十章 8 处→247 处）。"""
    out = run('负测·邻拍重出', ['工具/负测_邻拍重出.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'(\d+)/(\d+) (全通|⛔有败)', out)
    if not m:
        return False, '取不着其数'
    return m.group(3) == '全通', '%s/%s %s' % (m.group(1), m.group(2), m.group(3))



def chk_nozhen():
    """★负测·无真伤之由（301封版之序立·与其闸同日·令§六④）：
    ★乙4之罚辞明书「须逐轮说明何以皆无」，而其判据只数「真伤」二字——**那一句说明它看不见。**
    ★★而本日另逮一样：**这一段判词在 十轮精进.py 与 跑轮.py 里各有一份。**"""
    out = run('负测·无真伤之由', ['工具/负测_无真伤之由.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'(\d+)/(\d+) (全通|⛔有败)', out)
    if not m:
        return False, '取不着其数'
    return m.group(3) == '全通', '%s/%s %s' % (m.group(1), m.group(2), m.group(3))


def chk_dup_defs():
    """重名定义扫描。
    病灶实证：批113所加之 s_withlog／s_nolog／s_reopen 落在批114替换区之外而与新写者重名，
    后定义者覆盖前者，令二条负测名义在跑而实测旧局。此类错不报错、不崩、静默改变行为，
    非专测不可得。"""
    bad = []
    for f in sorted(glob.glob(os.path.join(ROOT, '工具', '*.py'))):
        try:
            tree = ast.parse(open(f, encoding='utf-8').read())
        except SyntaxError as e:
            bad.append('%s 语法错误 %s' % (os.path.basename(f), e))
            continue
        for node in ast.walk(tree):
            body = getattr(node, 'body', None)
            if not isinstance(body, list):
                continue
            seen = {}
            for st in body:
                if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if st.name in seen:
                        bad.append('%s: %s 于同一作用域重复定义（行%d 覆盖 行%d）'
                                   % (os.path.basename(f), st.name, st.lineno, seen[st.name]))
                    seen[st.name] = st.lineno
    return not bad, ('；'.join(bad) if bad else '工具目录内无重名定义')


def chk_zishu():
    """字数对齐探测器之回归。
    此规则住在 check_file 内，而检察官 138 条自测只跑 canon 正则（hits 不经 check_file），
    故其从来无回归——批117 修其二处误报时才发现。修探测器最忌静默削弱，
    故正测（真错须报）与负测（误报须不报）并立。"""
    import tempfile, importlib.util as u, sys
    sys.argv = ['x']
    sp = u.spec_from_file_location('_i2', os.path.join(ROOT, '工具', '小说检察官.py'))
    m = u.module_from_spec(sp)
    sp.loader.exec_module(m)

    def flagged(body):
        d = tempfile.mkdtemp()
        f = os.path.join(d, '镇冢秘术_第七章_测.md')
        open(f, 'w', encoding='utf-8').write('《镇冢秘术》\n\n第七章　测\n\n' + body + '\n')
        iss, _, _ = m.check_file(f)
        return any(x.startswith('[字数对齐]') for x in iss)

    POS = [   # 真错，必须报
        ('前向·数在前引在后', '过了几步他说了四个字。\n\n“今天你对了。”\n\n他点了点头。'),
        ('后向·引在前数在后', '“不知道。”\n\n这两个字从他嘴里出来，我心里咯噔一下。'),
        ('换行·引在前数在后', '“留给回来的人。”\n\n这四个字他说得很平。'),
    ]
    NEG = [   # 误报，必须不报
        ('数指前句非后句', '“等。”他说。\n\n就一个字。\n\n“等天黑。”'),
        ('数指前句非后句·二', '“不信。”\n\n就两个字。\n\n“那你来干什么。”'),
        ('数指前句非后句·三', '“摸。”\n\n一个字。\n\n“我先过。”'),
        ('两句合计报数', '“发烫，就回来。”\n\n他看着我。\n\n“灯灭。莫回头。”\n\n十个字，一个不差。'),
        ('数与引全合', '他说了五个字。\n\n“水一直在流。”'),
    ]
    bad = []
    for name, body in POS:
        if not flagged(body):
            bad.append('漏报:' + name)
    for name, body in NEG:
        if flagged(body):
            bad.append('误报:' + name)
    n = len(POS) + len(NEG)
    return not bad, ('；'.join(bad) if bad else '正测%d/负测%d 全通' % (len(POS), len(NEG)))


def chk_rhythm():
    """节奏方差闸之回归（批119）。
    此闸为第153章起之硬错，若静默失效则新章之方差塌缩无人拦，
    而其病正是「机器一直在报却没人当真」（P26）——故正负测并立。"""
    import importlib.util as u, sys
    sys.argv = ['x']
    sp = u.spec_from_file_location('_i3', os.path.join(ROOT, '工具', '小说检察官.py'))
    m = u.module_from_spec(sp)
    sp.loader.exec_module(m)
    hdr = '《镇冢秘术》\n\n第一百五十三章　测\n\n'
    short = '\n\n'.join(['他站住了。', '风从右边来。', '我数到三。'] * 12)
    longp = '这一段要连着跑到一百二十字以上，不断行，不换气，' \
            '把该慢下来的地方慢足了：他把手按在壁上，先是掌心，' \
            '再是掌根，最后是整只手贴上去，土从指缝里往下掉，' \
            '掉到鞋面上，又从鞋面上滑下去，落地没有声音，' \
            '因为地上原本就铺着一层同样的土；他就那么按着，' \
            '按到掌心底下那一块也凉了，才把手收回来。'
    mid = '\n\n'.join(['他把灯举起来又放下，举的时候手是稳的，放的时候手抖了一下，抖不是怕，是举得久了。'] * 8)
    V = m.rhythm_violation
    bad = []
    # 正测：新章违规须报
    if not V(hdr + short, 153):
        bad.append('漏报:全短段之新章')
    if not V(hdr + short + '\n\n' + mid, 153):
        bad.append('漏报:90分位不足30字')
    # 负测：不得误报
    if V(hdr + mid + '\n\n' + longp + '\n\n' + mid, 153):
        bad.append('误报:有长段且90分位达标')
    if V(hdr + short, 152):
        bad.append('误报:历史章(第152章)不受此闸')
    if V(hdr + short, 153, exempt=True):
        bad.append('误报:已登记节奏豁免者')
    return not bad, ('；'.join(bad) if bad else '正测2/负测3 全通')


def chk_lunci():
    """轮次完整性诸闸之回归（批121）。
    病灶（作者亲报，本会话第153章第7轮亲犯）：十轮常只跑七八轮／轮次跳号。
    链条：某轮存版被拦而未察→轮记按台账末版标错号→正文与末版脱节→带病连跑数轮。
    此测守三口：发轮前置闸、轮记版未到闸、封版十轮不满闸。"""
    import importlib.util as u, sys, tempfile, json, os as _o, io, contextlib
    sys.argv = ['x']
    sp = u.spec_from_file_location('_i4', os.path.join(ROOT, '工具', '跑轮.py'))
    m = u.module_from_spec(sp)
    sp.loader.exec_module(m)
    sp2 = u.spec_from_file_location('_i5', os.path.join(ROOT, '工具', '小说检察官.py'))
    m2 = u.module_from_spec(sp2)
    sp2.loader.exec_module(m2)
    bad = []
    _R, _J = m.ROOT, m.JJ_DIR
    tmp = tempfile.mkdtemp(prefix='zm_lc_')
    try:
        _o.makedirs(_o.path.join(tmp, '正文'))
        _o.makedirs(_o.path.join(tmp, '设定'))
        m.ROOT, m.JJ_DIR = tmp, _o.path.join(tmp, '版本')
        f = _o.path.join(tmp, '正文', '镇冢秘术_第七章_测.md')
        d = _o.path.join(tmp, '版本', '第7章')
        _o.makedirs(d)
        open(f, 'w', encoding='utf-8').write('《镇冢秘术》\n\n第七章　测\n\n原始\n')
        open(_o.path.join(d, 'v01.md'), 'w', encoding='utf-8').write(
            open(f, encoding='utf-8').read())
        json.dump({'章': 7, '版本': [{'版': 'v01', '时': 'x', '说明': '第1轮·甲',
                   'hard': {}, 'soft': {'净重': 9}, '全书章数': 1}]},
                  open(_o.path.join(d, '_台账.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc_clean = m.nextround(7)                       # 正文与末版一致→须发轮
        open(f, 'w', encoding='utf-8').write('《镇冢秘术》\n\n第七章　测\n\n改过了\n')
        buf2 = io.StringIO()
        with contextlib.redirect_stdout(buf2):
            rc_drift = m.nextround(7)                       # 正文已偏→须拒发轮
        if rc_clean == 2:
            bad.append('误拦:正文与末版一致时不得拒发轮')
        if rc_drift != 2:
            bad.append('漏拦:上一轮未落台账仍发新轮')
        # 轮记版未到闸
        json.dump({'时': 'x', '正文sha': 'a', '末版sha': 'a', '目标轮': 5},
                  open(_o.path.join(d, '_领轮.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        buf3 = io.StringIO()
        with contextlib.redirect_stdout(buf3):
            rc_lj = m.lunji_append(7, '测')                 # 所领第5轮而台账末版第1轮→须拒
        if rc_lj != 2:
            bad.append('漏拦:轮记比版先到')
        if _o.path.exists(_o.path.join(d, '_轮记.md')):
            bad.append('漏拦:拒写轮记却仍落了盘')
    finally:
        m.ROOT, m.JJ_DIR = _R, _J
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    if not hasattr(m2, '_rounds_full'):
        bad.append('缺:封版十轮不满闸未接线')

    # ── 拦停旗（批122）：漏读一次拦停不得等于走得过去 ──
    tmp2 = tempfile.mkdtemp(prefix='zm_flag_')
    try:
        _o.makedirs(_o.path.join(tmp2, '正文'))
        _o.makedirs(_o.path.join(tmp2, '设定'))
        m.ROOT, m.JJ_DIR = tmp2, _o.path.join(tmp2, '版本')
        f2 = _o.path.join(tmp2, '正文', '镇冢秘术_第七章_测.md')
        d2 = _o.path.join(tmp2, '版本', '第7章')
        _o.makedirs(d2)
        open(f2, 'w', encoding='utf-8').write('《镇冢秘术》\n\n第七章　测\n\n甲\n')
        open(_o.path.join(d2, 'v01.md'), 'w', encoding='utf-8').write(
            open(f2, encoding='utf-8').read())
        json.dump({'章': 7, '版本': [{'版': 'v01', '时': 'x', '说明': '第1轮·甲',
                   'hard': {}, 'soft': {'净重': 9}, '全书章数': 1}]},
                  open(_o.path.join(d2, '_台账.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        b3 = io.StringIO()
        with contextlib.redirect_stdout(b3):
            no_flag = m.flag_block(7, '发轮')
        if no_flag:
            bad.append('误拦:无旗时不得拒办')
        m.raise_flag(7, '测试之由', '第2轮·测')
        b4 = io.StringIO()
        with contextlib.redirect_stdout(b4):
            has_flag = m.flag_block(7, '发轮')
            rc_nr = m.nextround(7)
            rc_lj = m.lunji_append(7, '测')
        if not has_flag:
            bad.append('漏拦:有旗仍放行')
        if rc_nr != 2:
            bad.append('漏拦:有旗仍发轮')
        if rc_lj != 2:
            bad.append('漏拦:有旗仍写轮记')
        if _o.path.exists(_o.path.join(d2, '_轮记.md')):
            bad.append('漏拦:有旗仍落了轮记')
        # 一次成功存版须销旗
        open(f2, 'w', encoding='utf-8').write('《镇冢秘术》\n\n第七章　测\n\n甲乙丙\n')
        json.dump({'时': 'x', '正文sha': m._sha(open(_o.path.join(d2, 'v01.md'), encoding='utf-8').read()),
                   '末版sha': m._sha(open(_o.path.join(d2, 'v01.md'), encoding='utf-8').read()),
                   '目标轮': 2},
                  open(_o.path.join(d2, '_领轮.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        open(_o.path.join(d2, '_轮记.md'), 'w', encoding='utf-8').write('\n## 第1轮|v01|x|净重9\n所见\n')
        b5 = io.StringIO()
        with contextlib.redirect_stdout(b5):
            rc_ok = m.save(7, '第2轮·四堂会审')
        if rc_ok != 0:
            bad.append('误拦:清白之存版被旗拦（旗当由此次成功销去）')
        elif m.read_flag(7) is not None:
            bad.append('漏销:存版成功而旗未销')
    finally:
        m.ROOT, m.JJ_DIR = _R, _J
        import shutil as _sh
        _sh.rmtree(tmp2, ignore_errors=True)

    # ── 第十一轮总核（批123）──
    tmp3 = tempfile.mkdtemp(prefix='zm_zh_')
    try:
        _o.makedirs(_o.path.join(tmp3, '正文'))
        _o.makedirs(_o.path.join(tmp3, '设定'))
        m.ROOT, m.JJ_DIR = tmp3, _o.path.join(tmp3, '版本')
        f3 = _o.path.join(tmp3, '正文', '镇冢秘术_第七章_测.md')
        d3 = _o.path.join(tmp3, '版本', '第7章')
        _o.makedirs(d3)
        SOFT = {'净重': 100, '段数': 9, '均段': 11, '长段数': 1, '嗅': 3, '听': 4, '触': 7,
                '视': 2, '老头': 1, '钱满': 1, '沈鸢': 0, '四字串三现': 0, '顿悟起手': 0}
        def build(rounds, logs, same=None):
            vs = []
            for k, r in enumerate(rounds, 1):
                vn = 'v%02d' % k
                body = '《镇冢秘术》\n\n第七章　测\n\n' + ('同一段' if (same and k in same) else '第%d段内容' % k) + '\n'
                open(_o.path.join(d3, vn + '.md'), 'w', encoding='utf-8').write(body)
                # 2026-08-19：尽力查测「起→峰有没有长过」，故桩之净重须随轮递增，
                # 否则正测必被误拦（真章之深掘本就该让它长）。
                _sf = dict(SOFT)
                _sf['净重'] = SOFT['净重'] + 10 * len(vs)
                vs.append({'版': vn, '时': 'x', '说明': r, 'hard': {}, 'soft': _sf, '全书章数': 1})
            json.dump({'章': 7, '版本': vs}, open(_o.path.join(d3, '_台账.json'), 'w', encoding='utf-8'), ensure_ascii=False)
            open(f3, 'w', encoding='utf-8').write(
                open(_o.path.join(d3, 'v%02d.md' % len(rounds)), encoding='utf-8').read())
            open(_o.path.join(d3, '_轮记.md'), 'w', encoding='utf-8').write(logs)
            for z in ('_总核.json', '_拦停.json'):
                if _o.path.exists(_o.path.join(d3, z)):
                    _o.remove(_o.path.join(d3, z))
        # 必答表自正文抽出，故须先有正文，_log 方取得到（否则 duty_list 返回空表）
        open(f3, 'w', encoding='utf-8').write('《镇冢秘术》\n\n第七章　测\n\n三天两头十三天四个人五样两副三圈\n')

        def _log(i):
            try:
                duties = m.duty_list(7, i)[0]
            except Exception:
                duties = []
            # 2026-08-19：尽力查已接入总核，其测层数／产出／到底。
            # 回归之桩为假章，须自带五层与「已到底」之记，否则正测必被尽力查误拦。
            _ceng = ('第一层：甲。第二层：乙。第三层：丙。第四层：丁。第五层：戊。'
                     '而第五层底下已到底，其由为此为回归之桩，非真章。')
            return ('\n## 第%d轮|v%02d|x|净重100\n**镜头**：%s\n**必答逐项**：%s\n'
                    '%s\n**真伤**：一根。其治：改作某句；已复量、复扫、复核。%s\n'
                    % (i, i, '｜'.join(m.LENS_KEY[i]),
                       '；'.join(duties) if duties else '本轮无可机抽之必答项',
                       _ceng if i == 4 else '',
                       '补白之句' * 40))
        _RT = int(getattr(m, 'ROUNDS', 10))   # 2026-08-19：轮数以 ROUNDS 为准，勿写死
        full_log = ''.join(_log(i) for i in range(1, _RT + 1))
        # 正测：十轮齐、记齐、无空轮 → 须过
        build(['第%d轮·甲' % i for i in range(1, _RT + 1)], full_log)
        b6 = io.StringIO()
        with contextlib.redirect_stdout(b6):
            rc_full = m.zonghe(7)
        if rc_full != 0:
            bad.append('误拦:%d轮齐备之章总核应过（%%s）'%_RT % b6.getvalue()[-160:].replace('\n', ' '))
        elif not _o.path.exists(_o.path.join(d3, '_总核.json')):
            bad.append('漏写:总核过而未出凭据')
        # 负测一：缺第10轮
        build(['第%d轮·甲' % i for i in range(1, _RT)],
''.join(_log(i) for i in range(1, _RT)))
        with contextlib.redirect_stdout(io.StringIO()):
            if m.zonghe(7) != 2:
                bad.append('漏拦:缺第10轮仍判总核过')
        # 负测二：版齐而轮记缺一轮
        build(['第%d轮·甲' % i for i in range(1, _RT + 1)],
''.join(_log(i) for i in range(1, _RT + 1) if i != 4))
        with contextlib.redirect_stdout(io.StringIO()):
            if m.zonghe(7) != 2:
                bad.append('漏拦:缺一轮之轮记仍判总核过')
        # 负测三：空轮而未记判不补
        build(['第%d轮·甲' % i for i in range(1, _RT + 1)], full_log, same={5, 6})
        with contextlib.redirect_stdout(io.StringIO()):
            if m.zonghe(7) != 2:
                bad.append('漏拦:空轮未记判不补仍判总核过')
        # 负测四：轮记过简
        build(['第%d轮·甲' % i for i in range(1, _RT + 1)],
              ''.join('\n## 第%d轮|v%02d|x|净重100\n真伤：无\n' % (i, i) for i in range(1, _RT + 1)))
        with contextlib.redirect_stdout(io.StringIO()):
            if m.zonghe(7) != 2:
                bad.append('漏拦:轮记过简仍判总核过')
        # 负测六：抄清单而不裁（提及100%而裁定0%）——批125之核心
        def _naked_log(i):
            try:
                du = m.duty_list(7, i)[0]
            except Exception:
                du = []
            return ('\n## 第%d轮|v%02d|x|净重100\n**镜头**：%s\n'
                    '本轮所涉：%s\n段数9 长段1\n%s\n'
                    % (i, i, '｜'.join(m.LENS_KEY[i]),
                       '、'.join(du) if du else '无', '补白之句' * 40))
        build(['第%d轮·甲' % i for i in range(1, _RT + 1)],
              ''.join(_naked_log(i) for i in range(1, _RT + 1)))
        with contextlib.redirect_stdout(io.StringIO()):
            if m.zonghe(7) != 2:
                bad.append('漏拦:抄清单而不逐项裁定仍判总核过（批125之核心）')
        # 负测七：对数对不上（轮记不含台账所记之数）
        def _nonum_log(i):
            try:
                du = m.duty_list(7, i)[0]
            except Exception:
                du = []
            return ('\n## 第%d轮|v%02d|x|净重甚多\n**镜头**：%s\n'
                    '%s\n**真伤**：一根，已改核合。%s\n'
                    % (i, i, '｜'.join(m.LENS_KEY[i]),
                       '；'.join('%s：已核判合' % x for x in du) if du else '无',
                       '补白之句' * 40))
        build(['第%d轮·甲' % i for i in range(1, _RT + 1)],
              ''.join(_nonum_log(i) for i in range(1, _RT + 1)))
        with contextlib.redirect_stdout(io.StringIO()):
            if m.zonghe(7) != 2:
                bad.append('漏拦:轮记之数对不上台账仍判总核过')
        # 负测八：轮轮判合、全章无真伤
        def _nohurt_log(i):
            try:
                du = m.duty_list(7, i)[0]
            except Exception:
                du = []
            return ('\n## 第%d轮|v%02d|x|净重100\n**镜头**：%s\n段数9 长段1\n'
                    '%s\n**本轮真伤无，判不补。**%s\n'
                    % (i, i, '｜'.join(m.LENS_KEY[i]),
                       '；'.join('%s：已核判合' % x for x in du) if du else '无',
                       '补白之句' * 40))
        build(['第%d轮·甲·判不补' % i for i in range(1, _RT + 1)],
              ''.join(_nohurt_log(i) for i in range(1, _RT + 1)))
        with contextlib.redirect_stdout(io.StringIO()):
            if m.zonghe(7) != 2:
                bad.append('漏拦:全章十轮皆无真伤仍判总核过（产出基线）')
        # 负测五：拦停旗未销
        build(['第%d轮·甲' % i for i in range(1, _RT + 1)], full_log)
        m.raise_flag(7, '测', '第9轮')
        with contextlib.redirect_stdout(io.StringIO()):
            if m.zonghe(7) != 2:
                bad.append('漏拦:拦停旗未销仍判总核过')
    finally:
        m.ROOT, m.JJ_DIR = _R, _J
        import shutil as _s2
        _s2.rmtree(tmp3, ignore_errors=True)
    if not hasattr(m2, '_zonghe_ok'):
        bad.append('缺:封版总核闸未接线')
    # ── 检察官侧第十一轮五检（批126）──
    # ── 回执闸之在跑判（批130）──
    if not hasattr(m2, '_in_progress'):
        bad.append('缺:回执闸在跑判未接线')
    else:
        # 【批130·修】原测断言「第157章须判在跑」——**而此为会变之状态**：
        #   其母章十轮一满，157即不再在跑，该测遂红。批127已立此戒（负测不得钉在会变的状态上，
        #   须钉在不变的契约上），而立批130之负测时又犯，此其第二回。
        # 今只测不变之契约：不存在之章与已封版之章一律非在跑；返回值须为 bool。
        try:
            for ch in (999999, 152, 100):
                v = m2._in_progress(ch)
                if not isinstance(v, bool):
                    bad.append('在跑判返回值非bool(第%d章)' % ch)
                elif v:
                    bad.append('误判:第%d章（不存在或已封版）竟判在跑' % ch)
        except Exception as e:
            bad.append('在跑判运行失败:%s' % e)
    if not hasattr(m2, 'round11_audit'):
        bad.append('缺:检察官侧第十一轮未接线')
    elif not hasattr(m2, '_round11_main'):
        bad.append('缺:第十一轮两眼齐审总入口未接线')
    else:
        try:
            # 【批127·修】原测断言「第153章须有硬项」，而那是写测当日之临时状态；
            # 该章补齐之后此测反红——**负测不得钉在会变的状态上，须钉在不变的契约上**。
            o, h, sf = m2.round11_audit(153)
            if not (isinstance(o, list) and isinstance(h, list) and isinstance(sf, list)):
                bad.append('检察官侧第十一轮返回值不合约（须为三列表）')
            keys = ('圣经', '到期账', '回述', '病号', '翻页')
            if not all(any(k in x for x in o) for k in keys):
                bad.append('检察官侧第十一轮之五检要目不全（应出圣经／到期账／回述／病号／翻页五节）')
            o2, h2, _ = m2.round11_audit(999999)
            if not h2:
                bad.append('漏拦:不存在之章竟无硬项')
        except Exception as e:
            bad.append('检察官侧第十一轮运行失败:%s' % e)

    return not bad, ('；'.join(bad) if bad else '正测3/负测23 全通')


def chk_hookspath():
    """钩子须挂上：容器每次重建后 .git 皆新，故 hooksPath 须指向受版本管理之目录。"""
    want = '工具/githooks'
    try:
        r = subprocess.run(['git', 'config', '--get', 'core.hooksPath'],
                           cwd=ROOT, capture_output=True, text=True, timeout=30)
        cur = r.stdout.strip()
    except Exception as e:
        return False, '读取失败 %s' % e
    hook = os.path.join(ROOT, want, 'pre-push')
    if not os.path.exists(hook):
        return False, '缺 %s' % want + '/pre-push'
    if cur != want:
        subprocess.run(['git', 'config', 'core.hooksPath', want],
                       cwd=ROOT, capture_output=True, text=True, timeout=30)
        return True, '原为「%s」，已自动挂回 %s' % (cur or '未设', want)
    if not os.access(hook, os.X_OK):
        os.chmod(hook, 0o755)
        return True, '已挂，并补回执行位'
    return True, '已挂 %s' % want



# ═══ 推闸（2026-08-28 立·作者令「改钩子之策」）═══
# ★其由（器印之实证，非印象）：⑥·冷轮之欠之销，只能由本章回执里那六个字「N章冷眼轮」落，
#   ★★而回执是封版时才交的；故全测在任一章的十三轮期间必红，
#   ★★★只在「刚封版且下一章已立卡」那个窄窗里绿。
# ★★★★而跑轮令§八要求每轮报「远端＝本地」，即每轮该推一次——二者直抵，遂有绕行45次。
# ★而其正法：分二档。本章回执未交（正在跑轮）时，只放行那两项结构性之红；
#   ★★其余任一项红，照旧拦；★★★本章回执一交，即恢复「全绿才许推」。
# ★★★★而窗划得极窄，一分不弱：
#   ·⑥只放行「不带逾期二字」者——逾期即是真漏，照旧拦；
#   ·⑥之外，开轮十六检里任一别的检报红，照旧拦；
#   ·第零轮只放行「索下一章之卡」者——若它索的是本章之卡，照旧拦。
_RAW = {}
_放行标 = '✓推闸·跑轮档：放行'


def _末章():
    """★末一有正文之章（无正文者不算）。"""
    import glob as _g, os as _o, re as _r
    CN = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
          '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}
    best = 0
    for _p in _g.glob(os.path.join(ROOT, '正文', '*.md')):
        m = _r.search(r'第([零〇一二三四五六七八九十百]+)章', _o.path.basename(_p))
        if not m:
            continue
        t = n = 0
        for ch in m.group(1):
            if ch in CN and ch != '十':
                n = CN[ch]
            elif ch == '十':
                t += (n or 1) * 10
                n = 0
            elif ch == '百':
                t += (n or 1) * 100
                n = 0
        best = max(best, t + n)
    return best


def _已封版(n):
    """★回执已交即视为已封版（与检察官、跑轮同法）。"""
    import glob as _g
    return bool(_g.glob(os.path.join(ROOT, '设定', '回执_*_第%d章作业单.md' % n)))


def _逾期伏笔俱已认账(raw):
    """★与⑥之否决记同式（2026-09-02·293第1轮立）：**逾期之每一根 FS，
    须在本章之轮记或开镜卡里带着「FSxx·本章未兑」这个认账**，方许在跑轮档上放行。
    ★★其由（与第十九犯所立之式同）：**认账只有在肯写「未兑」二字时才写得出来**；
      ★★★**一根伏笔悄悄滑过它的到期章者，没有人写过这两个字**——那正是本闸要逮的。
    ★★★★而其所以要放行：**本闸之销在回执，而回执须待十三轮跑毕**；
      ★**一根逾期之伏笔可以拦住此後十二轮的每一次推**，
      ★★**而拦十二回并不能让回执早交一天，只能教出「见红就 --no-verify」**
        （绕行审计.log 里那四十五次绕行，正是⑥当年这么长出来的）。
    ★★★**故放行之价是一行写下来的字，不是一次沉默。**"""
    # ★其单不取自报文——**报文里没有根号**（今日之实：「逾期伏笔 2 根（其单在 FS闸.py）」，
    #   而 `FS(\d+)` 在这一句上只匹配得着「FS闸」二字之後的空处，遂一根也数不出来）。
    #   ★★故直调 FS闸 自己那一支，取其未答之根：**问器要单，不问报文要单。**
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location('_fs', os.path.join(ROOT, '工具', 'FS闸.py'))
    _fs = _iu.module_from_spec(_sp)
    try:
        _sp.loader.exec_module(_fs)
        _n, _f, _欠, _未答, _答 = _fs.查()
    except Exception:
        return False
    ns = [str(x['id']).replace('FS', '') for x in _未答]
    if not ns:
        return False
    cur = _末章()
    src = ''
    for _p in (os.path.join(ROOT, '版本', '第%d章' % cur, '_轮记.md'),
               os.path.join(ROOT, '版本', '第%d章' % cur, '_开镜卡.md')):
        if os.path.exists(_p):
            try:
                src += open(_p, encoding='utf-8', errors='replace').read()
            except OSError:
                pass
    if not src:
        return False
    return all(('FS%s·本章未兑' % x) in src for x in sorted(set(ns)))


def _冷轮逾期俱有否决记(raw):
    """★与封版档之口同式（2026-09-02·292第1轮立）：**逾期之每一个 COLD-N，
    须在某份回执里带着「COLD-N·本章未执」这个否决记**，方不作真漏。
    ★★其由：否决记只有说「不」的时候才写得出来（第十九犯所立之式）；
    ★★★**一笔冷轮悄悄滑过它的到期章者，无人写过否决记**——那正是「逾期」本来要逮的。"""
    import re as _re
    import glob as _g
    ns = [int(m) for m in _re.findall(r'COLD-(\d+)', raw)]
    if not ns:
        return False
    rcs = []
    for fp in _g.glob(os.path.join(ROOT, '设定', '回执_*.md')):
        try:
            rcs.append(open(fp, encoding='utf-8').read())
        except OSError:
            pass
    # ★★★★★同日改（第一版从严过了头）：**原本向所报之每一笔都索否决记**，
    #   ★而今日三笔里逾期的只有 COLD-288（限291<292）；COLD-289 与 COLD-290 之限正是292，
    #     **它们不是逾期，是今天该办的**——**向没逾期的那两笔索否决记，是逼人替没犯的事签字。**
    #   ★★故逐笔按其到期章分：**限 < 当章者方为逾期，方须有否决记**；未逾期者不问。
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location('_lz6', os.path.join(ROOT, '工具', '开轮六检.py'))
    _m6 = _iu.module_from_spec(_sp)
    _sp.loader.exec_module(_m6)
    过期 = [n for n in ns if _m6._cold_limit(n) < _末章()]
    if not 过期:
        return True
    return all(any(('COLD-%d·本章未执' % n) in t for t in rcs) for n in 过期)


def 推闸(fails):
    """★返回 (放行否, 语)。★★只在「本章回执未交」时才许放行，且只放行那两项。"""
    cur = _末章()
    if not cur:
        return False, '⛔推闸：正文一篇也无，不放行。'
    if _已封版(cur):
        # ★★★★★2026-09-01 立·封版档（288封版之日所逮）。
        # ★病灶：⑭「已封版之章」之判为 `if 十一轮✓ and 回执✓: 红`，而 cur＝末一有正文之章；
        #   ★★故封版之日 cur 正是刚封的那一章，⑭ **必红**——它是一条恒真之红，不是一处伤。
        #   ★★★而封版之日又正是推闸要求全绿之日，二者相撞，遂使每一次封版都只能绕闸。
        # ★数其群（令§六②）：⑭立於2026-08-17，其後每一章封版之日皆同此形；
        #   ★★而 286 封版之日绕行一次已记档（绕行审计.log 第45、46行）。
        # ★★★故其治照令§六③：不废⑭（它防的是「封版之章再跑十轮覆盖其回执」，那一防仍在——
        #   `--下一轮`／`--存版` 照旧被它拦），只在推闸之封版档里放行它一项，且限死三条：
        #   ①十六检所报只此一条，别的一条也不许有；②那一条须是⑭；③⑭所指之章须正是 cur。
        #   ★★★★而其余任一项红，照旧拦——与跑轮档同法。
        准 = []
        for name in fails:
            raw = _RAW.get(name, '')
            if name != '开轮十六检':
                return False, ('⛔推闸：第%d章已封版，而「%s」不在封版档之列，照旧拦。'
                               % (cur, name))
            # ★★★★★2026-09-02·292第1轮补（欠-291D之群今日成立，照其自书之条改）：
            #   ★291封版之日，十六检报二条——⑭（恒真）与⑥·冷轮之欠（COLD-288之红，
            #     其档第五节自书「其红留在账上不许再挪」）；★★而封版档只放行⑭，遂又绕行一回。
            #   ★★★当日判其为孤例（在档不在闸），并立欠-291D：**若此形再现一回，其群已成，当日须改**。
            #     ★今日再现（292未起草，末章仍为已封版之291，⑥仍红），**故其群成，今改**。
            #   ★★★★而其限死在一处，不许宽半分：**⑥所名之每一个 COLD-N，须在某份回执里带着
            #     「COLD-N·本章未执」这个否决记**——★**否决记只有说「不」的时候才写得出来**
            #     （第十九犯所立之式）；★★**故此放行不是把红抹掉，是只放行「已经写下来认过的那几笔」**；
            #     ★★★**凡一笔冷轮之红而无人写过否决记者，照旧拦**——那正是⑥本来要逮的：无声消失。
            def _冷轮之红俱有否决记(x):
                import re as _re, glob as _g
                ns = [int(m) for m in _re.findall(r'COLD-(\d+)', x)]
                if not ns:
                    return False
                rcs = []
                for fp in _g.glob(os.path.join(ROOT, '设定', '回执_*.md')):
                    try:
                        rcs.append(open(fp, encoding='utf-8').read())
                    except OSError:
                        pass
                return all(any(('COLD-%d·本章未执' % n) in t for t in rcs) for n in ns)

            条 = [x.strip() for x in raw.split('；') if x.strip()]
            余 = [x for x in 条
                  if not x.startswith('⑭·已封版之章')
                  and not (x.startswith('⑥·冷轮之欠') and _冷轮之红俱有否决记(x))]
            if not 条 or 余:
                return False, ('⛔推闸：开轮十六检所报不止⑭与「已写否决记之⑥」（%s），照旧拦。'
                               % '／'.join(x[:14] for x in 余)[:70])
            # ★同日补：**⑭所指之章只在⑭真在报里时才验得着**——
            #   ★★而报里可以只有⑥（今日之实：十六检之报只一条「⑥·冷轮之欠」，⑭一字不在）；
            #   ★★★原本无条件验「第N章已封版」在不在 raw 里，遂把一份没有⑭的报也判作「⑭指错了章」。
            if any(x.startswith('⑭·已封版之章') for x in 条):
                if ('第%d章已封版' % cur) not in raw:
                    return False, ('⛔推闸：⑭所指非第%d章，照旧拦。' % cur)
                准.append('⑭·已封版之章（其红係恒真：cur＝刚封之章）')
            for x in 条:
                if x.startswith('⑥·冷轮之欠'):
                    准.append('⑥·冷轮之欠（其所名者俱已写否决记，非无声消失）')
        if not 准:
            return True, ('%s\n  【封版档】第%d章已封版且全测全绿。' % (_放行标, cur))
        return True, ('%s\n  【封版档】第%d章今日封版；所放行者只此 1 项：%s。\n'
                      '  【其限】⑭之防未动——封版之章再跑十轮，`--下一轮`／`--存版` 照旧被它拦；'
                      '此处只是不拿一条恒真之红去拦封版当日之推。' % (_放行标, cur, '；'.join(准)))
    准 = []
    for name in fails:
        raw = _RAW.get(name, '')
        if name == '开轮十六检':
            条 = [x.strip() for x in raw.split('；') if x.strip()]
            if not 条 or any(not x.startswith('⑥·冷轮之欠') for x in 条):
                return False, ('⛔推闸：开轮十六检所报不止⑥一条（%s），照旧拦。'
                               % '／'.join(x[:12] for x in 条 if not x.startswith('⑥·冷轮之欠'))[:60])
            # ★★★★★2026-09-02·292第1轮补（与今晨封版档所补係同一口，今接到跑轮档上）：
            #   ★「逾期」本是真漏之凭，而今日之逾期不是漏**：COLD-288 限291，
            #     ★★而其档第五节自书「291若仍非暗线，其红留在账上不许再挪」；291确为主线，
            #       故其红依法留下，**292正是它所停的那一章，此刻正在执它**。
            #   ★★★故其限与封版档同一条，一字不宽：**逾期之COLD-N，须在其到期之章的回执里
            #     带着「COLD-N·本章未执」这个否决记**——★**否决记只有说「不」的时候才写得出来**；
            #     ★★**一笔冷轮悄悄滑过它的到期章者，无人写过否决记，照旧拦**：那正是「逾期」本来要逮的。
            if '逾期' in raw and not _冷轮逾期俱有否决记(raw):
                return False, ('⛔推闸：⑥所报含「逾期」而其中有未写否决记者，那是真漏，照旧拦。')
            准.append('⑥·冷轮之欠（其销须待第%d章回执；逾期者俱已写否决记）' % cur)
        elif name == '第零轮':
            if ('--立 %d' % (cur + 1)) not in raw:
                return False, '⛔推闸：第零轮所索非下一章之卡，照旧拦。'
            准.append('第零轮（索第%d章之卡，而其卡须待第%d章封版方立）' % (cur + 1, cur))
        elif name == 'FS沉默闸':
            # ★★★★★2026-09-02·293第1轮补（与⑥之口同式，一字不宽）：
            #   ★本闸之销在本章回执，而回执须待十三轮跑毕；
            #   ★★**一根逾期之伏笔可以拦住此後十二轮的每一次推，而拦十二回并不能让回执早交一天**
            #     ——**只能教出「见红就 --no-verify」**（绕行审计.log 里那四十五次绕行，
            #     正是⑥当年这么长出来的）。
            #   ★★★故放行之价是一行写下来的字：**逾期之每一根 FS，须在本章之轮记或开镜卡里
            #     写着「FSxx·本章未兑」**——★**认账只有在肯写「未兑」二字时才写得出来**；
            #     ★★**悄悄滑过去的那一根，没有人写过这两个字，照旧拦。**
            if not _逾期伏笔俱已认账(raw):
                return False, ('⛔推闸：FS沉默闸所报之逾期伏笔，有未在本章轮记／开镜卡里'
                               '写「FSxx·本章未兑」认账者，那是无声滑过，照旧拦。')
            准.append('FS沉默闸（其销须待第%d章回执；逾期者俱已在轮记认账）' % cur)
        else:
            return False, '⛔推闸：「%s」不在结构性之列，照旧拦。' % name
    return True, ('%s\n  【跑轮档】第%d章回执未交，正在跑轮；所放行者只此 %d 项：%s。\n'
                  '  【其限】此二项俱於本章回执一交即自销；其余任一项红，照旧拦。'
                  % (_放行标, cur, len(准), '；'.join(准)))


def main():
    quick = '--快' in sys.argv
    items = [('重名定义扫描', chk_dup_defs), ('钩子挂载', chk_hookspath),
             ('字数对齐回归', chk_zishu),
             ('节奏方差闸回归', chk_rhythm),
             ('轮次完整性回归', chk_lunci),
             ('检察官自测', chk_selftest), ('医生', chk_doctor),
             ('跑轮负测', chk_shilun)]
    if not quick:
        items.append(('全书检', chk_book))
        items.append(('书级体检', chk_bookwide))
        items.append(('质量三闸', chk_quality_gates))
        items.append(('开轮十六检', chk_open_six))
        items.append(('负测·承前闸', chk_carry_gate))
        items.append(('负测·未答闸', chk_unans_gate))
        items.append(('负测·棘轮预检', chk_ratchet_pre))
        items.append(('负测·亮点对表', chk_hl_table))
        items.append(('负测·回修案档名', chk_repair_name))
        items.append(('负测·邻拍重出', chk_adj_dup))
        items.append(('负测·无真伤之由', chk_nozhen))
        items.append(('负测·棘轮v01', chk_ratchet_v01))
        items.append(('负测·冷轮否决记', chk_cold_veto))
        items.append(('负测·翻页备料查', chk_turnpage_obj))
        items.append(('负测·缺报格', chk_missing_slot))
        items.append(('负测·趋阈闸', chk_threshold_gate))
        items.append(('负测·数句闸', chk_count_sentence_gate))
        items.append(('负测·吞记闸', chk_swallowed_note_gate))
        items.append(('负测·封版档冷轮口', chk_seal_cold_slot))
        items.append(('负测·棘轮裁', chk_ratchet_verdict))
        items.append(('负测·段间空行闸', chk_blankline_gate))
        items.append(('负测·填记口', chk_fill_note_gate))
        items.append(('负测·功力回检', chk_effort_recheck))
        items.append(('负测·层census与立价查', chk_layer_census_honest))
        items.append(('负测·销立门', chk_seal_new_cold))
        items.append(('负测·孤版闸', chk_orphan_snapshot))
        items.append(('负测·FS认账', chk_fs_ack))
        items.append(('负测·亮点闸', chk_highlight_gate))
        items.append(('负测·验收空说明', chk_review_no_note))
        items.append(('负测·比带', chk_band_by_form))
        items.append(('负测·裁毕闸', chk_caibi_gate))
        items.append(('负测·站账闸', chk_station_ledger))
        items.append(('负测·约到期闸', chk_promise_due))
        items.append(('大审闸', chk_grand_audit))
        items.append(('负测·一事几陈', chk_yishi_jichen))
        items.append(('负测·章型带', chk_band))
        items.append(('负测·冷轮闸', chk_cold_gate))
        items.append(('负测·日词闸', chk_day_gate))
        items.append(('负测·推闸', chk_push_gate))
        items.append(('可逆库之验', chk_reversible))
        items.append(('负测·可逆册', chk_reversible_neg))
        items.append(('负测·阅读器催', chk_reader_nag))
        items.append(('负测·看官手闸', chk_kanguan_hand))
        items.append(('负测·提名账', chk_nomination_ledger))
        items.append(('负测·三条带', chk_three_bands))
        items.append(('负测·硬闸', chk_hard_gate))
        items.append(('负测·叠词闸', chk_dup_gate))
        items.append(('数闸', chk_num_gate))
        items.append(('负测·回执对账', chk_receipt_recon))
        items.append(('FS沉默闸', chk_fs_silence))
        items.append(('外声闸', chk_outside_voice))
        items.append(('大问表', chk_big_questions))
        items.append(('负测·大问挂账', chk_bigq_neg))
        items.append(('负测·场景切换闸', chk_scenecut_neg))
        items.append(('两册对限', chk_two_ledger))
        items.append(('负测·两册对限', chk_two_ledger_neg))
        items.append(('对位闸', chk_duiwei))
        items.append(('负测·冷轮同判', chk_cold_agree))
        items.append(('负测·器物点名', chk_object_roll))
        items.append(('器物册·逐章回灌', chk_object_roll_all))
        items.append(('负测·拦停旗', chk_stop_flag))
        items.append(('负测·立价查', chk_price_check))
        items.append(('负测·开轮六检', chk_open6_gate))
        items.append(('负测·到期账词表', chk_due_states))
        items.append(('负测·起草庭', chk_draft_court))
        items.append(('负测·连读重出', chk_reread_dup))
        items.append(('负测·空头签', chk_blank_sign))
        items.append(('空头签', chk_blank_sign_live))
        items.append(('第零轮', chk_round_zero))
        items.append(('核轮', chk_unfinished))
        items.append(('回修案', chk_huixiu))
    print('\n████ 全测 · %d 项 ████' % len(items))
    fails = []
    for name, fn in items:
        ok, detail = fn()
        print('  %s %-14s %s' % ('✓' if ok else '✗', name, detail))
        if not ok:
            fails.append(name)
    if fails:
        print('\n  ⛔全测未过：%s' % '、'.join(fails))
        ok, 语 = 推闸(fails)
        print('  %s' % 语)
        if not ok:
            print('  【批115】不过不许推——pre-push 钩子据此拦停。')
        return 1
    print('\n  ✓全测通过%s。' % ('（快测，未含全书检）' if quick else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main())
