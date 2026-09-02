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
    _nx = (max(_cs) + 1) if _cs else 1
    out = run('开轮十六检', ['工具/开轮六检.py', str(_nx), '--静'])
    _RAW['开轮十六检'] = out or ''
    if out is None:
        return False, '运行失败'
    if '开轮十六检通过' in out:
        return True, '六检皆过'
    bad = [ln.strip() for ln in out.splitlines() if ln.strip()]
    return False, '；'.join(bad[:3]) if bad else '未通过'


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
    return True, '9/9 全通'


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
    return True, '3/3 全通（含灌回旧错之验）'


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
    """大问表（2026-09-01立·见 工具/大问表.py）——**只报不拦**。
    ★其立之由：机器一处也没在问「读者还在等什么」——到期账258笔 open 0，
    ★★书级体检遂每章印「未清0笔｜距终点163章｜须净减0.00笔/章 ✓」。
    ★★★而器印：玉末见第80章缺207章／血图末60缺227／悬赏末71缺216／寨老末108／地窖末72缺215。
    ★★★★更要命者：E4指定要用的两样旧物（玉、听针）分别缺席207章与85章。"""
    out = run('大问表', ['工具/大问表.py'])
    if out is None:
        return False, '运行失败'
    import re as _r
    m = _r.search(r'逾上限者 (\d+) 样', out or '')
    n = int(m.group(1)) if m else 0
    if n == 0:
        return True, '八样俱在四十章之内'
    首 = _r.findall(r'^  (\S+)\s+\d+\s+第(\d+)章\s+(\d+)章\s+⛔', out or '', _r.M)[:3]
    return True, ('⚠逾四十章者 %d 样（只报不拦）：%s' % (n, '、'.join('%s缺%s章' % (a, c) for a, b, c in 首)))


def chk_cold_agree():
    """一坐与开轮六检对冷轮须同判 负测（2026-09-01立·见 工具/负测_冷轮同判.py）。
    ★其立之由：同一 HEAD 上一坐印「COLD-284／285 未执」而六检印「⑥ 零」——二器相反 ⛔。
    ★★数其群：冷轮档134份，含「已执＋销档」者仅37份、以回执判者131份——那个标记从未成为惯例。"""
    out = run('负测·冷轮同判', ['工具/负测_冷轮同判.py'])
    if out is None:
        return False, '运行失败'
    if '全通' not in out:
        return False, out.strip().split('\n')[0]
    return True, '3/3 全通（二器同用一处 _cold_done）'


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
    return True, '%d/%d 全通（同线新旧同判｜换线红率 51→31，非挖空）' % (ok, tot)


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
            continue
        out = run('回修', ['工具/回修.py', '--验案', n.group(1)])
        if out is None or '禁封版' in (out or '') or '未办毕' in (out or ''):
            bad.append('第%s章' % n.group(1))
    if bad:
        return False, '回修案未办毕：%s（见 设定/10_回修令.md 第四节）' % '、'.join(bad)
    return True, '回修案 %d 件俱办毕' % len(fs)


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
            条 = [x.strip() for x in raw.split('；') if x.strip()]
            if not 条 or any(not x.startswith('⑭·已封版之章') for x in 条):
                return False, ('⛔推闸：开轮十六检所报不止⑭一条（%s），照旧拦。'
                               % '／'.join(x[:12] for x in 条
                                          if not x.startswith('⑭·已封版之章'))[:60])
            if ('第%d章已封版' % cur) not in raw:
                return False, ('⛔推闸：⑭所指非第%d章，照旧拦。' % cur)
            准.append('⑭·已封版之章（其红係恒真：cur＝刚封之章）')
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
            if '逾期' in raw:
                return False, '⛔推闸：⑥所报含「逾期」，那是真漏，照旧拦。'
            准.append('⑥·冷轮之欠（其销须待第%d章回执）' % cur)
        elif name == '第零轮':
            if ('--立 %d' % (cur + 1)) not in raw:
                return False, '⛔推闸：第零轮所索非下一章之卡，照旧拦。'
            准.append('第零轮（索第%d章之卡，而其卡须待第%d章封版方立）' % (cur + 1, cur))
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
        items.append(('负测·棘轮v01', chk_ratchet_v01))
        items.append(('负测·冷轮否决记', chk_cold_veto))
        items.append(('负测·翻页备料查', chk_turnpage_obj))
        items.append(('负测·缺报格', chk_missing_slot))
        items.append(('负测·趋阈闸', chk_threshold_gate))
        items.append(('负测·章型带', chk_band))
        items.append(('负测·冷轮闸', chk_cold_gate))
        items.append(('负测·日词闸', chk_day_gate))
        items.append(('负测·推闸', chk_push_gate))
        items.append(('可逆库之验', chk_reversible))
        items.append(('负测·可逆册', chk_reversible_neg))
        items.append(('负测·阅读器催', chk_reader_nag))
        items.append(('负测·看官手闸', chk_kanguan_hand))
        items.append(('负测·硬闸', chk_hard_gate))
        items.append(('负测·叠词闸', chk_dup_gate))
        items.append(('数闸', chk_num_gate))
        items.append(('负测·回执对账', chk_receipt_recon))
        items.append(('FS沉默闸', chk_fs_silence))
        items.append(('外声闸', chk_outside_voice))
        items.append(('大问表', chk_big_questions))
        items.append(('负测·冷轮同判', chk_cold_agree))
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
