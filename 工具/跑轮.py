#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跑轮机制（批102立法／批103并入检察官）

**本文件是库，不是命令面。**
作者只说两句话：「续」→ 检察官 --开拍；「挑刺」→ 检察官 --验收（自动带存版＋棘轮闸＋满十轮横评）。
下列 CLI 仅供机器自检与负测，日常不用：
    python3 工具/跑轮.py --存版 94 "第三轮·四堂会审"   （--存 为其别名，同走一路）
    python3 工具/跑轮.py --横评 94

立法要点：并行十版会丢弃已修好的真伤，故改为串行累积；
但每轮必存版打分，任何硬项劣于历史最优即棘轮闸拦停，末轮十版横评择优。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os
import re
import sys
import json
import glob
import datetime
import io
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
    paras = [re.sub(r'\s', '', x) for x in body.split('\n') if x.strip() and x.strip() != '＊']   # ★2026-09-05：分节符不算一段（P40 总则）
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
              if re.match(r'^(我忽然|我这才|我心里|我明白|我看出|我先以为|我在心里|想到这儿)', x))   # ★2026-09-05 添「想到这儿」（P37 起手惯用·复发3）

    # ★★★★★2026-09-01 改·硬项之集移入 工具/硬闸.py（全书审计第二层 2-5）。
    #   ★其由：此表先前与检察官各记一份，遂成两本账——
    #     ★★实测一段含 `? ! ;`、九鼎、赵阙、「那个那个」之稿跑预检，只报「英文」与「段间空行」，
    #        ★★★三样硬伤一样也没认出来；而「预检说可落盘而它不可落盘」正是 LAW-287A 已犯二回之病。
    #   ★★而并集之前先量（令§六②）：全书287章 `? ! ; '` 各 0 章、canon 22 个机制词各 0 章、
    #     ★★★叠词粘连（去「一个」後）0 处——**故此并集是纯超集，不动任何一章已封版之判** ✓。
    from 硬闸 import 硬项 as _硬项
    hard = _硬项(txt)

    soft = {
        # ★0924·第三把尺同之：换场符「＊」不是字（检察官 _weight_stats／净重对表 已同）——
        #   365 回修後三器报 2349／2296／2296，分量闸取的正是这一把多数＊的，遂假绿。
        '净重': sum(len(re.sub(r'\s', '', x)) for x in body.split('\n') if x.strip() != '＊'),
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

# ★★★★★2026-09-02 立（欠-289B·289第13轮所逮·本日单领一轮办）
#   ★病：四感之中器只守「嗅」。289自第1轮至第12轮，**听 15→12（−20%）、视 56→52**，
#     八轮无一处报过；而同期三回撞棘轮撞的全是嗅——**我以为我在守四感，器只替我守了一感。**
#   ★★而其治不是把听触视补进 RATCHET_MAX——**先取二组数（令§六①）**：
#     · **第一组·以峰为底（RATCHET_MAX之式）逐章回灌**：听30%／触33%／**视57%**／四感任一 **128章/177（72%）** ⛔
#       ——**一改即红一片，那是拆书不是修闸。**
#     · **第二组·以 v01（起草）为底逐章回灌**：**嗅2%／听6%／触5%／视7%** ✓
#   ★★★二组并列方见其因：**加法轮与减法轮是交替的**——深掘、在场庭把一样感官顶上去，
#     减法轮再削回来，而末版仍高於起草。**以峰为底，等於禁止减法轮碰任何带感官字的一拍。**
#   ★★★★故立第三类棘轮：**RATCHET_V01——四感不得低於起草之版**。
#     ★其所守者正是本坐三回手工守过的那一条：**换字不许换掉一样感官**
#     （289第8轮删「外头闻着轻」、第9轮删「搁下来我才闻见东头」、第10轮之补，
#      三回皆不加回原句，改以一个动作补之）。
#     ★★而「减法轮之净重下降属正常」那一条不及於此：**减的是解，不该减掉感官。**
RATCHET_V01 = ('嗅', '听', '触', '视')


# ═══ 趋阈闸（2026-09-02 立·291第7轮所逮） ═══
# ★其形：**一个数差一点就够到一条有名之限，而最省的一步，是补几个字把它顶过去。**
#   ★★而那几个字过得了每一道硬闸、抬得起净重、看起来跟正常落笔一模一样——
#     **没有任何器分得出「为事而写」与「为数而写」**；令四那一句
#     「墨随事重，不是墨随格子」，考的从来不是墨够不够，是**肯不肯为了格子去添墨**。
#   ★★★其实证（逐章回灌台账所得，非印象）：**版际之比共 3147 次，趋阈之红 68 次＝2.16%**；
#     **而其中四章落在线上一字不差**——
#       275 v22：3498→**3500**（余量2）｜276 v23：3495→**3500**（余量5）
#       283 v07：3499→**3500**（余量1）｜284 v15：3499→**3500**（余量1）
#     **四章各自封了版，而没有一道闸出过声。**
#   ★★★★故立此闸：**不是拦住补墨，是把补墨那一下留在账上。**
#     ★其判据只两样：①本版令某数跨过一条有名之限；②跨得勉强（余量≤此前之差的四分之一）。
#     ★★而其过法**不是签一个字**（LAW-290B：签核可以顺手写）：
#       须在本轮说明里写「**非凑数：<其由>**」，**而那一行连同其数一并落进台账**——
#       **日後可逐条回读，看那些「其由」是不是空话。**
THRESHOLDS = (
    ('净重', 2500, '常章带下沿'),
    ('净重', 3500, '常章带上沿'),
    # ★★★★★2026-09-02·291第7轮：令四之带改齐（转章带 3,501—5,999），此表随之。
    #   ★旧表之「转章带下沿4000」与「上沿5500」皆已作废——
    #     **其由：全书291章中，落在3,501—3,999者35章、落在5,501—5,999者39章，
    #     合前後二缝并「不足2500」者共99章＝34%在所有带之外，而全书净重中位3,691正落在前一道缝的正中。**
    #   ★★今存二线：**常章带上沿3,500（即转章带下沿之前一字）**与**爆章下沿6,000**。
    ('净重', 6000, '爆章下沿'),
    ('最长段', 120, 'P26·长段'),
    ('长段数', 1, 'P26·长段数'),
)


def 趋阈(prev_soft, soft):
    """★返回本版所跨之限（跨得勉强者），每笔为 dict：项／限／前／後／余量／此前之差／名。"""
    out = []
    for k, T, name in THRESHOLDS:
        if k not in (prev_soft or {}) or k not in (soft or {}):
            continue
        m0, m1 = prev_soft[k], soft[k]
        if not (m0 < T <= m1):
            continue
        gap, over = T - m0, m1 - T
        if gap > 0 and over <= 0.25 * gap:
            out.append({'项': k, '限': T, '名': name, '前': m0, '後': m1,
                        '余量': over, '此前之差': gap,
                        '落在线上': bool(over <= 2)})
    return out


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


def 漂移记因之判(记因):
    """漂移哨之「记因放行」纯判（⛔可负测）。返回 (放行, 由)。

    ⛔**空即不放**（照旧拦）；⛔**不足八字即不放**（一个词不算记因）。
    """
    因 = (记因 or '').strip()
    if not 因:
        return False, ''
    if len(因) < 8:
        return False, '⛔漂移记因太短（%d字，须八字以上）——⛔一个词不算记因。' % len(因)
    return True, 因


def _receipts_of(n):
    return sorted(glob.glob(os.path.join(ROOT, '设定', '回执_*_第%d章作业单.md' % n)))


def _round_of(note):
    m = re.match(r'\s*第\s*(\d+)\s*轮', note or '')
    return int(m.group(1)) if m else None


def _book_chapters():
    return len([p for p in glob.glob(os.path.join(ROOT, '正文', '*.md')) if chap_num(p)])


def 新增章号自末次存版(n):
    """自末次动本章 `_台账.json` 之commit 以来，`正文/` 新出之档之章号。

    ⛔**其用只一处**：章界闸判「所增者是不是尽在本章之後」。
    ★**取不到即返 None**（⛔**上游照旧拦**——「查不着」不是放行之由）。
    """
    import subprocess
    led = os.path.join(ROOT, '版本', '第%d章' % n, '_台账.json')
    if not os.path.exists(led):
        return None
    try:
        r = subprocess.run(['git', '-C', ROOT, 'log', '--format=%H', '-1', '--',
                            os.path.relpath(led, ROOT)],
                           capture_output=True, text=True, timeout=30)
        sha = (r.stdout or '').strip()
        if not sha:
            return None
        r2 = subprocess.run(['git', '-C', ROOT, '-c', 'core.quotepath=false',
                             'ls-tree', '-r', '--name-only', sha, '正文/'],
                            capture_output=True, text=True, timeout=30)
        if r2.returncode != 0:
            return None
        旧 = set(x.strip().strip('"') for x in (r2.stdout or '').split('\n')
                 if x.strip().endswith('.md'))
        if not 旧:
            return None
        今 = set(os.path.relpath(f, ROOT)
                 for f in glob.glob(os.path.join(ROOT, '正文', '*.md')))
        # ⛔**凡旧档少了一个（改名／并章／删档）——即返 None，让上游拦。**
        if 旧 - 今:
            return None
        return sorted(chap_num(x) for x in (今 - 旧))
    except Exception:
        return None


def gates(n, note, ledger, chapters_now, receipts, reopen='', force='', same_as_last=False,
          txt='', 新增章号=None):
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

    # 闸〇·说明闸（2026-09-13 立·325 之席三轮连栽，原样报上来的那一条）：
    #   ⛔**存版口收「说明为空／单字」之版**——325 之 v06、v09 皆存成占位字「x」、v15 存成空；
    #   **其害不在难看**：**台账之说明即轮号之源**（`_round_of(说明)`），
    #   **说明一空，那一版就没有号**；**`--写轮记` 遂拒（「不许以第?轮起头」），**
    #   **而那一轮的刀已经落在正文里了**——**活干了，账上没有它。**
    #   ★**并及本坐自己犯的同一样**：**0913 拿真器做探针，把「t」「probe」真存进了台账**
    #   （**v01「test」／v03「probe」／v10「x」之来历，即此**）。
    #   ⛔**故焊此一闸：说明须是一句人看得懂的话**——**汉字少於四个即当场拒收。**
    #   ★★**其所以取「汉字数」而不取「长度」**：**「x」「probe」「v12」「----」长短不一而皆非一句话**；
    #   **而本书一切真说明皆以汉字起（第N轮·某某庭／终版回补／回补·定案）。**
    #   ⛔**force 不免此闸**：**ZM_FORCE 是为「闸判错了」留的口，而一句空说明没有对错可判。**
    #   ⛔**并当面认一处自栽（立日同刻）**：**我头一版把界定在「汉字少於四个」**，
    #     **而真局里那四样（空／x／probe／test）汉字皆係零**——**四这个数是我想出来的，不是真局逼出来的**；
    #     **跑轮自测当场塌下九格**（其局作「第4轮·甲」「第1轮·甲」，汉字三个，皆是真说明）。
    #   ★**今收到真局所指之界：零汉字即拒。**
    #     **凡一个数写进判据而真局里没有它，那个数就是猜的**（本册 ㊙ 同族）。
    _han = len([c for c in (note or '') if '\u4e00' <= c <= '\u9fff'])
    if _han < 1:
        halt = True
        lines.append('   ⛔说明闸：本次说明「%s」一个汉字也没有——不成一句话，当场拒收。'
                     % (note or '')[:20])
        lines.append('     台账之说明即轮号之源：说明一空，那一版就没有号，轮记随之写不成，')
        lines.append('     而那一轮的刀已经落在正文里了——活干了，账上没有它。')
        lines.append('     处方：把这一版干了什么写成一句话再存（第N轮·某某庭：本轮之刀…）。')

    # 闸二·轮次单调闸：轮次只许持平或前进，不许倒退。
    done = [_round_of(x.get('说明', '')) for x in vs]
    done = [x for x in done if x]
    # ★★★★★★2026-09-13 收窄（体检账 ㊞·325 之五个「洞」係本闸挖的）：
    #   ⛔**旧式係「报一个比末轮小的号即拦」**，其由自书「多半是自己已推进而记不得（P22断层续手）」；
    #   ★**而十一段席的排法本就不按号走**——**第10轮·器物总账庭先於第9轮开｜第4轮·深掘三路各一席｜
    #     无伤席一轮一席**，皆 325 实事；**於是第2轮、第5轮之席存不上版**，
    #     **它们照令不肯改号去哄闸（「不许为迁就此闸而把轮号改作第10轮，那是把一轮在册上抹掉」·0912·318 祖案）**，
    #     **红原样交上；而 `验轮闸` 随後把这几处报成「洞：确有一轮跑了而未存版」。**
    #   ★★**即闸的前提是「诸轮按号次第开」，而盘上的规矩是「轮可乱序」——两句话谁也没跟谁对过账。**
    #   ⛔**而本闸要挡的那一样是真的，一格也不许松**：**把跑过的一轮再跑一遍（P22）。**
    #   ★★★**故只收窄一处**：**报一个比末轮小的号**——
    #     **那一轮在册上还没有＝补洞，许**；**那一轮已在册上＝重跑，照旧拦。**
    if r is not None and done and r < max(done) and r in done and not reopen:
        halt = True
        last = vs[-1]
        lines.append('   ⛔轮次闸：第%d轮台账里已有（末版 %s「%s」%s，已跑到第%d轮），本次又报第%d轮。'
                     % (r, last.get('版', ''), last.get('说明', ''),
                        last.get('时', ''), max(done), r))
        lines.append('     ⛔这一轮跑过了：多半是自己已推进而记不得（P22断层续手），仍按旧认知落笔——先读末版再定。')
        lines.append('     ★而「乱序开庭」不在此列：报一个册上还没有的号係补洞，本闸不拦。')

    # 闸三·章界闸：自上次存版以来全书章数变了＝别路拆了章或续了章，脚下的地已经动了。
    prev_ch = None
    for x in reversed(vs):
        if isinstance(x.get('全书章数'), int):
            prev_ch = x['全书章数']
            break
    # ★★★★★★2026-09-16 收窄（336 之实·救章席之刀无版可入）：
    #   ⛔**旧式係「章数不等即拦」**，其由自书「章数变动多半来自拆章／续章，
    #     **本章之界与净重基线俱已不同**」——★**而这一句只对「拆／并」成立。**
    #   ★★**书往前写了一章，对一个旧章的界与净重基线一格影响也没有**：
    #     **336 之界仍是 336，其净重仍是那些字**；**变的只是它後头多了一章。**
    #   ★★★**其果**：**照旧式，任何一章只要书往前走过一章，就再也补不了版**——
    #     **而这与 `跑轮` 自己那条「封版之後走回补／定案」之路正面相顶**
    #     （`:347` 逐字「封版之后的改动须走回补／定案并记因」）。
    #     **0916 之实：336 之救章席挖出二层、刀已落正文，而台账无格可装，一庭遂卡死。**
    #   ★★★★**故只收窄一处，一格不许多松**：
    #     **凡「章数只增、且所增者尽在本章之後」者，作往前写论**——**报而不拦**；
    #     ⛔**章数减了（并章）、或所增者落在本章之前（拆章）——照旧拦**，
    #     **因为那两样真会动本章之界。**
    # ★★★★★★2026-09-16 再收窄（336 第二回之实）：
    #   ⛔**上式之判係 `n >= prev_ch`**——**其意是「本章本来就在书末」**；
    #   ★**而本闸自书之律係「所增者尽在本章之後」**，**二者不是一回事**：
    #     **336 之後书往前写了 337、338，所增者皆在 336 之後，而 `336 >= 337` 为假**——
    #     ⛔**遂照旧拦，一庭仍卡死。即：上一回收窄之码，没有兑现它自己写下的那条律。**
    #   ★★**故今补一路真凭**：`新增章号`——**自末次存版以来 `正文/` 新出之档，逐档取其章号**
    #     （**其据係 git：末次动 `_台账.json` 之commit 之档单，与工作区之档单相减**）。
    #   ★★★**凡「只增、且所增之章号尽大於本章」者，作往前写论**；
    #     ⛔**章数减、或所增之中有一个号 ≤ 本章——照旧拦**（**那才是拆章并章**）。
    #   ⛔**其凭取不到时（`新增章号 is None`）照旧拦**——**不许拿「我没查着」当放行之由。**
    _尽在後 = (新增章号 is not None and len(新增章号) > 0
               and all(x > n for x in 新增章号))
    _只增而在後 = (prev_ch is not None and chapters_now > prev_ch
                   and (n >= prev_ch or _尽在後))
    if prev_ch is not None and chapters_now != prev_ch and not force and _只增而在後:
        lines.append('   ℹ章界闸·报而不拦：上次存版时全书%d章，现为%d章，'
                     '**而所增者尽在第%d章之後**——係书往前写，非拆章并章。'
                     % (prev_ch, chapters_now, n))
        lines.append('     ★**本章之界与净重基线未动**；⛔**若系拆章／并章，本闸照旧拦**。')
    elif prev_ch is not None and chapters_now != prev_ch and not force:
        halt = True
        lines.append('   ⛔章界闸：上次存版时全书%d章，现为%d章。'
                     % (prev_ch, chapters_now))
        lines.append('     章数变动多半来自拆章／续章，本章之界与净重基线俱已不同，不得按旧认知续改。')
        lines.append('     若系本路方才拆章／续章，置 ZM_FORCE="拆章 N→N+N1" 记因后再跑；')
        lines.append('     若不知情，则是自己失忆而地已动（P22），须先对表认路。')

    # 闸六·空轮闸（防假跑第1条）：正文与末版逐字相同＝本轮零改动，却要记一版。
    # 【批113·修】初版与验轮闸相犯：零刀之轮若被迫改用非「第N轮」之说明，验轮闸即判其未跑，
    #   遂令「审毕判不补」这一合法结局无从表述。故凡说明中明记判不补者放行，仍挂其轮号。
    # ═══ 闸十一·亮点闸（2026-09-02·293第2轮立·九犯而未机化，今机化）═══
    #   ★其法早已写在纸上（一坐⑬：「凡起草毕即须落亮点段，不得留到后轮」），
    #     ★★而它只报不拦——**病历本记「亮点段必犯病」8次，一坐今日印「此病已犯九次」。**
    #   ★★★数其群（令§六①②）：**有版可查之章174，亮点段落在 v01 或 v02 者125章，
    #     落在 v03 之後者 49 章（28%）**——★**群成，非孤例。**
    #   ★★★★而其位非在报，在存版之路上：**第1轮之存版若无亮点段，当场拦停**；
    #     ★**其向只朝前**（旧章不再重存，故全书106篇无亮点段之旧章零假红）；
    #     ★★**而不报轮号之存版不受此拦**（与领轮闸同律：说明一空即不认轮，此闸亦不认）。
    _liang = (_round_of(note) == 1) and ('【本章亮点' not in txt)
    _nocut = bool(re.search(r'判不补|零刀|不补|无真伤', note or ''))
    if _liang and not force:
        halt = True
        lines.append('   ⛔亮点闸：本版报第1轮，而正文无【本章亮点】。')
        lines.append('     一坐⑬之法：**凡起草毕即须落亮点段，不得留到后轮**；')
        lines.append('     而其群已成：有版可查之章174，落在v03之後者49章（28%）——**留到后轮就是留不住**。')
        lines.append('     处方：补齐亮点段（骨N层＋其数＋其底＋本章之位），再存。')
        lines.append('     ★而其尺与正文同：破折0／五逗0／半角0／拉丁字母0（全书亮点段无一处用拉丁字母）。')
    if same_as_last and not force and not _nocut:
        halt = True
        lines.append('   ⛔空轮闸：正文与末版逐字相同，本轮零改动。')
        lines.append('     记一版空轮＝台账上多一个跑过的样子，而实无一刀，日后横评择优必被它带偏。')
        lines.append('     若确为「本轮审毕判不补」，说明中明写「判不补」（如「第N轮·XX庭·判不补·记因」），')
        lines.append('     轮号照挂，验轮闸不会再判其未跑。')

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
    return rs, [i for i in range(1, ROUNDS + 1) if i not in rs]


def rounds_verdict(ledger):
    """【批113·修】验轮之裁。
    病因（自证）：初版验轮闸把「真轮不足1—10」一律判为无凭据，遂对105/106/143误报——
      105/106之末版为「定案轮／冷轮补执（十轮之外）」，活儿续跑了只是没挂第10轮之号；
      143之第9轮即收官减法并当场拆章，其末轮本就是9号。**此为轮号漂移，非丢版。**
      （轮号漂移之实证：全书台账中第8轮惯用「减法轮」、第9轮「收官减法轮」、第10轮「收官轮」，三者重叠。）
    故改判两级：
      · 洞（中间缺号，如1,2,3,5）＝确有一轮跑了而未存版 → 硬伤，须补。
      · 短（末尾不足十）＝或为轮号压缩，或为真丢 → 存疑，须回执写明，不得径判无凭据。
    返回 (holes, short, verdict_lines)。"""
    rs, _ = rounds_state(ledger)
    if not rs:
        return [], [], []
    top = max(rs)
    holes = [i for i in range(1, top) if i not in rs]
    short = [i for i in range(top + 1, 11)]
    lines = []
    if holes:
        lines.append('   ⛔验轮闸·洞：真轮缺 %s，而其后之轮已存——'
                     % '、'.join('第%d轮' % i for i in holes))
        lines.append('     中间缺号＝确有一轮跑了却未存版：未过棘轮闸，亦无快照可回退。须补存或于回执记因。')
    if short:
        # 【批113·再修】前修曰"机器判不了是哪一种"——此语亦错，凭据本就在台账里：
        #   ①末轮之后尚有「十轮之外」之版（定案轮／冷轮补执）＝流程走完了，只是没挂号（105、106即此）；
        #   ②末轮说明已达终局镜头（收官／减法／定案）＝其末轮本就是那一轮（143即此）。
        #   二者皆无，方为真存疑（151即此：末轮为跨章复审，其后无版）。
        vs = ledger.get('版本', [])
        tail = []
        seen_top = False
        for x in vs:
            if _round_of(x.get('说明', '')) == top:
                seen_top = True
                continue
            if seen_top:
                tail.append(x.get('说明', ''))
        after = [t for t in tail if re.search(r'十轮之外|定案|冷轮|横评|器物总账', t)]
        topnote = ''
        for x in vs:
            if _round_of(x.get('说明', '')) == top:
                topnote = x.get('说明', '')
        terminal = bool(re.search(r'收官|减法|定案', topnote))
        if after:
            lines.append('   ✓验轮闸·短而判合：真轮止于第%d轮，然其后尚有十轮之外之版（%s）——'
                         % (top, after[0][:20]))
            lines.append('     流程走完了，只是末轮未挂号（轮号压缩）。')
        elif terminal:
            lines.append('   ✓验轮闸·短而判合：真轮止于第%d轮，而该轮即终局镜头（%s）——'
                         % (top, topnote[:20]))
            lines.append('     其末轮本就是这一轮，非丢版。')
        else:
            lines.append('   ⚠验轮闸·短而存疑：真轮止于第%d轮（%s），其后既无十轮之外之版，'
                         % (top, topnote[:18]))
            lines.append('     该轮亦非终局镜头——多半确有一轮跑了未存版，须于回执写明。')
    return holes, short, lines


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
        print('  真轮：%d/%d%s' % (len(rs), ROUNDS, '' if not miss else
              '｜缺 ' + '、'.join('第%d轮' % i for i in miss)))
        # 【批112·闸四｜批113修】封版凭据之验，两级判：洞＝硬伤，短＝存疑。
        if rc:
            for l in rounds_verdict(lg)[2]:
                print(l)
    else:
        print('  台账：无')
    return 0


def _补存之基线(base, note):
    """补存口该往 _领轮.json 里落什么（None＝一个字也不落，且旧基线须销）。

    ★★★★★2026-09-09·307封版之序所逮（**同形第二口·当日治**）：
      ★0909 早间已治过第一口——`--下一轮` 之「无轮可领仍落 目标轮:null 基线」
        （见本档 `nextround` 里「无缺轮即不落基线」那一段）；
      ★★**而补存这一口原样未动**：旧式一律 `base['目标轮'] = _round_of(note)`，
        **说明里没有「第N轮」时即写下一个 None**——**空值照旧从这一口漏进盘里**。
    ★★★其实证（逐字，非拟）：307 之 v16 说明作
      「定案·案席封版（十三轮之外）·判不补·记因：…·补存」（无轮号），
      於是 `版本/第307章/_领轮.json` 落成 `"目标轮": null`，
      而 `开轮六检.check9` 正确判它「⛔基线里无「目标轮」（领了轮而没记所领之号）」。
    ★★★★故照第一口同一条判改：**无轮号即不落领轮之凭**（落一份空的等於领了一个不存在的轮）；
      ★而说明里没有轮号时，**旧基线里那个真轮号不许被抹掉**——那一轮领了还没用，
      抹掉它反倒把「领了轮没用」变成「没领过轮」。
    """
    b = dict(base or {})
    b['正文sha'] = b.get('末版sha')
    r = _round_of(note)
    if r is not None:
        b['目标轮'] = r
    b['补存'] = True
    return None if b.get('目标轮') is None else b


def buccun(n, note):
    """补存：专修「某轮跑了、正文改了、版没存上」。
    与 --存版 之别：本口显式承认基线已偏，故免闸八之「起手即已偏」，其余诸闸照走，
    且必于台账留「补存」之痕，使日后查得出这一版不是当场存的。"""
    d, led = paths(n)
    lg = _ling_path(n)
    base = {}
    if os.path.exists(lg):
        try:
            base = json.load(open(lg, encoding='utf-8'))
        except Exception:
            base = {}
    新 = _补存之基线(base, note)
    os.makedirs(d, exist_ok=True)
    if 新 is None:
        if os.path.exists(lg):
            os.remove(lg)
            print('  ℹ补存口：说明里无「第N轮」——不落领轮基线，并销去旧基线一份'
                  '（其目标轮为空，係此病之遗）。')
        else:
            print('  ℹ补存口：说明里无「第N轮」——不落领轮基线'
                  '（无轮可领，本就不该有领轮之凭）。')
    else:
        json.dump(新, open(lg, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('  ℹ补存口：已按末版对齐领轮基线（显式承认此版非当场所存）。')
    rc = save(n, note + '·补存')
    return rc


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
        print('     确要复原请跑：python3 工具/跑轮.py --还原 %d 确认' % n)
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
# ★★★★★2026-08-19 改·作者令：「你的目的不是为了跑完，是为了把质量达到最高。」
# ★病灶（作者问「字数是不是失衡了」而查出）：181—208均5770、标准差仅68；
#   而209起（下限由5500改2000之日）掉到均3428——两头都是惯性，不是事定的长短。
# ★★而更深一层：十庭之中八庭查错、一庭减字，只有升华庭算求好，
#   而升华庭我跑成了「查十招在不在」——那还是查，不是推。
# ★★★故十轮之中，从来没有一轮是专门用来「把每一层往下再推一层」的。
# ★★★★遂改第4轮为**深掘轮**：逐层问「这一层底下还有没有一层」，
#   答得出即当场写下去，答不出即明记「此层已到底」及其由。
# ★★★★★而招式比对不废，降为深掘轮之附检（其本为查，不该占一整轮）。
# ★★★★★2026-08-19 扩轮·作者令：
#   「跑轮可以加到13、14、15、16甚至更多，只要能让质量达到最高；
#    但前提是每一轮都要按照绝对最大的功率去跑。」
#   「有一轮就是从各个角度刁钻地看，这一章有没有达到质量最上乘、中国第一的小说。」
# ★而十轮之制立於批102，其时之职为「查错」；★★而查错十轮已足，求好则不足。
# ★★★故扩为十三轮：十轮如旧（第4轮已改深掘），另立三轮专司「求好」：
#   ★第11轮·四方庭：读者／作家／编辑／作者，四个角度逐一审
#   ★★第12轮·极限轮：把前十一轮凡判「合／已到底／不补」之处，再问一遍「真到底了吗」
#   ★★★第13轮·定稿轮：通读一遍，只问一句「这一章配不配放进中国第一的小说里」
# ★★★★而总轮数由 ROUNDS 定，一改全改；日后再扩不必翻遍全码。
ROUNDS = 13

LENS_FALLBACK = {
    1: '感官庭', 2: '四堂会审', 3: '挑刺王终读（逐数对表）', 4: '深掘轮（逐层下探·附招式比对）',
    5: '在场庭＋内面庭', 6: '内心庭', 7: '时序＋节奏＋留白', 8: '跨章复审',
    9: '收官减法轮', 10: '收官轮（器物总账＋逐段生死）',
    11: '四方庭（读者／作家／编辑／作者）', 12: '极限轮（复问一切判合之处）',
    13: '升华定稿轮（逐轮回检功力＋全章最后一次升级）'}


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
    for r in range(1, ROUNDS + 1):
        out[r] = tab[r].most_common(1)[0][0] if tab[r] else LENS_FALLBACK[r]
    return out



def _is_old_era(n):
    """【第102批·回修令】此章是不是「旧制封版」之章。
    ★判据二条并立：①已交回执（即已封版）②其台账所记之轮，最大值≤10。
    ★★而其用：凡今日方立之闸（十三轮制、深掘轮、尽力查），
       不得拿去量它立法之前就已封版的章——★★★那不是伤，是制度换代。"""
    try:
        sd = os.path.join(ROOT, '设定')
        sealed = any(('第%d章' % n) in f and '回执' in f for f in os.listdir(sd))
        if not sealed:
            return False
        led = os.path.join(JJ_DIR, '第%d章' % n, '_台账.json')
        if not os.path.exists(led):
            return False
        rs = set()
        for x in json.load(open(led, encoding='utf-8')).get('版本', []):
            m = re.match(r'第\s*(\d+)\s*轮', x.get('说明', ''))
            if m:
                rs.add(int(m.group(1)))
        return bool(rs) and max(rs) <= 10
    except Exception:
        return False


def _sha(t):
    import hashlib
    return hashlib.sha256(t.strip().encode('utf-8')).hexdigest()[:16]


def _flag_path(n):
    return os.path.join(paths(n)[0], '_拦停.json')


def raise_flag(n, why, note=''):
    """【批122·拦停旗】存版一被拦即落旗，旗在则后续一切轮务皆走不动。
    病灶（P28之残余，作者追问「彻底解决」时查出）：批121只给了一条「须看退出码」之戒律，
    而戒律是文档，文档不是闸——本会话反复自证。执笔纵漏读一次拦停，
    仍可若无其事继续动手；四道闸皆须待下一次调用方能再报，而那一次也可能再漏读。
    故改为**粘性**：拦停之事实落盘为旗，`--下一轮`／`--轮记` 见旗即拒，
    检察官逐章对表见旗即大声报。**旗只由一次成功的存版／补存销去。**
    如此「漏读一次」不再等于「走得过去」。"""
    # ★★★★★2026-09-12 补（321 收口当场自逮·**销一面立一面，永远清不掉**）：
    #   ★`_flag_stale` 立於 0904，其意是「**旗之义是那一轮的版没存上**；
    #     而空轮闸所拦者是『你存了第二回』——那时旗报的是一件不曾发生的事，故自失其义」。
    #   ★★**而它只销旧旗，不拦新旗**：`flag_block` 销毕即往下跑，
    #     **空轮闸照旧拦，拦毕照旧落一面新的**——**同一跑里销一面立一面**；
    #     ★★★其果：321 之旗连销三回而总核照旧报「拦停旗未销」，**一章之轮务就此走不动。**
    #   ★★★★故於落旗之口加同一条查：**凡本次之拦已失其义者，只报不落。**
    #     ⛔**其条件与 `_flag_stale` 逐字同**（因含空轮闸｜本次说明报得出轮号 R｜
    #     台账上已有一版其说明正报第 R 轮且非空非占位）——**一条也不放宽。**
    #   其负测：`工具/负测_旗之销立.py`。
    _试 = {'因': why, '本次说明': note}
    _失, _由 = _flag_stale(n, _试)
    if _失:
        print('\n  ℹ本次之拦已失其义，**不落旗**（第%d章）。' % n)
        print('     其由：%s' % _由)
        print('     ★旗之义是「那一轮的版没存上」；而此处所拦者是「你存了第二回」——'
              '**那一版明明在账上**。')
        # ★★★★★同日再补（321 当场自逮之第二半）：**只不落新旗还不够**——
        #   ★`clear_flag` 只挂在「存版成功」那一路上，**而这一版已经存过、再存必被空轮闸拦**，
        #     **那面旧旗於是永远等不到那一次成功**：321 之旗连销三回而总核照旧报未销。
        #   ★★故此处并销旧旗：**拦既已失其义，那面为同一件事落下的旧旗，其义一并失了。**
        #   ⛔**而其条件仍是上面那三条，一条不放宽**——**不许拿它去销「存坏了」那一类旗。**
        if read_flag(n):
            clear_flag(n)
            print('     ★★并销去为同一件事落下的那面旧旗（其义一并失了）。')
        return
    d = paths(n)[0]
    os.makedirs(d, exist_ok=True)
    json.dump({'时': datetime.datetime.now().strftime('%m-%d %H:%M'),
               '因': why, '本次说明': note, '流': _stream_id()},
              open(_flag_path(n), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def read_flag(n):
    f = _flag_path(n)
    if not os.path.exists(f):
        return None
    try:
        return json.load(open(f, encoding='utf-8'))
    except Exception:
        return {'时': '?', '因': '旗文件损坏', '本次说明': ''}


def clear_flag(n):
    try:
        if os.path.exists(_flag_path(n)):
            os.remove(_flag_path(n))
            return True
    except Exception:
        pass
    return False


def _flag_stale(n, fl):
    """旗自失其义之查（2026-09-04·299第6轮立）。返回 (是不是失了义, 其由)。

    ★立此查之由（其形上磁盘核过）：**一轮存过版之後再存一回，空轮闸拦第二回并落旗**——
      ★★而那一轮的版明明在账上；★★★旗之义是「**那一轮的版没存上**」，此时它报的是一件不曾发生的事；
      ★★★★而销旗之路只有一条「一次成功的存版／补存」，那一条路正被空轮闸堵着（正文与末版逐字相同）——
      **旗落下去就再也拿不掉，而它拦的是其後一切轮务。**
    ★其条件写死三样，缺一不算失义：
      ①**旗之「因」是空轮闸**（正文与末版逐字相同——即「你存了两回」，不是「你存坏了」）；
      ②旗之「本次说明」报得出轮号 R；
      ③台账上已有一版，其说明报的正是第 R 轮，且其说明非空、非占位。
    ★★**故凡棘轮回退、趋阈闸、硬项、闸八基线不符所落之旗，一面也不失义**——
      **那几样是「存坏了」，账上有没有那一版都不改其为伤。**
    """
    if '空轮闸' not in str(fl.get('因', '')):
        return False, ''
    R = _round_of(str(fl.get('本次说明', '')))
    if R is None:
        # ★1015 W42 所逮：还账、补正之存版⛔带轮号，其空轮之旗依上三条永不失义而拦其章一切轮务——
        #   旗之义是「那一版没存上」；若「因」只是空轮闸、且末版之说明非空非占位、正文与末版逐字同，则那一版已在，旗失其义。
        try:
            d, led = paths(n)
            vs = json.load(open(led, encoding='utf-8')).get('版本', []) if os.path.exists(led) else []
            末 = vs[-1] if vs else {}
            s = (末.get('说明') or '').strip()
            if s and s != _占位 and '说明闸' not in str(fl.get('因', '')):
                vp = os.path.join(d, '%s.md' % 末.get('版', ''))
                import 章料 as _章料
                f = _章料.章档(n)
                if f and os.path.exists(vp) and open(f, encoding='utf-8').read() == open(vp, encoding='utf-8').read():
                    return True, '末版（%s）已在账上且与正文逐字同，其说明：%s' % (末.get('版', '?'), s[:60])
        except Exception:
            pass
        return False, ''
    d, led = paths(n)
    if not os.path.exists(led):
        return False, ''
    try:
        vs = json.load(open(led, encoding='utf-8')).get('版本', [])
    except Exception:
        return False, ''
    for x in vs:
        s = (x.get('说明') or '').strip()
        if s and s != _占位 and _round_of(s) == R:
            return True, '第%d轮之版（%s）已在账上，其说明：%s' % (R, x.get('版', '?'), s[:60])
    return False, ''


def flag_block(n, who):
    """见旗即拒。返回 True 表示须拒。"""
    fl = read_flag(n)
    if not fl or os.environ.get('ZM_FORCE', '').strip():
        return False
    失, 由 = _flag_stale(n, fl)
    if 失:
        clear_flag(n)
        print('\n  ℹ拦停旗自失其义，已销（第%d章）。' % n)
        print('     旗之由：%s' % str(fl.get('因', ''))[:80])
        print('     而其事不成立：%s' % 由)
        print('     ★旗之义是「那一轮的版没存上」；空轮闸所拦者是「你存了第二回」，'
              '不是「你存坏了」——★★而账上那一版在，旗报的就是一件不曾发生的事。')
        print('     ★★★而棘轮回退／趋阈闸／硬项／闸八所落之旗，此口一面也销不掉。')
        return False
    print('\n  ⛔拦停旗未销：第%d章上一次存版被拦停（%s），至今未修。' % (n, fl.get('时', '?')))
    print('     拦停之由：%s' % str(fl.get('因', ''))[:160])
    print('     当时所报：%s' % str(fl.get('本次说明', ''))[:60])
    print('     **旗在，%s 一律不办。** 旗只由一次成功的存版／补存销去。' % who)
    print('     修法：python3 工具/跑轮.py --补存 %d "第N轮·镜头"' % n)
    print('       或：python3 工具/跑轮.py --还原 %d 确认' % n)
    return True


def 可领轮(正文在, 台账在):
    """⛔纯判·不碰盘——**在建之章方许领轮**。返回 (许?, 其由)。

    ★**在建之章必有 `_台账.json`**；**新章尚无正文，其台账自然也无**——那一样许。
    ⛔**正文早已在盘而台账从来没有过者，是一个写完了很久的章**：不许。
    """
    if not 正文在:
        return True, '新章起手（尚无正文）'
    if 台账在:
        return True, '在建之章（台账在）'
    return False, '正文早在而台账从无——不是在建之章'


def _ling_path(n):
    return os.path.join(paths(n)[0], '_领轮.json')


def _last_snap_sha(n):
    d = paths(n)[0]
    snaps = sorted(glob.glob(os.path.join(d, 'v[0-9][0-9].md')))
    return _sha(open(snaps[-1], encoding='utf-8').read()) if snaps else None


def _lunji_path(n):
    return os.path.join(paths(n)[0], '_轮记.md')


# ── 裁毕闸（2026-09-02·293第12轮立·第二十四犯第五形之治）────────────────
# ★其由：293第9轮之轮记写「近似≥0.60者21对，逐对裁毕」，而底下逐对写明其由者只六对；
#   ★★第12轮重跑同一把尺，见拍86与拍91那一对（0.62）从来没被裁过，且它落在全章收处。
#   ★★★即「逐对裁毕」这四个字，是我替那十五对签的字——**而没人报**。
# ★★★★它认哪几样（令§六④，立闸之日须写明）：
#   ①认「N对／N处／N拍／N句 … 逐对（逐处／逐拍／逐一）裁毕（答毕／问毕／看毕）」这一句式；
#   ②数其同节（自本句至下一个 ## 或文末）之内的明细条数——明细之形取本册之常法：
#     行首「·」「★」「|」「①…⑩」「1.」「拍NN」，凡一行含拍号或以列点起手者皆计一条。
#   ③**不认者**（不许把它的绿读成「凡称逐一者俱已逐一」）：
#     ·明细写在别节者（本闸只看同节）；·明细写在正文或回执而不在轮记者；
#     ·称「大半已裁」「多数答毕」之类不给数者——无数即无从数，本闸不管。
# ★而它只报不拦：轮记是记，拦住不许记比记错更坏（第二十四犯之教）。
# ★【293第12轮·立闸当日即修】初版取「逐…毕」之前**最先**遇着的那个数，遂於
#   「（全章161句两两比，近似≥0.60者21对）逐对裁毕」取了161，於
#   「（4486对）随机抽14对：逐对看毕」取了4486——**两处该数的都是後一个数。**
#   ★★其群非孤（改闸之前所数·令§六②）：**全书轮记「逐…毕」之称共266处，
#     其空档之内另有一数者45处（17%），且其形皆为「总数…抽样数…逐一毕」**——
#     **该给明细的是抽样那一个，不是总数那一个。**
#   ★★★故改取**最靠近「逐…毕」的那一个数**：空档之内不许再有「数＋量词」。
_CAIBI = re.compile(r'([一二三四五六七八九十百\d]+)\s*(?:对|处|拍|句|条|笔)'
                    r'(?:(?![一二三四五六七八九十百\d]+\s*(?:对|处|拍|句|条|笔))[^\n]){0,24}?'
                    r'逐(?:对|处|拍|句|条|笔|一)(?:裁|答|问|看|核|数)毕')
_HAN = {'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10,
        '十一':11,'十二':12,'十三':13,'十四':14,'十五':15,'十六':16,'十七':17,
        '十八':18,'十九':19,'二十':20,'二十一':21,'二十二':22}


def _num(x):
    x = x.strip()
    if x.isdigit():
        return int(x)
    if x in _HAN:
        return _HAN[x]
    if x.startswith('十') and x[1:] in _HAN:
        return 10 + _HAN[x[1:]]
    if len(x) == 3 and x[1] == '十' and x[0] in _HAN and x[2] in _HAN:
        return _HAN[x[0]] * 10 + _HAN[x[2]]
    return None


def caibi_gate(text):
    """★数「称几条」与「写几条」之差。返回 [(所称之数, 所见之数, 其句)]。"""
    out = []
    # 同节＝自该句起至下一个 ## 标题或文末
    for m in _CAIBI.finditer(text):
        want = _num(m.group(1))
        if not want:
            continue
        rest = text[m.end():]
        nx = rest.find('\n## ')
        seg = rest if nx < 0 else rest[:nx]
        got = 0
        for ln in seg.split('\n'):
            t2 = ln.strip()
            if not t2:
                continue
            if re.match(r'^(?:[·★|]|[①②③④⑤⑥⑦⑧⑨⑩]|\d+[.、]|拍\s*\d)', t2) or re.search(r'拍\s*\d+', t2):
                got += 1
        if got < want:
            out.append((want, got, m.group(0)[:40]))
    return out


def lunji_append(n, text):
    """append 一条轮记。轮次自台账末版推得。"""
    if flag_block(n, '写轮记'):
        return 2
    d, led = paths(n)
    os.makedirs(d, exist_ok=True)
    # 【批121·修】轮号原取台账末版，故存版一旦未成即标错号（本会话已犯，标出两条第6轮）。
    # 改为：优先取台账末版之轮号，且**必须与末版之说明一致**；台账末版与领轮之目标轮不符者，
    # 说明本轮之版未存上，遂拒写轮记——轮记不许比版先到。
    r, ver, jz = '?', '', ''
    if os.path.exists(led):
        vs = json.load(open(led, encoding='utf-8')).get('版本', [])
        if vs:
            last = vs[-1]
            ver = last.get('版', '')
            jz = last.get('soft', {}).get('净重', '')
            m = _round_of(last.get('说明', ''))
            if m is not None:   # ★2026-09-05：「第0轮」得 0 为假，旧式 `if m:` 把它丢成「?」
                r = str(m)
    _lg = _ling_path(n)
    if os.path.exists(_lg) and not os.environ.get('ZM_FORCE', '').strip():
        try:
            _tr = json.load(open(_lg, encoding='utf-8')).get('目标轮')
        except Exception:
            _tr = None
        if _tr and str(_tr) != r:
            print('  ⛔轮记闸·版未到：所领为第%s轮，而台账末版为第%s轮。' % (_tr, r))
            print('     即本轮之版未存上（存版多半被拦而未察），轮记不许比版先到。')
            print('     先把版存上，再写轮记。')
            return 2
    if r == '?':
        # ★2026-09-05·机制总审（八路·流程之缝审第5条）：旧式照写「## 第?轮」，_lunji_blocks 读不出——首块整个丢、非首块并入前一轮（器把活记到别人头上）。
        print('  ⛔轮记不许以「第?轮」起头：台账末版之说明无轮号（%s）——先 --填记／--补存 使其有号，再记。' % (last.get('说明', '')[:40] if last else '无版'))
        return 2
    head = '\n## 第%s轮｜%s｜%s｜净重%s\n' % (
        r, ver, datetime.datetime.now().strftime('%m-%d %H:%M'), jz)
    with open(_lunji_path(n), 'a', encoding='utf-8') as f:
        f.write(head + text.rstrip() + '\n')
    for _w, _g, _s in caibi_gate(text):
        print('  ⛔裁毕闸：此节称「%s」，而同节之内数得出明细 %d 条 — 少 %d 条。'
              % (_s, _g, _w - _g))
        print('     ★「逐一裁毕」四字，是替那 %d 条签的字；★★补其明细，或改其称。' % (_w - _g))
    print('  ✓轮记已落盘：%s（第%s轮）' % (os.path.relpath(_lunji_path(n), ROOT), r))
    return 0


def buji(n, r, text):
    """【批124】补记：把某轮之补核落在**其本轮之下**。
    与 --轮记 之别：轮记之轮号自台账末版推得（现轮），补记显式指定轮号，
    使覆盖查（按轮号归拢）能认得这是哪一轮补上的。必留「补记」之痕。"""
    d = paths(n)[0]
    os.makedirs(d, exist_ok=True)
    head = '\n## 第%d轮【补记·%s】\n' % (r, datetime.datetime.now().strftime('%m-%d %H:%M'))
    with open(_lunji_path(n), 'a', encoding='utf-8') as f:
        f.write(head + text.rstrip() + '\n')
    print('  ✓补记已落盘：第%d轮（%s）' % (r, os.path.relpath(_lunji_path(n), ROOT)))
    return 0


def nextround(n):
    """开轮之总入口：告诉执笔下一轮该跑哪一轮、镜头为何、前几轮看见了什么。
    前几轮之所见取自磁盘轮记，故压缩冲掉记忆亦不碍。"""
    # 2026-08-19·立位（作者令：「每次开始跑轮的时候都要去做一件事，
    #   先要把你变成最好的小说家；不要去做验证。」）
    # 其意不在自称，在换一把尺：落每一句之前不问「这一句能不能过闸」，
    # 问「这一句拿给最好的小说家看，他会怎么改」——而这两把尺之差，正是平庸与最好之差。
    # 故领轮之首先印此三行，令执笔在动手之前先把尺换过来。
    print('\n  ══ 立位（动手之前先换这把尺）══')
    print('   ★不问「这一轮能不能过闸」，问「这一处拿给最好的小说家看，他会怎么改」。')
    print('   ★★而一轮跑过去没把那一处推得更好，那一轮等於没跑——')
    print('     哪怕它十四检全绿、覆盖裁定俱100%。')
    print('   ★★★先读 设定/反面教材.md（0927）：为圆而凑之因、为过闸而缝之拍，一律重想到最好；过得去的不许交。')
    print(duibiao_brief(n))
    d, led = paths(n)
    lg = json.load(open(led, encoding='utf-8')) if os.path.exists(led) else {'版本': []}
    rs, miss = rounds_state(lg)
    tab = lens_table()
    print('  ── 下一轮 ──')
    if not miss:
        print('   ✓%d轮已满，请跑 --横评 %d 定案。' % (ROUNDS, n))
    else:
        nx = miss[0]
        print('   **该跑第%d轮：%s**' % (nx, tab[nx]))
        if len(miss) > 1:
            print('   其后未跑：%s' % '、'.join('第%d轮(%s)' % (i, tab[i]) for i in miss[1:]))
        print('   【铁则】只跑「下一个未跑之轮」，不认作者所报之号——号会漂，台账不会。')
    # 【批114·闸八】领轮基线落盘：七闸皆在存版时拦，而祸起于「动手在前」。
    # 领轮基线记下「起轮那一刻正文是什么样」，存版时回验，遂把防线提前到动手之前。
    # 【批123·解死结】旗为粘性且只由一次成功的存版销去（见 raise_flag）；
    # 而领轮见旗即 return，遂成环：领轮须销旗→销旗须存版→存版须领轮基线→基线须领轮。
    # 病灶（第221章第1轮亲犯，作者在场）：闸八之基线在 return 之后才落，
    # 故旗一落，执笔纵已把伤治完，也无路可走，只能 ZM_FORCE 绕闸——而绕闸即等于无闸。
    # 治：旗在时**仍落基线**（基线只是「起轮那一刻正文是什么样」的存照，落它无损于任何闸），
    # 只拒「发轮」这一件事。如此销旗之路留着，而闸一分不减。
    _flagged = flag_block(n, '发轮')
    src2 = find_chapter(n)

    # 【批121·闸九·发轮前置闸】上一轮之刀未落台账者，不发新轮。
    # 病灶（用户报「十轮常只跑七八轮／轮次跳号」，本会话第153章第7轮亲犯）：
    #   ①某轮存版被拦（本例为闸八报「起手即已偏」），而执笔以 grep 读输出、未看退出码，误当已存；
    #   ②`--轮记` 之轮号取自台账末版，台账未动则标错号（本例标成第6轮，与前一条重号）；
    #   ③正文继续前改，与末版愈离愈远；④下一轮领轮时闸再报，执笔再漏读，遂带病连跑数轮。
    # **闸一直是对的，断的是读闸那一环。** 故不再往闸上加，改为：没存上就领不到新轮。
    if src2 is not None and not os.environ.get('ZM_FORCE', '').strip():
        _ls = _last_snap_sha(n)
        _cur = _sha(open(src2, encoding='utf-8').read())
        if _ls and _ls != _cur:
            print('\n  ⛔发轮前置闸：上一轮之刀没落进台账，不发新轮。')
            print('     末版sha=%s，而当前正文sha=%s。' % (_ls, _cur))
            print('     即：有一轮跑了、正文改了，可版没存上（多半是存版被拦而未察）。')
            print('     **修法二选一**：')
            print('       ①补存那一轮：python3 工具/跑轮.py --补存 %d "第N轮·镜头"' % n)
            print('       ②还原到末版：python3 工具/跑轮.py --还原 %d 确认' % n)
            print('     修完再跑 --下一轮 %d。' % n)
            return 2

    # 【批120·修】新章起手时正文尚未存在，find_chapter 返回空则基线不落盘，
    #   闸八遂令新章之第1轮永远过不去。故无正文者亦落基线，只是标为新章、免其sha之验。
    # ★★2026-09-09·306 之封版所逮：**无轮可领时，从前照旧落一份「目标轮: null」的基线**——
    #   等於领了一个不存在的轮；而 `开轮六检.check9` 正确地判它「领了轮而没记所领之号」⛔。
    #   ★其形之毒在两头都对：**落基线的那一步没错（它只是照旧落），判红的那一步也没错**，
    #     错在中间那个 None——**一个谁也不为它负责的空值，被两头当成了各自那一头的正常输入。**
    #   ★★故改：**无缺轮即不落基线**（无轮可领，本就不该有领轮之凭），并当场说明。
    if not miss:
        print('   ✓十三轮已满，无轮可领——**不落领轮基线**（落一份「目标轮: null」等於领了一个不存在的轮）。')
        if os.path.exists(_ling_path(n)):
            os.remove(_ling_path(n))
            print('   ✓并销去旧基线一份（其目标轮为空，係此病之遗）。')
        return 0
    # ★★2026-09-16 立·**已封版之章不许领轮**（336 之席跑第7轮当日所逮）
    #   ⛔**其实**：`版本/第7章/_领轮.json` 於 07:05 凭空落盘（`目标轮:1`／`新章:false`），
    #     **而第7章早已封版三百章之久**；其时 336 之席正走**第7轮**（时序·节奏·留白）——
    #     **一个轮号被当成了章号送进来，而本器照旧给它落了一份基线。**
    #   ★**其所以该拦在此处**：封版之序本就把 `_领轮.json` 删去
    #     （一代封版之律：「封版之章不再需领轮基线」）——**故一份领轮出现在已封版之章上，
    #     按本仓自己的定义就是错的**，不必再问它是怎麽来的。
    #   ⛔**而本闸不拦回修**：封版之章若真要再动，其路是回补／定案并记因（见 `_drift_report`），
    #     **那一条路不经领轮**；故此处只拦领轮，一条真路也没有堵。
    #   ⛔**而「回执在不在」不是这一条的判据**（本坐头一版拿它作判，当场试而不中）：
    #     **回执闸自第73章起方立**，第7章根本没有回执——**拿一条只对後三百章成立的判据去拦前七十章，
    #     它一次也拦不住**。★**其真判在「台账在不在」**：**在建之章必有 `_台账.json`**
    #     （336 有、335 有），**而第7章连 `版本/第7章/` 这个目录都是本器当场造的**——
    #     **正文早已在盘而台账从来没有过，那就是一个写完了三百章之久的章。**
    _tz = os.path.join(paths(n)[0], '_台账.json')
    _ok, _why = 可领轮(src2 is not None, os.path.exists(_tz))
    if not _ok and not os.environ.get('ZM_FORCE', '').strip():
        print('\n  ⛔领轮闸·正文早在而台账从无：第%d章不是在建之章。' % n)
        print('     **十有八九是把一个轮号当成了章号**（如「第7轮」写成了「7」）——')
        print('     先对一眼：`python3 工具/心跳.py` 印的是第几章，就该领第几章的轮。')
        print('     ★若真要动一个已封版之章，其路是回补／定案并记因，**那一条路不经领轮**。')
        return 2

    base = {'时': datetime.datetime.now().strftime('%m-%d %H:%M'),
            '正文sha': _sha(open(src2, encoding='utf-8').read()) if src2 else None,
            '末版sha': _last_snap_sha(n),
            '目标轮': miss[0],
            '新章': src2 is None}
    os.makedirs(paths(n)[0], exist_ok=True)
    json.dump(base, open(_ling_path(n), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print('   ✓领轮基线已落盘（%s）。存版时回验。'
          % ('新章起手，尚无正文' if src2 is None else '起轮时正文 ' + base['正文sha']))
    # 【批123】基线已落，销旗之路留着；而旗未销者到此为止，不发新轮。
    if _flagged:
        print('   ⛔旗未销：基线已落（只为留出销旗之路），而本轮不发。'
              '\n     处方：把上一次被拦那一笔补存进台账（--补存 %d "…"），旗即销。' % n)
        return 2

    # ★★★★★2026-08-16 立·领轮即自动跑二检（其为「主动调动核查」之实）
    # ★其由：近日所逮之十bug里，六条无一处闸测之；★★而它们皆在开轮时最易治。
    # ★★★而二检为：质量五闸（一章一事／脉象／谜底之距／主线之距／暗线配额）
    #                ＋开轮六检（人名计数／撞号merged／冷轮／锚之长／领轮之号／招五第二形）。
    # ★★★★而其报而不拦——★★★★★拦停之权仍在存版闸与全测，此处只报，免其挡道。
    if src2 is not None:
        import subprocess as _sp
        # ★★★★★2026-08-19 补：领轮即报「本章之厚薄」，令执笔每一轮都看得见它。
        # ★其由：先前之数只在封版时才见，而那时已无从深掘。
        try:
            _lj0 = _lunji_blocks(n)
            _at = '\n'.join('\n'.join(v) for v in _lj0.values())
            _cg = max(len(set(re.findall(r'第([一二三四五六七八九十])层', _at))),
                      len(re.findall(r'★+\s*[一二三四五六七八九十]层', _at)))
            _bd = open(src2, encoding='utf-8').read().split('【本章亮点】')[0]
            _nw = len(re.sub(r'\s', '', _bd))
            print('   ── 本章之厚薄（尽力查·报而不拦）──')
            print('      层 %d %s｜净重 %d｜跑 --尽力 %d 可见其全'
                  % (_cg, '⛔<3，须深掘' if _cg < 3 else ('⚠<5' if _cg < 5 else '✓'), _nw, n))
        except Exception:
            pass
        for _nm, _f in (('质量五闸', '工具/质量三闸.py'), ('开轮六检', '工具/开轮六检.py'),
                        ('第零轮·下一章之开镜', '工具/第零轮开镜庭.py')):
            _fp = os.path.join(ROOT, _f)   # ★2026-09-05：REPO_ROOT 全档未定义、'REPO_ROOT' in dir() 恒假，cwd≠仓根即静默跳过
            if not os.path.exists(_fp):
                print('   ⚠%s 未找到（cwd=%s）' % (_f, os.getcwd()))
                continue
            try:
                _arg = str(n + 1) if '第零轮' in _nm else str(n)
                _r = _sp.run(['python3', _fp, _arg], capture_output=True, text=True, timeout=120)
                _bad = [x.strip() for x in _r.stdout.splitlines() if '⛔' in x]
                if _bad:
                    print('   ⚠%s 报 %d 处（报而不拦，须治）：' % (_nm, len(_bad)))
                    for _x in _bad[:4]:
                        print('      %s' % _x[:96])
                else:
                    print('   ✓%s 皆过' % _nm)
            except Exception as _e:
                print('   ⚠%s 未能跑：%s' % (_nm, _e))

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
        out.append('   真轮：%d/%d%s' % (len(rs), ROUNDS, '' if not miss else
                   '｜缺 ' + '、'.join('第%d轮' % i for i in miss)))
        if rc:
            out.extend(rounds_verdict(lg)[2])
    else:
        out.append('   台账：无（本章尚未起轮）')
    if src:
        dr, dl = drift_of(n, rc, src, open(src, encoding='utf-8').read())
        out.extend(dl)
    return '\n'.join(out)


LENS_KEY = {1: ['嗅', '听', '触', '密度', '感官'], 2: ['canon', '原场', '逻辑', '器物', '时序', '四堂'],
            3: ['数', '对表', '日', '逐数'], 4: ['层', '深掘', '到底', '招'], 5: ['在场', '内面', '分位', '人物'],
            6: ['器物', '耗材', '资源'], 7: ['节奏', '留白', '方差', '时序'],
            8: ['减', '刀', '删'], 9: ['减', '刀', '拆'],
            10: ['器物总账', '逐段', '收官', '生死'],
            11: ['读者', '作家', '编辑', '四方', '刁钻'],
            12: ['复问', '翻案', '功率', '极限'],
            13: ['回检', '升级', '配不配', '最弱', '定稿']}


def _lunji_blocks(n):
    """轮记按轮号归拢。同一轮可有多条（补记），一并归之。

    ★2026-08-19 补一漏（217第4轮补裁时实见）：
      原码以 '\n## ' 切块，凡块内另有 '## 某某' 之小标题者，其后半即被切成新块；
      而新块不匹配「第N轮」，遂被整个丢弃——★★而丢掉的正是那一轮真干的活。
      其祸之隐在此：轮记落盘时报「✓已落盘」，覆盖率却仍报 0%，
      而人只会以为是自己没写够，不会想到是块被切碎了。
    ★★★故改：切块之后，凡不匹配「第N轮」之块，一律并入其前一块（而非丢弃）。
    """
    f = _lunji_path(n)
    if not os.path.exists(f):
        return {}
    out = {}
    last = None
    # ★2026-09-02·292第13轮甲实见：切块只认「\n## 」，而我把第11、12轮之标题写作「\n# 」；
    #   ★其果不是漏掉那两轮——**是把那两轮的活并进了第10轮**（第10轮之数由 真伤0治5复量5
    #     变成 真伤1治6复量5，而它一个字也没多干）；★★而丁2照旧只列十轮，一声不出。
    #   ★★★此与本函上一修同祸：**器报的不是活没干，是器把活记到了别人头上**——
    #     而记错头比漏记更险：漏记看得出少了一行，记错看着一切正常。
    #   ★★★★故今改为一、二级标题皆认；且丁2另印一行「轮记见N轮／台账见M轮」，两数不符即出声。
    _raw = open(f, encoding='utf-8').read()
    for b in re.split(r'\n#{1,2} ', _raw):
        if not b.strip():
            continue
        m = re.match(r'第(\d+)轮', b)
        if m:
            last = int(m.group(1))
            out.setdefault(last, []).append('## ' + b)
        elif b.startswith('造式·'):
            # ★2026-10-08·造式（`工具/造式.py`）：「## 造式·逻辑审…」「## 造式·盲读」是造式之章之节，不属任何一轮——
            #   ⛔不许并进其前一轮（多半是机闸之第3轮）：并进去，那一轮之覆盖／裁定／对数即被别席之文撑高，是记错头。
            #   ★常式之轮记里无此标题，其归块一格不变。
            last = None
        elif last is not None:
            # 块内之小标题所切出者，归其前一轮（不丢）
            out[last].append('## ' + b)
    return out


# ★★★★★2026-09-05·机制总审所治·其红在哪一行（上磁盘核，非设想）：
#   **305 v13 拍61「前天那三处」对拍23「前天那四处」自相矛盾**——十二轮带器之轮一个没逮着，第13轮一遍通读撞上。
#   ★其所以没逮着：第3轮逐数对表之必答表自正文抽数，而其量词表只认 21 样，
#     **「处」「行」「道」「层」一个也不在其内**——305 全章「N处」二十四见（六处／三处／五处／四处／十一处），入表者零；
#     ★★於是那一对相犯之数从来没被摆到第3轮的桌上，逐数对表在它旁边稳稳地绿（七造§六之形）。
#   ★★★它认哪几样，本书同类共几样（`python3 工具/负测_必答表.py` 之①逐年重数）：
#     全书「数≥2之後一字」频≥50者三十四样；去「章」（章题）与「来那在的几头边」（非量词尾）余二十七样量词；
#     **本表今认 33 样**（旧 21 ＋ 新 12：处行道层件块级份笔印遍句）；**不认「只」「指」**（多作副词与手指，喊狼）。
#   ★★★★另立「同指对」：**同章同日词同量词而数不一者**（「前天那三处」对「前天那四处」），
#     其形全书 305 章中 8 章有之（305 v13 即其一）；★它不判红，只把那一对摆上必答表，逼人答「是不是同一物」——
#     同一物即真伤（305 v13）；不同物须各有其名（305 v14「昨天那三处」係纸上、「昨天那六处」係水里）。
_数尾 = r'个|下|回|段|样|类|把|条|根|卷|分|处|行|道|层|件|块|级|份|笔|印|遍|句'
_日词 = r'昨天|前天|今天|那天|昨儿|前儿'


def _数项(body):
    """第3轮逐数对表之必答项：自白文抽「作数据主张之数」，末尾附「同指对」。"""
    raw = set(re.findall(r'[零〇一二两三四五六七八九十百千]+(?:天|日|年|圈|尺|寸|步|成|副|盏|人|页|口气)', body))
    raw |= set(re.findall(r'前[十二三四五六七八九百]+[天日年章]?', body))
    raw |= set(re.findall(r'[零〇一二两三四五六七八九十百千]+(?:%s)' % _数尾, body))
    raw |= set(re.findall(r'第[一二三四五六七八九十]+(?:处|行|页|道|层|印)', body))
    raw = {x for x in raw if not re.fullmatch(r'[一零〇](?:%s|口|半)' % _数尾, x)}
    pairs = {}
    for m in re.finditer(r'(%s)那([零〇一二两三四五六七八九十]+)(%s)' % (_日词, _数尾), body):
        pairs.setdefault((m.group(1), m.group(3)), set()).add(m.group(0))
    同指 = ['／'.join(sorted(v)) for k, v in sorted(pairs.items()) if len(v) > 1]
    return sorted(raw) + 同指, ('逐数对表：凡作数据主张之数，须核其值、其日、其来处（口语量词不入表）；'
                              '★同指对（同章同日词同量词而数不一者，以「／」相连）须判是不是同一物——'
                              '同一物即真伤，不同物须各有其名')


# ★2026-09-05·机制总审（八路·覆盖之缺第1、2条，本坐上磁盘复核）：
#   ★P07 时序自破复发13、P36 泛日词复发4、P38 回述日词复发5——**三病之词，第2轮回述之必答项一个也不认**：
#     旧式只认「想起|记得|那天|那一回|昨天|前几天|早上|进来的时候|前十|二十七年前」十样；
#     **「前天」不在其内**——而 305 v13 之伤（拍61「前天那三处」对拍23「前天那四处」）正落在「前天」上。
#   ★★病历本自陈之黑名单：P36「这两天／前几天／这十来天／这几天」、P38「那时候／那天／那一天／那会儿」——
#     `grep '这两天\|这十来天\|这几天\|那会儿' 工具/*.py` 改前 0 处。
#   ★★★故今认 21 样（旧 10 ＋ 新 11：那一天 那时候 那会儿 昨儿 前天 前儿 大前天 前几日 这两天 这几天 这十来天）；
#     它只把词摆上必答表逼人贴原场，不判红——故宽表之价是几行裁语，不是喊狼。
_回述词 = (r'想起|记得|那一天|那天|那一回|那时候|那会儿|昨儿|昨天|大前天|前儿|前天|前几天|前几日|'
        r'这两天|这几天|这十来天|早上|进来的时候|前十|二十七年前|四十八年前')  # 0929 D1 五审：那一趟在四十八年前；二稿落定後去旧式


def _回述项(body):
    """第2轮四堂会审之必答项：凡涉前章之回述词，每一种须贴原场逐字比对。"""
    hits = set()
    for m in re.finditer(r'[^。！？\n]{0,26}(%s)[^。！？\n]{0,26}' % _回述词, body):
        hits.add(m.group(1))
    return sorted(hits), ('凡涉前章之回述词，每一种须贴原场逐字比对'
                         '（★2026-09-05 添「前天」与 P36 泛日词四型、P38 回述日词四型——305 v13 之伤正在「前天」上，旧式不认它）')


_QWDM = [None]


def _qwdm():
    """器物点名之器（只载一回·载了即缓存；每回 exec_module 之价太贵，全书回灌时尤甚）。"""
    if _QWDM[0] is None:
        import importlib.util as _u
        _s = _u.spec_from_file_location('qwdm', os.path.join(ROOT, '工具', '器物点名.py'))
        _m = _u.module_from_spec(_s)
        _s.loader.exec_module(_m)
        _QWDM[0] = _m
    return _QWDM[0]


_DUTY_CACHE = {}


def duty_clear_cache():
    """清必答表之缓存（凡在同一进程里改过正文者，须先清）。"""
    _DUTY_CACHE.clear()


def duty_list(n, r):
    """必答表（带缓存·其体见 _duty_list_raw）。"""
    key = (n, r)
    if key not in _DUTY_CACHE:
        _DUTY_CACHE[key] = _duty_list_raw(n, r)
    return _DUTY_CACHE[key]


def _duty_list_raw(n, r):
    """【批124·必答表】某轮该碰的地方，由正文自己长出来。
    立此表之由（作者问「怎么保证每一轮真干活」）：**努力不可观测**，
    可观测的只有痕迹，而痕迹能被无意地演出来（照着「一轮好轮记的样子」去凑）。
    故不测努力，改测**覆盖**：该碰的地方有没有全碰到。
    清单自正文抽取，正文一变清单即变，**事先凑不了**。
    返回 (必答项列表, 说明)。空列表＝该轮无可机抽之必答项，由人裁。"""
    src = find_chapter(n)
    if not src:
        return [], '无正文'
    txt = open(src, encoding='utf-8').read()
    body = txt.split('【本章亮点】')[0]
    if r == 1:
        return ['嗅', '听', '触'], '三密度须逐项报数（机器数与实计并报）'
    if r == 2:
        # ★2026-09-05 抽词之式移入 _回述项()（其由见彼处）。
        return _回述项(body)
    if r == 3:
        # 【批124·校准】本轮之职为「核数据主张」，非「数一切量词」。
        # 「一下／一个／一回／一样／一段／一口／一层」等为口语量词，不作主张，
        # 逼其逐个核即是喊狼来了（会喊狼的核对器比没有更糟）。
        # 故只收：①二以上之数 ②带天/日/年/圈/尺/寸/步/成之数 ③「前N…」「第N…」之序数主张。
        # ★2026-09-05 抽数之式移入 _数项()（其由见彼处）——一处判，一份码，负测方够得着它。
        return _数项(body)
    if r == 4:
        # ★★★★★2026-08-19 改·深掘轮之必答表。
        # ★而其前身为「十招逐招标在或缺」——那是查，查完字数一分不长。
        # ★★而本表逼的是「推」：一事之下须列层，逐层问其底下还有没有一层。
        # ★★★而「层」自开镜卡之五层取来；机器只验其数与其裁，不代人想。
        return (['第一层', '第二层', '第三层', '第四层', '第五层', '已到底', '深掘所得', '招式附检'],
                ('★深掘轮：一事之下逐层下探。'
                 '★★每一层须答一句「这一层底下还有没有一层」——'
                 '答得出即当场写进正文并复量四数；答不出即明记「已到底」及其由。'
                 '★★★而「深掘所得」一项须报本轮新写了几层、净重增了多少；'
                 '★★★★而「招式附检」为旧升华庭之遗，十招只作附检，一行带过即可。'))
    if r == 5:
        who = [w for w in ('老头', '钱满', '刘二', '东头', '沈鸢', '陈砚') if w in body or w in ('沈鸢',)]
        # ★★★★★2026-08-16 补：其先前只逼「说明其去向」——
        # ★而「判零处而合，其类为本不在场」这一句，八十五章过了八十五次闸，每次都对，合起来是错的。
        # ★★故加一项：暗线之账——须报「其末见於第几章、距今几章、本轮补不补」。
        # ★★★而其据为圣经原文：「副线（好几条线同时走）：逐卷插2—4篇视角」。
        who = who + ['暗线之账']
        return who, ('每一在场人物须报其分位分布；零处者须说明其去向。'
                     '★★★★★而「暗线之账」一项须逐一报：末见於第几章、距今几章、本轮补不补；'
                     '★零处者不得只书「本不在场」，须并报其距——而距逾80章者，本轮须补一处回切或插一篇暗线章。')
    if r == 6:
        # ★2026-09-05·机制总审丙⑭之一：此表原写死十二样——**而写死的表只认它立表那一天的器物**；
        #   ★本书第301章起有器物册（`版本/第N章/_器物.md`），册上之器由本章自报，後来新添之物只在册上，不在此表；
        #   ★★故改为「写死之十二样 ∪ 本章册上之器 ∪ 上一同线章册上之器」——**册在则以册为主，册不在则照旧十二样**。
        #   ★★★它认哪几样：**十二样旧器＋册上诸器**；本书今有册 11 份（296—305），其上之器 30 样，
        #     其中不在旧十二样者如「担架／毡子／针／竹片／炭／本子那一页」——**旧表一样也点不到它们**。
        props = ['绳', '灯', '刀', '架子', '本子', '笔', '腿上', '鞋', '水', '盐', '布包', '竹筒']
        try:
            _m6 = _qwdm()
            _seen = set(props)
            for _src in (n, _m6.上一同线章(n)):
                if not _src:
                    continue
                _rows6 = _m6.读册(_src)
                _rows6 = _rows6[0] if isinstance(_rows6, tuple) else (_rows6 or [])
                for _row in _rows6:
                    _名 = _row.get('名') if isinstance(_row, dict) else None
                    if _名 and _名 not in _seen and len(_名) <= 6:
                        _seen.add(_名)
                        props.append(_名)
        except Exception:
            pass
        return props, '器物逐件点名：在场者报其处，零字者判该点或不该点（★册上之器一并上桌）'
    if r == 7:
        return ['时标', '句长方差', '段长90分位', '说破密度'], '时序须逐时标核日；节奏与留白须报数并横比'
    if r in (8, 9):
        # ★2026-09-05·机制总审（八路·覆盖之缺审第9条·P21 整句复述复发7）：第8轮另上「复述」之项——
        #   本章凡 ≥10 字之整句与任一前章逐字同者，逐句上桌（式「复述·首十二字←第M章」），判「有意的回响」或「懒的搬」。
        #   ★其器 工具/整句复述哨.py（全书 357 处／165 章，故不判红只上桌）；第9轮不重上（一事不两裁）。
        项 = ['刀数', '减字']
        if r == 8:
            try:
                import importlib.util as _u
                _sp = _u.spec_from_file_location('zjfs', os.path.join(ROOT, '工具', '整句复述哨.py'))
                _m = _u.module_from_spec(_sp)
                _sp.loader.exec_module(_m)
                项 += _m.必答项(n, body)
            except Exception:
                pass
        return 项, ('减法轮须报刀数与实减字数'
                    + ('；★「复述·…←第M章」逐句须判：合（有意之回响）／删（懒的搬）' if len(项) > 2 else ''))
    if r == 10:
        return ['器物总账', '逐段生死'], '收官轮须出器物总账并逐段判生死'
    if r == 11:
        # 2026-08-19 立·作者令：编辑、广大读者、专业作家、读者本人，四个角度去读。
        # 前十轮皆自作者之内眼看（查错、对数、逐层）；而一章之好坏末了不由作者定，
        # 由读它的人定。故立四方庭：四席各有其问，其问互不可代。
        return (['读者之眼', '作家之眼', '编辑之眼', '作者之眼', '四席之判', '刁钻一问'],
                ('四方庭：一章须过四席。'
                 '①读者之眼：读得下去吗？哪一段会走神？看完记住了哪一样？'
                 '②作家之眼：有没有一处是别人写不出来的？其手法可有偷懒？'
                 '③编辑之眼：这一章能不能删？删了全书断什么？读者凭什么翻下一页？'
                 '④作者之眼：这一章离我心里那个样子还差多远？'
                 '而四席之判须逐席给一句定论（过／不过＋其由）；'
                 '而刁钻一问须自问一句最难堪的——一个存心挑刺的人读完，'
                 '他会拿哪一句来打这一章。'))
    if r == 12:
        # 2026-08-19 立·作者令：500%的功率去跑，不能只用10%。
        # 功率不可直测；可测者为：前十一轮凡判合／已到底／不补之处，回头再问一遍——
        # 而应付之轮，其判合处必经不起第二问。
        # ★2026-09-05·机制总审（八路·覆盖之缺审第7条·P12 题眼自毁复发3 与 LAW-288A 同族皆无闸）：加一项「题眼复问」——
        #   本章自立之律（象征物之法则／自定之规矩）有没有被本章末拍自己推翻；机器判不了，故只上桌逼人答。
        return (['判合复问', '已到底复问', '不补复问', '翻案几处', '功率自评', '题眼复问'],
                ('极限轮：把前十一轮凡判「合／已到底／判不补」之处逐一复问。'
                 '其法：不看当初之裁语，只看正文那一处本身，重判一次。'
                 '而翻案几处须报实数——零翻案者，须明写何以前十一轮无一处判错；'
                 '而功率自评须逐轮报：这一轮我用了几成力，其凭据为何。'
                 '★而题眼复问须答一句：本章自立之律，末拍有没有自己推翻（P12／LAW-288A）——答「无」者须指出立律之拍与末拍。'))
    if r == 13:
        # 2026-08-19 改·作者令：「最后一轮是一个检测，要看每一轮有没有尽最大的功力去跑、
        #   有没有跑到最好；而最后一轮就是对这篇文章的质量来进行一个全面彻底的升级。」
        # 故本轮之职有二，且其序不可颠倒：
        #   甲·逐轮回检：十二轮逐轮问「这一轮尽力了没有」——不尽力者，当场补跑。
        #   乙·全章升级：通读一遍，凡有一处能更好的，当场改——本轮是「改」，不是「查」。
        # 而其判之尺不是「过不过闸」，是「这一句拿给最好的小说家看，他会怎么改」。
        return (['逐轮回检', '不尽力之轮', '补跑几轮', '全章升级', '升级几处',
                 '最神一句', '最弱一句', '配不配'],
                ('升华定稿轮·其职有二，序不可颠倒。'
                 '甲·逐轮回检：第1至12轮逐轮问一句「这一轮尽最大功力了没有」——'
                 '答「没有」者须报其轮号，并当场补跑那一轮（不补跑即不许进乙）。'
                 '乙·全章升级：通读一遍，凡有一处能更好的当场改；'
                 '而「升级几处」须报实数，零处者须明写何以全章无一处可再好。'
                 '而「最弱一句」须指名道姓——一章之中必有最弱者，指不出即是没读透。'
                 '而「配不配」须给一句定论：这一章配不配放进中国第一的小说里；'
                 '答「配」者须说出它凭什么配——说不出，就是不配。'))
    return [], '本轮无可机抽之必答项'


def bida(n, r):
    """印某轮之必答表。"""
    items, why = duty_list(n, r)
    print('\n████ 第%d章 · 第%d轮 必答表 ████' % (n, r))
    print('  【why】%s' % why)
    print('  【立表之由】努力不可观测，覆盖可观测。此表自正文抽出，正文一变表即变，事先凑不了。')
    if not items:
        print('  本轮无可机抽之必答项，由人裁。')
        return 0
    print('  必答 %d 项：' % len(items))
    for i, x in enumerate(items, 1):
        print('   %2d. %s' % (i, x))
    print('  【交法】本轮轮记须逐项交代（改／判合＋记因）。总核轮按覆盖率验收。')
    return 0


# ★★★★★2026-09-11 补二字（315 收口当场自逮）：**词表里没有「删」，也没有「刀」**——
#   ★其实证逐字：315 第8轮之必答「1. **刀数**：**一刀**（行305，只删不添）。
#     ⛔**白文别处一字未动；骨记同笔添⑰⑱两条。**」——**这是一句明明白白的裁**，
#     而窗内 VERDICT 一个词也不命中，**裁定率遂判 0%（0/2）**。
#   ★★而「只删不添」正是本仓十三轮里最常见的一种裁（修席、减法、时序诸庭皆以删为刀）——
#     **即：这一洞不是偶发，是把一整类裁判成了没裁。**
#   ★★★而补这二字不致放松：`_judged_near` 之第二层仍索「剔去清单与判语记号之後，
#     余文须 ≥8 字，且 ≥20 字或含实据（数／其由／係／印／据／凭）」——
#     **抄一遍清单每行加一个「删」字，照旧不过**（其证在 `工具/负测_裁语词表.py` 之②）。
VERDICT = ('✓', '合', '改', '核', '真伤', '判', '未见', '零', '缺', '对', '错', '撞', '补',
           '删', '刀')

# ★2026-09-05·机制总审丙⑧之治：裁定查之「近旁有裁语」本身有两个洞（本坐上磁盘坐实）：
#   ★①**抄一遍清单，每行加一个「对」字，裁定率即 100%**（六轮实测皆 100）；
#   ★②**更隐者：项自己带裁语之字即自绿**——如「三对」「一对」之项（同指对，甲一所加），
#      纯抄清单一字不加，第300章第11轮裁定率仍报 100%。**器把清单当成了活。**
# ★★故改判据为两层（判据之改须不误伤旧章：本坐以磁盘上 151 章 1777 轮回灌，
#   新旧两式逐轮同判——⛔114 ⚠247 ✓1416，一轮不动；见 selftest 之「裁定查·全书回灌」）：
#   **①裁语须出在「余文」里**——即窗内之字先剔去本轮必答项之原文，再剔去标点；
#   **②余文除裁语之外，还须有本轮自己的字**（≥8字），且**其中须见实据**（数带量词／拍号／器印／其由）
#      **或余文本身够长（≥20字）**。
# ★★★它认哪几样：**纯抄清单（0%）｜抄清单加一个「对」（0%）｜项自带裁语之字而自绿（0%）**——
#   本书同类之器共三样（覆盖查·裁定查·对数查），此为其二。
# ★★★★它认不得哪一样（须直说）：**一句像样的套话**（「判合，其由见上，已核过一遍，无真伤」）
#   **照旧 100%**——**认字之器认不得诚意**；其守不在此闸，在对数查（轮记之数须与台账相符）
#   与十一轮之器印（数得自器，写不出来）。**故此闸只拦「连话都懒得编」，不拦「话编得像」。**
_JUDGE_MARK = re.compile(r'[\s\*\-·|「」（）()【】：:；;，,。．\.、>#…—～~]+')
_JUDGE_REAL = re.compile(
    r'[0-9０-９]'
    r'|[〇零一二三四五六七八九十百千]\s*(?:刀|拍|字|处|行|层|个|回|下|段|页|寸|分|口|样|针|条|根|轮|章|句|件|遍)'
    r'|py|其由|因|係|见|印|据|凭')


def _judged_near(seg, items_desc, minres=8, longres=20):
    """窗内之字够不够算「裁过」。items_desc：本轮必答项，按长到短排（先剔长者）。"""
    res = seg
    for y in items_desc:
        res = res.replace(y, '')
    res = _JUDGE_MARK.sub('', res)
    if not any(v in res for v in VERDICT):
        return False
    own = res
    for v in VERDICT:
        own = own.replace(v, '')
    if len(own) < minres:
        return False
    return len(own) >= longres or bool(_JUDGE_REAL.search(own))


def 必答之锚(x):
    """★把一条必答项化作它的「锚」——⛔**其所指之实，去其装饰**。

    ⛔**其所由来·0916·339 第8轮之实**：必答项作 `复述·她的手从被子底下进去摸到←第333章`，
      **而轮记写的是**「①「她的手从被子底下进去摸到…」（339:73，逐字同 333:237……）——**留**。」
      ★**八项逐项如此，项项有判、有据、有行号**；**而闸判「提及 1/8、裁定 1/8」。**
    ★★**其由**：`duty_cover2` 以 `re.escape(x)` 整串直配——
      **「复述·」这三字与「←第333章」这四字，席不会照写**（**它们是清单的装饰，不是书里的话**）。
    ★★★**而其果最刺目者，本坐当场拿沙盘量过**：
      **同一轮之实文得 12%，而「把清单逐行抄一遍、每行後缀一句『判合，其由：……』」得 100%**
      ——⛔**而本闸之罚辞逐字写着「抄清单不算干活」。**
      **即：闸说抄清单不算干活，闸的码说只有抄清单才算干活。**
    ★★★★**故今只改一样：拿锚去配，不拿整串去配。**
      ⛔**防作弊那一层（`_judged_near`：裁语须出在剔去清单之余文里）一格未动**——
      **本改只增召回（认得出老实话），不减精度（照旧防得住抄）。**
    """
    y = str(x)
    if '·' in y:
        y = y.split('·', 1)[1]          # 去「复述·」一类之头
    y = re.sub(r'←.*$', '', y)          # 去「←第333章」一类之尾
    return y.strip()


def duty_cover2(n, r, logtext, win=70):
    """【批125·逐项裁定查】覆盖查只测「提没提」，而**抄一遍清单就能得100%**——
    那才是最像干活的偷懒。故加一层：每一必答项之近旁（±win字）须见裁语，
    方算「碰过」；只提名而无裁，计入「提了没裁」。
    ★2026-09-05 补第二层（见上 _judged_near 之注）：裁语须出在剔去清单之余文里，
      且余文须有本轮自己的字与实据——**否则抄清单加一个「对」字即满分**。
    返回 (提及率, 裁定率, 提及数, 裁定数, 总数, 只提未裁之项)。"""
    items, _ = duty_list(n, r)
    if not items:
        return None, None, 0, 0, 0, []
    desc = sorted(items, key=len, reverse=True)
    ment, judged, naked = 0, 0, []
    for x in items:
        # ★先拿整串配（旧式，一格未减）；配不着再拿其锚配（0916 新增之召回）
        pos = [m.start() for m in re.finditer(re.escape(x), logtext)]
        if not pos:
            _锚 = 必答之锚(x)
            # ⛔锚太短者不认（如「刀」「灯」之类，拿它去配即满纸皆是）——
            #   **其界取 4 字**：⛔**短於此者只走旧式，宁可漏，不可假。**
            if len(_锚) >= 4 and _锚 != x:
                pos = [m.start() for m in re.finditer(re.escape(_锚), logtext)]
        if not pos:
            continue
        ment += 1
        ok = False
        for i in pos:
            seg = logtext[max(0, i - win):i + len(x) + win]
            if _judged_near(seg, desc):
                ok = True
                break
        if ok:
            judged += 1
        else:
            naked.append(x)
    tot = len(items)
    return ment * 100 // tot, judged * 100 // tot, ment, judged, tot, naked


def metric_reconcile(n, r, logtext):
    """【批125·对数查】轮记所报之数须对得上机器所记之数。
    立此查之由：**说了不算，得对得上**——凡未真跑量器而凭印象写的轮记，
    其数必与台账所存对不上；对得上者，至少证明写记时人眼在机器输出上。
    验：本轮之版所记诸软项（净重／段数／长段数／嗅／触／四字串三现）之数值，
    须至少有 2 个以字面出现在其轮记里。"""
    d, led = paths(n)
    if not os.path.exists(led):
        return None, []
    for x in json.load(open(led, encoding='utf-8')).get('版本', []):
        if _round_of(x.get('说明', '')) != r:
            continue
        sf = x.get('soft') or {}
        keys = ['净重', '段数', '长段数', '嗅', '触', '四字串三现']
        # ★2026-09-05·机制总审（八路·流程之缝审第3条）：旧式 `str(数) in logtext`——单位数（长段数0／嗅3）在任何文里都在，对数查永不红。
        #   今须「名与数相邻」（名後至多三个连接符再接其数，如「嗅6」「嗅：6」「嗅 6」「嗅＝6」）。
        hit = [k for k in keys if k in sf and re.search(re.escape(k) + r'[：:＝= ]{0,3}' + re.escape(str(sf[k])) + r'(?!\d)', logtext)]
        return len(hit), [k for k in keys if k in sf and k not in hit]
    return None, []


def jinli(n):
    """【2026-08-19·尽力查】作者令：「你的目的不是为了跑完，是为了把质量达到最高。
    这个闸需要做这么一个事情叫质量检测：这一轮有没有尽全力去跑，把质量已经跑到最高了。」

    ★立此查之由（全书最要之一处补漏）：
      先前九道闸（六闸＋覆盖查＋对数查＋产出基线查）**测的全是「有没有错」，
      没有一道测「够不够好」**。故一章可以十四检全绿而事小、层薄、字少——
      而机器一路报✓，因为它只管2000之下限。
    ★★而其证：181—208均5770（标准差68），209起均3428——掉四成而无一闸出声。

    ★★★而本查之难处在「尽力不可观测」。故不测尽力，改测**尽力必留之三样痕迹**：
      甲·**层数**：一事之下推了几层（深掘轮之实）——层薄者，事必小。
      乙·**产出**：全章十轮之净重曲线，是往上长还是原地打转。
      丙·**到底**：有几层明记「已到底」及其由——一层不记者，多半是没问到底。
    ★★★★三者皆自磁盘取，事先凑不了；而三者俱低即判「跑完了，没跑透」。
    """
    d, led = paths(n)
    if not os.path.exists(led):
        print('  ✗第%d章尚无台账' % n)
        return 2
    lg = json.load(open(led, encoding='utf-8'))
    vs = lg.get('版本', [])
    lj = _lunji_blocks(n)
    allt = '\n'.join('\n'.join(v) for v in lj.values())
    src = find_chapter(n)
    body = open(src, encoding='utf-8').read().split('【本章亮点】')[0] if src else ''
    net_now = len(re.sub(r'\s', '', body))
    hard, warn = [], []

    print('\n████ 尽力查 · 第%d章 ████' % n)
    print('  【why】不测「跑完了没有」，测「跑透了没有」。')

    # 甲·层数
    print('\n  ── 甲·层数（一事之下推了几层）──')
    ceng = len(set(re.findall(r'第([一二三四五六七八九十])层', allt)))
    ceng2 = len(re.findall(r'★+\s*[一二三四五六七八九十]层', allt))
    n_ceng = max(ceng, ceng2)
    print('   轮记所见之层：%d 层' % n_ceng)
    # 【第102批·回修令】旧制封版之章只报不拦：★深掘轮（第4轮）系217章方立；
    #   ★★而其前之章，第4轮跑的是旧制别的镜头，轮记里自然没有「第N层」之语。
    #   ★★★拿今日之尺去量，则每一章回修都必然红在层数——那不是这一刀之伤。
    #   ★★★★而「只报不拦」不是放过：报仍在，作者见得着；拦的是不该拦的那一下。
    if n_ceng < 3:
        if _is_old_era(n):
            print('   ⚠只推得出%d层（★而本章系旧制封版，深掘轮尚未立；'
                  '此项只报不拦）' % n_ceng)
        else:
            hard.append('一事之下只推得出%d层——层薄即事小，本章须回第4轮深掘' % n_ceng)
    elif n_ceng < 5:
        warn.append('层数%d（<5），须于轮记明记何以不足五层' % n_ceng)
    else:
        print('   ✓五层以上，事之厚薄合格。')

    # 乙·产出曲线
    print('\n  ── 乙·产出（十轮之净重曲线）──')
    ws = [x.get('soft', {}).get('净重') for x in vs if x.get('soft', {}).get('净重')]
    if len(ws) >= 3:
        w0, wmax, wend = ws[0], max(ws), ws[-1]
        gain = wend - w0
        print('   起 %d ｜ 峰 %d ｜ 终 %d ｜ 净增 %+d（%+.0f%%）'
              % (w0, wmax, wend, gain, 100.0 * gain / w0))
        # ★2026-08-19 订：原判「净增≤0 即硬拦」——而此判过硬，有二不当：
        #   ①减法轮本就该减；一章若前段深掘充分、后段减得狠，其净增可为负而质量更高。
        #   ②回归之桩净重恒定，必被误拦（本会话实见）。
        # ★★故改：只看「峰」与「起」之差——即这十几轮里，有没有哪一轮真让它长过。
        #   长过而后减，是好刀；从头到尾没长过，才是十轮只在修补。
        grew = wmax - w0
        # ★★★★★2026-09-10·311 实卡所治（其形须写全，免下一坐当它是放水）：
        #   ★**旧判之尺是「峰 − 起」**，其所假定者：**起草那一版是这一章的地板**。
        #   ★★而 311 打破了这个假定：起版 2768 里有四句「说明句」（「这一张纸是拿来看图的」
        #     「所以这个数大」…），诸轮把它们逐句削去（→2590）——**那是好刀，不是修补**；
        #     其後五路深掘落了三层（道与回／过夜之紧一线／他没有问／钱满那只手之照／那一格之两个点）
        #     （→2743），**而仍低於起版 25 字**。於是旧尺印「自起版至峰值一字未长」——
        #     ★★★**它量不出「先削掉假的，再长出真的」这一条路**：
        #     **一章削去说明句而後掘出真层，与一章从头到尾只在修补，在旧尺上是同一个数。**
        #   ★★★★**故补第二把尺，不动第一把**：**谷之後有没有长过**（终 − 谷）。
        #     **两把尺俱不过，才判红**：既没长过起版，**又**自最低处起再没长过——**那才是只在修补。**
        #   ★★★★★**其非放水之凭**（负测 `工具/负测_产出曲线.py` 逐局回灌）：
        #     **一份从头到尾只降的台账（2768→2700→2600→2500），两把尺俱不过，照旧判红。**
        #     ⛔**而本处之改，一个字也没有放松「不许补字」那一条**——311 之绿不是靠添字得的，
        #     是靠「削去说明句 −178｜掘出真层 +153」这两笔各自可数、各自可查得的。
        wmin = min(ws)
        _i谷 = ws.index(wmin)
        rise = (wend - wmin) if _i谷 < len(ws) - 1 else 0     # 谷在末版则无「谷之後」
        if grew <= 0 and rise <= 0:
            hard.append('自起版至峰值一字未长（%+d），而自谷（%d）至终亦未长（%+d）——'
                        '两把尺俱不过：十几轮只在删和改，没有一轮在长；其治是回深掘轮，不是补字'
                        % (grew, wmin, rise))
        elif grew <= 0:
            print('   ✓自起版未长（%+d），**而自谷 %d 至终长 %+d**——'
                  '係「先削去说明句、再掘出真层」之形，非只在修补。' % (grew, wmin, rise))
        elif gain < 0 and abs(gain) > grew:
            warn.append('峰值曾长%+d，而终版反低於起版%+d——减得比长得多，须核减法轮是否削了层'
                        % (grew, gain))
        elif gain < w0 * 0.10:
            warn.append('净增仅%+d（%.0f%%），十轮之功多在修补，少在深掘' % (gain, 100.0 * gain / w0))
        else:
            print('   ✓十轮之中确有所长。')
    else:
        print('   （版数不足，暂不评）')

    # 丙·到底
    print('\n  ── 丙·到底（有几层明记「已到底」及其由）──')
    daodi = len(re.findall(r'已到底|到底了|不必再推|无可再推', allt))
    print('   明记「已到底」之处：%d' % daodi)
    if daodi == 0 and n_ceng:
        warn.append('无一层明记「已到底」——没问到底者，多半是没往下问')

    # 丁2·功力回检（2026-08-19 立·作者令：「要看每一轮有没有尽最大的功力去跑。」）
    # 其测不了功力本身，测其必留之痕：一轮真尽力者，其轮记必有「真伤／治／复量」之实；
    # 而只写「判合」「零根」而无一处动手者，多半是走了个过场。
    print('\n  ── 丁2·功力回检（逐轮之动手痕迹）──')

# 【2026-08-21·修·245第13轮甲实见】上二式之字符类原作 [一二三四五六七八九十\\d]，
#   ★而 r-串中 \\d 是「反斜杠」与字母 d 两个字面字符，不是数字类；
#   ★★其果：轮记凡以阿拉伯数字写「真伤2根」「翻案2处」者一概不认，只认「真伤二根」；
#   ★★★而本册轮记通篇用阿拉伯数字——遂有八轮明明逐根落了刀，却被判为「只在判合、走了过场」，
#      并由此触硬项拦停，逼人回头去补早已补过的活。此患与旧日「\n## 分块丢补记」同类：
#      器报的不是活没干，是器看不见活。
#   ★★★★今改为 [一二三四五六七八九十\d]（真数字类），并广治痕之词表以纳本册实用之动手词
#      （补毕／今正／俱正／后移／缩为／落一短段）。
    # 第五路之料：自台账取「第N轮」之末版与其前一版之净重差（读账，不读轮记之词）
    _轮版动否 = {}
    try:
        _vs = json.load(io.open(led, encoding='utf-8'))['版本']
        _末 = {}
        for _i, _x in enumerate(_vs):
            _m2 = re.match(r'第(\d+)轮', _x.get('说明', ''))
            if _m2:
                _末[int(_m2.group(1))] = _i
        for _rr, _i in _末.items():
            _cur = (_vs[_i].get('soft') or {}).get('净重')
            _pre = (_vs[_i - 1].get('soft') or {}).get('净重') if _i > 0 else None
            if _cur is not None and _pre is not None and _cur != _pre:
                _轮版动否[_rr] = _cur - _pre
    except Exception:
        pass
    _idle = []
    for _r in sorted(lj):
        _b = '\n'.join(lj[_r])
        _zs = len(re.findall(r'真伤[一二三四五六七八九十\d]+根', _b))
        _zhi = len(re.findall(r'其治|已治|当场治|补於|改作|削|斩|补毕|今正|俱正|後移|后移|缩为|落一短段', _b))
        _fl = len(re.findall(r'复量|复扫|复跑|复核', _b))
        # 【2026-08-19·修】原判只数「治／复量」之字面词频，而 _zs（真伤N根）算了却没用；
        #   ★其果：一轮明写「真伤三根，三处俱治」者，字面只有一个「治」，遂被判为走过场。
        #   ★★而真伤之数才是动手之实凭——一根真伤必有一处落刀，否则它不叫真伤。
        #   ★★★故加一路：凡轮记明记真伤（或翻案）者，即为有动手之痕。
        _fan = len(re.findall(r'翻案[一二三四五六七八九十\d]+处', _b))
        # 【2026-08-22·修】247至250连四章，第1、4、5轮皆被判「无动手之痕」，而那几轮实增数百字并立层立身。
        #   ★究其由：本器只认「治／复量／真伤N根／翻案N处」四路，而十三轮之中另有三轮，其职本不在治：
        #     第4轮深掘轮之职在掘层，第5轮在场庭之职在落身，第10轮收官轮之职在判死与移位；
        #     此三轮之实，落在「掘出N层／增N字／落身N处／判死N段／移位N处」上，而器一样也不认。
        #   ★★而其治不可是「广收动手之词」——凡只认词者，写一个词即可蒙混。
        #   ★★★故今所加之路，一律须带数：掘出N层／增N字／落身N处／判死N段／移位N处。
        #      带数即是可对账之实（其数须与台账之净重曲线相符，两眼齐审时逐轮回对）。
        #   ★★★★而一轮若既无真伤、又无翻案、又无治、又报不出一个带数的产出，
        #      那它确是走了过场——此闸仍拦得住它。
        _chan = len(re.findall(
            r'掘出[^。；\n]{0,8}[一二三四五六七八九十\d]+层'
            r'|增[一二三四五六七八九十\d]+字'
            r'|落身[一二三四五六七八九十\d]+处'
            r'|判死[一二三四五六七八九十\d]+段'
            r'|移位[一二三四五六七八九十\d]+处', _b))
        # 【2026-08-22·再修】上一修加了「带数之产出」五式，然仍是认词——
        #   ★而249、250之第5轮明明各增百余字，只因写的是「净重2622→2775（增153）」而无「字」，遂仍被判走过场。
        #   ★★故再加一路，且这一路不认词，只认账：轮记里凡明记「净重A→B」而A≠B者，
        #      即是此轮动过正文之实凭——其数出自台账，作伪即与台账不符，两眼齐审时逐轮回对得出来。
        #   ★★★而A＝B者不算（正文一字未动）；一轮若连这一笔也报不出来，那它确是走了过场。
        for _a, _c in re.findall(r'净重\s*(\d+)\s*→\s*(\d+)', _b):
            if _a != _c:
                _chan += 1
                break
        # 【2026-09-02·292第12轮·极限轮所修·第五路】
        #   ★此闸至今五修，前四修皆是「再加几个词」（08-19加真伤路／08-21修数字类并广词表／
        #     08-22加带数之产出／08-22再修加净重A→B）——★★而一道靠加词修的闸，
        #     每加一个词就多一个「写这个词即可蒙混」的口，且它照旧看不见没写那个词的活。
        #   ★★★今日之实：292第7轮之轮记里有十一版回灌表、一个相关系数、一处「42→27」，
        #     **是全十轮里量得最细的一轮**，而器判它「五路俱无·走了过场」——
        #     **器报的不是活没干，是器看不见活**（此语係08-21那一修自己写下的，今日又应验一回）。
        #   ★★★★故第五路不认词，只认账：**从台账取该轮之版，与其前一版逐字比**；
        #     文动了即是动手之实凭——**这一路写什么词也蒙混不了，因为它读的是正文本身。**
        #   ★而其绿不许含糊：下印一行「凭何而绿」，见得出哪一轮是靠轮记之实、哪一轮只靠正文动过。
        _tz = _轮版动否.get(_r)
        _by = []
        if _zs >= 1 or _fan >= 1: _by.append('真伤/翻案')
        if _zhi >= 2: _by.append('治')
        if _fl >= 2: _by.append('复量')
        if _chan >= 1: _by.append('带数之产出')
        if _tz: _by.append('正文实动%+d字' % _tz)
        _mark = '✓' if _by else '⚠'
        if _mark == '⚠':
            _idle.append(_r)
        print('   第%-2d轮 真伤%d 治%2d 复量%2d 产出%d %s %s'
              % (_r, _zs + _fan, _zhi, _fl, _chan, _mark, '｜凭：' + '、'.join(_by) if _by else ''))
    # 两数并印（292第13轮甲立）：轮记见几轮、台账见几轮。不符即出声——
    # 一份只列十轮而台账说跑了十二轮的回检，它漏的那两轮不会自己举手。
    _账轮 = sorted(_末.keys()) if _末 else []
    _记轮 = sorted(lj.keys())
    print('   ── 轮记见 %d 轮（%s）｜台账见 %d 轮（%s）──'
          % (len(_记轮), '、'.join(str(x) for x in _记轮) or '无',
             len(_账轮), '、'.join(str(x) for x in _账轮) or '无'))
    _缺记 = [x for x in _账轮 if x not in lj]
    _缺账 = [x for x in _记轮 if x not in _末]
    if _缺记:
        warn.append('台账有而轮记无者第%s轮——那一轮存了版而没留话，回检看不见它'
                    % '、'.join(str(x) for x in _缺记))
    if _缺账:
        warn.append('轮记有而台账无者第%s轮——那一轮写了话而没存版（或其版之说明未报轮号）'
                    % '、'.join(str(x) for x in _缺账))
    if _idle:
        warn.append('第%s轮无动手之痕（治、复量、真伤、翻案、带数之产出，五路俱无）——须自问那几轮是不是走了过场'
                    % '、'.join(str(x) for x in _idle))
    if len(_idle) >= 4:
        hard.append('无动手之痕者达%d轮——过半之轮只在判合，'
                    '其治是回那几轮补跑，不是往下走' % len(_idle))

    # 丁·横比（与全书之势）
    print('\n  ── 丁·横比（本章之厚薄在全书何处）──')
    import glob as _g
    allw = []
    for f in _g.glob(os.path.join(ROOT, '正文', '*章*.md')):
        tt = open(f, encoding='utf-8').read().split('【本章亮点】')[0]
        allw.append(len(re.sub(r'\s', '', tt)))
    if allw:
        allw.sort()
        rank = sum(1 for x in allw if x < net_now)
        pct = 100 * rank // len(allw)
        med = allw[len(allw) // 2]
        print('   本章 %d 字｜全书中位 %d｜本章位於第 %d 百分位' % (net_now, med, pct))
        if pct < 25:
            warn.append('本章厚薄在全书末四分之一（第%d百分位）——须自问这一事是不是切得太小' % pct)

    print('\n  ══════════════════════════════════════════')
    if hard:
        print('  【尽力查·不过】硬项 %d 条：' % len(hard))
        for h in hard:
            print('     ⛔ %s' % h)
        for w in warn:
            print('     ⚠ %s' % w)
        print('  ★而其治不是补字，是回第4轮把没推的那一层推下去。')
        print('  ══════════════════════════════════════════')
        return 2
    for w in warn:
        print('     ⚠ %s' % w)
    print('  【尽力查·通过】层够厚、有所长、问到底。')
    print('  ══════════════════════════════════════════')
    return 0


def duty_cover(n, r, logtext):
    """算某轮之覆盖率：必答项中有几项在其轮记里被点到。"""
    items, _ = duty_list(n, r)
    if not items:
        return None, 0, 0
    hit = [x for x in items if x in logtext]
    return (len(hit) * 100 // len(items)), len(hit), len(items)


def _造式判(n):
    """★2026-10-08·造式（作者令「名著是写出来的，不是改出来的」·`工具/席/一章.js` 之 args.式==='虫洞'）：
    本章是不是造式之章、造式之实缺什么。**判据只一处，在 `工具/造式.py`**（⛔不另抄一份——抄一段闸的逻辑就生一个不会同步的双胞胎）。
    ★以 `JJ_DIR` 之上一层为仓根（负测换 ROOT／JJ_DIR 时随之走）。
    ⛔挂着 `_式.md` 而判据取不到者，判「缺」——不许读不出就放行。返回 (是造式, 所缺)。"""
    if not os.path.exists(os.path.join(JJ_DIR, '第%d章' % n, '_式.md')):
        return False, []
    try:
        import importlib.util as _u
        _sp = _u.spec_from_file_location('_zaoshi', os.path.join(os.path.dirname(os.path.abspath(__file__)), '造式.py'))
        _zm = _u.module_from_spec(_sp)
        _sp.loader.exec_module(_zm)
        return _zm.判(n, os.path.dirname(JJ_DIR))
    except Exception as _e:
        return True, ['造式之判跑不起来（%s）——⛔读不出不放行' % _e]


def zonghe(n):
    """【批123·第十一轮·总核轮】十轮跑完之后的那一轮，专核前十轮「跑满」与「跑透」。
    立此轮之由（作者令）：十条记录齐全不等于每一轮真干了活；
    而本会话已实证漏跑之链（P28），故须有一轮专门回头查，且其结论须能禁封版。
    四查一断：甲·跑满查（版与轮记齐否）乙·跑透查（空轮／实质／镜头相符／补存／兑现）
    丙·状态查（旗／正文与末版）丁·横评择优。任一硬项不过即不出总核凭据，封版闸据此拦。"""
    d, led = paths(n)
    if not os.path.exists(led):
        # 【批127】拆出之章无自己的台账，其十轮即母章之十轮（母章第9轮拆出、第10轮覆盖两章）。
        # 此为正当情形，非缺轮：故认母章之账，并印明所认为何。
        pd, pled = paths(n - 1)
        plj = _lunji_blocks(n - 1)
        ptxt = '\n'.join('\n'.join(v) for v in plj.values())
        if os.path.exists(pled) and ('拆' in ptxt and str(n) in ptxt):
            print('\n  ℹ第%d章无自己的台账：其系第%d章第9轮依三步法拆出，'
                  '十轮之版与记俱在母章。**左眼改核母章第%d章。**' % (n, n - 1, n - 1))
            # 【批127·修】此处原顺手写 _总核.json 作凭据——**等于左眼一只眼就把封版闸开了，绕过右眼**。
            # 凭据只许由 小说检察官 --十一轮（两眼齐审）写出。此处只返回左眼之结论。
            return zonghe(n - 1)
        print('  ✗第%d章尚无台账，亦未见其为拆出之章。' % n)
        return 2
    lg = json.load(open(led, encoding='utf-8'))
    vs = lg.get('版本', [])
    lj = _lunji_blocks(n)
    src = find_chapter(n)
    txt = open(src, encoding='utf-8').read() if src else ''
    hz = ''.join(c for c in txt if '\u4e00' <= c <= '\u9fa5')
    hard, soft_warn = [], []

    print('\n████ 第十一轮·总核轮 · 第%d章 ████' % n)

    # 甲·跑满查
    print('\n  ── 甲·跑满查 ──')
    byr = {}
    for x in vs:
        r = _round_of(x.get('说明', ''))
        if r:
            byr.setdefault(r, []).append(x)
    # 【第102批·回修令】旧制封版之章，须按其封版时之轮制量，不按今日之 ROUNDS。
    #   ★其由：十三轮制立於217章；而217之前104章皆十轮制所封。
    #   ★★若拿今日之尺去量昨日封的章，则每一章回修都必然红在「缺11/12/13轮」——
    #      而那不是这一刀之伤，是制度换代之常态。
    #   ★★★故：取本章「有版之轮」之最大值为其制；十轮制之章按10轮量。
    #   ★★★★而新章（未封版者）一律按 ROUNDS 量，此路不放行。
    _era = 10 if _is_old_era(n) else ROUNDS
    if _era != ROUNDS:
        print('   ℹ本章系旧制（%d轮制）封版，按其自身之制量；今制为%d轮。'
              % (_era, ROUNDS))
    # ★★2026-09-09·与 `工具/十轮精进.py` 同笔改（**同一段逻辑抄在两个器里，改一处另一处照旧红**——
    #   此係本仓一处旧病，今日为它记一笔：**抄一段闸的逻辑，就是给它生一个不会同步的双胞胎**）。
    #   其理见 十轮精进.py 同处之注：轮记是强证，存版是弱证；存过版或轮记有实文（≥120字）者，皆算跑过。
    def _有实记(i):
        b = '\n'.join(lj.get(i, []))
        return len(re.sub(r'\s', '', b)) >= 120
    # ★★2026-10-08·造式之章（`版本/第N章/_式.md`·其判在 `工具/造式.py`）：⛔无审改之轮（三庭／五庭／修席／极限），
    #   故「十轮之版与记俱齐」问的是另一制之章——**改问造式之实**（三稿／三构思／行家评之名次·致命·大进·逐条回话／
    #   轮记之合稿·逻辑审·盲读），缺一样即硬项；⛔**非豁免**：挂了牌而无其实，照旧不过。
    #   ★而在册之轮（机闸之第3轮）照旧须有轮记——跑过的那一轮，一格不松；乙丙丁诸查亦一格不动。
    _造, _造缺 = _造式判(n)
    print('   有版之轮：%s' % ('、'.join(str(i) for i in sorted(byr)) or '无'))
    print('   有记之轮：%s' % ('、'.join(str(i) for i in sorted(lj)) or '无'))
    if _造:
        print('   ★本章係造式之章（版本/第%d章/_式.md）：⛔无审改之轮——跑满查改核造式之实（工具/造式.py）。' % n)
        for _x in _造缺:
            hard.append('造式之实缺：' + _x)
        _缺记 = [i for i in sorted(byr) if i not in lj]
        if _缺记:
            hard.append('缺轮记之轮（在册而无记）：' + '、'.join('第%d轮' % i for i in _缺记))
        if not _造缺 and not _缺记:
            print('   ✓造式之实俱齐；在册之轮版与记俱齐。')
    else:
        miss_v = [i for i in range(1, _era + 1) if i not in byr and not _有实记(i)]
        miss_l = [i for i in range(1, _era + 1) if i not in lj]
        if miss_v:
            hard.append('缺凭之轮（既无版、轮记亦无实文）：' + '、'.join('第%d轮' % i for i in miss_v))
        if miss_l:
            hard.append('缺轮记之轮：' + '、'.join('第%d轮' % i for i in miss_l))
        if not miss_v and not miss_l:
            print('   ✓十轮之版与记俱齐。')

    # 乙·跑透查
    print('\n  ── 乙·跑透查 ──')
    prev_txt = None
    for i, x in enumerate(vs):
        vp = os.path.join(d, x.get('版', '') + '.md')
        cur = open(vp, encoding='utf-8').read() if os.path.exists(vp) else None
        r = _round_of(x.get('说明', ''))
        tag = []
        if cur is not None and prev_txt is not None and cur.strip() == prev_txt.strip():
            tag.append('**空轮（与前版逐字相同）**')
            # ★★★★★★2026-09-17（339 v03 之实·⛔同一档之内，一条律两份词表）：
            #   ⛔**此处只认「判不补」四字**；★**而同一档之 `gates()::空轮闸` 认的是
            #     `判不补|零刀|不补|无真伤` 四样**（其码就在本档 `:478` 一带）。
            #   ★★**339 v03 之说明逐字写着「……本转零刀；新见 339:137←333:85 七字跨章重出
            #     落在复述哨界底下，判留并原样报出」**——**它照存版那一口的话写了，
            #     而总核这一口不认。**
            #   ★★★**即：存版时放它过去的那句话，封版时成了它的罪状。**
            #     ⛔**一条律两份词表，而写记的人只可能照见过的那一份写。**
            #   ★★★★**故今取同一份词表**，⛔**不新造第三份**。
            if not re.search(r'判不补|零刀|不补|无真伤', x.get('说明', '')):
                hard.append('%s 第%s轮为空轮而未记判不补／零刀' % (x.get('版'), r))
        if '补存' in x.get('说明', ''):
            tag.append('补存（非当场所存）')
        if r and r in lj:
            body = '\n'.join(lj[r])
            n_ch = len(re.sub(r'\s', '', body))
            if n_ch < 120:
                hard.append('第%d轮轮记过简（仅%d字），不足以证其跑透' % (r, n_ch))
                tag.append('轮记仅%d字' % n_ch)
            # ★★★★★★2026-09-17 加词（339 第9轮之实·⛔与裁定查之治同族）：
            #   ⛔**旧式只认四个词**：真伤／判不补／零刀／判合。
            #   ★**而 339 第9轮之首行逐字係**：「**本轮无刀。读席四条逐条裁过，四条皆拒。交白卷。**」
            #     ——**一句「无刀」、一句「四条皆拒」、一句「交白卷」，全篇「判」字十五处**，
            #     **而四个词一个也不在，遂判「无裁语」之硬红。**
            #   ★★**其中「交白卷」三字，正是席令自己的话**（`一章.js` 第4轮之令逐字：
            #     「**交白卷是有用的答案**」）——⛔**即：闸不认它自己派工书上写的那句话。**
            #   ★★★**故补三词，⛔只补三词**：**无刀｜皆拒｜交白卷**。
            #     **三者皆係「本轮之结论」之说法，非顺手可撞之常字**
            #     （⛔**「拒」单字不补**——**一字太泛，撞得着别处**）。
            #   ⛔**并及本补之限**：**它只治「说法不同」这一样**；
            #     **一轮若真的什么也没写，`轮记过简（<120字）`那一条照旧先咬住它。**
            # ★★★★★★2026-09-23 再加一族（358 第10轮之实·⛔与上一补同族同治）：
            #   ⛔**旧式认得「零刀」而不认「只落一刀」**——**一刀与零刀是同一句话的两个数**。
            #   ★**358 第10轮之记逐字有**：「**本轮只落一刀。**」「**总账之判**」「**硬项合计 0**」，
            #     **通篇四千余字逐拍裁过**，而七个词一个不在，遂判「无裁语」之硬红。
            #   ★★**故补一族，⛔只补这一族**：**「落〈数〉刀」与「不落刀／未落刀」**——
            #     **与已在表上的「零刀」是同一个句式，只是数不是零。**
            #   ⛔**不补者并记在此**：「硬项合计0」「判留／判删」「本轮之判」——
            #     **前者係器之印非席之裁，後二者撞得着别处**（「判留」满纸皆是），⛔**一概不收。**
            #   ⛔**并及本补之限**：它只治「一刀二刀写成了别的形」，
            #     **一轮若真的什么也没写，`轮记过简（<120字）`那一条照旧先咬住它。**
            if not re.search(r'真伤|判不补|零刀|判合|无刀|皆拒|交白卷'
                             r'|[不未]落刀|落[一二三四五六七八九十两\d]+刀', body):
                hard.append('第%d轮轮记无「真伤／判不补／零刀／判合／无刀／皆拒／交白卷／落〈数〉刀」之裁，'
                            '不足以证其跑透' % r)
                tag.append('无裁语')
            if r in LENS_KEY and not any(k in body for k in LENS_KEY[r]):
                soft_warn.append('第%d轮轮记未见其镜头关键词%s（轮号或已漂，须人裁）' % (r, LENS_KEY[r]))
                tag.append('镜头存疑')
        print('   %-5s %-26s %s' % (x.get('版'), x.get('说明', '')[:26], '｜'.join(tag) or '✓'))
        if cur is not None:
            prev_txt = cur

    # 兑现查：轮记所称之改是否真在正文
    print('\n  ── 乙2·兑现抽查（轮记所引之句是否真在正文）──')
    print('     【读法】此为软项，不作硬拦。低命中有三种正当解：'
          '①所引系别章原场（比对canon用）②已被后头减法轮减去③引的是外部凭据。'
          '**须人裁者只有第四种：当初根本没落笔。**')
    for r in sorted(lj):
        qs = [q for q in re.findall(r'「([^」]{6,40})」', '\n'.join(lj[r]))]
        qs = [q for q in qs if len(''.join(c for c in q if '\u4e00' <= c <= '\u9fa5')) >= 6]
        if not qs:
            print('   第%-2d轮 无可抽之引句' % r)
            continue
        hit = sum(1 for q in qs
                  if ''.join(c for c in q if '\u4e00' <= c <= '\u9fa5') in hz)
        print('   第%-2d轮 引句%2d 句，现存正文 %2d 句（%d%%）%s'
              % (r, len(qs), hit, 100 * hit // len(qs),
                 '' if hit else '  ← 一句不存，须人裁：是被后轮减去，还是当初未落笔'))

    # 乙3·覆盖查（批124）：该碰的地方有没有全碰到
    print('\n  ── 乙3·覆盖查（必答表·自正文抽出，事先凑不了）──')
    print('     【读法】此测覆盖，不测努力。覆盖不足＝该轮有该碰而没碰的地方。')
    for r in sorted(lj):
        body_r = '\n'.join(lj[r])
        mp, jp, mc, jc, tot, naked = duty_cover2(n, r, body_r)
        if mp is None:
            print('   第%-2d轮 无可机抽之必答项' % r)
        else:
            mark = '✓' if jp >= 80 else ('⚠' if jp >= 50 else '⛔')
            print('   第%-2d轮 提及 %3d%%（%d/%d）｜**裁定 %3d%%（%d/%d）** %s'
                  % (r, mp, mc, tot, jp, jc, tot, mark))
            if naked:
                print('        只提未裁：%s' % '、'.join(naked[:8]))
            if jp < 50:
                # 【第102批·回修令】旧制封版之章只报不拦：★必答表随镜头而定，
                #   而第4轮之必答表系「深掘轮」之八项（217章方立）；
                #   ★★旧制之章第4轮跑的是别的镜头，其轮记自然对不上今日之表。
                if _is_old_era(n):
                    print('        ⚠裁定率低（★而本章系旧制封版，'
                          '此轮之镜头与今制不同；此项只报不拦）')
                else:
                    hard.append('第%d轮裁定率仅%d%%（%d/%d）——提了而未裁者过半，'
                                '抄清单不算干活' % (r, jp, jc, tot))
            elif jp < 80:
                soft_warn.append('第%d轮裁定率%d%%（%d/%d），只提未裁者须于回执补裁'
                                 % (r, jp, jc, tot))
        nh, nmiss = metric_reconcile(n, r, body_r)
        if nh is not None:
            print('        对数：轮记与台账相符 %d 项%s'
                  % (nh, '' if nh >= 2 else '  ← **不足2项**'))
            if nh < 2:
                hard.append('第%d轮对数不足（仅%d项与台账相符）——'
                            '未真跑量器而凭印象写记者，其数必对不上' % (r, nh))

    # 乙4·产出基线查（批125）：一章十轮而真伤寥寥者，须解释
    print('\n  ── 乙4·产出基线查（防「轮轮判合」之应付）──')
    zc = sum(len(re.findall(r'真伤', '\n'.join(v))) for v in lj.values())
    # ★★★★★2026-09-04 治（301封版之序自逮）：**这道闸写着一句它自己认不出来的话。**
    #   ★其罚辞明书「须逐轮说明何以皆无，否则视为应付」，而其判据只数「真伤」二字——
    #     **那一句「说明」写得再全，它一个字也看不见**；★★於是它给的路走不通：照它说的做，它照旧拦。
    #   ★★★故补一式，认其所索之说明：**逐轮一行，作「· **第N轮·无真伤之由**：…」，且行内须有裁语。**
    #   ★★★★而本日另逮一样，须记：**这一段判词在 `工具/十轮精进.py` 与本档里各有一份**，
    #     **改了前一份，器照旧印旧数**——**一处判，两份码；而改一份的人以为自己改完了。**
    _said = {int(m.group(1)) for m in re.finditer(
        r'·\s*\*\*第(\d+)轮·无真伤之由\*\*(?P<尾>[^\n]*)', '\n'.join(
            '\n'.join(v) for v in lj.values()))
        # ★裁语只在其尾上找：**标头自带「真伤」二字，拿整行去找即永远为真**（本日自逮）。
        if any(x in m.group('尾') for x in
               ('✓', '合', '改', '核', '真伤', '判', '未见', '零', '缺', '对', '错', '撞', '补', '⛔'))}
    # ★★★★★★2026-09-17·MECH-343-真伤之词 之治（其裁见 `设定/机制体检账.md` 八十二）：
    #   ⛔**旧式只问「文里有没有『真伤』二字」**——**它数的是那两个字出现过没有，不是那一刀落过没有。**
    #   ★**其实测（325—341·四百七十轮亲跑）**：**照批134写那一行者 26 轮（5.5%）**，
    #     **而其文里看得出落过刀者 431 轮（91.7%）**——**一条令写了十七章而九成五没照办，问题多半不在人。**
    #   ★★**故今改判据：认那一刀落过没有，不认那两个字。**
    #   ⛔**其认刀之形须是「说得出落在哪儿」者**（删某某／净减N字／净增N字／改作某某／补N字），
    #     **而不是光说「有伤」**——★**故『真伤』二字本身不算一刀**（⛔**抄那两个字不算干活**）。
    #   ⛔**并及一条不许**：**此数每回自盘上现数，不许把 5.5%／91.7% 写进码里当判据**（㊸）。
    _刀式 = re.compile(r'删(?!去之由)|落一刀|落刀|净减\s*[〇零一二三四五六七八九十百廿卅两\d]|'
                      r'净增\s*[〇零一二三四五六七八九十百廿卅两\d]|改作|补\s*[〇零一二三四五六七八九十百廿卅两\d]{1,4}\s*字')
    nz = sum(1 for r, v in lj.items()
             if not _刀式.search('\n'.join(v)) and r not in _said)
    print('     全章轮记提「真伤」%d 处；无真伤之轮 %d 个。' % (zc, nz))
    print('     【基线】全书152份回执实测：各轮含真伤之比例为 60%—76%，'
          '即十轮中约六到七轮当有所获。')
    if nz >= 5:
        hard.append('无真伤之轮达%d个（≥5）——远低于全书基线（十轮中约六七轮有所获），'
                    '须逐轮说明何以皆无，否则视为应付' % nz)
    elif nz >= 3:
        soft_warn.append('无真伤之轮%d个，须于回执说明其由' % nz)

    # 丙·状态查
    print('\n  ── 丙·状态查 ──')
    fl = read_flag(n)
    if fl:
        hard.append('拦停旗未销（%s）' % fl.get('时'))
    ls = _last_snap_sha(n)
    cur_sha = _sha(txt) if txt else None
    drift = bool(ls and cur_sha and ls != cur_sha)
    if drift:
        hard.append('正文与末版已偏（末轮之刀没落台账）')
    _bu = sum(1 for x in vs if '补存' in x.get('说明', ''))
    print('   拦停旗：%s｜正文与末版：%s｜补存版数：%d'
          % ('无' if not fl else '**有**', '已偏' if drift else '一致', _bu))
    # ★2026-09-05·机制总审丙④：补存口本是「显式承认此版非当场所存」之口——
    #   ★而它把领轮基线按末版对齐，等於替这一版补了一张当场的票；
    #   ★★於是台账上「跑了十三轮」与「十三轮是当场跑的」两句话，看不出分别。
    #   ★★★故此处印其率并与全书比：**不拦，只让它看得见**（拦它即逼人不补存，那更坏：
    #     那一版就彻底不入账了）。★★★★本书之实（2026-09-05 逐章数）：
    #     **全书 3631 版，补存 1364 版，率 37.6%；章级中位 38%；补存过半之章 37 章**
    #     （159/160/170/172/173/175/176/177/183/184/185/187…皆在 156—190 之间）；
    #     ★而近十章已降：299 为 24%、301 为 35%、304 为 37%、**305 为 13%**。
    if vs:
        _rate = _bu * 100 // len(vs)
        _mark = '（★逾半：此章之轮多半非当场所跑，读其轮记须知此）' if _rate > 50 else ''
        print('   补存率：%d%%（%d/%d）｜全书中位 38%%｜305章 13%%%s'
              % (_rate, _bu, len(vs), _mark))
        if _rate > 50:
            soft_warn.append('补存率 %d%%（%d/%d）逾半——非当场所存之版多於当场，'
                             '其轮记之凭据须另说一句（不拦，只记）' % (_rate, _bu, len(vs)))

    # ★★★★★丙2·尽力查（2026-08-19 接入·作者令「目的不是跑完，是把质量跑到最高」）
    # ★其为本闸链中唯一测「够不够好」者；先前九道皆只测「有没有错」。
    # ★★而其硬项计入总核之硬项——即：跑透不了，封不了版。
    print('\n  ── 丙2·尽力查（测跑透，非测跑完）──')
    if _造:
        # ★造式之章：尽力查所认之三痕（深掘之层／十轮之净重曲线／到底之记）皆审改之轮之痕，造式无此轮；
        #   造式之「尽力」在造——三稿各写整章、蒙名之选、只办致命与大进，其凭已在甲·造式之实里核过。
        print('   ★造式之章不跑尽力查（其三痕皆审改之轮之痕）——其力在造，见上甲·造式之实。')
    else:
        try:
            _jl = jinli(n)
            if _jl != 0:
                hard.append('尽力查未过——层薄／十轮无所长／未问到底，'
                            '其治不是补字，是回第4轮深掘')
        except Exception as _e:
            soft_warn.append('尽力查未能跑：%s' % _e)

    # 丁·横评择优
    print('\n  ── 丁·横评择优 ──')
    compare(n)

    print('\n  ══════════════════════════════════════════')
    if hard:
        print('  【总核·不过】硬项 %d 条：' % len(hard))
        for h in hard:
            print('     ⛔ %s' % h)
        for w in soft_warn:
            print('     ⚠ %s' % w)
        print('  第%d章：**总核未过，禁封版**。修毕重跑 --十一轮 %d。' % (n, n))
        print('  ══════════════════════════════════════════')
        return 2
    for w in soft_warn:
        print('     ⚠ %s（软项，须于回执裁定）' % w)
    json.dump({'时': datetime.datetime.now().strftime('%m-%d %H:%M'),
               '版数': len(vs), '真轮': sorted(byr), '轮记轮': sorted(lj),
               '补存版数': sum(1 for x in vs if '补存' in x.get('说明', '')),
               '软项': soft_warn, '流': _stream_id(), **({'式': '造式'} if _造 else {})},
              open(os.path.join(d, '_总核.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print('  【总核·通过】%s、无未记之空轮、无旗、正文与末版一致。'
          % ('造式之实俱齐（造式之章·无审改之轮）' if _造 else '十轮之版与记俱齐'))
    print('  已出总核凭据：版本/第%d章/_总核.json（封版闸据此放行）。' % n)
    print('  ══════════════════════════════════════════')
    return 0


def yanlun(n):
    """【批122】权威轮况一屏。
    立此口之由：批121之末，执笔曾向作者误报「第7轮跑完」而台账实无其版。
    闸能拦住做错，拦不住报错——故须有一处**机器出的定论**，报状态时只许引它，不许凭记忆。"""
    d, led = paths(n)
    src = find_chapter(n)
    fl = read_flag(n)
    rs, miss = ([], list(range(1, ROUNDS + 1)))
    ver, jz = '无', '?'
    if os.path.exists(led):
        lg = json.load(open(led, encoding='utf-8'))
        vs = lg.get('版本', [])
        rs, miss = rounds_state(lg)
        rs = sorted(rs)
        if vs:
            ver = vs[-1].get('版', '')
            jz = vs[-1].get('soft', {}).get('净重', '?')
    drift = '（无正文）'
    if src:
        ls = _last_snap_sha(n)
        cur = _sha(open(src, encoding='utf-8').read())
        drift = '一致' if (ls is None or ls == cur) else '**已偏（上一轮之刀没落台账）**'
    rc = _receipts_of(n)
    print('\n████ 权威轮况 · 第%d章 ████' % n)
    print('  真轮 %d/%d %s' % (len(rs), ROUNDS, '已跑：' + '、'.join(str(x) for x in rs) if rs else ''))
    print('  缺轮 %s' % ('无' if not miss else '、'.join('第%d轮' % i for i in miss)))
    print('  末版 %s（净重%s）｜正文与末版：%s' % (ver, jz, drift))
    print('  拦停旗：%s' % ('无' if not fl else '**有**（%s｜%s）' % (fl.get('时'), str(fl.get('因'))[:60])))
    print('  回执：%s' % ('已交' if rc else '未交'))
    ok = (not miss) and (not fl) and drift == '一致'
    print('  ── 一行定论 ──')
    print('  第%d章：真轮%d/%d｜缺%s｜正文与末版%s｜旗%s｜回执%s ⇒ %s'
          % (n, len(rs), ROUNDS, ('无' if not miss else str(len(miss)) + '轮'),
             ('一致' if drift == '一致' else '已偏'), ('无' if not fl else '有'),
             ('已交' if rc else '未交'), '可续' if ok else '**须先修**'))
    return 0 if ok else 2


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

    # ★★★★★2026-09-01 补·半角冒之闸（287第3轮所立）：
    # ★一个新加的硬项，须当场证三样：①它逮得住 ②它不误伤全角 ③它没把已封版之章打红。
    # ★★而第三样最要紧：新硬项若把二百八十七章打红一片，那不是修闸，是拆书。
    chk('半角冒·逮得住', score('他说:好。')[0].get('半角冒') == 1)
    chk('半角冒·不误伤全角', score('他说：好。')[0].get('半角冒') == 0)
    chk('半角冒·空文为零', score('')[0].get('半角冒') == 0)
    chk('半角冒·多处须逐个数', score('a:b:c')[0].get('半角冒') == 2)
    try:
        import glob as _g
        _bad = 0
        _root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        for _f in _g.glob(os.path.join(_root, '正文', '*.md')):
            with open(_f, encoding='utf-8') as _fh:
                _t = _fh.read()
            if score(_t)[0].get('半角冒'):
                _bad += 1
        chk('半角冒·不打红已封版之章（全书须零）', _bad == 0)
    except Exception as _e:
        print('  ✗负测失败：半角冒·全书之验跑不起来（%s）' % _e)
        chk('半角冒·全书之验跑得起来', False)

    # ★★★★★2026-09-05·机制总审丙⑧（裁定查之两洞·本坐上磁盘坐实後所补）：
    #   ★一道核对器若「抄一遍清单就满分」，它报的绿不是活干了，是活抄了；
    #   ★★而其负测须证三样：①旧式在此攻之下满分（故非陪跑）②新式拦得住 ③新式不打红旧章。
    # ★★★★★2026-09-11 治（315 收口当场自逮·**共用常量之坑**）：
    #   ★本函自称「旧式·负测之对照，勿改」，**而它读的是 `VERDICT` 这个全局**——
    #     ★★於是本日给 VERDICT 补「删」「刀」二字，**这个「旧式」也跟着变了**；
    #     **一个自称不动的对照，随着被它对照的那一样一起动**，其对照遂不成对照。
    #   ★★★故把旧词表**写死在本函之内**（十三词，即 0905 立第二层那一日之表）。
    _OLD_VERDICT = ('✓', '合', '改', '核', '真伤', '判', '未见',
                    '零', '缺', '对', '错', '撞', '补')

    def _old_judged(n_, r_, txt):
        """旧式裁定率（窗内见裁语即算）——负测之对照，**其词表写死，不随今日之 VERDICT 动**。"""
        it, _u = duty_list(n_, r_)
        if not it:
            return None
        j = 0
        for x in it:
            for m in re.finditer(re.escape(x), txt):
                sg = txt[max(0, m.start() - 70):m.start() + len(x) + 70]
                if any(v in sg for v in _OLD_VERDICT):
                    j += 1
                    break
        return j * 100 // len(it)

    def _body_of(n_, r_):
        return '\n'.join(_lunji_blocks(n_).get(r_, []))

    _di, _ = duty_list(305, 3)
    if _di:
        _copy = '\n'.join('- %s' % x for x in _di)
        _copy_ok = '\n'.join('- %s：对' % x for x in _di)
        chk('裁定查·旧式在「抄清单+对」之下满分（故此负测非陪跑）',
            _old_judged(305, 3, _copy_ok) == 100)
        chk('裁定查·新式拦得住「抄清单+对」', duty_cover2(305, 3, _copy_ok)[1] == 0)
        chk('裁定查·新式拦得住纯抄清单', duty_cover2(305, 3, _copy)[1] == 0)
        _d11 = '\n'.join('- %s' % x for x in duty_list(300, 11)[0])
        chk('裁定查·项自带裁语之字不许自绿（旧式於300第11轮报100）',
            _old_judged(300, 11, _d11) == 100 and duty_cover2(300, 11, _d11)[1] == 0)
        chk('裁定查·真轮记照旧算数（305第3轮·磁盘之实）',
            duty_cover2(305, 3, _body_of(305, 3))[1] >= 50)
        chk('裁定查·套话之限须直说在册（认不得「判合，其由见上」一类）',
            '认不得哪一样' in open(__file__, encoding='utf-8').read())
        try:
            import glob as _g2
            _root2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            _diff = _tot = _worse = 0
            _gate = lambda q: 0 if q < 50 else (1 if q < 80 else 2)
            # ★0924 立·逐轮点名、带据（⛔不是放宽：新式在此判对了，旧式是多算）：
            #   359 第11轮：轮记自书「作者之眼——读席未及此项」「四席之判——只得一席」，
            #   旧式在「四席之判」四字自身里撞见「判」字即算裁，得 83；新式 66 才是实。
            #   ⛔增一条须同此式：写明轮记原话，证其项确未裁。
            _新式判对之轮 = {(359, 11)}
            for _d in sorted(_g2.glob(os.path.join(_root2, '版本', '第*章'))):
                _n = int(re.search(r'第(\d+)章', _d).group(1))
                if not os.path.exists(os.path.join(_d, '_轮记.md')):
                    continue
                for _r in _lunji_blocks(_n):
                    _b = _body_of(_n, _r)
                    _o = _old_judged(_n, _r, _b)
                    if _o is None:
                        continue
                    _tot += 1
                    _g0, _g1 = _gate(_o), _gate(duty_cover2(_n, _r, _b)[1])
                    if _g0 != _g1:
                        _diff += 1
                    if _g1 < _g0 and (_n, _r) not in _新式判对之轮:   # ★新式比旧式更严＝把旧章打红，⛔此係本条所禁
                        _worse += 1
            # ★★★★★2026-09-11 照其本意重述（同 `负测_销立门.py` ④之b／④之c 之先例）：
            #   ★此条原索 `_diff == 0`，**而它所守者其辞自书得明明白白：「新式不打红一章旧章」**
            #     ——**即：新式不许比旧式更严**。
            #   ★★而本日给 VERDICT 补「删」「刀」二字之後，**差出来的那几轮全是反方向**：
            #     **旧式判不出而新式判得出**（「只删不添」那一类裁，旧词表一个词也不命中）——
            #     **那正是本日之补要办的事**，⛔**拿它来拦，等於拿快照拦住改进。**
            #   ★★★故判据改为：**新式不许把任何一章由绿打红**（_gate 新 ≥ _gate 旧）；
            #     **由红转绿者逐轮记其数，报而不拦。**
            chk('裁定查·全书回灌 %d 轮·新式一章旧章也没有打红（转绿 %d 轮，係补「删」「刀」二字之果）'
                % (_tot, _diff),
                _worse == 0 and _tot > 1000)
        except Exception as _e:
            chk('裁定查·全书回灌跑得起来（%s）' % _e, False)

    # ★2026-09-05·机制总审丙⑭之一（第6轮必答表写死十二样）之负测：
    #   ①册上之器须上桌 ②无册之章照旧十二样 ③旧式认不着册上之器（故非陪跑）④不打红已封版之章。
    _FIX6 = ['绳', '灯', '刀', '架子', '本子', '笔', '腿上', '鞋', '水', '盐', '布包', '竹筒']
    _i6 = duty_list(305, 6)[0]
    chk('第6轮·册上之器上桌（305之钥匙与针）', '钥匙' in _i6 and '针' in _i6)
    chk('第6轮·旧式写死十二样认不着册上之器（故此负测非陪跑）',
        '钥匙' not in _FIX6 and '针' not in _FIX6)
    chk('第6轮·无册之章照旧十二样（290）', duty_list(290, 6)[0] == _FIX6)
    chk('第6轮·册在则十二样一样不少', all(x in _i6 for x in _FIX6))
    try:
        _red = []
        for _n6 in range(290, 306):
            _b6 = '\n'.join(_lunji_blocks(_n6).get(6, []))
            if not _b6:
                continue
            _it6 = duty_list(_n6, 6)[0]
            _j6 = duty_cover2(_n6, 6, _b6)[1]
            _o6 = 0
            for _x6 in _FIX6:
                for _m6 in re.finditer(re.escape(_x6), _b6):
                    if _judged_near(_b6[max(0, _m6.start() - 70):_m6.start() + len(_x6) + 70],
                                    sorted(_FIX6, key=len, reverse=True)):
                        _o6 += 1
                        break
            _o6 = _o6 * 100 // len(_FIX6)
            _g6 = lambda q: 0 if q < 50 else (1 if q < 80 else 2)
            if _g6(_j6) < _g6(_o6):
                _red.append((_n6, _o6, _j6))
        chk('第6轮·册上之器上桌不打红已封版之章（290—305）', not _red)
    except Exception as _e6:
        chk('第6轮·封版之章之验跑得起来（%s）' % _e6, False)

    # ★2026-09-05·丙④补存率之负测：①率算得对 ②逾半即出声 ③不逾半不出声（不喊狼）。
    def _burate(vs_):
        b = sum(1 for x in vs_ if '补存' in x.get('说明', ''))
        return b * 100 // len(vs_) if vs_ else None
    chk('补存率·算得对（2/15＝13%）',
        _burate([{'说明': 'x·补存'}, {'说明': 'y·补存'}] + [{'说明': 'z'}] * 13) == 13)
    chk('补存率·逾半之判（8/15＝53%）',
        _burate([{'说明': 'x·补存'}] * 8 + [{'说明': 'z'}] * 7) > 50)
    chk('补存率·恰半不算逾（不喊狼）', _burate([{'说明': 'x·补存'}] * 5 + [{'说明': 'z'}] * 5) == 50)
    try:
        import json as _js
        _t = _js.load(open(os.path.join(_root, '版本', '第305章', '_台账.json'), encoding='utf-8'))
        chk('补存率·磁盘之实（305须13%·2/15）', _burate(_t.get('版本', [])) == 13)
    except Exception as _e4:
        chk('补存率·磁盘之验跑得起来（%s）' % _e4, False)

    # ★★★★★2026-09-09·307封版之序·补存口之空基线（**同形第二口**·见 `_补存之基线`）。
    #   ★令§六③：一份在旧式下也全过的测就是陪跑——**故此四条须先证旧式真绿**。
    #     旧式逐字为：`base['正文sha']=base.get('末版sha'); base['目标轮']=_round_of(note); base['补存']=True`
    #     ——**一律落盘，说明无轮号时那个键即为 None**。
    def _旧式补存基线(base, note):
        b = dict(base or {})
        b['正文sha'] = b.get('末版sha')
        b['目标轮'] = _round_of(note)
        b['补存'] = True
        return b                       # ★旧式从不返 None：一律落盘
    _实307 = {'时': '09-09 09:23', '正文sha': '0277a436cd27c821',
              '末版sha': '0277a436cd27c821', '目标轮': 1, '新章': False}
    _定案 = '定案·案席封版（十三轮之外）·判不补·记因：本轮之刀不在正文而在册子上'
    chk('补存基线·①旧式回灌：无轮号之说明把真轮号抹成 null（证此洞是真的）',
        _旧式补存基线(_实307, _定案).get('目标轮') is None
        and '目标轮' in _旧式补存基线(_实307, _定案)
        and _旧式补存基线({}, _定案).get('目标轮') is None)
    chk('补存基线·②新式：说明无轮号者，旧基线那个真轮号原样留着（1，不抹成 null）',
        (_补存之基线(_实307, _定案) or {}).get('目标轮') == 1)
    chk('补存基线·③新式不误伤：说明带轮号者照旧落盘，且其号即说明之号',
        (_补存之基线(_实307, '第13轮·升华定稿') or {}).get('目标轮') == 13)
    chk('补存基线·④无轮可记者一个字也不落（返 None·305之遗即此形）',
        _补存之基线({}, _定案) is None
        and _补存之基线({'末版sha': 'abc'}, _定案) is None)
    # ★★而⑤是这一治的真凭：旧式落下的那一份，`开轮六检.check9` 判红；新式那一份判绿。
    try:
        import importlib.util as _iu9, tempfile as _tf9, shutil as _sh9
        _sp9 = _iu9.spec_from_file_location('_lz9', os.path.join(_root, '工具', '开轮六检.py'))
        _m9 = _iu9.module_from_spec(_sp9)
        _sp9.loader.exec_module(_m9)
        _tmp9 = _tf9.mkdtemp(prefix='zm_ling_')
        _d9 = os.path.join(_tmp9, '版本', '第9章')
        os.makedirs(_d9)
        _js.dump({'版本': [{'版': 'v01'}]}, open(os.path.join(_d9, '_台账.json'), 'w',
                                                encoding='utf-8'))
        _old9 = _m9.ROOT
        _m9.ROOT = _tmp9
        try:
            _p9 = os.path.join(_d9, '_领轮.json')
            _js.dump(_旧式补存基线(_实307, _定案), open(_p9, 'w', encoding='utf-8'),
                     ensure_ascii=False)
            _红 = not _m9.check9(9)[0][1]
            _js.dump(_补存之基线(_实307, _定案), open(_p9, 'w', encoding='utf-8'),
                     ensure_ascii=False)
            _绿甲 = _m9.check9(9)[0][1]          # 新式·真轮号留着者
            os.remove(_p9)                        # 新式·无轮可记者一个字不落
            _绿乙 = _m9.check9(9)[0][1]
        finally:
            _m9.ROOT = _old9
            _sh9.rmtree(_tmp9, ignore_errors=True)
        chk('补存基线·⑤旧式那一份 check9 判红、新式两局俱绿（非陪跑）',
            _红 and _绿甲 and _绿乙)
    except Exception as _e9:
        chk('补存基线·⑤之验跑得起来（%s）' % _e9, False)

    L = lambda vs: {'章': 1, '版本': vs}
    _SOFT = {'净重': 100, '段数': 9, '均段': 11, '长段数': 0, '嗅': 3, '听': 4,
             '触': 7, '视': 2, '老头': 1, '钱满': 1, '沈鸢': 0,
             '四字串三现': 0, '顿悟起手': 0}
    v = lambda note, ch=None: ({'版': 'v01', '时': '', '说明': note,
                                'hard': {}, 'soft': dict(_SOFT)}
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
    # ★2026-09-13 随闸收窄同笔改（体检账 ㊞）：旧局係「第9轮在册而报第4轮＝倒退·拦」，
    #   ⛔**而那正是十一段席乱序开庭之常形**（第10轮先於第9轮开·第4轮三路各一席）；
    #   **今之判据改作「那一轮册上有没有」**：**没有＝补洞·许；有＝重跑·拦。**
    chk('轮次闸须拦重跑（第4轮已在册而又报第4轮）',
        gates(1, '第4轮·甲', L([v('第4轮·丙'), v('第9轮·乙')]), 5, [])[0])
    chk('轮次闸不得误拦补洞（第9轮在册而报册上没有的第4轮）',
        not gates(1, '第4轮·甲', L([v('第9轮·乙')]), 5, [])[0])
    chk('轮次闸不得误拦持平', not gates(1, '第9轮·甲', L([v('第9轮·乙')]), 5, [])[0])
    # ★章界闸之收窄（2026-09-16·336 之实）：往前写不拦，拆／并照旧拦
    def _Lch(ch):
        d = L([v('第1轮·甲')]); d['版本'][-1]['全书章数'] = ch; return d
    chk('章界闸·往前写（章数只增而所增在本章之後）不得拦',
        not gates(336, '终版回补·甲', _Lch(336), 337, [])[0])
    chk('章界闸·往前写十章亦不拦（其增仍尽在本章之後）',
        not gates(336, '终版回补·甲', _Lch(336), 346, [])[0])
    chk('章界闸·⛔并章（章数减）照旧拦',
        gates(336, '终版回补·甲', _Lch(337), 336, [])[0])
    chk('章界闸·⛔拆章（所增落在本章之前）照旧拦',
        gates(100, '终版回补·甲', _Lch(336), 337, [])[0])
    chk('章界闸·报而不拦之时须印其由（不许闷着放行）',
        any('章界闸·报而不拦' in x for x in gates(336, '终版回补·甲', _Lch(336), 337, [])[1]))
    chk('轮次闸不得误拦前进', not gates(1, '第10轮·甲', L([v('第9轮·乙')]), 5, [])[0])
    chk('轮次闸不得误拦首版',
        not gates(1, '第1轮·甲', L([]), 5, [], txt='甲。\n【本章亮点】\n①甲。')[0])
    # ★亮点闸自身之二测（其详在 工具/负测_亮点闸.py）
    chk('亮点闸·第1轮无亮点段须拦',
        gates(1, '第1轮·甲', L([]), 5, [], txt='甲。\n')[0])
    chk('亮点闸·第2轮无亮点段不问（其位只在第1轮）',
        not any('亮点闸' in x for x in
                gates(1, '第2轮·乙', L([v('第1轮·甲')]), 5, [], txt='甲。\n')[1]))

    # 闸三·章界闸
    chk('章界闸须拦章数增（别路拆章）',
        gates(1, '第4轮·甲', L([v('第3轮·乙', ch=151)]), 152, [])[0])
    chk('章界闸须拦章数减', gates(1, '第4轮·甲', L([v('第3轮·乙', ch=152)]), 151, [])[0])
    # ★★★★★★空轮之词表归一之负测（0917·339 v03 之实）
    #   ⛔**其守**：**总核那一口与存版那一口，须认同一份词表**。
    _空词 = lambda note: bool(re.search(r'判不补|零刀|不补|无真伤', note))
    _v03 = '第3轮·逐数对表·第2转复核：十六道器全绿……本转零刀；新见七字跨章重出，判留并原样报出。·补存'
    chk('空轮·「零刀」今认得（与存版那一口同表）', _空词(_v03))
    chk('⛔而旧式（只认「判不补」）对同一句不认——故上一格非陪跑',
        '判不补' not in _v03)
    chk('空轮·旧词一格未动（判不补）', _空词('第5轮·审毕判不补。'))
    chk('空轮·⛔什么也没写者照旧不认', _空词('第5轮·续存。') is False)
    chk('空轮·二口同表（拿 gates 之空轮闸那一份逐字对）',
        _空词('零刀') and _空词('无真伤') and _空词('不补'))

    # ★★★★★★裁语词表加三词之负测（0917·339 第9轮之实）
    _裁语 = lambda b: bool(re.search(r'真伤|判不补|零刀|判合|无刀|皆拒|交白卷'
                                    r'|[不未]落刀|落[一二三四五六七八九十两\d]+刀', b))
    _旧裁语 = lambda b: bool(re.search(r'真伤|判不补|零刀|判合', b))
    _九 = '本轮无刀。读席四条逐条裁过，四条皆拒。交白卷。'
    chk('裁语·339 第9轮之首行今认得（无刀／皆拒／交白卷）', _裁语(_九))
    chk('⛔而旧式对同一句一个词也不认——故上一格非陪跑', not _旧裁语(_九))
    chk('裁语·旧四词一格未动（判不补）', _裁语('本轮审毕判不补。'))
    chk('裁语·⛔什么结论也没写者照旧不认',
        not _裁语('本轮跑毕，逐项看过，甚好。'))
    chk('裁语·⛔「拒」单字不补（一字太泛，撞得着别处）',
        not _裁语('他拒了一步，没有再往前。'))

    # ★★★★★★裁语词表再加一族之负测（0923·358 第10轮之实·⛔每一局皆验其反面）
    _中裁 = lambda b: bool(re.search(r'真伤|判不补|零刀|判合|无刀|皆拒|交白卷', b))
    _十 = '本轮只落一刀。四十一拍逐拍问过，答得出「什么也不丢」的确实只有那一拍。'
    chk('裁语·358 第10轮之结句今认得（落一刀）', _裁语(_十))
    chk('⛔而中式（七词）对同一句一个词也不认——故上一格非陪跑', not _中裁(_十))
    chk('裁语·「不落刀」认得（物堂只报之式）', _裁语('另报一件不落刀的：草秆。'))
    chk('裁语·阿拉伯数亦认（落3刀）', _裁语('本轮落3刀，皆在句中。'))
    chk('裁语·旧词一格未动（零刀）', _裁语('本转零刀。'))
    chk('裁语·⛔「刀」单字不补（满纸皆是）', not _裁语('他把刀搁回石皮上。'))
    chk('裁语·⛔「落刀」无数无否亦不认（没说落了几刀就不是裁）',
        not _裁语('本轮落刀之处，容後再议。'))

    # ★★★★★★必答之锚之负测（0916·339 第8轮之实·⛔每一局皆验其反面）
    #   ⛔**其所治者**：闸之罚辞写着「抄清单不算干活」，而其码以整串直配，
    #     **遂使「照抄清单」成为唯一配得上的写法**——**说与做正面相反。**
    chk('必答之锚·去其头（「复述·」）与其尾（「←第333章」）',
        必答之锚('复述·她的手从被子底下进去摸到←第333章')
        == '她的手从被子底下进去摸到')
    chk('必答之锚·无装饰者原样返回', 必答之锚('刀数') == '刀数')
    chk('必答之锚·只有尾者亦去', 必答之锚('那一道槽←第323章') == '那一道槽')
    chk('必答之锚·⛔短锚（<4字）不许走新路（拿「刀」去配即满纸皆是）',
        len(必答之锚('刀数')) < 4)
    def _cov(t, its):
        """沙盘·拿一份手造之必答单跑 duty_cover2（⛔不动磁盘）。"""
        _真 = globals()['duty_list']
        try:
            globals()['duty_list'] = lambda n, r: (its, None)
            return duty_cover2(1, 1, t)
        finally:
            globals()['duty_list'] = _真
    _its = ['复述·她的手从被子底下进去摸到←第333章',
            '复述·腕上那一条筋她的指腹一落←第333章']
    _真文 = ('①「她的手从被子底下进去摸到…」（339:73，逐字同 333:237）——**留**。其由：日课之一字不变。\n'
             '②「腕上那一条筋她的指腹一落」——**留**，同由。')
    chk('沙盘·老实话（引其句而不抄清单之装饰）今配得上',
        _cov(_真文, _its)[0] == 100)
    _旧式 = [m.start() for m in re.finditer(re.escape(_its[0]), _真文)]
    chk('⛔而旧式（整串直配）对同一份老实话一处也配不着——故上一格非陪跑',
        _旧式 == [])
    chk('沙盘·⛔什么也没写者照旧零', _cov('本轮跑毕。', _its)[0] == 0)
    chk('沙盘·⛔提而不裁者：提及有，而裁定零',
        _cov('「她的手从被子底下进去摸到」在此。', _its)[0] > 0
        and _cov('「她的手从被子底下进去摸到」在此。', _its)[1] == 0)

    # ★漂移哨·记因放行之负测（0916 立·⛔每一局皆验其反面）
    chk('漂移记因·空者不放（照旧拦）', not 漂移记因之判('')[0])
    chk('漂移记因·只一个词者不放', not 漂移记因之判('回补')[0])
    chk('漂移记因·七字不放（界在八字）', not 漂移记因之判('一二三四五六七')[0])
    chk('漂移记因·八字放', 漂移记因之判('一二三四五六七八')[0])
    chk('漂移记因·实写者放，且原样交回以挂进说明',
        漂移记因之判(' 救章席之刀·封版後之回补 ')[1] == '救章席之刀·封版後之回补')
    chk('漂移记因·不放者须给出其由（非哑拦）',
        漂移记因之判('回补')[1].startswith('⛔'))
    # ★★2026-09-16 再收窄之负测（336 第二回之实）：`新增章号` 这一路真凭
    #   ⛔**每一局皆先跑旧式（不给 `新增章号`）验其仍红**，⛔**旧式也绿者即陪跑。**
    chk('章界闸·新增之章尽在本章之後者不拦（336 而新增 338）',
        not gates(336, '终版回补·甲', L([v('第9轮·乙', ch=337)]), 338, [],
                  新增章号=[338])[0])
    chk('章界闸·⛔而旧式对同一局判红（证上一局非陪跑）',
        gates(336, '终版回补·甲', L([v('第9轮·乙', ch=337)]), 338, [])[0])
    chk('章界闸·新增之中有一号 ≤ 本章者照旧拦（拆章落在本章之前）',
        gates(336, '终版回补·甲', L([v('第9轮·乙', ch=337)]), 338, [],
              新增章号=[200])[0])
    chk('章界闸·新增之中有一号正是本章者照旧拦（拆的就是本章）',
        gates(336, '终版回补·甲', L([v('第9轮·乙', ch=337)]), 338, [],
              新增章号=[336])[0])
    chk('章界闸·凭取不到（None）照旧拦——⛔「查不着」不是放行之由',
        gates(336, '终版回补·甲', L([v('第9轮·乙', ch=337)]), 338, [],
              新增章号=None)[0])
    chk('章界闸·空单（章数增而一档未新出＝改名／拆档）照旧拦',
        gates(336, '终版回补·甲', L([v('第9轮·乙', ch=337)]), 338, [],
              新增章号=[])[0])
    chk('章界闸·章数减者，纵有新增章号亦拦（并章）',
        gates(336, '终版回补·甲', L([v('第9轮·乙', ch=338)]), 337, [],
              新增章号=[400])[0])
    chk('章界闸·报而不拦之印落在新路上',
        any('章界闸·报而不拦' in x for x in
            gates(336, '终版回补·甲', L([v('第9轮·乙', ch=337)]), 338, [],
                  新增章号=[338])[1]))
    # ★并及 `新增章号自末次存版` 本身：旧档少了一个即返 None（改名／并章／删档）
    chk('新增章号自末次存版·取不着台账之章返 None',
        新增章号自末次存版(999999) is None)
    chk('章界闸不得误拦章数不变',
        not gates(1, '第4轮·甲', L([v('第3轮·乙', ch=151)]), 151, [])[0])
    chk('章界闸不得误拦旧台账（无全书章数字段）',
        not gates(1, '第4轮·甲', L([v('第3轮·乙')]), 151, [])[0])
    # ★2026-09-05·机制总审（八路·覆盖之缺审第12条·P40 总则）：score 不把分节符「＊」算段——以 305 v01（不变之版）回灌
    _v01 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '版本', '第305章', 'v01.md')
    if os.path.exists(_v01):
        _s305 = score(open(_v01, encoding='utf-8').read())[1]
        chk('score 不把「＊」算段：305 v01 段数须 125（含＊之旧式为 249）', _s305.get('段数') == 125)
    # ★2026-09-05·机制总审（八路·覆盖之缺审第3条·P37）：「想到这儿我…」须入顿悟起手之数（旧式只认「我忽然」一族）
    _s37 = score('《镇冢秘术》\n\n第九百九十九章　试\n\n想到这儿我往后偏了一下头。\n\n我忽然明白了。\n')[1]
    chk('顿悟起手认「想到这儿」起手（P37）：二段须计 2', _s37.get('顿悟起手') == 2)
    chk('章界闸须认 ZM_FORCE 之豁免',
        not gates(1, '第4轮·甲', L([v('第3轮·乙', ch=151)]), 152, [], force='已对表')[0])

    # 全清之常态
    chk('三闸俱通时不得拦', not gates(1, '第4轮·甲', L([v('第3轮·乙', ch=151)]), 151, [])[0])
    # 批120：HEAD前进不得再作拦停之据（自噪声）
    import inspect as _ins
    _src = _ins.getsource(save)
    chk('HEAD前进不得再拦停（批120降级）',
        'ℹHEAD自上次记录以来已前进' in _src and '⛔HEAD前进闸' not in _src)

    # 151实录回放：当日之真况须被拦下
    chk('151实录回放须拦（回执已交＋轮次倒退＋章数增·同一执笔失忆续手）',
        gates(151, '第4轮·升华庭', L([v('第3轮·校对庭逐数对表', ch=151)]), 152,
              ['设定/回执_20260804_第151章作业单.md'])[0])

    # 闸四·验轮
    chk('验轮须认满%d轮'%ROUNDS, rounds_state(L([v('第%d轮·x' % i) for i in range(1, ROUNDS+1)]))[1] == [])
    chk('验轮须报缺末诸轮', rounds_state(L([v('第%d轮·x' % i) for i in range(1, 10)]))[1] == list(range(10,ROUNDS+1)))
    chk('验轮不得把回补当真轮', rounds_state(L([v('终版回补')]))[0] == set())
    chk('151实录回放·验轮须报缺末诸轮',
        rounds_state(L([v('第%d轮·x' % i) for i in range(1, 10)]))[1] == list(range(10,ROUNDS+1)))

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
                if want_rc == 0:
                    clear_flag(7)
                rc = save(7, note)
            after = sorted(glob.glob(os.path.join(tmp, '版本', '**', '*'), recursive=True))
            good = (rc == want_rc)
            if want_rc == 2:
                # 拦停之轮：不得多出版本与台账；**惟拦停旗须写**（批122：旗是粘性故障标记，
                # 漏读一次拦停不得等于走得过去，故落旗本身即拦停之一部分）。
                nf = [x for x in after if x not in before and os.path.isfile(x)
                      and not x.endswith('_拦停.json')]
                good = good and not nf
                if nf:
                    print('  ✗端到端：拦停却写入了 %s' % nf)
                if not any(x.endswith('_拦停.json') for x in after):
                    good = False
                    print('  ✗端到端：拦停却未落旗（批122）')
            if good:
                ok += 1
            else:
                fail += 1
                print('  ✗端到端失败：%s（rc=%s，期望%s）' % (name, rc, want_rc))
                for _l in buf.getvalue().split('\n'):
                    if '⛔' in _l or '✗' in _l:
                        print('      ' + _l.strip()[:96])
        finally:
            ROOT, JJ_DIR = _R, _J
            shutil.rmtree(tmp, ignore_errors=True)

    def _ch(tmp, body='一二三四五六七八九十', 亮=True):
        # ★2026-09-02·亮点闸立後补：**样章须带亮点段**——
        #   ★亮点闸拦的是「第1轮之存版而正文无亮点段」，而旧样章正是那个样子，
        #     遂使「干净首版须放行」与「新章起手第1轮须放行」二测由绿转红；
        #   ★★**而红得对**：那两测所设之「干净首版」，照今日之法本就不干净。
        #   ★★★故改样章，不改闸——**样章是拿来代表合法之版的，它自己先得合法。**
        h = '\n\n【本章亮点】\n\n**★而其骨一层**：\n①甲。\n' if 亮 else ''
        open(os.path.join(tmp, '正文', '镇冢秘术_第七章_测.md'), 'w',
             encoding='utf-8').write('《镇冢秘术》\n\n第七章　测\n\n' + body + '\n' + h)

    def _led(tmp, vs):
        d = os.path.join(tmp, '版本', '第7章')
        os.makedirs(d, exist_ok=True)
        json.dump({'章': 7, '版本': vs}, open(os.path.join(d, '_台账.json'), 'w',
                  encoding='utf-8'), ensure_ascii=False)
        return d

    def _cur(tmp):
        return open(os.path.join(tmp, '正文', '镇冢秘术_第七章_测.md'), encoding='utf-8').read()

    def _ling(tmp, target, zheng=None, mo=None):
        d = os.path.join(tmp, '版本', '第7章')
        os.makedirs(d, exist_ok=True)
        json.dump({'时': 'x', '正文sha': zheng, '末版sha': mo, '目标轮': target},
                  open(os.path.join(d, '_领轮.json'), 'w', encoding='utf-8'),
                  ensure_ascii=False)

    def _ready(tmp, prev_round, target, body_now, log=True):
        """布置一个「第prev_round轮已存版并录记，现起第target轮」之合法局面。"""
        _ch(tmp, '原始内容')
        snap = _cur(tmp)
        d = _led(tmp, [v('第%d轮·前' % prev_round, ch=1)])
        open(os.path.join(d, 'v01.md'), 'w', encoding='utf-8').write(snap)
        if log:
            open(os.path.join(d, '_轮记.md'), 'w', encoding='utf-8').write(
                '\n## 第%d轮|v01|x|净重9\n所见若干\n' % prev_round)
        _ling(tmp, target, zheng=_sha(snap), mo=_sha(snap))
        _ch(tmp, body_now)          # 本轮之改动
        return d

    def s_receipt(tmp):
        _ready(tmp, 9, 4, '改过的内容')
        open(os.path.join(tmp, '设定', '回执_x_第7章作业单.md'), 'w',
             encoding='utf-8').write('x')

    def s_clean(tmp):
        _ch(tmp, '甲乙丙丁')
        _ling(tmp, 1, zheng=_sha(_cur(tmp)), mo=None)

    def s_empty(tmp):
        """正文与末版逐字相同＝空轮。"""
        _ch(tmp, '原始内容')
        snap = _cur(tmp)
        d = _led(tmp, [v('第3轮·前', ch=1)])
        open(os.path.join(d, 'v01.md'), 'w', encoding='utf-8').write(snap)
        open(os.path.join(d, '_轮记.md'), 'w', encoding='utf-8').write(
            '\n## 第3轮|v01|x|净重9\n所见\n')
        _ling(tmp, 4, zheng=_sha(snap), mo=_sha(snap))

    def s_nolog(tmp):
        _ready(tmp, 1, 2, '改过的内容', log=False)

    def s_withlog(tmp):
        _ready(tmp, 1, 2, '改过的内容')

    def s_reopen(tmp):
        d = _ready(tmp, 1, 2, '改过的内容')
        led2 = os.path.join(d, '_台账.json')
        lg = json.load(open(led2, encoding='utf-8'))
        lg['版本'].append({'版': '重开', '时': 'x', '说明': '【重开·记因】测',
                          'hard': {}, 'soft': {}, '全书章数': 1})
        json.dump(lg, open(led2, 'w', encoding='utf-8'), ensure_ascii=False)

    def s_noling(tmp):
        _ready(tmp, 1, 2, '改过的内容')
        os.remove(os.path.join(tmp, '版本', '第7章', '_领轮.json'))

    def s_wronground(tmp):
        d = _ready(tmp, 1, 2, '改过的内容')
        _ling(tmp, 5, zheng='x', mo='x')

    def s_drifted(tmp):
        """起轮时正文已偏离末版＝上一轮之刀没落进台账。"""
        d = _ready(tmp, 1, 2, '改过的内容')
        _ling(tmp, 2, zheng='deadbeefdeadbee0', mo='deadbeefdeadbee1')

    e2e('回执已交＋轮次倒退须拦停且零写入', s_receipt, '第4轮·升华庭', 2)
    e2e('空轮须拦停且零写入', s_empty, '第4轮·升华庭', 2)
    e2e('干净首版须放行并写入', s_clean, '第1轮·感官庭', 0)
    e2e('前轮未录轮记须拦停且零写入', s_nolog, '第2轮·四堂会审', 2)
    e2e('前轮已录轮记须放行', s_withlog, '第2轮·四堂会审', 0)
    e2e('台账含空soft之重开记录时存版不得崩', s_reopen, '第2轮·四堂会审', 0)
    e2e('未领轮即存版须拦停且零写入', s_noling, '第2轮·四堂会审', 2)
    e2e('所报之轮与所领不符须拦停', s_wronground, '第2轮·四堂会审', 2)
    e2e('起轮时正文已偏离末版须拦停', s_drifted, '第2轮·四堂会审', 2)
    e2e('非第N轮之说明（回补／定案）不受领轮闸拘', s_noling, '终版回补·器物', 0)

    def s_newch(tmp):
        """新章起手：领轮时正文尚不存在，基线标新章，第1轮须放行。"""
        _ch(tmp, '新章正文')
        d = os.path.join(tmp, '版本', '第7章')
        os.makedirs(d, exist_ok=True)
        json.dump({'时': 'x', '正文sha': None, '末版sha': None, '目标轮': 1, '新章': True},
                  open(os.path.join(d, '_领轮.json'), 'w', encoding='utf-8'), ensure_ascii=False)

    e2e('新章起手（基线无正文sha）第1轮须放行', s_newch, '第1轮·感官庭', 0)
    e2e('存版成功后领轮基线须销（一领一存不得复用）',
        s_withlog, '第2轮·四堂会审', 0)

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

    # 闸四·验轮两级判（批113修·防误报）
    R = lambda ls: L([v('第%d轮·x' % i) for i in ls])
    chk('验轮·洞：中间缺号须判硬伤', rounds_verdict(R([1, 2, 3, 5, 6]))[0] == [4])
    chk('验轮·洞：满%d轮不得报洞'%ROUNDS, rounds_verdict(R(range(1, ROUNDS+1)))[0] == [])
    chk('验轮·短：止于第9轮须判存疑而非硬伤',
        rounds_verdict(R(range(1, 10)))[0] == [] and rounds_verdict(R(range(1, 10)))[1] == [10])
    _txt = lambda ls: '\n'.join(rounds_verdict(ls)[2])
    _R9 = [v('第%d轮·x' % i) for i in range(1, 10)]
    chk('验轮·105/106实录：第9轮后有「定案轮（十轮之外）」须判合',
        '判合' in _txt(L(_R9 + [v('定案轮（十轮之外）：逐版比对')])))
    chk('验轮·143实录：第9轮即收官减法轮须判合',
        '判合' in _txt(L([v('第%d轮·x' % i) for i in range(1, 9)] +
                         [v('第9轮·收官减法轮：七刀减9字')])))
    chk('验轮·151实录：第9轮为跨章复审且其后无版，须判存疑',
        '存疑' in _txt(L([v('第%d轮·x' % i) for i in range(1, 9)] +
                         [v('第9轮·跨章复审')])))
    chk('验轮·满%d轮不得报短'%ROUNDS, rounds_verdict(R(range(1, ROUNDS+1)))[1] == [])
    chk('验轮·空台账不得报', rounds_verdict(L([])) == ([], [], []))

    # 闸六·空轮闸与验轮闸不得相犯（批113修）
    chk('空轮闸须放行明记判不补之轮（轮号照挂）',
        not gates(1, '第4轮·升华庭·判不补·记因', L([v('第3轮·乙', ch=5)]), 5, [],
                  same_as_last=True)[0])
    chk('空轮闸仍拦未记判不补之零改动轮',
        gates(1, '第4轮·升华庭', L([v('第3轮·乙', ch=5)]), 5, [], same_as_last=True)[0])

    # 闸七·轮记闸端到端

    _src_self = open(os.path.abspath(__file__), encoding='utf-8').read()
    # 闸九·领轮闸（2026-09-16 立·336 之席跑第7轮当日所逮）
    # ⛔其实：`版本/第7章/_领轮.json` 於 07:05 凭空落盘（目标轮1／新章false），
    #   而第7章早已写完三百章之久；其时 336 之席正走**第7轮**——
    #   **一个轮号被当成了章号送进来，而本器照旧给它落了一份基线。**
    chk('领轮闸·新章起手须放行（尚无正文）', 可领轮(False, False)[0] is True)
    chk('领轮闸·在建之章须放行（台账在）', 可领轮(True, True)[0] is True)
    chk('领轮闸·⛔正文早在而台账从无者不许领轮', 可领轮(True, False)[0] is False)
    chk('领轮闸·其由说得出「不是在建之章」', '不是在建之章' in 可领轮(True, False)[1])
    # ⛔并记本坐头一版之错判：**原拿「回执在不在」作判，当场试而不中**——
    #   **回执闸自第73章起方立，第7章根本没有回执**；
    #   ★拿一条只对後三百章成立的判据去拦前七十章，它一次也拦不住。
    chk('领轮闸·⛔不拿「回执在不在」作判（回执闸自73章起，前章无回执）',
        '_receipts_of(n)' not in _src_self.split('def 可领轮')[1].split('def _ling_path')[0])

    # ── 造式之总核（2026-10-08·作者令「名著是写出来的，不是改出来的」）──
    #   ★总核见 `_式.md` 即改核造式之实（`工具/造式.py`）——⛔非豁免：挂牌无实照旧不过；旗、正文与末版、在册之轮之记照旧咬。
    def _造局(tmp, 缺=(), 旗=False, 偏=False, 无式=False, 无三记=False):
        import importlib.util as _u
        _sp = _u.spec_from_file_location('_zs_t', os.path.join(os.path.dirname(os.path.abspath(__file__)), '造式.py'))
        _zm = _u.module_from_spec(_sp); _sp.loader.exec_module(_zm)
        d = _zm.造一局(tmp, 7, 缺=缺)
        if 无式:
            os.remove(os.path.join(d, '_式.md'))
        body = '《镇冢秘术》\n\n第七章　测\n\n她把手搁在桶沿上，等那口气落稳。\n'
        open(os.path.join(tmp, '正文', '镇冢秘术_第七章_测.md'), 'w', encoding='utf-8').write(body + ('偏了' if 偏 else ''))
        open(os.path.join(d, 'v01.md'), 'w', encoding='utf-8').write(body)
        json.dump({'章': 7, '版本': [{'版': 'v01', '时': 'x', '说明': '第3轮·逐数对表·判不补·记因：诸器全绿',
                   'hard': {}, 'soft': {'净重': 100, '段数': 9, '均段': 11, '长段数': 1, '嗅': 3, '听': 4, '触': 7, '视': 2,
                                                '老头': 1, '钱满': 1, '沈鸢': 0, '四字串三现': 0, '顿悟起手': 0}, '全书章数': 1}]},
                  open(os.path.join(d, '_台账.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        实 = '看见了什么：逐器跑过，起草闸甲层九格全绿，硬闸零红，本转零刀判合，其由为诸数与台账逐一对上。' * 3
        lj = open(os.path.join(d, '_轮记.md'), encoding='utf-8').read()
        lj = lj.replace('## 第3轮·逐数对表\n', '## 第3轮·逐数对表\n' + ('' if 无三记 else '净重100｜段数9 ' + 实 + '\n'))
        if 无三记:
            lj = re.sub(r'## 第3轮·逐数对表\n[^#]*', '', lj)
        open(os.path.join(d, '_轮记.md'), 'w', encoding='utf-8').write(lj)
        if 旗:
            raise_flag(7, '测', '造式')

    def _造核(name, want, **kw):
        nonlocal ok, fail
        global ROOT, JJ_DIR
        tmp = tempfile.mkdtemp(prefix='zm_zs_')
        try:
            os.makedirs(os.path.join(tmp, '正文'))
            os.makedirs(os.path.join(tmp, '设定'))
            ROOT, JJ_DIR = tmp, os.path.join(tmp, '版本')
            _造局(tmp, **kw)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = zonghe(7)
            if rc == want:
                ok += 1
            else:
                fail += 1
                print('  ✗负测失败：造式之总核·%s（rc=%s，期望%s）' % (name, rc, want))
                for _l in buf.getvalue().split('\n'):
                    if '⛔' in _l:
                        print('      ' + _l.strip()[:110])
        finally:
            ROOT, JJ_DIR = _R, _J
            shutil.rmtree(tmp, ignore_errors=True)
    _造核('①造式之实俱齐、在册之轮有记、无旗、正文与末版一致者过', 0)
    _造核('②挂造式之牌而合稿逐条回话缺者不过（⛔非豁免）', 2, 缺=('回话',))
    _造核('③漏回一号者不过', 2, 缺=('漏回',))
    _造核('④无逻辑审之节者不过', 2, 缺=('逻辑审之节',))
    _造核('⑤拦停旗未销者照旧不过', 2, 旗=True)
    _造核('⑥正文与末版已偏者照旧不过', 2, 偏=True)
    _造核('⑦同一局而无 _式.md 者照常式量（缺十余轮）不过', 2, 无式=True)
    _造核('⑧在册之第3轮无轮记者照旧不过', 2, 无三记=True)
    # ⑨造式之节不并进其前一轮（防第3轮之覆盖／对数被别席之文撑高）
    tmp = tempfile.mkdtemp(prefix='zm_zs9_')
    try:
        ROOT, JJ_DIR = tmp, os.path.join(tmp, '版本')
        os.makedirs(os.path.join(JJ_DIR, '第7章'))
        open(os.path.join(JJ_DIR, '第7章', '_轮记.md'), 'w', encoding='utf-8').write(
            '# 轮记\n## 第3轮·逐数对表\n甲\n### 小节\n乙\n## 造式·逻辑审·起草·第1回\n丙P04\n## 造式·盲读\n丁\n## 第4轮·x\n戊\n')
        _b = _lunji_blocks(7)
        _t3 = '\n'.join(_b.get(3, []))
        chk('造式之节不并进其前一轮（第3轮块含其小节而不含造式之节）', '乙' in _t3 and '丙' not in _t3 and '丁' not in _t3)
        chk('造式之节之後之轮照旧归块', '戊' in '\n'.join(_b.get(4, [])))
    finally:
        ROOT, JJ_DIR = _R, _J
        shutil.rmtree(tmp, ignore_errors=True)

    # ★1018 X07：造式二代未封之章，阅读器过期只报、指封版 --後（⛔⛔、⛔另跑同步之处方）；他章照旧处方（回灌旧报——一律⛔与同步处方——即红）
    _旧 = _reader_stale(lambda: '不合')
    _二 = _reader_stale(lambda: '不合', 交封版=398)
    chk('X07·二代未封之章：阅读器过期只报、指封版 --後',
        len(_二) == 1 and '⛔阅读器' not in _二[0] and '推送必被拦' not in _二[0] and '封版.py 398 --後' in _二[0]
        and '处方：python3 工具/同步全本阅读器.py' not in _二[0])
    chk('X07·他章照旧处方；合则不报', any('同步全本阅读器.py' in x for x in _旧) and _reader_stale(lambda: '同步检查通过', 交封版=398) == [])
    import inspect as _ins
    chk('X07·存版之报经交封版之判（⛔回调旧 _reader_stale()）', '_reader_stale(交封版=n if _阅读器交封版(n) else None)' in _ins.getsource(save))
    tmp = tempfile.mkdtemp(prefix='zm_x07_')
    try:
        ROOT, JJ_DIR = tmp, os.path.join(tmp, '版本')
        for _k, _式 in ((7, '式：虫洞（造式二代·1013）'), (8, '式：虫洞（造式二代·1013）'), (9, '式：虫洞（一代）')):
            os.makedirs(os.path.join(JJ_DIR, '第%d章' % _k))
            open(os.path.join(JJ_DIR, '第%d章' % _k, '_式.md'), 'w', encoding='utf-8').write(_式 + '\n')
        open(os.path.join(JJ_DIR, '第8章', '_十一轮.json'), 'w', encoding='utf-8').write('{}')
        chk('X07·判：二代未封者交封版；已封（十一轮在）、一代、无式者照旧',
            _阅读器交封版(7) is True and _阅读器交封版(8) is False and _阅读器交封版(9) is False and _阅读器交封版(10) is False)
    finally:
        ROOT, JJ_DIR = _R, _J
        shutil.rmtree(tmp, ignore_errors=True)

    print('\n  八闸负测（含端到端真跑）：%d/%d' % (ok, ok + fail))
    return 0 if fail == 0 else 1


def _reader_check():
    """★跑器之验，返其全部输出。★★另立此函，是为负测可替（本文件不在模块层 import subprocess）。"""
    import subprocess
    r = subprocess.run([sys.executable, os.path.join(ROOT, '工具', '同步全本阅读器.py'),
                        '--check'], cwd=ROOT, capture_output=True, text=True, timeout=300)
    return (r.stdout or '') + (r.stderr or '')


def _阅读器交封版(n):
    """★1018 X07：造式二代之章（造式.是二代）而封版·後未过（`_十一轮.json` 不在）——其阅读器之同步係
    `封版.py N --後` 之一步（净重对表补之次），合稿／回写之席之令无此器：报而⛔拦、指封版。
    已封之章（还账改旧章）、一代之章照旧处方。⛔读不出即 False（照旧处方，⛔静）。"""
    if os.path.exists(os.path.join(JJ_DIR, '第%d章' % n, '_十一轮.json')):
        return False
    try:
        import importlib.util as _u
        _sp = _u.spec_from_file_location('_zaoshi', os.path.join(os.path.dirname(os.path.abspath(__file__)), '造式.py'))
        _zm = _u.module_from_spec(_sp)
        _sp.loader.exec_module(_zm)
        return bool(_zm.是二代(n, os.path.dirname(JJ_DIR)))
    except Exception:
        return False


def _reader_stale(_check=None, 交封版=None):
    """★阅读器与正文合不合：合则返空，不合则返一行催语（只报不改）。
    ★★取器之函，不自写比对：跑 同步全本阅读器.py --check，认其「同步检查通过」六字。
    ★★★而认不出即催——一个「看不懂就当没事」的催，比没有更坏。
    交封版＝章号（`_阅读器交封版` 判真者）：只报一行、指 `封版.py N --後`（⛔⛔、⛔推必拦之语、⛔另跑同步之处方）。"""
    try:
        out = (_check or _reader_check)()
    except Exception as e:
        return ['  ⚠阅读器之验跑不起来（%s）——须人自跑一回。' % e]
    if '同步检查通过' in out:
        return []
    if 交封版:
        return ['  ·阅读器未同步（正文改了而 HTML 未改）——第%d章係造式二代、未封版：'
                '其同步在 python3 工具/封版.py %d --後（⛔此处另跑、⛔为此停；报而不拦）' % (交封版, 交封版)]
    return ['  ⛔阅读器已过期（正文改了而 HTML 未改）：'
            '★医生／检察官自测／全书检三项皆据之报红，推送必被拦。',
            '     处方：python3 工具/同步全本阅读器.py（改毕再推）']


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
    # ★★★★★2026-09-02·293第1轮自逮：**此处原比「磁盘上最後一个 vNN.md」**，
    #   ★而快照之写在诸闸之前，趋阈闸一拦即 return——**快照落了盘，台账没落**；
    #   ★★於是磁盘上多一个无账之孤版，而它恰与正文逐字相同，
    #     **空轮闸遂把「上一次被拦」读成「本轮零改动」，此後同一段文再也存不进去**：
    #     **一道闸拦了我一回，然後把门锁上了。**
    #   ★★★故改比「台账所记之末版」——**账上没有的版，不作数**。
    _vs = ledger.get('版本') or []
    _last = os.path.join(d, 'v%02d.md' % len(_vs)) if _vs else ''
    same_as_last = bool(_last) and os.path.exists(_last) and \
        open(_last, encoding='utf-8').read().strip() == txt.strip()
    halt, glines = gates(n, note, ledger, chapters_now, receipts,
                         reopen, force, same_as_last, txt,
                         新增章号=新增章号自末次存版(n))
    # 闸十·法典闸（283封版后立）：把「立过而屡犯之法」搬进这条已经卡在路上的闸里。
    #   ★其由：写在轮记散文里的法，一条也没被调起来过（掘层须有身连犯五章）；
    #     而写进闸里的（感官三密度·280第13轮立），立了就没再犯过。
    #   ★★法之生效不在措辞，在它卡不卡在路上。详见 设定/法典.json 与 工具/法典闸.py。
    try:
        import importlib.util as _ilu
        _sp = _ilu.spec_from_file_location(
            '_fadian', os.path.join(os.path.dirname(os.path.abspath(__file__)), '法典闸.py'))
        _fd = _ilu.module_from_spec(_sp); _sp.loader.exec_module(_fd)
        # ★2026-09-02·293第2轮：`snaps` 已随空轮闸之改而去，而此处仍引它——
        #   ★★遂使法典闸整个跑不成（其报只一行「未跑成」，且不拦）；
        #   ★★★**一道不拦的闸出了错，报一行就过去了**——**这一行我今日才看见。**
        #   故改与空轮闸同源：取台账所记之末版。
        _pv = os.path.join(d, 'v%02d.md' % len(_vs)) if _vs else ''
        _prev = open(_pv, encoding='utf-8').read() if (_pv and os.path.exists(_pv)) else ''
        _h10, _l10 = _fd.查(note, _prev, txt)
        if _h10 and not force:
            halt = True
        glines.extend(_l10)
    except Exception as _e:
        glines.append('   ⚠法典闸未跑成：%s（不拦，然须查）' % _e)
    # 闸八·领轮闸（批114）：凡报「第N轮」者，须先经 --下一轮 领轮。
    # 其验有三：①领过没有（未领＝未对表即动手）；
    #          ②起轮时之正文与末版是否一致（不一致＝这一轮起手时地就已经动过了）；
    #          ③所报之轮与所领之轮是否相符（不符＝轮号漂移，P23）。
    _r0 = _round_of(note)
    if _r0 and not force:
        _lg = _ling_path(n)
        if not os.path.exists(_lg):
            halt = True
            glines.append('   ⛔领轮闸：未见领轮基线——本轮未经 --下一轮 领轮即动手。')
            glines.append('     七闸皆在存版时拦，而祸起于「动手在前」；领轮是唯一能把防线提到动手之前的一步。')
            glines.append('     处方：跑 python3 工具/跑轮.py --下一轮 %d，读末版与前轮所见，再落笔。' % n)
        else:
            _b = json.load(open(_lg, encoding='utf-8'))
            _ls = _last_snap_sha(n)
            if _b.get('新章'):
                _ls = None      # 新章起手无正文可比，免其sha之验
            if _ls and _b.get('正文sha') != _b.get('末版sha'):
                halt = True
                glines.append('   ⛔领轮闸·起手即已偏：领轮时正文(%s)与当时末版(%s)不同。'
                              % (_b.get('正文sha'), _b.get('末版sha')))
                glines.append('     即这一轮起手之前，正文就已被改过而未存版——上一轮之刀没落进台账。')
                glines.append('     处方：先查那笔改动之来历，补存或还原，再起本轮。')
            if _b.get('目标轮') and _r0 != _b['目标轮']:
                halt = True
                glines.append('   ⛔领轮闸·轮号不符：所领为第%d轮，而本次报第%d轮。'
                              % (_b['目标轮'], _r0))
                glines.append('     只跑「下一个未跑之轮」——号会漂，台账不会。')

    # 闸七·轮记闸（批113）：前一轮未录轮记，不许存下一轮。
    # 轮记是压缩之后唯一能接上的东西；若可选，则必不写（本会话已反复证明「文档≠闸」）。
    _r = _round_of(note)
    _prev = max([x for x in rounds_state(ledger)[0]], default=0)
    if _r and _prev and _r > _prev and not force:
        _lp = _lunji_path(n)
        # ★2026-09-05·机制总审（八路·流程之缝审第2条）：旧式以子串「第N轮」判前轮已录轮记——前轮之引文（「留第N轮判」）先把它满足了，闸从未有机会红。
        #   今须一、二级标题以「第N轮」起头（与 _lunji_blocks 同尺）。
        _has = os.path.exists(_lp) and bool(re.search(r'^#{1,2}\s*第%d轮' % _prev, open(_lp, encoding='utf-8').read(), re.M))
        if not _has:
            halt = True
            glines.append('   ⛔轮记闸：第%d轮未录轮记，不许起第%d轮。' % (_prev, _r))
            glines.append('     轮记是压缩之后唯一能接上的东西；此刻不写，下一坐就接不上。')
            glines.append('     补录：printf \'...\' | python3 工具/跑轮.py --轮记 %d' % n)
    print('\n  ── 六闸（批112·不认人，只认磁盘之账与认知对不对得上） ──')
    for l in glines:
        print(l)
    drifted, dlines = drift_of(n, receipts, src, txt)
    for l in dlines:
        print(l)
    # ★★★★★★2026-09-16（336 第二回之实）：**给漂移哨那条处方一条真路**
    #   ⛔**旧式：本哨一红即拦，而无论如何都拦**——**其处方自书「封版之后的改动
    #     须走回补／定案并记因」（`:347` 逐字），★而「记因」二字在码里一处也没有兑现。**
    #   ★**其果**：**已封版之章一旦被救章席改过，正文与 HEAD 必不同，遂再也存不进台账**——
    #     **改动只能压在盘上，台账永远停在旧版**（0916 之实：336 之刀两次无版可入）。
    #   ★★**故立 `ZM_DRIFT_WHY` 一路，⛔只放这一哨，别哨一格不动**（⛔**非 `ZM_FORCE`**，
    #     **那一个会把回执闸／空轮闸／亮点闸一齐放倒**）；
    #     ⛔**其因须实写（八字以上），且当场记进本版之说明**——**放行即留痕，非豁免。**
    _漂因 = os.environ.get('ZM_DRIFT_WHY', '').strip()
    if drifted and not force and _漂因:
        _放, _由 = 漂移记因之判(_漂因)
        if not _放:
            halt = True
            print('   ' + _由)
        else:
            print('   ℹ漂移哨·记因放行：%s' % _由)
            print('     ★**本版之说明当场挂上此因**；⛔**别哨一格未动。**')
            note = (note + '｜漂移记因：' + _由) if note else ('漂移记因：' + _由)
            drifted = False
    if drifted and not force:
        halt = True
    git_found, git_txt = concurrency_check(quiet=True)
    if git_found:
        print(git_txt)
    if git_found:
        # 【批120·修】HEAD前进降为提示，不再拦停。
        # 病因：本路自己推送之后 HEAD 必然前进，故每推必响＝自噪声；
        #   响多了真信号被淹，此为批112所修「工作区脏」之同型（旧闸失效第二因）。
        # 且内容安全已由闸八（领轮基线：起轮时正文sha vs 当时末版sha）覆盖，
        #   HEAD 这一路本就不是内容之凭据，只是「有人提交过」之弱信号。
        print('   ℹHEAD自上次记录以来已前进（多为本路自身推送）；'
              '内容安全由闸八领轮基线把守，此处只报不拦。')
    if halt:
        raise_flag(n, '；'.join(x.strip() for x in glines if '⛔' in x) or '存版被拦', note)
        print('  ⛔存版已拦停，未写入任何文件。')
        print('  ══════════════════════════════════════════')
        print('  【定论】第%d章「%s」存版失败（rc=2）。拦停旗已落，未修之前一切轮务不办。' % (n, note))
        print('  ══════════════════════════════════════════')
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
    # ★快照之写已下移至台账之写旁（2026-09-02·293第1轮）：
    #   **原在此处落盘，而其下诸闸（棘轮／趋阈）拦停时 return，遂留一个无账之孤版**；
    #   ★★而那一句「⛔存版已拦停，未写入任何文件」当时是假话——**文件写了。**
    #   ★★★二者今同落：**账上有它，磁盘才有它。**

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
        # 【批113·修】棘轮闸须容得下 soft 不全之旧版与「重开」记录（其 soft 为空）。
        # 原码直取 r['soft'][k]，遇缺键即 KeyError——ZM_REOPEN 所写之重开记录正是空 soft，
        # 故此前只要用过一次重开，下一次存版必崩。逐键存在方参与比对。
        best = {}
        for r in ledger['版本']:
            sf = r.get('soft') or {}
            for k in RATCHET_MIN:
                if k in sf:
                    best[k] = min(best.get(k, sf[k]), sf[k])
            for k in RATCHET_MAX:
                if k in sf:
                    best[k] = max(best.get(k, sf[k]), sf[k])
            if '净重' in sf:
                best['净重'] = max(best.get('净重', sf['净重']), sf['净重'])
        # ★v01之底（RATCHET_V01·2026-09-02立）：四感不得低於起草之版。
        #   ★★其底取台账首个有 soft 之版，非历来最优——二者之别见 RATCHET_V01 之注。
        v01 = {}
        for r in ledger['版本']:
            sf = r.get('soft') or {}
            if sf:
                v01 = sf
                break
        worse = []
        for k in RATCHET_MIN:
            if k in best and soft[k] > best[k]:
                worse.append('%s %d→%d(升)' % (k, best[k], soft[k]))
        for k in RATCHET_MAX:
            if k in best and soft[k] < best[k]:
                worse.append('%s %d→%d(降)' % (k, best[k], soft[k]))
        for k in RATCHET_V01:
            if k in v01 and k in soft and soft[k] < v01[k]:
                worse.append('%s v01之%d→%d(低於起草)' % (k, v01[k], soft[k]))
        if '净重' in best and soft['净重'] < best['净重'] * 0.92:
            worse.append('净重 %d→%d(减逾8%%)' % (best['净重'], soft['净重']))
        print('  ── 棘轮闸（与历史最优逐项比） ──')
        if worse:
            print('   ⚠回退项：' + '；'.join(worse))
            print('   减法轮之净重下降属正常，须于回执写明理由；其余回退须裁定或改回。')
        else:
            # ★★★★★2026-09-02 治·**绿只及於器自印之项名**（六造§一⑤）：
            #   ★原只印一行「✓无回退」，而其下棘轮三类共八目；
            #   ★★人读到这一行，读成的是「棘轮这一项没事」——**而它只守它认的那几样**；
            #   ★★★其实证：第289章由这一行一路绿到第12轮，**听 15→12、视 56→52，八轮无一报**
            #     （其时 RATCHET_MAX 只有嗅与沈鸢，听触视三感无人守）。
            #   ★★★★故改印所守之项名：**列「所守」，不列「不守」**——不守是开集，列不全。
            print('   ✓无回退｜所守八目：%s（峰之底）｜%s（峰之底）｜%s（v01之底·四感）'
                  % ('、'.join(RATCHET_MIN), '、'.join(RATCHET_MAX), '、'.join(RATCHET_V01)))
            print('   ★而此绿只及於上列八目；未列之项本轮作「未查」，不许作「已过」。')

    # ═══ 趋阈闸（每次存版必跑·不认人只认数） ═══
    _prev = {}
    for _r in reversed(ledger.get('版本') or []):
        if _r.get('soft'):
            _prev = _r['soft']
            break
    _qy = 趋阈(_prev, soft)
    if _qy:
        print('  ── 趋阈闸（2026-09-02立·令四：墨随事重，不是墨随格子） ──')
        for _h in _qy:
            print('   %s%s %d→%d，跨过%s（限%d），**余量%d字**（此前差%d字）'
                  % ('⛔落在线上：' if _h['落在线上'] else '⚠勉强跨过：',
                     _h['项'], _h['前'], _h['後'], _h['名'], _h['限'],
                     _h['余量'], _h['此前之差']))
        if '非凑数' not in (note or ''):
            print('   ★此一跨须自证其非为格子而添：**在本轮说明里写「非凑数：<其由>」**，')
            print('     而那一行连同上列之数一并落进台账，日後可逐条回读。')
            print('   ★★其立闸之由（回灌全书台账所得）：版际之比3147次，趋阈之红68次＝2.16%；')
            print('     **而其中275、276、283、284 四章落在3500线上，余量1至5字，各自封了版，无一道闸出过声。**')
            print('  ⛔存版已拦停，未写入任何文件。')
            raise_flag(n, '趋阈闸：某数勉强跨过一条有名之限而说明未自证', note)
            return 2
        print('   ✓已自证（说明含「非凑数」），其数与其由一并落账。')

    if not note.strip():
        print('  ⛔本轮说明为空——防假跑第2条：空说明视为该轮未做。')
    _entry = {
        '版': 'v%02d' % v,
        '时': datetime.datetime.now().strftime('%m-%d %H:%M'),
        '说明': note, 'hard': hard, 'soft': soft,
        '全书章数': chapters_now, '流': _stream_id()}
    if _qy:
        _entry['趋阈'] = _qy
    # ★2026-09-05·机制总审（八路·流程之缝审第7条）：ZM_FORCE 绕闸原不落痕——台账不记其值，只有旗与免拦。
    #   今凡以 ZM_FORCE 存之版，其「记因」逐字入台账；无因者不得绕（空串即不算 force）。
    if force:
        _entry['ZM_FORCE记因'] = force[:200]
    ledger['版本'].append(_entry)
    _snap = os.path.join(d, 'v%02d.md' % v)
    open(_snap, 'w', encoding='utf-8').write(txt)
    json.dump(ledger, open(led, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    # ★0918·**本块原落在快照之写与台账之写之间，而 `负测_孤版闸` 当场报红**：
    #   ⛔**「快照之写须在台账之写之前一步（二者同落）」係一条有来历的律**——
    #   **其来历係一个真出过的孤版**（账上没有它而磁盘上有它）。
    #   ★**本坐插了二十五行在二者之间，把那一步撑开了**；**负测逮得对。**
    #   ★★**故今移到二者之後**：⛔**不减一格，反更稳**——
    #     **对档之时盘上二者皆已落定，所报之差即係盘上之实，不是半途之实。**
    # ★★★★★2026-09-18·**版档指纹之真治落码**（`设定/裁_0918_MECH-345_版档指纹_记与档之间那一段.md` 判二；
    #   其限自 345 改 347 而今提前一章办，⛔不许再往後挪第三回）：
    #   ⛔**其病**：`版档指纹.py` 逐章亲跑，印出**二十五处「台账所记之净重」与「其快照实算之净重」对不上**
    #     （−43 至 +46）；★**其害不在数之大小，在它使一整本台账不可信**——
    #     **`棘轮预检`／`趋阈`／`净重对表`／`分量闸` 逐器皆拿 `soft.净重` 当据**，
    #     ⛔**而一个曾经为真的数，与一个假数，在下游器眼里长得一模一样。**
    #   ★★**故治在写档那一下**：**档写毕，当场把它再读一回、再量一回，与将落进台账的那个数对一回。**
    #     ★★★**其义係把一件「几个月後才看得出」的事，变成一件「当场就拦下来」的事。**
    #   ⛔**其量之法自 `score` 取回，⛔不另抄一份**——**抄一份即又成两把尺，改了一头另一头照旧。**
    try:
        _回 = open(_snap, encoding='utf-8').read()
        _, _软回 = score(_回)
        _差 = [(k, soft[k], _软回[k]) for k in ('净重', '段数', '长段数')
               if k in soft and k in _软回 and soft[k] != _软回[k]]
    except Exception as _e:                      # ⛔读不回来本身即是一处红，不许静悄悄放过
        _差 = [('读不回', -1, -1)]
        print('  ⛔版档指纹·当场对档：快照写毕而读不回来（%s）' % _e)
    if _差:
        print('  ⛔**版档指纹·当场对档不合**（记与档之间那一段）：')
        for _k, _记, _档 in _差:
            print('     %s：将落台账之记 %s ｜ 快照 %s 实算 %s ｜ 差 %+d'
                  % (_k, _记, os.path.basename(_snap), _档,
                     (_档 - _记) if isinstance(_档, int) and isinstance(_记, int) else 0))
        print('     ★**台账与快照已同落，二者原样留在盘上**（⛔本器不改任何一个数——'
              '改它即是把一处「对不上」抹成一处「对得上」，而下一回它还会再来，'
              '只是再没有人看得出它来过）。')
        print('     ⛔**须当面查是哪一头错了**：`python3 工具/版档指纹.py %d`。' % n)

    try:
        # ★★★★★2026-09-02·293第2轮：**「一领一存」之「一存」，只算认了轮号的那一存。**
        #   ★领轮闸自己认的是说明里那个「第N轮」（闸八）——**说明一空，它整个不适用**；
        #   ★★而基线之销从前不问说明，於是一次 `--验收 N`（不带说明）的自动存版
        #     **既不受领轮闸管，又把领轮基线吃掉了**：★★★**不归它管的那一步，把归它管的那一步的凭据销了。**
        #   ★★★★今日一坐之内我从这个口走过三回（292 v16/v17、293 v05），三回都得回头补领轮。
        #   故改：**报轮号者方销基线；不报轮号者，基线原样留着。**
        if _round_of(note) and os.path.exists(_ling_path(n)):
            os.remove(_ling_path(n))   # 一领一存，基线用毕即销，下一轮须重领
    except Exception:
        pass
    clear_flag(n)
    print('  台账：%s（共%d版）' % (os.path.relpath(led, ROOT), v))
    # ★★★★★2026-09-01 补（287第2轮所逮·令§十一「法须变成闸方生效」）：
    # ★病灶：每轮改文之后阅读器即过期，而医生、检察官自测、全书检三项俱据之报红，
    #   ★★遂使每一轮之推送皆被拦一回——而推闸判它「不在结构性之列」，拦得对。
    # ★★★而其治只一条命令，难只在「想不起来」；故不靠记性，靠此处每存一版即报一句。
    # ★★★★而此处只报不改 HTML：改 HTML 之权在人（检察官明书「检察官未改 HTML」），
    #   ★此闸不夺其权，只把「该去改了」这一句摆到眼前。
    for _l in _reader_stale(交封版=n if _阅读器交封版(n) else None):
        print(_l)
    _rs, _miss = rounds_state(ledger)
    print('  ══════════════════════════════════════════')
    print('  【定论】第%d章「%s」存版成功（rc=0）。台账共%d版，真轮%d/%d%s'
          % (n, note, v, len(_rs), ROUNDS, '' if not _miss else '，缺 ' + '、'.join('第%d轮' % i for i in _miss)))
    print('  ══════════════════════════════════════════')
    # 【批111·修】原以"版本数"充"轮数"：而 v01 为封版基线、冷轮／终版回补／定案皆在十轮之外，
    # 故"10版"实为"基线＋9轮"，机器却报十轮已满。改为只数真轮（说明以"第N轮"起者）。
    _rounds = set()
    for _r in ledger['版本']:
        _m = re.match(r'第(\d+)轮', _r.get('说明', ''))
        if _m:
            _rounds.add(int(_m.group(1)))
    _done = len(_rounds)
    _miss = [i for i in range(1, ROUNDS + 1) if i not in _rounds]
    if _done < ROUNDS:
        print('  ⏳精进：真轮已跑 %d/%d（版本%d）；**未跑之轮：%s**'
              % (_done, ROUNDS, v, '、'.join('第%d轮' % i for i in _miss)))
    else:
        print('  ✓%d轮已满（真轮%d/%d，版本%d），请跑 --横评 %d'
              % (ROUNDS, ROUNDS, ROUNDS, v, n))
    return 0


def compare(n):
    d, led = paths(n)
    if not os.path.exists(led):
        print('  ✗第%d章尚无版本台账，先跑 --存版 %d' % (n, n))
        return 1
    versions = json.load(open(led, encoding='utf-8'))['版本']
    # ★★★★★2026-09-09·308封版之序·案席治（第一律：活干完了闸还红→闸错了，改它）：
    #   ★其红在哪一行：**「重开」是一条记因，不是一版**——其 hard/soft 皆为空表；
    #     而本函逐版取 r['soft']['净重']，遇上它当场 KeyError，
    #     **於是 `--十一轮 N` 之左眼整只瞎掉，只印一句「跑轮侧总核未能运行：'净重'」**。
    #   ★★其所以到 308 才犯：**「重开」这一记是本章之轮乱序跑才头一回大量出现的**（本章九条）；
    #     ★★★而 306／307 皆无一条，故此洞在两章封版之下一次也没有响过（P32·假绿病之同族：不是判错，是没有位）。
    #   ★★★★其治只一样：**凡无量项之记（重开／记因）不入横评之列，且当场印出它有几条**——
    #     **不是把它们算作零分，是认它们不是版**；判据一个字也没有动。
    #   ★其验在 `工具/负测_横评重开.py`（同日立·第二律）：
    #     ①拿本章今日之台账回灌，旧式抛 KeyError 而新式跑得完；
    #     ②去掉那九条「重开」，二式所印之表逐字相同（**证它只滤记因，不动任何一版**）；
    #     ③把一版之净重改坏，新式照旧在「逐项冠军」里点得出它不是末版持有（**证它没被洗白**）。
    _记因 = [r for r in versions if not (r.get('soft') or {}).get('净重')]
    versions = [r for r in versions if (r.get('soft') or {}).get('净重')]
    print('\n███ 十版横评 · 第%d章（共%d版） ███' % (n, len(versions)))
    if _记因:
        print('  ℹ另有「重开／记因」%d 条不入横评（其 hard/soft 皆空，是一条记因，不是一版）：%s'
              % (len(_记因), '、'.join(dict.fromkeys(r['版'] for r in _记因))))
    if not versions:
        print('  ✗第%d章台账里没有一版带量项，横评无从跑' % n)
        return 1

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
    if len(versions) < ROUNDS:
        print('\n  ⏳尚未满%d轮（%d/%d），横评仅供中途参考。' % (ROUNDS, len(versions), ROUNDS))
    return 0


# ★★★★★填记口（2026-09-02·292第11轮自逮）：吞记闸之同族第二形。
#   ★其形：`--验收 N` 之说明亦係位置参数（argv[3]），不写即自动存版并落一行占位说明
#     「（本轮说明未填，须在回执补记开庭与真伤级别）」；★★而落完之後，正文与末版已逐字相同，
#     空轮闸遂拦住一切 --存版／--补存——**那一行占位说明再也改不掉了。**
#   ★★★即：账上多一版跑过的样子，而它说不出自己跑的是哪一轮、动的是哪一刀；
#     真轮数轮号数的正是这一行。**一轮真跑过了，而账上说不出它跑了什么。**
#   ★★★★故立此口：只许填洞，不许覆盖记录——
#     凡该行说明非占位原文者，一律拒填（要改真说明，去 --补存 另存一版，留得下痕）。
_占位 = '（本轮说明未填，须在回执补记开庭与真伤级别）'
# ★★★★★2026-09-04·299第6轮自逮：**吞记闸之第三形**。
#   ★其形：`--存版 N` 不带说明，存版口只印一行「⛔本轮说明为空」而**照旧写盘**——
#     台账上遂多一行说明为 `''` 的版；★★而其後正文与末版逐字相同，空轮闸拦住 --存版／--补存；
#   ★★★回头走填记口，填记口只认 `_占位` 那一串字，**空字串它不认**——
#     於是那一行既补不上，也存不掉：**账上一版跑过的样子，永远说不出它跑了什么。**
#   ★★★★故今把「空说明」也算作一个洞：**填空不是覆盖真话**；
#     ★而真说明照旧不许覆盖（其判据仍是 `old` 是不是一句实话）。
_洞 = ('', _占位)


def tianji(n, ver, note):
    """填记：把台账上一行占位说明补成真说明。只填洞，不覆盖。"""
    import json as _j
    d, led = paths(n)
    if not os.path.exists(led):
        print('  ✗ 无台账：%s' % led); return 2
    if not note or note.startswith('--'):
        print('⛔填记口：说明是位置参数，不是选项。')
        print('   正确：python3 工具/跑轮.py --填记 %d v17 "第N轮·某庭：所改何事"' % n)
        return 2
    obj = _j.load(io.open(led, encoding='utf-8'))
    vs = obj['版本']
    hit = [x for x in vs if x.get('版') == ver]
    if not hit:
        print('  ✗ 台账无此版：%s（现有 %s）' % (ver, '、'.join(x.get('版', '?') for x in vs[-6:])))
        return 2
    row = hit[0]
    old = row.get('说明', '')
    if old.strip() not in _洞:
        print('⛔填记口：此行已有真说明，不许覆盖——本口只填洞。')
        print('   %s 现说明：%s' % (ver, old[:80]))
        print('   ★要改一个已写实的说明，须另存一版（--补存），让两行都留在账上；')
        print('   ★★账是用来查的，不是用来好看的：改掉一行真话，日後就查不出它原来说的是什么。')
        return 2
    row['说明'] = note + '·填记'
    # ★原说明记的是那一格原来实际是什么（空字串即记「（空）」），不许写死成占位那一串：
    #   2026-09-04·299第6轮自逮——空说明那一格填进去之後，账上会多出一句它从来没说过的话。
    row['原说明'] = old if old else '（空）'
    io.open(led, 'w', encoding='utf-8').write(_j.dumps(obj, ensure_ascii=False, indent=1))
    print('  ✓填记 %s：%s' % (ver, note[:70]))
    print('  ℹ并留「原说明」一格（原：%s），见得出这一行是後填的，不是当场写的。'
          % (old if old else '（空）'))
    # ★★销旗之路（2026-09-04·299第6轮立）：**只销「填的正是它拦的那一轮」那一面旗**。
    #   ★其由：旗之义是「那一轮的版没存上」；而填记既已把那一轮之版落成真说明，
    #     那一轮在账上就有了身——旗所报之事已不成立。
    #   ★★而其条件写死三样，缺一不销：①旗在｜②旗之「本次说明」所报之轮号
    #     与本次所填之轮号同｜③所填之版即台账上报那一轮之版。
    #   ★★★如此它销不掉任何一面「别的轮被拦」之旗，亦销不掉一面「说明里报不出轮号」之旗。
    fl = read_flag(n)
    本轮 = _round_of(note)
    if fl and 本轮 is not None and _round_of(str(fl.get('本次说明', ''))) == 本轮 \
            and _round_of(row['说明']) == 本轮:
        clear_flag(n)
        print('  ✓拦停旗已销：旗所拦者即第%d轮，而第%d轮之版（%s）今已在账上有真说明。'
              % (本轮, 本轮, ver))
        print('     ★其所以销得**：旗之义是「那一轮的版没存上」，而它存上了；'
              '★★而别的轮之旗、报不出轮号之旗，此口一面也销不掉。')
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
    if cmd == '--补记':
        return buji(n, int(sys.argv[3]), sys.stdin.read())
    if cmd == '--必答':
        return bida(n, int(sys.argv[3]))
    if cmd in ('--十一轮', '--总核'):
        return zonghe(n)
    if cmd == '--尽力':
        return jinli(n)
    if cmd == '--验轮':
        return yanlun(n)
    # ★★★★★吞记闸（2026-09-02·291第13轮开轮时自逮）：说明是位置参数（argv[3]），
    #   ★而我写成 `--存版 291 --记 "…"`，於是「--记」当了说明，我那一行真文被静静丢弃；
    #   ★★两版之说明尽失（v15「--记」、v16「--记·补存」），真轮遂数不着第12轮——
    #      **一轮真跑过了，而账上说它没跑。**
    #   ★★★其族同第二十三犯：**器收下了一样它本该拒收的东西，而它一声没出。**
    #   ★★★★故凡说明以「--」起手者，当场拦停并印出正确写法；不许猜、不许拼。
    def _记(argv):
        t = argv[3] if len(argv) > 3 else ''
        if t.startswith('--'):
            print('⛔吞记闸：说明写成了「%s」——说明是位置参数，不是选项。' % t)
            print('   ★你多写的那一行真文已被丢弃（argv[4] 起本器一概不读）。')
            print('   正确：python3 工具/跑轮.py %s %s "第N轮·某庭：所改何事"' % (argv[1], argv[2]))
            if len(argv) > 4:
                print('   ★★你本来要写的是：%s' % ' '.join(argv[4:]))
            raise SystemExit(2)
        return t

    if cmd == '--填记':
        return tianji(n, sys.argv[3] if len(sys.argv) > 3 else '',
                      sys.argv[4] if len(sys.argv) > 4 else '')
    if cmd == '--补存':
        # ⛔★★★★★2026-09-24 立·**说明短於八字者拒存**（体检账通例一〇二之第二回·本坐所犯）：
        #   ★通例一〇二记过一回「**拿一件会写盘的器去『看一眼』，於是往台账上落了一行『x』**」；
        #   ⛔**0924 本坐一字不差地复犯**：以 `--补存 363 "x"` 探存版闸之错，**它其实存成了**，
        #     台账上遂落一版说明作「x」，并又立一面旗——**而那条通例就在本坐当日立的进化链里。**
        #   ★★**一条教训写在纸上，拦不住下一次；故立器**：一版之说明係其凭据，**短於八字者不是说明，是探针**。
        _说 = _记(sys.argv)
        if len(re.sub(r'\s', '', _说 or '')) < 8:
            print('  ⛔补存拒：说明「%s」短於八字——⛔**一版之说明係其凭据；短於此者多半是拿存版器当探针**'
                  '（体检账通例一〇二·0924 复犯）。**要看闸报什么，读 `--对表`，⛔不许拿会写盘的器去「看一眼」。**'
                  % (_说 or ''))
            return 2
        return buccun(n, _说)
    if cmd == '--还原':
        return huanyuan(n, sys.argv[3] if len(sys.argv) > 3 else '')
    if cmd == '--下一轮':
        return nextround(n)
    if cmd == '--轮记':
        return lunji_append(n, sys.stdin.read())
    # ★★★★★存口之别名（0909·308第3轮第3转立·同一坑第三回，依令第五部分之律涨器）：
    #   ★起草令与本坐所奉之令写的是 `--存`，而本器只认 `--存版`——
    #     **奉令者照令打字，器一声不出地印出 __doc__ 返 1；他多半当它跑过了。**
    #   ★★其历：308第1轮之轮记记过一回｜第2转之轮记记过一回（并自书「第三回就该涨器」）｜本转第三回。
    #   ★★★**这一改是补入口，不是放宽**：判据、闸序、吞记闸一字未动，`--存` 与 `--存版` 逐路同走。
    if cmd in ('--存版', '--存'):
        return save(n, _记(sys.argv))
    if cmd == '--横评':
        return compare(n)
    print(__doc__)
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
