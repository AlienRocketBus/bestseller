#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跑轮（存版之器·批102立法；1027 汰十三轮之支，只留存版与其闸）

**本文件是库，亦是存版之口。**今之用（造式二代）：
    python3 工具/跑轮.py --存 410 "造式二代·合稿：<一句话>"   （--存版 为其别名；⛔说明以「第N轮」起）
    python3 工具/跑轮.py --十一轮 410      第十一轮之左眼（造式之实·空版·旗·正文与末版·横评）；凭由 小说检察官 --十一轮 出
    python3 工具/跑轮.py --补存 / --对表 / --还原 / --自测
库：score、gates（回执／轮次／章界／空轮／亮点）、法典闸、concurrency_check、drift_of、zonghe、chap_num、body_of。
⛔所废（1027·十三轮之制）：--下一轮 --轮记 --补记 --填记 --必答 --尽力 --验轮 --横评 与必答表、裁定查、尽力查。
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
    故改为**粘性**：拦停之事实落盘为旗（旧 `--下一轮`／`--轮记` 见旗即拒，1027 随十三轮汰），
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


# 旧填记口之占位说明（填记口 1027 随十三轮汰；旧台账或存此串，_flag_stale 仍须认之）
_占位 = '（本轮说明未填，须在回执补记开庭与真伤级别）'


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


def _ling_path(n):
    return os.path.join(paths(n)[0], '_领轮.json')


def _last_snap_sha(n):
    d = paths(n)[0]
    snaps = sorted(glob.glob(os.path.join(d, 'v[0-9][0-9].md')))
    return _sha(open(snaps[-1], encoding='utf-8').read()) if snaps else None


