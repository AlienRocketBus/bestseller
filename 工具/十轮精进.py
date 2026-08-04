#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
十轮精进机制（批102立法／批103并入检察官）

**本文件是库，不是命令面。**
作者只说两句话：「续」→ 检察官 --开拍；「挑刺」→ 检察官 --验收（自动带存版＋棘轮闸＋满十轮横评）。
下列 CLI 仅供机器自检与负测，日常不用：
    python3 工具/十轮精进.py --存版 94 "第三轮·四堂会审"
    python3 工具/十轮精进.py --横评 94

立法要点：并行十版会丢弃已修好的真伤，故改为串行累积；
但每轮必存版打分，任何硬项劣于历史最优即棘轮闸拦停，末轮十版横评择优。
"""
import os
import re
import sys
import json
import glob
import datetime
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JJ_DIR = os.path.join(ROOT, '版本')
CN = {'零': 0, '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4,
      '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}


def chap_num(path):
    m = re.search(r'第([零〇一二三四五六七八九十百]+)章', os.path.basename(path))
    if not m:
        return -1
    s = m.group(1)
    total, num = 0, 0
    for ch in s:
        if ch in CN:
            num = CN[ch]
        elif ch == '十':
            total += (num or 1) * 10
            num = 0
        elif ch == '百':
            total += (num or 1) * 100
            num = 0
    return total + num


def find_chapter(n):
    for f in sorted(glob.glob(os.path.join(ROOT, '正文', '*.md'))):
        if chap_num(f) == n:
            return f
    return None


def paths(n):
    d = os.path.join(JJ_DIR, '第%d章' % n)
    return d, os.path.join(d, '_台账.json')


def body_of(txt):
    prose = txt.split('【本章亮点】')[0]
    return re.sub(r'^.*?第.+?章[^\n]*\n', '', prose, count=1, flags=re.S)


def score(txt):
    """机器可测之十七项。硬项须为0；量项供横评比对。"""
    body = body_of(txt)
    hl = txt[txt.find('【本章亮点】'):] if '【本章亮点】' in txt else ''
    sents = re.split(r'(?<=[。！？…])', txt)
    paras = [re.sub(r'\s', '', x) for x in body.split('\n') if x.strip()]
    lens = [len(x) for x in paras] or [0]

    def cnt(pat, s=body):
        return len(re.findall(pat, s))

    seen = {}
    for i in range(len(body) - 3):
        k = body[i:i + 4]
        if re.match(r'^[\u4e00-\u9fa5]{4}$', k):
            seen[k] = seen.get(k, 0) + 1
    rep3 = sum(1 for v in seen.values() if v >= 3)
    epi = sum(1 for x in paras
              if re.match(r'^(我忽然|我这才|我心里|我明白|我看出|我先以为|我在心里)', x))

    hard = {
        '破折': txt.count('—'),
        '半角逗': txt.count(','),
        '半角引号': txt.count('"'),
        '五逗句': sum(1 for s in sents if s.count('，') >= 5),
        '英文': len(re.findall(r'[A-Za-z]', txt)),
        '章号入正文': len(re.findall(r'[一二三四五六七八九十百]+章', body)),
        '禁抖': body.count('抖'),
        '永禁词': sum(body.count(w) for w in ['哆嗦', '骊山', '僵尸', '点亮']),
        '段间空行病': len(re.findall(r'。\n(?!\n)[^\n]', txt)),
        '亮点段破折': hl.count('—'),
        '亮点段五逗': sum(1 for s in re.split(r'(?<=[。！？…])', hl) if s.count('，') >= 5),
        '亮点段半角': hl.count(',') + hl.count('"'),
    }
    soft = {
        '净重': len(re.sub(r'\s', '', body)),
        '段数': len(paras),
        '均段': sum(lens) // max(len(lens), 1),
        '最长段': max(lens),
        '长段数': sum(1 for x in lens if x >= 90),
        '嗅': cnt(r'味|气味|鼻|闻'),
        '听': cnt(r'听|响|声|叫|吠'),
        '触': cnt(r'凉|温|烫|硬|软|摸|按|贴'),
        '视': cnt(r'灯|光|看|眼|见'),
        '老头': cnt('老头'),
        '钱满': cnt('钱满'),
        '沈鸢': cnt('沈鸢'),
        '四字串三现': rep3,
        '顿悟起手': epi,
    }
    return hard, soft



# ══════ 术语裸奔检测（ENG-TERM·批105）══════
# 立法：专名首现须带解释，不得裸奔。近四十字内须含解释锚（是／叫／门里管这个叫／就是／指的是等）。
TERMS = ['长明', '安点', '半拍', '衔木', '见壳记位不动', '不呼名', '血印', '测点',
         '合玉', '拓片', '稳楼', '记号', '数道', '同拍']
ANCHORS = ['是', '叫', '就是', '指的是', '门里', '意思', '＝', '＝', '所谓']


def term_check(txt, prev_text=''):
    """返回本章首现且四十字内无解释锚之术语。prev_text＝此前各章正文，用于判定是否首现。"""
    body = body_of(txt)
    naked = []
    for w in TERMS:
        if w in prev_text:
            continue  # 前章已解释过，非首现
        i = body.find(w)
        if i < 0:
            continue
        win = body[max(0, i - 40):i + 40]
        if not any(a in win for a in ANCHORS):
            naked.append(w)
    return naked


# ══════ 并发闸（批107·2026-07-30 立法）══════
# 立法：两路以上写作流同写一仓时，双绿闸与棘轮闸只对"当前文件"负责，
# 拦不住"另一路刚改过而我不知道"。故立此闸：每次开拍／验收前，先查仓库是否被别路动过。
# 【批108·修】指纹须按写作流分档：共用一档时，别路跑存版亦刷新基线，本闸遂被抹平。
# 流号取自环境变量 ZM_STREAM（未设则以 会话起始HEAD 之短号为号，落盘后不再变）。
def _stream_id():
    sid = os.environ.get('ZM_STREAM', '').strip()
    if sid:
        return re.sub(r'[^A-Za-z0-9_-]', '', sid)[:24] or 'anon'
    # 【批109·再修】后备档不得置于仓库内：仓内之档两路皆可读，二流遂同号，指纹重归共用而本闸再被抹平。
    # 故后备档移出仓库，落于本机 HOME，随会话／容器而异；无则当场生成一个随机号并落盘。
    marker = os.path.join(os.path.expanduser('~'), '.zm_stream')
    if os.path.exists(marker):
        try:
            sid = open(marker, encoding='utf-8').read().strip()
            if sid:
                return sid
        except Exception:
            pass
    import uuid
    sid = 'S' + uuid.uuid4().hex[:8]
    try:
        open(marker, 'w', encoding='utf-8').write(sid)
    except Exception:
        return 'anon'
    return sid


def _fp_path():
    return os.path.join(JJ_DIR, '_并发指纹_%s.json' % _stream_id())


def _git(*args):
    import subprocess
    try:
        r = subprocess.run(['git'] + list(args), cwd=ROOT,
                           capture_output=True, text=True, timeout=30)
        return r.stdout.strip()
    except Exception:
        return ''


def concurrency_check(quiet=False):
    """返回 (是否检出别路改动, 报告文本)。并更新指纹。"""
    head = _git('rev-parse', 'HEAD')
    if not head:
        return False, '  ⚠并发闸：非 git 仓库或 git 不可用，本闸跳过。'
    os.makedirs(JJ_DIR, exist_ok=True)
    rec = {}
    FP = _fp_path()
    if os.path.exists(FP):
        try:
            rec = json.load(open(FP, encoding='utf-8'))
        except Exception:
            rec = {}
    lines = ['  ── 并发闸（批107·批108修） ──', '   本流号：%s' % _stream_id()]
    found = False
    if not rec.get('head'):
        lines.append('   ⚠指纹缺失（首次或被清），本次无法与上次比对——不等于无别路提交。已建档，下次起可比。')
    elif rec['head'] == head:
        lines.append('   ✓无别路提交（HEAD 与上次一致）。')
    else:
        found = True
        rng = '%s..%s' % (rec['head'], head)
        log = _git('log', '--pretty=%h %an %s', rng)
        files = _git('diff', '--name-only', rng)
        lines.append('   ⚠检出别路提交！自上次本闸记录以来，仓库已前进：')
        for x in [l for l in log.split('\n') if l.strip()][:8]:
            lines.append('     · ' + x[:96])
        if files:
            fl = [f for f in files.split('\n') if f.strip()]
            lines.append('   ⚠涉及文件 %d 个：' % len(fl))
            for f in fl[:10]:
                lines.append('     · ' + f)
        lines.append('   **处方**：先读别路所改之处再落笔；若与本轮拟改同段，须先并轨，不得直接覆写。')
    dirty = _git('status', '--porcelain')
    dn = len([l for l in dirty.split('\n') if l.strip()]) if dirty else 0
    if dn:
        # 【批112·修】工作区脏是本路自身之噪声，每跑必响则真信号被淹（原闸失效第二因）。
        # 故降为一行提示，不参与拦停判定；拦停只认 HEAD 前进。
        lines.append('   ℹ工作区未提交改动 %d 处（含本路自身之改，非撞车凭据）。' % dn)
    rec['head'] = head
    rec['时'] = datetime.datetime.now().strftime('%m-%d %H:%M')
    json.dump(rec, open(FP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    txt = '\n'.join(lines)
    if not quiet:
        print(txt)
    return found, txt   # found ＝ HEAD 已前进（真撞车），不含工作区脏

# 棘轮方向：min＝越小越好，max＝越大越好
RATCHET_MIN = ('四字串三现', '顿悟起手')
RATCHET_MAX = ('嗅', '沈鸢')


# 【批112·立｜立法理由已由作者当面订正】四闸——不认人，只认"磁盘之账与我脑中之认知对不对得上"。
#
# 【订正】本闸初立时执笔断为"二路并发撞车"（151章台账 v01—v03 与 v04—v09 分属两段，
#   而执笔对后六轮全无记忆）。作者澄清：**全程只有一个对话、一个执笔**。
#   那六轮是同一执笔所作，只是其往来已被上下文压缩冲掉。
#   故真病为 P22 断层续手病：执笔之认知落后于磁盘实况，而按过期认知续手。
#   连带存疑：批107起"另一路·并发协作"诸记（101章为首）多半为同型误判；
#   其上所立之并发设施（ZM_STREAM 分档、_并发指纹_*.json）建于未经证实之前提，留而不用。
#
# 【做法恰对，理由说错，故闸留】旧闸（批107—109）失效有三，皆实测：
#   ①只比 git HEAD，而改动只写工作区未提交时 HEAD 不动，遂报"无别路提交"；
#   ②concurrency_check 的返回值被 save() 丢弃，是打印机不是闸（"只喷字的，等于没做"）；
#   ③流号靠 ZM_STREAM 分档，而本项目约定每次调用皆冠 ZM_STREAM=streamA-cli，二流同号，分档自废。
# 故四闸一律不依赖提交、不依赖流号、不依赖工作区脏否（脏是自噪声），只用确定性状态差。
#
# 【归属戒律】不得由"我不记得"推出"不是我"。凡无记忆之改动，先按"己作而失忆"处理，
#   跑 --对表 核实后再定；不得据此新立并发设施。
def _rel(path):
    return os.path.relpath(path, ROOT).replace(os.sep, '/')


def _git_raw(*args):
    import subprocess
    try:
        r = subprocess.run(['git'] + list(args), cwd=ROOT,
                           capture_output=True, text=True, timeout=30)
        return r.stdout if r.returncode == 0 else None
    except Exception:
        return None


def drift_of(n, receipts, src, txt):
    """【批112·闸五】封版后漂移哨。
    回执已交＝该章已封版；其工作区正文若与 HEAD 所存不同，即封版之后又被改过。
    此闸补的是四闸之盲区：四闸只在存版时拦，而正文早在存版之前就被改了。
    返回 (drifted, lines)。非 git／未入库者一律不判漂移（宁可不报，不可误报）。"""
    if not receipts:
        return False, []
    head = _git_raw('show', 'HEAD:%s' % _rel(src))
    if head is None:
        return False, ['   ℹ漂移哨：该章尚未入库或 git 不可用，本哨跳过。']
    if head.strip() == txt.strip():
        return False, ['   ✓漂移哨：已封版之正文与 HEAD 一致，封版后未被改动。']
    a = len([c for c in head if not c.isspace()])
    b = len([c for c in txt if not c.isspace()])
    return True, [
        '   ⛔漂移哨：第%d章回执已交（已封版），而工作区正文与 HEAD 不同。' % n,
        '     全文字数（含亮点段，非正文净重）HEAD %d → 工作区 %d（差%+d）。' % (a, b, b - a),
        '     封版之后的改动须走回补／定案并记因；若系误改，跑 --还原 %d 确认 复原。' % n]


def _receipts_of(n):
    return sorted(glob.glob(os.path.join(ROOT, '设定', '回执_*_第%d章作业单.md' % n)))


def _round_of(note):
    m = re.match(r'\s*第\s*(\d+)\s*轮', note or '')
    return int(m.group(1)) if m else None


def _book_chapters():
    return len([p for p in glob.glob(os.path.join(ROOT, '正文', '*.md')) if chap_num(p)])


def gates(n, note, ledger, chapters_now, receipts, reopen='', force='', same_as_last=False):
    """闸一至闸三之纯函数（可负测）。闸四·验轮在 duibiao。返回 (halt, lines)。"""
    lines, halt = [], False
    vs = ledger.get('版本', [])
    r = _round_of(note)

    # 闸一·回执闸：回执已交＝十轮已闭。此后只许回补／定案（说明不以"第N轮"起），不许再报新轮。
    if receipts and r is not None and not reopen:
        halt = True
        lines.append('   ⛔回执闸：第%d章回执已交（%s），十轮已闭。'
                     % (n, os.path.basename(receipts[-1])))
        lines.append('     本次说明报「第%d轮」＝在已封版之章上重开轮次。' % r)
        lines.append('     若确须重开，置 ZM_REOPEN="理由" 再跑；回补／定案请勿以「第N轮」起头。')

    # 闸二·轮次单调闸：轮次只许持平或前进，不许倒退。
    done = [_round_of(x.get('说明', '')) for x in vs]
    done = [x for x in done if x]
    if r is not None and done and r < max(done) and not reopen:
        halt = True
        last = vs[-1]
        lines.append('   ⛔轮次闸：台账已跑到第%d轮（末版 %s「%s」%s），本次报第%d轮，轮次倒退。'
                     % (max(done), last.get('版', ''), last.get('说明', ''),
                        last.get('时', ''), r))
        lines.append('     多半是自己已推进而记不得（P22断层续手），仍按旧认知落笔——先读末版再定。')

    # 闸三·章界闸：自上次存版以来全书章数变了＝别路拆了章或续了章，脚下的地已经动了。
    prev_ch = None
    for x in reversed(vs):
        if isinstance(x.get('全书章数'), int):
            prev_ch = x['全书章数']
            break
    if prev_ch is not None and chapters_now != prev_ch and not force:
        halt = True
        lines.append('   ⛔章界闸：上次存版时全书%d章，现为%d章。'
                     % (prev_ch, chapters_now))
        lines.append('     章数变动多半来自拆章／续章，本章之界与净重基线俱已不同，不得按旧认知续改。')
        lines.append('     若系本路方才拆章／续章，置 ZM_FORCE="拆章 N→N+N1" 记因后再跑；')
        lines.append('     若不知情，则是自己失忆而地已动（P22），须先对表认路。')

    # 闸六·空轮闸（防假跑第1条）：正文与末版逐字相同＝本轮零改动，却要记一版。
    if same_as_last and not force:
        halt = True
        lines.append('   ⛔空轮闸：正文与末版逐字相同，本轮零改动。')
        lines.append('     记一版空轮＝台账上多一个跑过的样子，而实无一刀，日后横评择优必被它带偏。')
        lines.append('     若确为「本轮审毕判不补」，请以非「第N轮」之说明存版（如「第N轮·判不补·记因」），')
        lines.append('     或置 ZM_FORCE="判不补之由" 明记。')

    if not halt:
        lines.append('   ✓四闸（回执／轮次／章界／空轮）全通。')
    else:
        lines.append('   **处方**：先跑 --对表 %d 读末版与回执，再决定并轨或让路。' % n)
    return halt, lines


def rounds_state(ledger):
    """返回 (已跑真轮集合, 缺轮列表)。真轮＝说明以「第N轮」起者。"""
    rs = set()
    for x in ledger.get('版本', []):
        r = _round_of(x.get('说明', ''))
        if r:
            rs.add(r)
    return rs, [i for i in range(1, 11) if i not in rs]


def duibiao(n):
    """开轮前对表：末版、回执、当前实况一屏看全。"""
    d, led = paths(n)
    print('\n███ 对表 · 第%d章 ███' % n)
    src = find_chapter(n)
    if src:
        txt = open(src, encoding='utf-8').read()
        body = body_of(txt)
        ls = [l for l in body.split('\n') if l.strip()]
        print('  正文：%s' % os.path.relpath(src, ROOT))
        print('  净重%d｜全书%d章' % (len([c for c in body if not c.isspace()]),
                                     _book_chapters()))
        if ls:
            print('  首句：%s' % ls[0][:60])
            print('  末句：%s' % ls[-1][:60])
    else:
        print('  ✗未找到第%d章正文' % n)
    rc = _receipts_of(n)
    print('  回执：%s' % ('、'.join(os.path.basename(x) for x in rc) if rc else '未交'))
    if src:
        _, dl = drift_of(n, rc, src, open(src, encoding='utf-8').read())
        for l in dl:
            print(l)
    if os.path.exists(led):
        lg = json.load(open(led, encoding='utf-8'))
        vs = lg.get('版本', [])
        print('  台账共%d版，末三版：' % len(vs))
        for x in vs[-3:]:
            print('    · %s %s 「%s」净重%s'
                  % (x.get('版', ''), x.get('时', ''), x.get('说明', ''),
                     x.get('soft', {}).get('净重', '?')))
        rs, miss = rounds_state(lg)
        print('  真轮：%d/10%s' % (len(rs), '' if not miss else
              '｜缺 ' + '、'.join('第%d轮' % i for i in miss)))
        # 【批112·闸四】封版凭据之验：回执已交而真轮未满＝有轮跑了却未存版，
        # 该轮既未过棘轮闸、亦无快照可回退，回执之"十轮跑毕"遂无凭据。
        if rc and miss:
            print('  ⛔验轮闸：回执已交，而真轮缺 %s——'
                  % '、'.join('第%d轮' % i for i in miss))
            print('     该轮无版可查：未过棘轮闸，亦无快照可回退，回执所称十轮跑毕无凭据。')
            print('     处方：补存该轮之版（说明以「第N轮」起），或在回执写明该轮并入他轮并记因。')
    else:
        print('  台账：无')
    return 0


def huanyuan(n, confirm=''):
    """自 HEAD 复原某章正文（误改封版之章时用）。须显式带「确认」二字。"""
    src = find_chapter(n)
    if not src:
        print('  ✗未找到第%d章正文' % n)
        return 1
    head = _git_raw('show', 'HEAD:%s' % _rel(src))
    if head is None:
        print('  ✗该章尚未入库或 git 不可用，无从复原。')
        return 1
    cur = open(src, encoding='utf-8').read()
    if cur.strip() == head.strip():
        print('  ✓第%d章正文与 HEAD 一致，无须复原。' % n)
        return 0
    a = len([c for c in cur if not c.isspace()])
    b = len([c for c in head if not c.isspace()])
    print('\n███ 还原 · 第%d章 ███' % n)
    print('  全文字数（含亮点段）工作区 %d → HEAD %d' % (a, b))
    if confirm.strip() != '确认':
        print('  ⛔未确认，未改动任何文件。')
        print('     确要复原请跑：python3 工具/十轮精进.py --还原 %d 确认' % n)
        print('     （复原将丢弃工作区对该章之全部改动，不可撤销）')
        return 2
    bak = src + '.漂移备份'
    open(bak, 'w', encoding='utf-8').write(cur)
    open(src, 'w', encoding='utf-8').write(head)
    print('  ✓已复原至 HEAD；工作区原文另存为 %s' % os.path.basename(bak))
    return 0


# 【批113·立】轮记——每轮之所见须落盘。
# 病因（实证）：105／106／143／151四章皆「跑到第9轮，缺第10轮」，丢的永远是最后一轮；
#   第10轮为最重之一turn（收官减法＋器物总账＋拆章＋写回执），正是上下文最满、最易压缩之刻。
#   存版只存文本与数字，不存「这一轮看见了什么」；压缩一来，那一部分就没了，
#   下一轮遂无从承前，而执笔尚不自知（P22断层续手）。
# 故立轮记：一轮一录，落盘即不怕忘。轮记在，则「一次跑几轮」这个问题自然消解——
#   任何一轮之边界皆成安全重启点，压缩至多损一轮。
LENS_FALLBACK = {
    1: '感官庭', 2: '四堂会审', 3: '挑刺王终读（逐数对表）', 4: '升华庭（招式比对）',
    5: '在场庭＋内面庭', 6: '内心庭', 7: '时序＋节奏＋留白', 8: '跨章复审',
    9: '收官减法轮', 10: '收官轮（器物总账＋逐段生死）'}


def lens_table():
    """各轮惯用镜头：自全书台账取历史众数，取不到则用兜底表。"""
    from collections import Counter, defaultdict
    tab = defaultdict(Counter)
    for f in glob.glob(os.path.join(JJ_DIR, '第*章', '_台账.json')):
        try:
            d = json.load(open(f, encoding='utf-8'))
        except Exception:
            continue
        for x in d.get('版本', []):
            m = re.match(r'第\s*(\d+)\s*轮[·．、]?\s*(.*)', x.get('说明', ''))
            if not m:
                continue
            nm = re.split(r'[：:]', m.group(2))[0].strip()
            if nm:
                tab[int(m.group(1))][nm] += 1
    out = {}
    for r in range(1, 11):
        out[r] = tab[r].most_common(1)[0][0] if tab[r] else LENS_FALLBACK[r]
    return out


def _lunji_path(n):
    return os.path.join(paths(n)[0], '_轮记.md')


def lunji_append(n, text):
    """append 一条轮记。轮次自台账末版推得。"""
    d, led = paths(n)
    os.makedirs(d, exist_ok=True)
    r, ver, jz = '?', '', ''
    if os.path.exists(led):
        vs = json.load(open(led, encoding='utf-8')).get('版本', [])
        if vs:
            last = vs[-1]
            ver = last.get('版', '')
            jz = last.get('soft', {}).get('净重', '')
            m = _round_of(last.get('说明', ''))
            if m:
                r = str(m)
    head = '\n## 第%s轮｜%s｜%s｜净重%s\n' % (
        r, ver, datetime.datetime.now().strftime('%m-%d %H:%M'), jz)
    with open(_lunji_path(n), 'a', encoding='utf-8') as f:
        f.write(head + text.rstrip() + '\n')
    print('  ✓轮记已落盘：%s（第%s轮）' % (os.path.relpath(_lunji_path(n), ROOT), r))
    return 0


def nextround(n):
    """开轮之总入口：告诉执笔下一轮该跑哪一轮、镜头为何、前几轮看见了什么。
    前几轮之所见取自磁盘轮记，故压缩冲掉记忆亦不碍。"""
    print(duibiao_brief(n))
    d, led = paths(n)
    lg = json.load(open(led, encoding='utf-8')) if os.path.exists(led) else {'版本': []}
    rs, miss = rounds_state(lg)
    tab = lens_table()
    print('  ── 下一轮 ──')
    if not miss:
        print('   ✓十轮已满，请跑 --横评 %d 定案。' % n)
    else:
        nx = miss[0]
        print('   **该跑第%d轮：%s**' % (nx, tab[nx]))
        if len(miss) > 1:
            print('   其后未跑：%s' % '、'.join('第%d轮(%s)' % (i, tab[i]) for i in miss[1:]))
        print('   【铁则】只跑「下一个未跑之轮」，不认作者所报之号——号会漂，台账不会。')
    lp = _lunji_path(n)
    if os.path.exists(lp):
        t = open(lp, encoding='utf-8').read()
        blocks = [b for b in t.split('\n## ') if b.strip()]
        print('  ── 前轮所见（自磁盘轮记，共%d条，录末二条）──' % len(blocks))
        for b in blocks[-2:]:
            for line in ('## ' + b).strip().split('\n')[:9]:
                print('   ' + line[:100])
    else:
        print('  ── 前轮所见：无轮记（本章尚未起轮，或起于轮记立法之前）──')
    return 0


def duibiao_brief(n):
    """精简对表：供检察官逐章封版门内嵌，三五行给出「磁盘之实况」。
    其价值在于：执笔每章必看封版门，遂不必倚赖「记得去跑 --对表」——
    而「记得」正是 P22 断层续手病所毁之器官。"""
    out = []
    src = find_chapter(n)
    rc = _receipts_of(n)
    d, led = paths(n)
    out.append('  ── 开轮对表（批112·磁盘为准，非记忆为准） ──')
    out.append('   回执：%s｜全书%d章'
               % ('已交（十轮已闭，只许回补／定案）' if rc else '未交', _book_chapters()))
    if os.path.exists(led):
        lg = json.load(open(led, encoding='utf-8'))
        vs = lg.get('版本', [])
        rs, miss = rounds_state(lg)
        last = vs[-1] if vs else {}
        out.append('   台账：共%d版，末版 %s「%s」%s'
                   % (len(vs), last.get('版', ''), last.get('说明', ''), last.get('时', '')))
        out.append('   真轮：%d/10%s' % (len(rs), '' if not miss else
                   '｜缺 ' + '、'.join('第%d轮' % i for i in miss)))
        if rc and miss:
            out.append('   ⛔验轮闸：回执已交而真轮缺 %s，「十轮跑毕」无凭据。'
                       % '、'.join('第%d轮' % i for i in miss))
    else:
        out.append('   台账：无（本章尚未起轮）')
    if src:
        dr, dl = drift_of(n, rc, src, open(src, encoding='utf-8').read())
        out.extend(dl)
    return '\n'.join(out)


def selftest():
    """契约负测：每闸须能拦（正测）且不误拦（负测）。"""
    ok = fail = 0

    def chk(name, cond):
        nonlocal ok, fail
        if cond:
            ok += 1
        else:
            fail += 1
            print('  ✗负测失败：' + name)

    L = lambda vs: {'章': 1, '版本': vs}
    v = lambda note, ch=None: ({'版': 'v01', '时': '', '说明': note,
                                'hard': {}, 'soft': {'净重': 100}}
                               | ({'全书章数': ch} if ch else {}))

    # 闸一·回执闸
    chk('回执闸须拦已封版之章上报新轮',
        gates(1, '第4轮·升华庭', L([v('第10轮·收官')]), 5, ['设定/回执_x_第1章作业单.md'])[0])
    chk('回执闸不得误拦回补（说明非第N轮起）',
        not gates(1, '终版回补·器物', L([v('终版回补')]), 5, ['设定/回执_x_第1章作业单.md'])[0])
    chk('回执闸不得误拦未交回执之章',
        not gates(1, '第4轮·升华庭', L([v('第3轮·校对')]), 5, [])[0])
    chk('回执闸须认 ZM_REOPEN 之豁免',
        not gates(1, '第4轮·升华庭', L([v('第10轮·收官')]), 5,
                  ['设定/回执_x_第1章作业单.md'], reopen='作者令重开')[0])

    # 闸二·轮次单调闸
    chk('轮次闸须拦倒退', gates(1, '第4轮·甲', L([v('第9轮·乙')]), 5, [])[0])
    chk('轮次闸不得误拦持平', not gates(1, '第9轮·甲', L([v('第9轮·乙')]), 5, [])[0])
    chk('轮次闸不得误拦前进', not gates(1, '第10轮·甲', L([v('第9轮·乙')]), 5, [])[0])
    chk('轮次闸不得误拦首版', not gates(1, '第1轮·甲', L([]), 5, [])[0])

    # 闸三·章界闸
    chk('章界闸须拦章数增（别路拆章）',
        gates(1, '第4轮·甲', L([v('第3轮·乙', ch=151)]), 152, [])[0])
    chk('章界闸须拦章数减', gates(1, '第4轮·甲', L([v('第3轮·乙', ch=152)]), 151, [])[0])
    chk('章界闸不得误拦章数不变',
        not gates(1, '第4轮·甲', L([v('第3轮·乙', ch=151)]), 151, [])[0])
    chk('章界闸不得误拦旧台账（无全书章数字段）',
        not gates(1, '第4轮·甲', L([v('第3轮·乙')]), 151, [])[0])
    chk('章界闸须认 ZM_FORCE 之豁免',
        not gates(1, '第4轮·甲', L([v('第3轮·乙', ch=151)]), 152, [], force='已对表')[0])

    # 全清之常态
    chk('三闸俱通时不得拦', not gates(1, '第4轮·甲', L([v('第3轮·乙', ch=151)]), 151, [])[0])

    # 151实录回放：当日之真况须被拦下
    chk('151实录回放须拦（回执已交＋轮次倒退＋章数增·同一执笔失忆续手）',
        gates(151, '第4轮·升华庭', L([v('第3轮·校对庭逐数对表', ch=151)]), 152,
              ['设定/回执_20260804_第151章作业单.md'])[0])

    # 闸四·验轮
    chk('验轮须认满十轮', rounds_state(L([v('第%d轮·x' % i) for i in range(1, 11)]))[1] == [])
    chk('验轮须报缺第10轮', rounds_state(L([v('第%d轮·x' % i) for i in range(1, 10)]))[1] == [10])
    chk('验轮不得把回补当真轮', rounds_state(L([v('终版回补')]))[0] == set())
    chk('151实录回放·验轮须报缺第10轮',
        rounds_state(L([v('第%d轮·x' % i) for i in range(1, 10)]))[1] == [10])

    # 闸六·空轮闸
    chk('空轮闸须拦零改动之轮',
        gates(1, '第4轮·甲', L([v('第3轮·乙', ch=5)]), 5, [], same_as_last=True)[0])
    chk('空轮闸不得误拦有改动之轮',
        not gates(1, '第4轮·甲', L([v('第3轮·乙', ch=5)]), 5, [], same_as_last=False)[0])
    chk('空轮闸须认 ZM_FORCE 之豁免',
        not gates(1, '第4轮·甲', L([v('第3轮·乙', ch=5)]), 5, [],
                  force='审毕判不补', same_as_last=True)[0])

    # ── 端到端负测：在临时 ROOT 上真跑 save()，验其确实拦停且零写入 ──
    import tempfile, shutil, io, contextlib, subprocess
    global ROOT, JJ_DIR
    _R, _J = ROOT, JJ_DIR

    def e2e(name, mk, note, want_rc):
        """mk(tmp) 布置场景；跑 save；验返回码与「版本目录零增长」。"""
        nonlocal ok, fail
        global ROOT, JJ_DIR
        tmp = tempfile.mkdtemp(prefix='zm_e2e_')
        try:
            os.makedirs(os.path.join(tmp, '正文'))
            os.makedirs(os.path.join(tmp, '设定'))
            ROOT, JJ_DIR = tmp, os.path.join(tmp, '版本')
            mk(tmp)
            before = sorted(glob.glob(os.path.join(tmp, '版本', '**', '*'), recursive=True))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = save(7, note)
            after = sorted(glob.glob(os.path.join(tmp, '版本', '**', '*'), recursive=True))
            good = (rc == want_rc)
            if want_rc == 2:
                # 拦停之轮：除自动建出的空目录外，不得多出任何文件
                nf = [x for x in after if x not in before and os.path.isfile(x)]
                good = good and not nf
                if nf:
                    print('  ✗端到端：拦停却写入了 %s' % nf)
            if good:
                ok += 1
            else:
                fail += 1
                print('  ✗端到端失败：%s（rc=%s，期望%s）' % (name, rc, want_rc))
        finally:
            ROOT, JJ_DIR = _R, _J
            shutil.rmtree(tmp, ignore_errors=True)

    def _ch(tmp, body='一二三四五六七八九十'):
        open(os.path.join(tmp, '正文', '镇冢秘术_第七章_测.md'), 'w',
             encoding='utf-8').write('《镇冢秘术》\n\n第七章　测\n\n' + body + '\n')

    def _led(tmp, vs):
        d = os.path.join(tmp, '版本', '第7章')
        os.makedirs(d, exist_ok=True)
        json.dump({'章': 7, '版本': vs}, open(os.path.join(d, '_台账.json'), 'w',
                  encoding='utf-8'), ensure_ascii=False)
        return d

    def s_receipt(tmp):
        _ch(tmp)
        _led(tmp, [v('第9轮·乙', ch=1)])
        open(os.path.join(tmp, '设定', '回执_x_第7章作业单.md'), 'w',
             encoding='utf-8').write('x')

    def s_clean(tmp):
        _ch(tmp)

    def s_empty(tmp):
        _ch(tmp)
        d = _led(tmp, [v('第3轮·乙', ch=1)])
        open(os.path.join(d, 'v01.md'), 'w', encoding='utf-8').write(
            open(os.path.join(tmp, '正文', '镇冢秘术_第七章_测.md'), encoding='utf-8').read())

    e2e('回执已交＋轮次倒退须拦停且零写入', s_receipt, '第4轮·升华庭', 2)
    e2e('空轮须拦停且零写入', s_empty, '第4轮·升华庭', 2)
    e2e('干净首版须放行并写入', s_clean, '第1轮·感官庭', 0)

    # ── 漂移哨端到端：临时 git 库，封版后改动须被逮到 ──
    tmp = tempfile.mkdtemp(prefix='zm_drift_')
    try:
        os.makedirs(os.path.join(tmp, '正文'))
        os.makedirs(os.path.join(tmp, '设定'))
        ROOT, JJ_DIR = tmp, os.path.join(tmp, '版本')
        f = os.path.join(tmp, '正文', '镇冢秘术_第七章_测.md')
        open(f, 'w', encoding='utf-8').write('《镇冢秘术》\n\n第七章　测\n\n原文\n')
        rp = os.path.join(tmp, '设定', '回执_x_第7章作业单.md')
        open(rp, 'w', encoding='utf-8').write('x')
        q = lambda *a: subprocess.run(a, cwd=tmp, capture_output=True, text=True)
        q('git', 'init', '-q')
        q('git', 'config', 'user.email', 't@t')
        q('git', 'config', 'user.name', 't')
        q('git', 'add', '-A')
        q('git', 'commit', '-q', '-m', 'x')
        chk('漂移哨：未改动时不得误报',
            not drift_of(7, [rp], f, open(f, encoding='utf-8').read())[0])
        open(f, 'w', encoding='utf-8').write('《镇冢秘术》\n\n第七章　测\n\n原文被改了\n')
        chk('漂移哨：封版后被改须逮到',
            drift_of(7, [rp], f, open(f, encoding='utf-8').read())[0])
        chk('漂移哨：未交回执之章不判漂移',
            not drift_of(7, [], f, open(f, encoding='utf-8').read())[0])
    finally:
        ROOT, JJ_DIR = _R, _J
        shutil.rmtree(tmp, ignore_errors=True)

    print('\n  六闸负测（含端到端真跑）：%d/%d' % (ok, ok + fail))
    return 0 if fail == 0 else 1


def save(n, note=''):
    d, led = paths(n)
    os.makedirs(d, exist_ok=True)
    src = find_chapter(n)
    if not src:
        print('  ✗未找到第%d章正文' % n)
        return 1
    ledger = json.load(open(led, encoding='utf-8')) if os.path.exists(led) \
        else {'章': n, '版本': []}

    # 【批112】诸闸须在落盘之前拦：拦得住交付的才算闸。
    reopen = os.environ.get('ZM_REOPEN', '').strip()
    force = os.environ.get('ZM_FORCE', '').strip()
    chapters_now = _book_chapters()
    receipts = _receipts_of(n)
    txt = open(src, encoding='utf-8').read()
    snaps = sorted(glob.glob(os.path.join(d, 'v[0-9][0-9].md')))
    same_as_last = bool(snaps) and \
        open(snaps[-1], encoding='utf-8').read().strip() == txt.strip()
    halt, glines = gates(n, note, ledger, chapters_now, receipts,
                         reopen, force, same_as_last)
    print('\n  ── 六闸（批112·不认人，只认磁盘之账与认知对不对得上） ──')
    for l in glines:
        print(l)
    drifted, dlines = drift_of(n, receipts, src, txt)
    for l in dlines:
        print(l)
    if drifted and not force:
        halt = True
    git_found, git_txt = concurrency_check(quiet=True)
    if git_found:
        print(git_txt)
    if git_found and not force:
        halt = True
        print('   ⛔HEAD前进闸：自上次记录以来 HEAD 已前进，须先读其所改再落笔。')
    if halt:
        print('  ⛔存版已拦停，未写入任何文件。')
        return 2
    if reopen:
        ledger['版本'].append({'版': '重开', '时': datetime.datetime.now().strftime('%m-%d %H:%M'),
                               '说明': '【重开·记因】' + reopen, 'hard': {}, 'soft': {},
                               '全书章数': chapters_now})
        print('   ⚠已记重开：%s' % reopen)

    hard, soft = score(txt)
    prev = ''
    for pf in sorted(glob.glob(os.path.join(ROOT, '正文', '*.md'))):
        if chap_num(pf) < n:
            prev += open(pf, encoding='utf-8').read()
    naked = term_check(txt, prev)
    v = len(ledger['版本']) + 1
    open(os.path.join(d, 'v%02d.md' % v), 'w', encoding='utf-8').write(txt)

    print('\n███ 存版 v%02d · 第%d章 ███' % (v, n))
    hb = sum(hard.values())
    print('  硬项合计 %d %s' % (hb, '✓' if hb == 0 else '⛔须清零，非零不得为最终版'))
    if hb:
        print('   ', {k: x for k, x in hard.items() if x})
    print('  净重%d 段数%d 均段%d 长段%d | 嗅%d 听%d 触%d 视%d | 老%d 钱%d 沈%d | 四字三现%d 顿悟%d'
          % (soft['净重'], soft['段数'], soft['均段'], soft['长段数'],
             soft['嗅'], soft['听'], soft['触'], soft['视'],
             soft['老头'], soft['钱满'], soft['沈鸢'],
             soft['四字串三现'], soft['顿悟起手']))

    if naked:
        print('  ── 术语裸奔检测（ENG-TERM·批105） ──')
        print('   ⚠首现而四十字内无解释锚：' + '、'.join(naked))
        print('   （专名首现须带解释；若确为前文已解而本章复用，可裁定豁免并记回执）')
    if ledger['版本']:
        best = {}
        for r in ledger['版本']:
            for k in RATCHET_MIN:
                best[k] = min(best.get(k, r['soft'][k]), r['soft'][k])
            for k in RATCHET_MAX:
                best[k] = max(best.get(k, r['soft'][k]), r['soft'][k])
            best['净重'] = max(best.get('净重', r['soft']['净重']), r['soft']['净重'])
        worse = []
        for k in RATCHET_MIN:
            if soft[k] > best[k]:
                worse.append('%s %d→%d(升)' % (k, best[k], soft[k]))
        for k in RATCHET_MAX:
            if soft[k] < best[k]:
                worse.append('%s %d→%d(降)' % (k, best[k], soft[k]))
        if soft['净重'] < best['净重'] * 0.92:
            worse.append('净重 %d→%d(减逾8%%)' % (best['净重'], soft['净重']))
        print('  ── 棘轮闸（与历史最优逐项比） ──')
        if worse:
            print('   ⚠回退项：' + '；'.join(worse))
            print('   减法轮之净重下降属正常，须于回执写明理由；其余回退须裁定或改回。')
        else:
            print('   ✓无回退')

    if not note.strip():
        print('  ⛔本轮说明为空——防假跑第2条：空说明视为该轮未做。')
    ledger['版本'].append({
        '版': 'v%02d' % v,
        '时': datetime.datetime.now().strftime('%m-%d %H:%M'),
        '说明': note, 'hard': hard, 'soft': soft,
        '全书章数': chapters_now, '流': _stream_id()})
    json.dump(ledger, open(led, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('  台账：%s（共%d版）' % (os.path.relpath(led, ROOT), v))
    # 【批111·修】原以"版本数"充"轮数"：而 v01 为封版基线、冷轮／终版回补／定案皆在十轮之外，
    # 故"10版"实为"基线＋9轮"，机器却报十轮已满。改为只数真轮（说明以"第N轮"起者）。
    _rounds = set()
    for _r in ledger['版本']:
        _m = re.match(r'第(\d+)轮', _r.get('说明', ''))
        if _m:
            _rounds.add(int(_m.group(1)))
    _done = len(_rounds)
    _miss = [i for i in range(1, 11) if i not in _rounds]
    if _done < 10:
        print('  ⏳十轮精进：真轮已跑 %d/10（版本%d）；**未跑之轮：%s**'
              % (_done, v, '、'.join('第%d轮' % i for i in _miss)))
    else:
        print('  ✓十轮已满（真轮10/10，版本%d），请跑 --横评 %d' % (v, n))
    return 0


def compare(n):
    d, led = paths(n)
    if not os.path.exists(led):
        print('  ✗第%d章尚无版本台账，先跑 --存版 %d' % (n, n))
        return 1
    versions = json.load(open(led, encoding='utf-8'))['版本']
    print('\n███ 十版横评 · 第%d章（共%d版） ███' % (n, len(versions)))

    print('\n  ── 一·硬项（任一非零即不可为最终版） ──')
    clean = []
    for r in versions:
        hb = sum(r['hard'].values())
        print('   %s 硬项%-3d %s %s' % (r['版'], hb, '✓' if hb == 0 else '⛔', r['说明'][:34]))
        if hb == 0:
            clean.append(r)

    print('\n  ── 二·量项走势 ──')
    head = ('版', '净重', '段数', '长段', '嗅', '触', '沈鸢', '顿悟', '四字三现')
    print('   %-5s %-6s %-5s %-5s %-4s %-4s %-5s %-5s %-8s' % head)
    for r in versions:
        s = r['soft']
        print('   %-5s %-6d %-5d %-5d %-4d %-4d %-5d %-5d %-8d'
              % (r['版'], s['净重'], s['段数'], s['长段数'], s['嗅'],
                 s['触'], s['沈鸢'], s['顿悟起手'], s['四字串三现']))

    print('\n  ── 三·逐项冠军 ──')
    pool = clean or versions
    champs = {}
    for k, pick in [('净重', max), ('长段数', max), ('嗅', max), ('触', max),
                    ('沈鸢', max), ('四字串三现', min), ('顿悟起手', min)]:
        best_val = pick(r['soft'][k] for r in pool)
        holders = [r['版'] for r in pool if r['soft'][k] == best_val]
        # 【批104】并列修正：末版若同为最优即算持有，避免"首次达标版"误判为唯一冠军
        champs[k] = pool[-1]['版'] if pool[-1]['soft'][k] == best_val else holders[0]
        tie = '（并列%d版，末版持有）' % len(holders) if len(holders) > 1 and \
              pool[-1]['soft'][k] == best_val else ''
        print('   %-8s 最优值%-6d 持有 %s%s' % (k, best_val, champs[k], tie))

    print('\n  ── 四·择优裁定（机器只给候选，最终由AI四席定夺） ──')
    if not clean:
        print('   ⛔无硬项全清之版，不得择优；先清零再评。')
        return 1
    last = clean[-1]
    print('   机器候选＝%s（硬项全清之末版，承载全部累积修复）' % last['版'])
    dist = Counter(champs.values())
    print('   逐项冠军分布：%s' % dict(dist))
    if dist.most_common(1)[0][0] != last['版']:
        losing = [k for k, v in champs.items() if v != last['版']]
        print('   ⚠末版未持有以下项之最优值，须逐项核对是否在后续轮次被改坏：%s' % '、'.join(losing))
        print('     改回该项，而非退回旧版；若经裁定为必要代价，须在回执记因。')
    else:
        print('   ✓末版同时为多数项冠军，累积有效。')
    print('\n  【铁律】择优不是挑一版丢九版。取末版为底，逐项回补其余版之冠军项；')
    print('        任何回补须再跑 --存版 生成新版，且新版硬项须全清。')
    if len(versions) < 10:
        print('\n  ⏳尚未满十轮（%d/10），横评仅供中途参考。' % len(versions))
    return 0


def main():
    if len(sys.argv) == 2 and sys.argv[1] == '--自测':
        return selftest()
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    cmd = sys.argv[1]
    if cmd == '--自测':
        return selftest()
    n = int(sys.argv[2])
    if cmd == '--对表':
        return duibiao(n)
    if cmd == '--还原':
        return huanyuan(n, sys.argv[3] if len(sys.argv) > 3 else '')
    if cmd == '--下一轮':
        return nextround(n)
    if cmd == '--轮记':
        return lunji_append(n, sys.stdin.read())
    if cmd == '--存版':
        return save(n, sys.argv[3] if len(sys.argv) > 3 else '')
    if cmd == '--横评':
        return compare(n)
    print(__doc__)
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
