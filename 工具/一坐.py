# -*- coding: utf-8 -*-
"""一坐.py —— 起手唯一之令。

★立此器之由（拿账说，不拿主意说）：
  · 2026-08-27 本坐十八次自撰工具回执，全发生在一份很详细的提示词之下。
  · 提示词里明写「一坐只发四五个调用」「存版后另发独立调用复核」——照样违反。
  · ★★故：提示词管不住我。管得住的只有一样——把「报告」从我手上拿走。

★★此器之职：查完实况，印出「现在该干什么」与「哪里坏了、怎么修」。
  ★★★我只负责干活，与把它的输出原样贴出来；它没印的数，我不许说。

用法：
    python3 工具/一坐.py          # 自动取 open_brief 之章
    python3 工具/一坐.py 286      # 指定章
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


# ─────────────────────────────────────────────────────────────
# 逐轮之器（八造·2026-09-03 立·对位闸所逮）
#
# ★立此表之由：**器立了，位没给。**
#   一事几陈（293第12轮立）／层census（292第13轮立）／立价查（292第13轮立）
#   ／亮点对表（289第10轮立）／回执对账／复核台账——**逐件皆在某一轮里立过、贺过，
#   而後全仓无一条路够得着它**（对位闸 2026-09-03 一扫：孤器八件）。
# ★★作者令（2026-09-03）：「**我们所有的机制都得跑起来。**」
#   ★★★而「跑起来」不是「码在仓库里」：**它得在某一轮的印子上，且那一轮我每坐都读。**
# ★★★★故此表焊在「下一轮」那一行底下——**印下一轮，必连本轮该跑之器一并印。**
逐轮之器 = {
    4:  [('工具/层census.py %d', '逐层占几拍——深掘轮问「这一层底下还有没有一层」，先得知道现有几层、各占几拍')],
    5:  [('工具/比带.py %d --全', '形比镜重：拿同形之章比，不拿同叙者之章比；--全 方带四感（第5轮即在场庭，不带四感等於没跑）')],
    6:  [('工具/器物点名.py %d', '★器物逐件点名（入／用／出三格，逐格验其拍上真有此名；★2026-09-05 加「主=谁」一格与跨章之比：对上一同线章之册，其主换人即⛔，上章在手而本章无声／已出又入而无一句怎么回来的只⚠）——'
             '令§三③把这条法指名归给第6轮，而此表原来第6轮空着（欠-295A，295第7轮之坐兑）')],
    7:  [('工具/小说检察官.py --五钩 %d', '★钩／新问／情绪波／危机升档／承诺推进——**本书唯一一件量「读者翻不翻页」的器**；'
                                    '从前只在封版之下出声，八造移到此轮，**趁文还改得动**')],
    8:  [('工具/一事几陈.py %d', '一事几陈：查重之尺量的是字，而一部书里最贵的重复是命题'),
         ('工具/整句复述哨.py %d', '★整句复述哨（2026-09-05·机制总审立·P21 复发7）：本章哪几句与任一前章逐字同——'
                                 '连读客只比 N-2，四字串只看章内，跨十六章之搬（93←77）无一器读；不判红，逐句上第8轮必答表判合／删')],
    9:  [('工具/立价查.py %d', '这一章立了几个价，收了几个——立而不收者，是欠')],
    10: [('工具/邻拍重出.py %d', '★收官轮之逐段生死检，人问其意，此器问其字——'
              '**一句话拆开来摆在两拍上，读起来是两步；逐字一比，是一句**；'
              '★★其立之由：301第10轮之生死检漏了拍31（其意逐字在下一拍之首句），'
              '而第11轮之小说家席一提即中（301第13轮·甲之逐轮回检所逮）；'
              '★★★本书之群：近四十章共8处，均每章0.2处、顶2处——**其常态是零**')],
    11: [('工具/看官.py --连读 %d %d', '★连读客·五席中唯一跨章之输入（令§八之二：旧五席两个月只出过一处真伤，出自它）；'
              '★★而296第11轮给它补了问五「上一章的句子有没有原样搬过来」——'
              '**其前四问在294→296逐字重出13.8%（本书31对之顶，中位2.1%）之时，四问俱绿**；'
              '★★★其式须给一对章号，如 --连读 292 296')],
    12: [('工具/大问表.py', '读者挂着的那几样，各自末见第几章；逾限者须挂账（设定/大问挂账.md）')],
}

# ★★★★★2026-09-04·作者亲令所加二口——**起草庭之两头**
#   ★作者令：「**再去构思下一章的时候，这一章要怎么写才能把它写到质量最高、才能写到最好**？」
#   ★★其红在哪一行：**开镜卡 102 份，写了「五钩」者 0 份、「新问」0 份、「弃卷」0 份；
#     一事之另二候选 3 份；「最神一句」轮记 87 份而卡上 0 份。**
#   ★★★故第7轮除真五钩之外，另加一口：**拿真数回来对起草之日所拟的那五个数**
#     ——**一个只在起草之日说得漂亮、事後无人回来对的格，就是摆设**（§十四）。
逐轮之器[7].append(
    ('工具/起草庭.py --对 %d',
     '★预实对表：起草之日拟的五钩，与本轮真跑之数，逐项之差；'
     '★★而其红不是「写坏了」，是**「起草之日看错了这一章」**——**其治在下一章起草之日**'))
逐轮之器[13] = [
    ('工具/起草庭.py --对 %d',
     '★定稿之前再对一回（第7轮之後若又动过文，其分未必还是那几个）'),
]


def 本轮之器(nxt, n):
    """印本轮该跑之器。★其位即在此：一坐每坐必读，故此处即是它们的位。"""
    out = []
    for 式, 由 in 逐轮之器.get(nxt, []):
        k = 式.count('%d')
        # ★2026-09-03·296第11轮：第11轮之式要一对章号（--连读 N-4 N），故按%d之数配参。
        if k == 2:
            cmd = ('python3 ' + 式) % (n - 4, n)
        elif k == 1:
            cmd = ('python3 ' + 式) % n
        else:
            cmd = 'python3 ' + 式
        out.append('★★★本轮之器：%s' % cmd)
        out.append('     ← %s' % 由)
    return out


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


def R(*a):
    """跑一个命令，返回其 stdout（失败则返回空串）。"""
    try:
        p = subprocess.run(list(a), cwd=ROOT, capture_output=True,
                           text=True, timeout=600)
        return p.stdout
    except Exception:
        return ''


def R2(*a):
    """跑一个命令，返回 (stdout, 跑成了没有)。

    ★2026-08-27 立。其由：旧只有 R()，凡命令崩／超时一律返空串；
      而空串到了 `bad = [l for l in six... if '⛔' in l]` 那里成了 bad==[]，
      屏上照印「六检全绿」。**实测：蓄意令 开轮六检.py 崩，一坐印「六检全绿」。**
    ★★一道不会响的闸，比没有闸更坏——它还发虚假的安心。
    ★★★故凡以此函之输出下「全绿」之判者，须先看 ok。
    """
    try:
        p = subprocess.run(list(a), cwd=ROOT, capture_output=True,
                           text=True, timeout=600)
        # ★不以返回码判生死：查出问题者本就返非零（开轮六检查出即返2）。
        #   ★★判据取「活体标记」：器正常必印 ✓ 或 ⛔ 之一；而 traceback 一个也没有。
        o = p.stdout
        return o, bool(o.strip()) and ('✓' in o or '⛔' in o)
    except Exception:
        return '', False


def body(n):
    """取第n章白文（去章题与亮点段）。"""
    for f in glob.glob(os.path.join(ROOT, '正文', '*.md')):
        m = re.search(r'第([零一二三四五六七八九十百]+)章', os.path.basename(f))
        if not m or cn2i(m.group(1)) != n:
            continue
        t = io.open(f, encoding='utf-8').read().split('【本章亮点】')[0]
        return re.sub(r'^.*?第.+?章[^\n]*\n', '', t, count=1, flags=re.S)
    return None


def main():
    fix = []          # 坏了的地方与其修法
    out = []

    # ── 本章之号 ──
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        n = int(sys.argv[1])
    else:
        try:
            d = json.load(io.open(os.path.join(ROOT, '设定', 'canon事实库.json'),
                                  encoding='utf-8'))
            n = int(d['open_brief']['for_ch'])
        except Exception:
            print('⛔ 取不到 open_brief.for_ch，请以 python3 工具/一坐.py N 指定章号')
            return
    # ★2026-08-27 补：上一坐器起手报第280章而实为286（彼器顺着找第一个无台账之章即停）。
    #   ★★故章号须带其来处：印哪一章就是哪一章，交接／记忆所报之号不作数。
    src = ('命令行所指' if (len(sys.argv) > 1 and sys.argv[1].isdigit())
           else 'canon事实库·open_brief.for_ch')
    out.append('════ 一坐 · 第%d章 ════' % n)
    out.append('（此号出於 %s。★交接所报之号不作数；不符者先查缺件，不许绕过。）' % src)

    # ── 一·台账与正文 ──
    lp = os.path.join(ROOT, '版本', '第%d章' % n, '_台账.json')
    b = body(n)
    tw = len(re.sub(r'\s', '', b)) if b else 0
    if os.path.exists(lp):
        L = json.load(io.open(lp, encoding='utf-8'))
        vs = L.get('版本', [])
        last = vs[-1] if vs else {}
        lw = last.get('soft', {}).get('净重', 0)
        hard = sum(last.get('hard', {}).values()) if last.get('hard') else 0
    # ★2026-09-05·机制总审：轮号之式与 跑轮._round_of 同源（re.match 锚句首；「回补·第6轮镜头之补」不算第6轮）
        rounds = sorted({int(m.group(1)) for x in vs
                         for m in [re.match(r'\s*第\s*(\d+)\s*轮', x.get('说明', ''))] if m})
        out.append('台账：%d版｜末版 %s｜硬项 %d' % (len(vs), last.get('版', '?'), hard))
        out.append('净重：台账 %d ｜ 正文 %d ｜ %s'
                   % (lw, tw, '相符' if lw == tw else '★相违（差%d）' % (tw - lw)))
        out.append('真轮：%d/13　已跑 %s' % (len(rounds), rounds if rounds else '无'))
        # ★2026-08-27 补·不许漏轮（作者原话）。此器旧只数轮之多少，不问二事：
        #   ★★一·断号（跑了一轮而未存版，或存版而未记轮——P28轮次蒸发病之形）；
        #   ★★二·空轮（台账有其号而轮记无其条——286第5轮即是：全部痕迹只一次自动对账）。
        缺号 = [r for r in range(1, max(rounds) + 1) if r not in rounds] if rounds else []
        if 缺号:
            out.append('★断号：第%s轮在台账里没有' % '、'.join(str(r) for r in 缺号))
            fix.append('轮号断於第%s轮 → 那一轮或跑了而未存版，或根本没跑；'
                       '查 版本/第%d章/_轮记.md 定其一，补跑或补存，不许径直往下走'
                       % ('、'.join(str(r) for r in 缺号), n))
        jp = os.path.join(ROOT, '版本', '第%d章' % n, '_轮记.md')
        if rounds and os.path.exists(jp):
            j = io.open(jp, encoding='utf-8').read()
            空 = [r for r in rounds if not re.search(r'##\s*第\s*%d\s*轮' % r, j)]
            if 空:
                out.append('★空轮：第%s轮台账有其号，而轮记无其条'
                           % '、'.join(str(r) for r in 空))
                fix.append('第%s轮跑了等於没跑（轮记无其条）→ 补其条：'
                           '真伤几根·捕几治几·一疑一句；'
                           '答不出即当作未跑，须补跑该轮'
                           % '、'.join(str(r) for r in 空))
            # ★★★★★2026-09-02 立·**缺报格闸**（六造§八：跑过之凭据是两样）：
            #   ★令§〇之二逼我每轮写一行「本可问而未问：我选了X，其由为Y」，
            #     **而没有任何器数它在不在**——漏写既不报红也不留痕，
            #     下一坐无从知道那一轮到底选了什么、办了什么。
            #   ★★而其数须**按轮号合数，一轮拆数节者并作一轮，非按节**：
            #     289一轮拆二十三节，按节数必吐假红。
            #   ★★★缺者印红入 fix，**不拦下一轮**（与空轮、断号同例）。
            _blk = re.split(r'^##\s*第\s*(\d+)\s*轮', j, flags=re.M)
            _by = {}
            for _i in range(1, len(_blk) - 1, 2):
                try:
                    _r = int(_blk[_i])
                except ValueError:
                    continue
                _by[_r] = _by.get(_r, '') + _blk[_i + 1]
            缺格 = [r for r in rounds
                    if r in _by and '本可问而未问' not in _by[r]]
            if 缺格:
                out.append('★缺报格：第%s轮之记里无「本可问而未问」一行'
                           % '、'.join(str(r) for r in 缺格))
                fix.append('第%s轮缺「本可问而未问」→ 补其行；'
                           '本轮实无可问者，写「本可问而未问：无」——'
                           '不许留空（令§八：跑过之凭据是两样，缺一即跑了等於没跑）'
                           % '、'.join(str(r) for r in 缺格))
        if lw != tw:
            fix.append('台账与正文相违 → 跑 python3 工具/跑轮.py --补存 %d "说明"，'
                       '再以独立调用复核' % n)
        if hard:
            fix.append('硬项 %d 未清 → 扫破折／说破／五逗／半角／英文，清零后补存' % hard)
        # ★2026-08-27 补：286第6轮存版报「四字串三现15→23（升）」。
        #   直接认则改回，直接驳则是自我安慰；逐版复算方知它随净重长，本轮零增。
        #   ★★故此处自比，不待存版报；报即连其复算之命一并给。
        for k, 优 in (('四字串三现', min), ('顿悟起手', min), ('嗅', max), ('沈鸢', max)):
            xs = [v.get('soft', {}).get(k) for v in vs]
            xs = [x for x in xs if isinstance(x, int)]
            if len(xs) >= 2 and xs[-1] != 优(xs):
                out.append('★棘轮·%s：末版 %d ｜历来最优 %d' % (k, xs[-1], 优(xs)))
                fix.append('棘轮回退（%s）→ 跑 python3 工具/预检.py --棘轮 %d --项 %s；'
                           '以其逐版之表裁之，不许直接认亦不许直接驳；'
                           '裁毕写进轮记（认／驳／留后轮，三者必居其一）' % (k, n, k))
        nxt = (max(rounds) + 1) if rounds else 1
        # ★2026-10-08·造式之章（`版本/第N章/_式.md`·判在 `工具/造式.py`）：⛔审改之轮——⛔不许印「下一轮／先领轮」把人引去跑轮
        _zs = os.path.exists(os.path.join(ROOT, '版本', '第%d章' % n, '_式.md'))
        if _zs:
            try:
                import importlib.util as _zu
                _zsp = _zu.spec_from_file_location('_zaoshi_yz', os.path.join(ROOT, '工具', '造式.py'))
                _zm = _zu.module_from_spec(_zsp)
                _zsp.loader.exec_module(_zm)
                _zs, _zq = _zm.判(n, ROOT)
            except Exception as _ze:
                _zq = ['造式之判跑不起来（%s）' % _ze]
        if _zs:
            out.append('▶ 本章係造式之章（⛔审改之轮，⛔领轮跑轮）：' + ('造式之实俱齐 → 该跑封版之序' if not _zq
                       else '造式之实缺 %d 样（%s）' % (len(_zq), '｜'.join(_zq[:3]))))
            if _zq:
                fix.append('造式之实缺 → 跑 python3 工具/造式.py %d 看全；缺哪一席之档派那一席补（⛔以跑轮补）' % n)
        elif len(rounds) >= 13:
            out.append('▶ 十三轮已满 → 该跑封版之序')
        else:
            out.append('▶ 下一轮：第%d轮' % nxt)
            # ★2026-08-27 补：286第1、2轮连犯两回「未领轮即动手」，闸拦二次且落旗成死结。
            #   ★★故此处焊一行：印下一轮，必连其领轮之命令一并印。
            out.append('   ★动手之前先领轮：python3 工具/跑轮.py --下一轮 %d' % n)
            out.append('   ★★若旗已落（存版被拦），领轮不落基线；须以 --补存 销旗。')
            for c in 本轮之器(nxt, n):
                out.append('   ' + c)
    else:
        out.append('台账：无（本章尚未起轮）')
        out.append('正文：%s（%d字）' % ('在' if b else '不在', tw))
        out.append('▶ 该跑第1轮（起草）')

    # ── 二·闸 ──
    six, six_ok = R2('python3', '工具/开轮六检.py', str(n))
    bad = [l.strip() for l in six.split('\n') if '⛔' in l]
    out.append('── 闸 ──')
    if not six_ok:
        out.append('  ⛔ 六检跑不成（器崩／超时／无输出）——★不作全绿论')
        fix.append('六检跑不成 → 单独跑 python3 工具/开轮六检.py %d 看它报什么错；'
                   '★修好再往下走。器崩之输出不许当作「查过了」' % n)
    elif bad:
        for l in bad[:6]:
            out.append('  ' + re.sub(r'\s+', ' ', l)[:100])
    else:
        out.append('  六检全绿')
    for l in bad:
        if '冷轮之欠' in l:
            fix.append('冷轮未执 → 读其原档第五节全文再落笔，'
                       '不许凭记忆；补执毕於第11轮落回执')
        if '锚' in l and '未备' in l:
            fix.append('下一章之锚未备 → 改圣经三样（本章之条／下一章之锚／进位），'
                       '★每改一样，另发一个只做核查的调用验它')
        if '亮点段' in l:
            fix.append('亮点段缺 → 补毕当场以正文之尺扫一遍（破折／说破／五逗／半角／英文）')

    # ── 三·冷轮（只看近四章）──
    out.append('── 冷轮（近四章）──')
    ck = []
    for f in glob.glob(os.path.join(ROOT, '设定', '冷轮_COLD*.md')):
        m = re.search(r'COLD(\d+)_於(\d+)', os.path.basename(f))
        if not m:
            continue
        src, due = int(m.group(1)), int(m.group(2))
        if abs(due - n) > 3:
            continue
        # ★★★★★2026-09-01 治·二器对同一笔给相反之判（全书审计第二层 2-8）：
        #   ★同一 HEAD 上，一坐印「COLD-284／285 未执」，而开轮六检印「⑥·冷轮之欠 零」⛔。
        #   ★★其由：一坐读档内之「已执＋销档」二词，而六检读回执之「N章冷眼轮」六字——**两处判据**。
        #   ★★★数其群（令§六②）：冷轮档 134 份，**含「已执＋销档」者仅 37 份，97 份没有**——
        #     ★★★★那个标记从来没成为惯例；而回执那一路是封版之序强制的（令§十①），也是⑥所读。
        #   ★故判：**判据错在一坐，改闸不改档**；此後与六检同用一处 `_cold_done`，二器不许再各记各的。
        try:
            import importlib.util as _u
            _sp = _u.spec_from_file_location('_六检', os.path.join(ROOT, '工具', '开轮六检.py'))
            _m6 = _u.module_from_spec(_sp)
            _sp.loader.exec_module(_m6)
            done = _m6._cold_done(src)
        except Exception:
            s = io.open(f, encoding='utf-8').read()
            done = ('已执' in s and '销档' in s)
        ck.append('  COLD-%d 限%d %s' % (src, due, '已执' if done else '★待执'))
        if not done and due <= n:
            fix.append('COLD-%d 限%d 未执 → 於第%d章补执，'
                       '照其档第五节抄，不凭记忆' % (src, due, due))
    out += (ck or ['  无'])

    # ── 四·看官凭据 ──
    out.append('── 看官 ──')
    try:
        import importlib.util as u
        sp = u.spec_from_file_location('_k', os.path.join(ROOT, '工具', '看官.py'))
        k = u.module_from_spec(sp)
        sp.loader.exec_module(k)
        ok, lack, old = k.验凭(n)
        out.append('  五席%s｜缺 %s｜过期 %s'
                   % ('齐' if ok else '未齐', lack or '无', old or '无'))
        if lack or old:
            fix.append('看官未齐或过期 → 跑 --生客/--挑刺/--小说家/--评论 %d 与 --连读 %d %d；'
                       '小说家所交三拍须逐一回话，答不出即删' % (n, n - 3, n))
    except Exception as e:
        out.append('  凭据查不成：%s' % str(e)[:40])

    # ── 五·圣经三样 ──
    out.append('── 圣经 ──')
    try:
        C = io.open(os.path.join(ROOT, '设定', '00_镇冢秘术_唯一总圣经.md'),
                    encoding='utf-8').read().split('\n')
        # ★本章十三轮已满者，其身已成「前章」：查本章之条与下一章之锚。
        #   ★★未满者仍查前章之条与本章之锚。此别2026-08-27立（器初造时漏之）。
        done13 = (os.path.exists(lp) and len(rounds) >= 13) if os.path.exists(lp) else False
        # ★2026-10-08·造式之章：造式之实俱齐即其「十三轮已满」之刻（无审改之轮，轮数永不满）
        if os.path.exists(lp) and not done13 and _zs and not _zq:
            done13 = True
        base = n if done13 else (n - 1)
        e_prev = sum(1 for l in C if l.startswith('### 第 %d 章' % base))
        a_cur = sum(1 for l in C if l.startswith('第 %d 章必须从' % (base + 1)))
        pos = sum(1 for l in C if '已写 1—%d 章' % base in l)
        out.append('  第%d章之条 %d｜第%d章之锚 %d｜进位%d %d'
                   % (base, e_prev, base + 1, a_cur, base, pos))
        if not (e_prev and a_cur and pos):
            fix.append('圣经三样不全 → 逐样写，★每写一样另发一个只做核查的调用；'
                       '不许一次写三样')
    except Exception as e:
        out.append('  查不成：%s' % str(e)[:40])

    # ── 六·git ──
    # ★2026-08-27 补：280—286之正文、四器、全部台账曾只存於一机，一次未推——几乎丢七章。
    #   ★★圣经第五十五批《仓库即时同步铁律》立了一个月，从未跑过：此为「写下来的法不生效」之极。
    #   ★★★故此处不问本地缓存（git status -sb 之 ahead 只信上回 fetch），直问远端。
    st = R('git', 'status', '--short')
    lg = R('git', 'log', '--oneline', '-1')
    dirty = len([x for x in st.split('\n') if x.strip()])
    br = R('git', 'rev-parse', '--abbrev-ref', 'HEAD').strip()
    head = R('git', 'rev-parse', 'HEAD').strip()
    rem = R('git', 'ls-remote', 'origin', br)
    rhead = rem.split('\t')[0].strip() if rem.strip() else ''
    # ★★★★★2026-09-01 补·大问表与外声（全书审计第一层第二、三条）。
    #   ★其由：一坐印的是「本章之欠」，而这两样是「全书之欠」——
    #     ★★而全书之欠一处也没摆在眼前，於是玉缺席了 207 章没人报过一声。
    try:
        import subprocess as _sp
        _r = _sp.run(['python3', os.path.join(ROOT, '工具', '大问表.py')],
                     capture_output=True, text=True, timeout=90)
        _m = re.search(r'逾上限者 (\d+) 样', _r.stdout or '')
        if _m and int(_m.group(1)):
            # ★★★★★2026-09-04·作者第二令：起草账焊在起手
            #   ★其由：一道闸只答得出「这一次填了没有」；**认不认真，只有事後结算才看得出来**；
            #   ★★而其要害在累积——**一章敷衍看不出来，三章敷衍摆在一起，谁都看得出来。**
            out.append('── 起草账（起草之日所拟的，与事後真跑出来的）──')
            try:
                import io as _io2, contextlib as _ctx2
                import 起草庭 as _qcz2
                _b = _io2.StringIO()
                with _ctx2.redirect_stdout(_b):
                    _qcz2.账(静=True)
                for _l in _b.getvalue().strip().split('\n'):
                    out.append('  ' + _l)
            except Exception as _e:
                out.append('  ⚠起草账读不出：%s' % _e)
            out.append('── 大问（读者还挂着的·可以欠，不可以不认）──')
            for _l in (_r.stdout or '').split('\n'):
                if '⛔' in _l and '章' in _l:
                    out.append('  ' + _l.strip())
    except Exception:
        pass
    # ★★★★★人账（2026-09-05·作者亲令「防剧情崩坏」所立）：**一个人可以不出场，不可以无声。**
    #   ★其位与大问同轮（第12轮·翻案）＋每坐起手——**大问认的是「问」，人账认的是「人」**；
    #   ★★其红之实：小周末见第12章·距293章｜陈队末见第9章·距296章，而大问表一个字也不说。
    try:
        import subprocess as _sp9
        _r9 = _sp9.run(['python3', os.path.join(ROOT, '工具', '人账.py')],
                       capture_output=True, text=True, timeout=90)
        _bad = [l.strip() for l in (_r9.stdout or '').split('\n')
                if l.strip().startswith('⛔')]   # ★2026-09-05：任一⛔行皆红，不再以子串过滤（「⛔真欠」旧式被吞）
        _warn = [l.strip() for l in (_r9.stdout or '').split('\n')
                 if '已挂账·限第' in l]
        out.append('── 人账（一个人可以不出场，不可以无声）──')
        if _bad:
            for _l in _bad[:4]:
                out.append('  ' + _l)
        else:
            out.append('  ✓逐人各有其账｜挂着的 %d 笔：%s'
                       % (len(_warn), '｜'.join(x.split('｜')[0].replace('⚠ ', '')
                                               for x in _warn[:3]) or '无'))
    except Exception:
        pass
    # ★★★★★日差哨（2026-09-05·机制总审所立）：**二线之历对不对得上。**
    #   ★其红之实：201章钉两本同一日（差0），272主93／273暗89之照面她记86——差7；其间九处之漂无一器看见。
    #   ★★哨只判「差有没有变」（自306起），差本身归 canon（作者点头）；每坐起手印一行，免得下一坐又拿邻章去补。
    try:
        import subprocess as _sp10
        _r10 = _sp10.run(['python3', os.path.join(ROOT, '工具', '日差哨.py'), '--静'],
                         capture_output=True, text=True, timeout=90)
        _l10 = [l.strip() for l in (_r10.stdout or '').split('\n') if l.strip()]
        out.append('── 日差哨（二线之历：暗线之日差＝前一主线章之天−本章之日）──')
        out.append('  ' + (_l10[-1] if _l10 else '（哨未出声）'))
    except Exception:
        pass
    # ★★★★★接口验（2026-09-05·机制总审所立）：圣经之锚所录「N-1之末句逐字」对不对得上正文——锚不许凭记忆抄，回修之後尤须对。
    try:
        import subprocess as _sp11
        _r11 = _sp11.run(['python3', os.path.join(ROOT, '工具', '接口验.py'), '--静'],
                         capture_output=True, text=True, timeout=90)
        _l11 = [l.strip() for l in (_r11.stdout or '').split('\n') if l.strip()]
        out.append('── 接口验（圣经之锚所录末句 对 正文真末句）──')
        out.append('  ' + (_l11[-1] if _l11 else '（器未出声）'))
    except Exception:
        pass
    # ★★★★★看官账（2026-09-05·机制总审·八路之数与册审第6条）：看官账律③「封那一章时全测据此拦」而全测无一处读其 open／限——今起手先印其数（报）。
    try:
        import subprocess as _sp12
        _r12 = _sp12.run(['python3', os.path.join(ROOT, '工具', '看官.py'), '--欠'],
                         capture_output=True, text=True, timeout=120)
        _items = [l for l in (_r12.stdout or '').split('\n') if l.strip().startswith('·')]
        out.append('── 看官账（open 之笔·报而不拦）──')
        out.append('  未清 %d 笔（`python3 工具/看官.py --欠`）；★律③所言「封版时全测据此拦」今仍无器，其治见 机制总审 丙' % len(_items))
    except Exception:
        pass
    # ★而旧账须逐坐印在眼前，否则「不回头判红」就成了「不了了之」。
    try:
        import subprocess as _sp3
        _r3 = _sp3.run(['python3', os.path.join(ROOT, '工具', '数闸.py')],
                       capture_output=True, text=True, timeout=90)
        _m3 = re.search(r'不符 (\d+) 处', _r3.stdout or '')
        _r4 = _sp3.run(['python3', os.path.join(ROOT, '工具', 'FS闸.py')],
                       capture_output=True, text=True, timeout=90)
        _m4 = re.search(r'未答 (\d+) 根', _r4.stdout or '')
        if _m3 or _m4:
            out.append('── 旧账（立闸於287·其前不回头判红，而一笔不许躺着）──')
            if _m3:
                out.append('  数闸：「N个字」之标签不符 %s 处 ⛔硬拦（旧账已於2026-09-01还清）' % _m3.group(1))
            if _m4 and int(_m4.group(1)):
                out.append('  FS：逾期之伏笔未回话 %s 根 ⛔硬拦（旧账已於2026-09-01还清）' % _m4.group(1))
    except Exception:
        pass
    try:
        import subprocess as _sp2
        _r2 = _sp2.run(['python3', os.path.join(ROOT, '工具', '外声闸.py'), '6'],
                       capture_output=True, text=True, timeout=90)
        _q = re.search(r'(240—\d+章 \d+)', _r2.stdout or '')
        _z = re.search(r'末尾连续出声为零：(\d+) 章', _r2.stdout or '')
        if _q:
            out.append('── 外声 ──')
            out.append('  全角引号 %s 处｜末尾连续无声 %s 章'
                       % (_q.group(1), _z.group(1) if _z else '?'))
    except Exception:
        pass
    # ★★★★★2026-09-02 补·站账（作者令「一切服务於质量，不管张数」之机化）
    #   ★其位在此，不在末：**一站还剩一章时问，还来得及改次序；走满了再问，只改得动章数。**
    try:
        import subprocess as _sp3
        _r3 = _sp3.run(['python3', os.path.join(ROOT, '工具', '站账.py'), '--闸'],
                       capture_output=True, text=True, timeout=90)
        _zz = [x.strip() for x in (_r3.stdout or '').splitlines()
               if x.strip().startswith(('⛔', '⚠'))]
        if _zz:
            out.append('── 站账（约之令：每写完一站回来对一次）──')
            for _x in _zz[:4]:
                out.append('  ' + _x[:150])
            fix.append('站账未对 → 跑 python3 工具/站账.py，'
                       '并逐件点名本站之事摸完几件；★而它不催字数，只逼你回头看一眼')
    except Exception:
        pass
    # ★★★★★2026-09-02 补·约到期（九席审读所逮：291立约「要分出来得有第三天」，
    #   而293正是那第三天，全章一步没去看，而无一处出声）
    try:
        import subprocess as _sp4
        _r4 = _sp4.run(['python3', os.path.join(ROOT, '工具', '约到期.py'), '--闸'],
                       capture_output=True, text=True, timeout=90)
        _yy = [x.strip() for x in (_r4.stdout or '').splitlines()
               if x.strip().startswith('⛔欠约')]
        if _yy:
            out.append('── 约到期（正文里自陈之约，到期那一章须回话）──')
            for _x in _yy[:3]:
                out.append('  ' + _x[:150])
            fix.append('欠约 → 跑 python3 工具/约到期.py；'
                       '★其治不是补一段回忆，是在到期那一章让它在手上再出现一回')
    except Exception:
        pass
    # ★★★★★2026-09-02 补·大审（作者令：平均十章一回，从头到尾，逐席真读）
    try:
        import subprocess as _sp5
        _r5 = _sp5.run(['python3', os.path.join(ROOT, '工具', '大审.py'), '--闸'],
                       capture_output=True, text=True, timeout=90)
        _da = [x.strip() for x in (_r5.stdout or '').splitlines() if x.strip().startswith('⛔')]
        if _da:
            out.append('── 大审（十章一回·逐席真读）──')
            for _x in _da[:2]:
                out.append('  ' + _x[:150])
            fix.append('大审 → 跑 python3 工具/大审.py；'
                       '★其席须各说得出「它看得见而别席看不见的那一样」，'
                       '★★不强制出负，强制留痕；★★★挂须带限')
    except Exception:
        pass
    out.append('── git ──')
    out.append('  未提交 %d 件｜枝 %s｜末笔 %s' % (dirty, br, lg.strip()[:44]))
    if not rhead:
        out.append('  ★远端答不出（网断或无此枝）')
        fix.append('远端未验 → 跑 git ls-remote origin %s；'
                   '答不出即当作未推，不许以「我方才推过」为凭' % br)
    elif rhead == head:
        out.append('  远端 %s ＝ 本地 ✓ 已推' % rhead[:8])
    else:
        out.append('  ★远端 %s ≠ 本地 %s ⛔ 未推' % (rhead[:8], head[:8]))
        fix.append('本地未推 → git push；推毕再跑 git ls-remote origin %s 验其等於本地。'
                   '★全令之中，唯此一险不可逆' % br)
    if dirty > 20:
        fix.append('未提交逾二十件 → 先提交，免其失於一处')

    # ── 修法 ──
    out.append('')
    if fix:
        out.append('════ 该修者 %d 处 ════' % len(fix))
        seen = []
        for x in fix:
            if x in seen:
                continue
            seen.append(x)
            out.append('  · ' + x)
    else:
        out.append('════ 无待修 ════')

    # ── 铁则（每回印，不许略）──
    out.append('')
    out.append('════ 三铁则 ════')
    out.append('  ① 一次只干一件事，干完发一个只做核查的调用，把它的输出原样贴出来。')
    out.append('  ② 此器没印的数，不许说。「我以为」「应该已经」一律作未做。')
    out.append('  ③ 修不动的，报出来交作者判；不许自造诊断，不许说「已定」。')

    print('\n'.join(out))


if __name__ == '__main__':
    main()