def _lunji_path(n):
    return os.path.join(paths(n)[0], '_轮记.md')


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
               % ('已交（已封，只许回补／定案）' if rc else '未交', _book_chapters()))
    if os.path.exists(led):
        lg = json.load(open(led, encoding='utf-8'))
        vs = lg.get('版本', [])
        last = vs[-1] if vs else {}
        out.append('   台账：共%d版，末版 %s「%s」%s'
                   % (len(vs), last.get('版', ''), last.get('说明', ''), last.get('时', '')))
    else:
        out.append('   台账：无')
    if src:
        dr, dl = drift_of(n, rc, src, open(src, encoding='utf-8').read())
        out.extend(dl)
    return '\n'.join(out)


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
    """【第十一轮·左眼】造式之章之总核：造式之实（工具/造式.py）、空轮、旗、正文与末版、横评。
    ⛔1027 汰十三轮：非造式之章（十三轮所封）⛔再核——其凭已出於其封版之日；挂牌无实照旧不过（⛔豁免）。
    任一硬项不过即不出总核凭据，封版闸据此拦。"""
    d, led = paths(n)
    if not os.path.exists(led):
        print('  ✗第%d章尚无台账。' % n)
        return 2
    _造, _造缺 = _造式判(n)
    if not _造:
        print('\n  ⛔第%d章非造式之章（无 版本/第%d章/_式.md）：十三轮之制 1027 已汰，⛔再走总核。' % (n, n))
        print('     旧章之凭（_总核.json／_十一轮.json）已出於其封版之日；改旧章走 改单 --施单／还账，⛔重开轮。')
        return 2
    lg = json.load(open(led, encoding='utf-8'))
    vs = lg.get('版本', [])
    lj = _lunji_blocks(n)
    src = find_chapter(n)
    txt = open(src, encoding='utf-8').read() if src else ''
    hard, soft_warn = [], []

    print('\n████ 第十一轮·总核轮 · 第%d章 ████' % n)

    # 甲·造式之实
    print('\n  ── 甲·造式之实 ──')
    byr = {}
    for x in vs:
        r = _round_of(x.get('说明', ''))
        if r:
            byr.setdefault(r, []).append(x)
    print('   ★本章係造式之章（版本/第%d章/_式.md）：核造式之实（工具/造式.py）。' % n)
    for _x in _造缺:
        hard.append('造式之实缺：' + _x)
    # ★在册之轮（一代造式之机闸第3轮）照旧须有轮记——跑过的那一轮，一格不松
    _缺记 = [i for i in sorted(byr) if i not in lj]
    if _缺记:
        hard.append('缺轮记之轮（在册而无记）：' + '、'.join('第%d轮' % i for i in _缺记))
    if not _造缺 and not _缺记:
        print('   ✓造式之实俱齐%s。' % ('；在册之轮版与记俱齐' if byr else ''))

    # 乙·空轮查（版与前版逐字同而未记判不补／零刀者）
    print('\n  ── 乙·空轮查 ──')
    prev_txt = None
    for x in vs:
        vp = os.path.join(d, x.get('版', '') + '.md')
        cur = open(vp, encoding='utf-8').read() if os.path.exists(vp) else None
        r = _round_of(x.get('说明', ''))
        tag = []
        if cur is not None and prev_txt is not None and cur.strip() == prev_txt.strip():
            tag.append('**空轮（与前版逐字相同）**')
            # ★与 gates()::空轮闸 同一份词表（0917·339 v03：⛔一条律两份词表）
            if not re.search(r'判不补|零刀|不补|无真伤', x.get('说明', '')):
                hard.append('%s 为空版而未记判不补／零刀' % x.get('版'))
        if '补存' in x.get('说明', ''):
            tag.append('补存（非当场所存）')
        if r and r in lj:
            body = '\n'.join(lj[r])
            n_ch = len(re.sub(r'\s', '', body))
            if n_ch < 120:
                hard.append('第%d轮轮记过简（仅%d字），不足以证其跑透' % (r, n_ch))
                tag.append('轮记仅%d字' % n_ch)
            if not re.search(r'真伤|判不补|零刀|判合|无刀|皆拒|交白卷'
                             r'|[不未]落刀|落[一二三四五六七八九十两\d]+刀', body):
                hard.append('第%d轮轮记无裁语（真伤／判不补／零刀／判合／无刀／皆拒／交白卷／落〈数〉刀），'
                            '不足以证其跑透' % r)
                tag.append('无裁语')
        print('   %-5s %-26s %s' % (x.get('版'), x.get('说明', '')[:26], '｜'.join(tag) or '✓'))
        if cur is not None:
            prev_txt = cur

    # 丙·状态查
    print('\n  ── 丙·状态查 ──')
    fl = read_flag(n)
    if fl:
        hard.append('拦停旗未销（%s）' % fl.get('时'))
    ls = _last_snap_sha(n)
    cur_sha = _sha(txt) if txt else None
    drift = bool(ls and cur_sha and ls != cur_sha)
    if drift:
        hard.append('正文与末版已偏（末一刀没落台账）')
    print('   拦停旗：%s｜正文与末版：%s'
          % ('无' if not fl else '**有**', '已偏' if drift else '一致'))

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
    json.dump({'时': datetime.datetime.now().strftime('%m-%d %H:%M'),
               '版数': len(vs), '真轮': sorted(byr), '轮记轮': sorted(lj),
               '补存版数': sum(1 for x in vs if '补存' in x.get('说明', '')),
               '软项': soft_warn, '流': _stream_id(), '式': '造式'},
              open(os.path.join(d, '_总核.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print('  【总核·通过】造式之实俱齐、无未记之空版、无旗、正文与末版一致。')
    print('  已出总核凭据：版本/第%d章/_总核.json（封版闸据此放行）。' % n)
    print('  ══════════════════════════════════════════')
    return 0


def 旧字残留(prev, txt, k=2):
    """★1110 X93（435 总编辑改 :47「灶口里还红着」而亮点六仍书「灶口还红」，记席方逮）：
    取末版→今版白文所删之处（含删口两侧），其 k 字串已从今之白文绝迹而仍见於【本章亮点】者，回 [(亮点之第几行, [串…])]。
    纯判·可负测。只报不拦：亮点述物可用异於白文之称（436「记水那一页」），2 字之检有此假红——拦则误拦（丝滑主义）。"""
    import difflib
    分 = '【本章亮点】'
    if not prev or 分 not in txt:
        return []
    旧白 = prev.split(分)[0]
    新白, 新亮 = txt.split(分, 1)
    sm = difflib.SequenceMatcher(None, 旧白, 新白, autojunk=False)
    删 = set()
    for op, a1, a2, _b1, _b2 in sm.get_opcodes():
        if op in ('replace', 'delete'):
            s = 旧白[max(0, a1 - k + 1):a2 + k - 1]
            for i in range(len(s) - k + 1):
                g = s[i:i + k]
                if g not in 新白 and not any(c in '，。、：；！？「」『』…—\n \t' for c in g):
                    删.add(g)
    出 = []
    for j, l in enumerate(新亮.split('\n')):
        hit = sorted(g for g in 删 if g in l)
        if hit:
            出.append((j, hit))
    return 出


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
    # ★1110 X93·旧字残留：逮得住（435 之例）、不误报（亮点未引所删者）、无亮点即空
    chk('旧字残留·逮得住', 旧字残留('灶口里还红着。\n【本章亮点】\n', '灶口埋着灰。\n【本章亮点】\n六·灶口还红\n') == [(1, ['还红'])])
    chk('旧字残留·不误报', 旧字残留('灶口里还红着。\n【本章亮点】\n', '灶口埋着灰。\n【本章亮点】\n六·灰拨匀\n') == [])
    chk('旧字残留·无亮点即空', 旧字残留('甲乙丙。', '甲丁丙。') == [])
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

    # ── 拦停旗之生灭（1027 自全测「轮次完整性回归」移入）：存版被拦即落旗；旗在而一次成功之存版销之。
    #   ★旗不销，总核（zonghe·丙）即拦「拦停旗未销」而封不了版——故销之一路须真跑一回。
    def _旗局(mk, note, 先立旗=False, 局=None):
        global ROOT, JJ_DIR
        tmp = tempfile.mkdtemp(prefix='zm_flag_')
        try:
            os.makedirs(os.path.join(tmp, '正文'))
            os.makedirs(os.path.join(tmp, '设定'))
            ROOT, JJ_DIR = tmp, os.path.join(tmp, '版本')
            mk(tmp)
            if 局:
                局(tmp)
            if 先立旗:
                raise_flag(7, '测试之由（棘轮回退）', '第2轮·测')
            立 = read_flag(7) is not None
            with contextlib.redirect_stdout(io.StringIO()):
                rc = save(7, note)
            return 立, rc, read_flag(7)
        finally:
            ROOT, JJ_DIR = _R, _J
            shutil.rmtree(tmp, ignore_errors=True)

    _立, _rc, _旗 = _旗局(s_nolog, '第2轮·四堂会审')
    chk('拦停旗·存版被拦即落旗（rc=%s 须2，旗须在）' % _rc, (not _立) and _rc == 2 and _旗 is not None)
    _立, _rc, _旗 = _旗局(s_withlog, '第2轮·四堂会审', 先立旗=True)
    chk('拦停旗·旗在而一次成功之存版销之（rc=%s 须0，旗须无）' % _rc, _立 and _rc == 0 and _旗 is None)

    # ── 1027：造式二代未封之章 save() ⛔调阅读器之验（约六秒之子进程只得一句定语；其同步在 封版 --後）；
    #   已封（_十一轮.json 在）、一代之章照旧验——还账改旧章即走後者。⛔回灌旧式（一律调之）须红：以调数验。
    _调 = []
    _真验 = globals()['_reader_check']

    def _式局(式, 已封):
        def mk(tmp):
            d = os.path.join(tmp, '版本', '第7章')
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, '_式.md'), 'w', encoding='utf-8').write(式 + '\n')
            if 已封:
                open(os.path.join(d, '_十一轮.json'), 'w', encoding='utf-8').write('{}')
        return mk

    globals()['_reader_check'] = lambda: (_调.append(1), '同步检查通过')[1]
    try:
        _结 = []
        for _式, _封 in (('式：虫洞（造式二代·1013）', False), ('式：虫洞（造式二代·1013）', True), ('式：虫洞（一代）', False)):
            del _调[:]
            _, _rc, _ = _旗局(lambda t: _ch(t, '甲乙丙丁戊己'), '造式二代·合稿：测之一句足八字以上', 局=_式局(_式, _封))
            _结.append((_rc, len(_调)))
    finally:
        globals()['_reader_check'] = _真验
    chk('X07·二代未封之章存版⛔调阅读器之验；已封、一代照旧验（%s）' % _结,
        _结 == [(0, 0), (0, 1), (0, 1)])

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

    # 闸六·空轮闸与验轮闸不得相犯（批113修）
    chk('空轮闸须放行明记判不补之轮（轮号照挂）',
        not gates(1, '第4轮·升华庭·判不补·记因', L([v('第3轮·乙', ch=5)]), 5, [],
                  same_as_last=True)[0])
    chk('空轮闸仍拦未记判不补之零改动轮',
        gates(1, '第4轮·升华庭', L([v('第3轮·乙', ch=5)]), 5, [], same_as_last=True)[0])

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
    _造核('⑦同一局而无 _式.md 者（非造式之章·十三轮 1027 汰）⛔总核', 2, 无式=True)
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

    # ★1018 X07：他章（已封、一代）阅读器过期照旧处方；合则不报（二代未封之章之⛔调见上之端到端）
    _旧 = _reader_stale(lambda: '不合')
    chk('X07·他章照旧处方；合则不报', any('同步全本阅读器.py' in x for x in _旧) and _reader_stale(lambda: '同步检查通过') == [])
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


def _reader_stale(_check=None):
    """★阅读器与正文合不合：合则返空，不合则返一行催语（只报不改）。
    ★★取器之函，不自写比对：跑 同步全本阅读器.py --check，认其「同步检查通过」六字。
    ★★★而认不出即催——一个「看不懂就当没事」的催，比没有更坏。
    ⛔造式二代未封之章 save() ⛔调之（其同步在 封版 --後；1027）。"""
    try:
        out = (_check or _reader_check)()
    except Exception as e:
        return ['  ⚠阅读器之验跑不起来（%s）——须人自跑一回。' % e]
    if '同步检查通过' in out:
        return []
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
        for _j, _g in 旧字残留(_prev, txt):
            glines.append('   ⚠旧字残留（X93·只报）：白文已删「%s」，而【本章亮点】第 %d 行仍见——查亮点／骨记随改否' % ('」「'.join(_g), _j))
    except Exception as _e:
        glines.append('   ⚠法典闸未跑成：%s（不拦，然须查）' % _e)
    # 闸八·领轮闸（批114）：凡报「第N轮」者，须有领轮之基线（旧由 --下一轮 落；1027 十三轮汰，⛔再领——故第N轮之说明今恒拦）。
    # 其验有三：①领过没有（未领＝未对表即动手）；
    #          ②起轮时之正文与末版是否一致（不一致＝这一轮起手时地就已经动过了）；
    #          ③所报之轮与所领之轮是否相符（不符＝轮号漂移，P23）。
    _r0 = _round_of(note)
    if _r0 and not force:
        _lg = _ling_path(n)
        if not os.path.exists(_lg):
            halt = True
            glines.append('   ⛔领轮闸：说明以「第%d轮」起而无领轮基线——十三轮之制 1027 已汰。' % _r0)
            glines.append('     处方：说明⛔以「第N轮」起（造式二代作「造式二代·合稿／回写／定稿：<一句话>」），再存。')
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
            glines.append('     处方：十三轮之制 1027 已汰——说明⛔以「第N轮」起（造式二代作「造式二代·…」）。')
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
    # ★1027 汰：造式二代未封之章，阅读器之同步係 封版 --後 之一步——其验（约六秒之子进程）只得一句定语，⛔跑；
    #   已封之章（还账改旧章）、一代之章照旧验而处方。
    if not _阅读器交封版(n):
        for _l in _reader_stale():
            print(_l)
    print('  ══════════════════════════════════════════')
    print('  【定论】第%d章「%s」存版成功（rc=0）。台账共%d版。' % (n, note, v))
    print('  ══════════════════════════════════════════')
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
    if cmd in ('--十一轮', '--总核'):
        return zonghe(n)
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
            print('   正确：python3 工具/跑轮.py %s %s "造式二代·合稿：所改何事"' % (argv[1], argv[2]))
            if len(argv) > 4:
                print('   ★★你本来要写的是：%s' % ' '.join(argv[4:]))
            raise SystemExit(2)
        return t

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
    # ★★★★★存口之别名（0909·308第3轮第3转立·同一坑第三回，依令第五部分之律涨器）：
    #   ★起草令与本坐所奉之令写的是 `--存`，而本器只认 `--存版`——
    #     **奉令者照令打字，器一声不出地印出 __doc__ 返 1；他多半当它跑过了。**
    #   ★★其历：308第1轮之轮记记过一回｜第2转之轮记记过一回（并自书「第三回就该涨器」）｜本转第三回。
    #   ★★★**这一改是补入口，不是放宽**：判据、闸序、吞记闸一字未动，`--存` 与 `--存版` 逐路同走。
    if cmd in ('--存版', '--存'):
        return save(n, _记(sys.argv))
    print(__doc__)
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
