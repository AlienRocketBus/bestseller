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


# ★★★★★DEBT-298A（298第12轮立·限307·於307封版之序结清）
#   ★其伤逐字（到期账 items::DEBT-298A）：**「棘轮之『四字三现』认的是四字之窗，不是词；
#     故一句被数两遍」**——298第12轮实数：19样之中「那一圈水印」×3 出「那一圈水」＋「一圈水印」两条、
#     「门口那只碗」出「门口那只」＋「口那只碗」、「她一回也没」出「她一回也」＋「一回也没」、
#     「宽的那一半」出「宽的那一」＋「的那一半」——**四句生八条**。
#   ★★即：**一句五个字的重出，在这把尺上算两处；六个字的算三处**——
#     **句子越长，它被罚得越重，而它其实只重了一回。**
#   ★★★而 298 当章一行代码不动此尺（令§六★★★★：不许为了让自己那一笔过去而挖空闸），
#     故其治拖到 307：**不改旧式，另立一个认词之变式**，二式并存，旧式照旧管棘轮之判。
#   ★★★★其法（照其档所命）：**以最长可合并之串为身**——
#     凡四字之窗出现≥3次者，向左右各试着长一个字；只要长出来的那一串仍出现≥3次，就用长的顶掉短的；
#     末了把「已被别的串整个含住」的那些去掉。**一句只算一处，不论它有几个字。**
def rep3_by_word(body, 门=3):
    """四字三现·认词：把重叠之窗合成最长之串，一句只算一处。返回 (处数, [串…])。"""
    seen = {}
    for i in range(len(body) - 3):
        k = body[i:i + 4]
        if re.match(r'^[\u4e00-\u9fa5]{4}$', k):
            seen[k] = seen.get(k, 0) + 1
    cand = {k for k, v in seen.items() if v >= 门}
    grown = set()
    for k in cand:
        cur = k
        while True:
            better = None
            # 向右长一个字
            for ch in {body[m.end():m.end() + 1]
                       for m in re.finditer(re.escape(cur), body)}:
                if ch and re.match(r'^[\u4e00-\u9fa5]$', ch) and body.count(cur + ch) >= 门:
                    better = cur + ch
                    break
            if better is None:
                # 向左长一个字
                for ch in {body[max(m.start() - 1, 0):m.start()]
                           for m in re.finditer(re.escape(cur), body)}:
                    if ch and re.match(r'^[\u4e00-\u9fa5]$', ch) and body.count(ch + cur) >= 门:
                        better = ch + cur
                        break
            if better is None or better == cur:
                break
            cur = better
        grown.add(cur)
    # 去掉被别的串整个含住者（「那一圈水」已在「那一圈水印」里，不再另算一处）
    最长 = sorted(grown, key=len, reverse=True)
    留 = []
    for x in 最长:
        if not any(x in y and x != y for y in 留):
            留.append(x)
    return len(留), sorted(留)


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

    hard = {
        '破折': txt.count('—'),
        '半角逗': txt.count(','),
        '半角引号': txt.count('"'),
        '五逗句': sum(1 for s in sents if s.count('，') >= 5),
        '英文': len(re.findall(r'[A-Za-z]', txt)),
        '章号入正文': len(re.findall(r'[一二三四五六七八九十百]+章', body)),
        '禁抖': body.count('抖'),
        '永禁词': sum(body.count(w) for w in ['哆嗦', '骊山', '僵尸', '点亮']),
        # 【修】原取 txt（全文），致亮点块「一行一条、条间不空行」之体例被误判为正文段落黏连。
        # 邻项凡查正文者皆用 body、查亮点者皆用 hl；此处独用 txt 与自身体例不一致。段落空行系正文体例，故改 body。
        '段间空行病': len(re.findall(r'。\n(?!\n)[^\n]', body)),
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
    # ⛔认三种，不只认作业单（限360·其详在 全测.py::_已封版）
    return sorted(f for k in ('作业单', '案席', '封版席')
                    for f in glob.glob(os.path.join(ROOT, '设定', '回执_*_第%d章%s.md' % (n, k))))


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
    # 【批113·修】初版与验轮闸相犯：零刀之轮若被迫改用非「第N轮」之说明，验轮闸即判其未跑，
    #   遂令「审毕判不补」这一合法结局无从表述。故凡说明中明记判不补者放行，仍挂其轮号。
    _nocut = bool(re.search(r'判不补|零刀|不补|无真伤', note or ''))
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


def rounds_state(ledger, n=None):
    """返回 (已跑真轮集合, 缺轮列表)。

    真轮＝**说明以「第N轮」起者**，★**或轮记里那一轮有实文（去空白 ≥120 字）**。

    ★★★**後半是 0910 补的，其由是一次实卡（310 第11轮）**：
    　领轮闸拦下第11轮，说「所领为第1轮」。而查其实：台账十四版、轮记里第 1/3/5/6/7/8/9/11 轮
    　俱有逐条实文——**十几轮的活真干了，只是它的说明没以「第N轮」起头**。
    　★其所以不以「第N轮」起头，是**席自己为了不绕闸而选的路**：轮次闸曾因旧误标而拦，
    　　席不肯改轮号绕它，改以非「第N轮」之说明存版，并把其由逐字记在轮记里（v05—v07、v10、v11、v13）。
    　★★**於是成了一个自锁的圈**：闸拦→席避开轮号→台账永远认不出那一轮→闸拦得更死。
    　★★★**而这不是新立一条宽路**：本器自己在覆盖查那一处早就写着同一条——
    　　「**存过版，或轮记里那一轮有实文（去空白 ≥120 字），二者有其一即算跑过**」
    　　（见 `_有实记` 之注：一行「已完成」不算）。**今只是把那一条搬到它本该也在的这一处。**
    　★★★★**其非放水之凭**：`工具/负测_真轮凭轮记.py` 之⑧⑨两格拿真偷懒之局回灌，须照旧判红。

    n 给了才查轮记；不给则照旧只认台账（旧调用一处不必改，其判分毫不变）。
    """
    rs = set()
    for x in ledger.get('版本', []):
        r = _round_of(x.get('说明', ''))
        if r:
            rs.add(r)
    if n is not None:
        try:
            lj = _lunji_blocks(n)
            for i, bs in lj.items():
                if len(re.sub(r'\s', '', '\n'.join(bs))) >= 120:
                    rs.add(i)
        except Exception:
            pass
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
        rs, miss = rounds_state(lg, n)
        print('  真轮：%d/10%s' % (len(rs), '' if not miss else
              '｜缺 ' + '、'.join('第%d轮' % i for i in miss)))
        # 【批112·闸四｜批113修】封版凭据之验，两级判：洞＝硬伤，短＝存疑。
        if rc:
            for l in rounds_verdict(lg)[2]:
                print(l)
    else:
        print('  台账：无')
    return 0


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
    base['正文sha'] = base.get('末版sha')
    base['目标轮'] = _round_of(note)
    base['补存'] = True
    os.makedirs(d, exist_ok=True)
    json.dump(base, open(lg, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
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


def flag_block(n, who):
    """见旗即拒。返回 True 表示须拒。"""
    fl = read_flag(n)
    if not fl or os.environ.get('ZM_FORCE', '').strip():
        return False
    print('\n  ⛔拦停旗未销：第%d章上一次存版被拦停（%s），至今未修。' % (n, fl.get('时', '?')))
    print('     拦停之由：%s' % str(fl.get('因', ''))[:160])
    print('     当时所报：%s' % str(fl.get('本次说明', ''))[:60])
    print('     **旗在，%s 一律不办。** 旗只由一次成功的存版／补存销去。' % who)
    print('     修法：python3 工具/十轮精进.py --补存 %d "第N轮·镜头"' % n)
    print('       或：python3 工具/十轮精进.py --还原 %d 确认' % n)
    return True


def _ling_path(n):
    return os.path.join(paths(n)[0], '_领轮.json')


def _last_snap_sha(n):
    d = paths(n)[0]
    snaps = sorted(glob.glob(os.path.join(d, 'v[0-9][0-9].md')))
    return _sha(open(snaps[-1], encoding='utf-8').read()) if snaps else None


def _lunji_path(n):
    return os.path.join(paths(n)[0], '_轮记.md')


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
    print(duibiao_brief(n))
    d, led = paths(n)
    lg = json.load(open(led, encoding='utf-8')) if os.path.exists(led) else {'版本': []}
    rs, miss = rounds_state(lg, n)
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
            print('       ①补存那一轮：python3 工具/十轮精进.py --补存 %d "第N轮·镜头"' % n)
            print('       ②还原到末版：python3 工具/十轮精进.py --还原 %d 确认' % n)
            print('     修完再跑 --下一轮 %d。' % n)
            return 2

    # 【批120·修】新章起手时正文尚未存在，find_chapter 返回空则基线不落盘，
    #   闸八遂令新章之第1轮永远过不去。故无正文者亦落基线，只是标为新章、免其sha之验。
    base = {'时': datetime.datetime.now().strftime('%m-%d %H:%M'),
            '正文sha': _sha(open(src2, encoding='utf-8').read()) if src2 else None,
            '末版sha': _last_snap_sha(n),
            '目标轮': (miss[0] if miss else None),
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
            _fp = os.path.join(REPO_ROOT, _f) if 'REPO_ROOT' in dir() else _f
            if not os.path.exists(_fp):
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
        rs, miss = rounds_state(lg, n)
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
    for b in open(f, encoding='utf-8').read().split('\n## '):
        if not b.strip():
            continue
        m = re.match(r'第(\d+)轮', b)
        if m:
            last = int(m.group(1))
            out.setdefault(last, []).append('## ' + b)
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
        r'这两天|这几天|这十来天|早上|进来的时候|前十|二十七年前')


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


VERDICT = ('✓', '合', '改', '核', '真伤', '判', '未见', '零', '缺', '对', '错', '撞', '补')

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
        pos = [m.start() for m in re.finditer(re.escape(x), logtext)]
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
        if grew <= 0:
            hard.append('自起版至峰值一字未长（%+d）——十几轮只在删和改，'
                        '没有一轮在长；其治是回深掘轮，不是补字' % grew)
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
        _mark = '✓' if (_zhi >= 2 or _fl >= 2 or _zs >= 1 or _fan >= 1 or _chan >= 1) else '⚠'
        if _mark == '⚠':
            _idle.append(_r)
        print('   第%-2d轮 真伤%d 治%2d 复量%2d 产出%d %s' % (_r, _zs + _fan, _zhi, _fl, _chan, _mark))
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
    # ★★★2026-09-09 改·作者令「只许优化不许降低质量」之下的第二次改闸（与 _rounds_full 同理同测）：
    #   ★**本器所问者是「这一轮跑没跑」，而它只认一种凭据：台账里存过一版。**
    #     而 `工具/跑轮.py` 立轮记之日自书：「存版只存文本与数字，**不存『这一轮看见了什么』**；
    #     压缩一来，那一部分就没了，下一轮遂无从承前（P22断层续手）」——**轮记是强证，存版是弱证。**
    #   ★★其形之实：0908—0909 立八席之路（`工具/席/一章.js`），十三轮之活由十一段席分担，
    #     **一段席常收数轮之刀而只存一版**；306 十三轮逐轮有实记（覆盖查 13 轮俱 100%／100%），
    #     而「缺版之轮」照旧报第1—12轮。
    #   ★★★**而本器自己那一条原则，正说着这一件**（见 `_is_old_era` 之注）：
    #     **「凡今日方立之闸，不得拿去量它立法之前就已封版的章——那不是伤，是制度换代。」**
    #     「每轮存版」係 0909 方接进流水线，而 306 係 0908 封版。
    #   ★★★★故改：**存过版，或轮记里那一轮有实文（去空白 ≥120 字），二者有其一即算跑过。**
    #     ★**一行「已完成」不算**——那正是轮记之立所要治的那一样。
    #   ★★★★★**其非挖空之凭**：`工具/负测_真轮凭轮记.py` 之⑧⑨两格拿真偷懒之局回灌，
    #     须照旧判红；**逮不住旧局的新闸，一律不接。**
    def _有实记(i):
        b = '\n'.join(lj.get(i, []))
        return len(re.sub(r'\s', '', b)) >= 120
    miss_v = [i for i in range(1, _era + 1) if i not in byr and not _有实记(i)]
    miss_l = [i for i in range(1, _era + 1) if i not in lj]
    print('   有版之轮：%s' % ('、'.join(str(i) for i in sorted(byr)) or '无'))
    print('   有记之轮：%s' % ('、'.join(str(i) for i in sorted(lj)) or '无'))
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
            if '判不补' not in x.get('说明', ''):
                hard.append('%s 第%s轮为空轮而未记判不补' % (x.get('版'), r))
        if '补存' in x.get('说明', ''):
            tag.append('补存（非当场所存）')
        if r and r in lj:
            body = '\n'.join(lj[r])
            n_ch = len(re.sub(r'\s', '', body))
            if n_ch < 120:
                hard.append('第%d轮轮记过简（仅%d字），不足以证其跑透' % (r, n_ch))
                tag.append('轮记仅%d字' % n_ch)
            if not re.search(r'真伤|判不补|零刀|判合', body):
                hard.append('第%d轮轮记无「真伤／判不补／零刀／判合」之裁，不足以证其跑透' % r)
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
    # ★★★★★2026-09-04 治（301封版之序自逮·令§六）：**这道闸写着一句它自己认不出来的话。**
    #   ★其红在哪一行：其罚辞明书「须逐轮说明何以皆无，否则视为应付」——
    #     ★★而其判据只数「真伤」二字之出现，**那一句「说明」写得再全，它一个字也看不见**；
    #     ★★★於是它给的那一条路走不通：**照它说的做，它照旧拦。**
    #   ★★★★故补一式，认其所索之「说明」：**逐轮一行，作「· **第N轮·无真伤之由**：…」，
    #     且其行内须有裁语**（判合／⛔／✓之属）——**式硬，不许含糊。**
    #   ★它认哪几样，本书同类共几样：**只认这一个式**；
    #     ★★回灌全书 `grep -rl "无真伤之由" 版本/*/_轮记.md` 印 **1 份（301本身）**——
    #     **旧史一册不动，故非挖空，是给它补一个「说得出口」的口。**
    _said = {int(m.group(1)) for m in re.finditer(
        r'·\s*\*\*第(\d+)轮·无真伤之由\*\*(?P<尾>[^\n]*)', '\n'.join(
            '\n'.join(v) for v in lj.values()))
        # ★裁语只在其尾上找：**标头自带「真伤」二字，拿整行去找即永远为真**（本日自逮）。
        if any(x in m.group('尾') for x in VERDICT)}
    nz = sum(1 for r, v in lj.items()
             if not re.search(r'真伤[^无]', '\n'.join(v)) and r not in _said)
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
    print('   拦停旗：%s｜正文与末版：%s｜补存版数：%d'
          % ('无' if not fl else '**有**', '已偏' if drift else '一致',
             sum(1 for x in vs if '补存' in x.get('说明', ''))))

    # ★★★★★丙2·尽力查（2026-08-19 接入·作者令「目的不是跑完，是把质量跑到最高」）
    # ★其为本闸链中唯一测「够不够好」者；先前九道皆只测「有没有错」。
    # ★★而其硬项计入总核之硬项——即：跑透不了，封不了版。
    print('\n  ── 丙2·尽力查（测跑透，非测跑完）──')
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
               '软项': soft_warn, '流': _stream_id()},
              open(os.path.join(d, '_总核.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print('  【总核·通过】十轮之版与记俱齐、无未记之空轮、无旗、正文与末版一致。')
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
        rs, miss = rounds_state(lg, n)
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
    # ★0910 补三格·钉死「真轮亦凭轮记」这一路（其立之由见 rounds_state 之注）
    chk('真轮·不给章号时照旧只认台账（旧调用之判分毫不变）',
        rounds_state(L([v('第3轮·x')]))[0] == {3})
    import tempfile as _tf, os as _os
    _d = _tf.mkdtemp(prefix='真轮凭轮记_')
    try:
        # ⑨之形：轮记里一行「已完成」——**不许算跑过**
        _os.makedirs(_os.path.join(_d, '版本', '第900章'), exist_ok=True)
        _lj = _os.path.join(_d, '版本', '第900章', '_轮记.md')
        open(_lj, 'w', encoding='utf-8').write('# 第900章 · 轮记\n\n## 第7轮·x\n\n已完成。\n')
        _old = globals()['_lunji_path']
        globals()['_lunji_path'] = lambda nn: _lj
        chk('真轮·轮记里一行「已完成」不算跑过（去空白<120字）',
            7 not in rounds_state(L([]), 900)[0])
        # ⑧之形：轮记里有逐条实文——算跑过
        open(_lj, 'w', encoding='utf-8').write(
            '# 第900章 · 轮记\n\n## 第7轮·x\n\n' + ('本轮所见：逐处抄出来之後看见一样器印不出的事。' * 8) + '\n')
        chk('真轮·轮记里有实文（≥120字）即算跑过', 7 in rounds_state(L([]), 900)[0])
        globals()['_lunji_path'] = _old
    finally:
        import shutil as _sh
        _sh.rmtree(_d, ignore_errors=True)
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

    def _ch(tmp, body='一二三四五六七八九十'):
        open(os.path.join(tmp, '正文', '镇冢秘术_第七章_测.md'), 'w',
             encoding='utf-8').write('《镇冢秘术》\n\n第七章　测\n\n' + body + '\n')

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

    print('\n  八闸负测（含端到端真跑）：%d/%d' % (ok, ok + fail))
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
            glines.append('     处方：跑 python3 工具/十轮精进.py --下一轮 %d，读末版与前轮所见，再落笔。' % n)
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
        _has = os.path.exists(_lp) and ('第%d轮' % _prev) in open(_lp, encoding='utf-8').read()
        if not _has:
            halt = True
            glines.append('   ⛔轮记闸：第%d轮未录轮记，不许起第%d轮。' % (_prev, _r))
            glines.append('     轮记是压缩之后唯一能接上的东西；此刻不写，下一坐就接不上。')
            glines.append('     补录：printf \'...\' | python3 工具/十轮精进.py --轮记 %d' % n)
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
        worse = []
        for k in RATCHET_MIN:
            if k in best and soft[k] > best[k]:
                worse.append('%s %d→%d(升)' % (k, best[k], soft[k]))
        for k in RATCHET_MAX:
            if k in best and soft[k] < best[k]:
                worse.append('%s %d→%d(降)' % (k, best[k], soft[k]))
        if '净重' in best and soft['净重'] < best['净重'] * 0.92:
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
    try:
        if os.path.exists(_ling_path(n)):
            os.remove(_ling_path(n))   # 一领一存，基线用毕即销，下一轮须重领
    except Exception:
        pass
    clear_flag(n)
    print('  台账：%s（共%d版）' % (os.path.relpath(led, ROOT), v))
    _rs, _miss = rounds_state(ledger)
    print('  ══════════════════════════════════════════')
    print('  【定论】第%d章「%s」存版成功（rc=0）。台账共%d版，真轮%d/10%s'
          % (n, note, v, len(_rs), '' if not _miss else '，缺 ' + '、'.join('第%d轮' % i for i in _miss)))
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
    # ★★★★★死门闸（2026-09-02·292第11轮自逮·第二十四犯之第三形）
    #   ★其形：本器係 跑轮.py 之旧身（批103改名并入检察官），全工具箱无一处引它，
    #     ★★而它仍跑得动，且写的是同一批真台账、真快照——
    #     ★★★而自改名以来加进 跑轮.py 的闸，它一个也没有（吞记闸、趋阈闸、填记口…）。
    #   ★★★★即：**账房有两道门，新那道上了锁，旧那道还开着，而两道通同一间屋。**
    #   ★而设定诸档至今仍印着它的名（11_全书审计、十轮精进机制_立法与操作）——
    #     故不删（删了那些档就指向一个不存在的东西），只封其写路：
    #     ★★读的照读（审计要按行号查它），写的一概让路。
    _写口 = ('--存版', '--补存', '--还原', '--下一轮', '--轮记', '--补记')
    if cmd in _写口:
        print('⛔死门闸：本器係跑轮之旧身，早已无人引用，而自改名以来的闸它一个也没有。')
        print('   ★写的一概不办——两道门通同一间屋，旧那道没锁。')
        print('   正门：python3 工具/跑轮.py %s %s ...' % (cmd, ' '.join(sys.argv[2:3])))
        print('   ★★读口（--对表／--尽力／--验轮／--十一轮／--横评／--必答）照旧可跑。')
        return 2
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
    if cmd == '--补存':
        return buccun(n, sys.argv[3] if len(sys.argv) > 3 else '')
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
