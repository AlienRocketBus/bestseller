#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
质量三闸（2026-08-15 立·见 设定/02_全书之约_逐站事数表.md）

★而其立之由：2026-08-15 核账当场逮出三处打架（施工表220／圣经300／正文在E3而已到200），
★★而其真因为「蓝图按治前写法所排，而169章起本书换了写法」；
★★★遂重排全书为约450章，并立此三闸——★★★★而三闸所防者，非长度，是质量之三敌。

用法：
    python3 工具/质量三闸.py 200          # 单章之查
    python3 工具/质量三闸.py --段 192 200  # 一段之查（每站写满十章后回测用）
"""
import sys, re, os, glob, json

CN = {'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10}

def cn(p):
    m = re.search(r'第([零〇一二三四五六七八九十百]+)章', os.path.basename(p))
    if not m: return -1
    s = m.group(1); t = n = 0
    for ch in s:
        if ch in CN and ch != '十': n = CN[ch]
        elif ch == '十': t += (n or 1) * 10; n = 0
        elif ch == '百': t += (n or 1) * 100; n = 0
    return t + n

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = {cn(p): p for p in glob.glob(os.path.join(ROOT, '正文', '*.md')) if cn(p) > 0}

def body(c):
    return open(F[c], encoding='utf-8').read().split('【本章亮点')[0]

def net(t):
    return len(re.sub(r'\s', '', t))

def lunji(c):
    p = os.path.join(ROOT, '版本', '第%d章' % c, '_轮记.md')
    return open(p, encoding='utf-8').read() if os.path.exists(p) else ''

# ───────── 闸① 一章一事 ─────────
def is_dark(c):
    """★暗线章之判（2026-08-16立）：「我」之密度<3/千字者，即为第三人称之暗线章。
    ★★其据为圣经原文「暗线章用第三人称」；★★★而主线近十章之密度为22—31/千字。"""
    b = body(c); w = net(b)
    return (b.count('我') / w * 1000) < 3 if w else False


def gate1(c):
    """★防「一章塞多事」。其测三：①轮记有「本章之一事」；②净重≥5500；③一章之日词唯一。
    ★★而2026-08-16订其c项：先前只认「第N天头一件事」——★★★而暗线章在洞外，其日词非此形，
    ★★★★故会误伤；★★★★★遂改为「主线之章测日词，暗线之章测其场景不逾一处」。"""
    b = body(c); lj = lunji(c); out = []
    dark = is_dark(c)
    has = ('本章之一事' in lj)
    out.append(('①之a·轮记有「本章之一事」', has, '✓' if has else '⛔须於轮记之首写明'))
    w = net(b)
    out.append(('①之b·净重≥5500', w >= 5500, '%d 字%s' % (w, '（暗线章）' if dark else '')))
    if dark:
        cut = len(re.findall(r'那一边|另一头|与此同时|同一时候', b))
        out.append(('①之c·暗线章：场景不逾一处', cut <= 1, '切换词 %d 处' % cut))
    else:
        days = set(re.findall(r'第([一二三四五六七八九十百]+)天头一件事', b))
        out.append(('①之c·一章一日（章首日词唯一）', len(days) == 1, '%d 处' % len(days)))
    return out


# ───────── 闸④之二·人设护栏 ─────────
# ★★★★★2026-08-16 立·其由：作者令「不要把黎东来刻画成蠢蛋式的傀儡」——
# ★而核圣经，其层早已立硬护栏：「禁止给他任何苦衷（快死的孩子/绝症/身不由己/其实也是受害者）」；
# ★★而该护栏今日只在圣经里躺着，正文尚未写过他一篇视角（卷四起方有）；
# ★★★故焊为机器之测，免其往后写岔。
GUARD = {
    '黎东来': {
        '禁': ['苦衷', '身不由己', '也是受害者', '被逼的', '没办法才', '绝症', '快死的孩子'],
        '须': ['算', '资源', '流程', '证据', '批', '查'],
        '据': ('★圣经原文：「他不是贪生怕死的有钱人——怕死的人去买保健品，不去挖古墓」；'
               '★★「他要永生，因为他亲眼看见了……对只信证据的人，这不是奇迹，是新事实」；'
               '★★★「以前认命是因为没有第二条路；现在看见有了，还认命我就是傻子。'
               '这不是贪，是逻辑，而且逻辑没错」；'
               '★★★★「他是自己贴上去的，不是被挑中」；'
               '★★★★★「与霍钧平级利用、互不统属、互相看不起，都直接对赵阙负责」。'
               '★而【护栏·硬】禁止给他任何苦衷——他的罪不是想活，是为了想活而挖墓追捕灭口伤人。'),
    },
    '霍钧': {
        '禁': ['纯粹的恶', '天生坏'],
        '须': ['怕', '线', '欠'],
        '据': ('★圣经原文：「他不是坏人，他是在干樗里该干的活儿时快死的」；'
               '★★「一个救人的人，因为救人快死了，被续了一口气，然后用那口气杀了二十七年的人」；'
               '★★★而其命拴在赵阙身上（吊瓶命·管在贼手），每天怕线断。'),
    },
}

def gate4b(c):
    """★人设护栏：凡本章及於受护之人者，须核其禁词与须有之骨。
    ★★而其只测「有无」，不代裁——★★★裁在人，闸只报。"""
    b = body(c)
    out = []
    for who, g in GUARD.items():
        if who not in b:
            continue
        bad = [k for k in g['禁'] if k in b]
        hit = [k for k in g['须'] if k in b]
        out.append(('④之二·%s之护栏' % who, not bad,
                    ('★禁词零｜骨见 %d 样' % len(hit)) if not bad
                    else '⛔禁词 %s（★而其据：%s）' % ('、'.join(bad), g['据'][:60])))
    if not out:
        out.append(('④之二·人设护栏', True, '★本章未及受护之人'))
    return out


# ───────── 闸⑤ 暗线配额 ─────────
# ★★★★★2026-08-16立·其据为圣经原文：「副线（好几条线同时走）：沿用十三的暗线章铁律，
# ★逐卷插2—4篇霍钧/黎东来/赵阙视角，卷七转为人物主战场。」
# ★★而实测：全书200章，第三人称暗线章零篇——★★★三卷欠账6—12篇。
# ★★★★而其配额：今日一章只装一日，卷长远逾蓝图，故折合每10章至少1篇。
DARK_EVERY = 10
GATE5_FROM = 200  # ★闸⑤立於2026-08-16·第200章；其前之欠账（约20篇）记而不拦
# ★可切镜者（圣经之令·2026-08-16逐条取毕）
DARK_WHO = {
    '沈鸢':   '★无禁令｜CHAR-191A限210',
    '黎东来': '★★卷四起每卷至少1篇其流程视角（明令）｜恐怖不在凶相，在流程',
    '霍钧':   '★★★须分层揭露，不得一篇交尽｜卷六末前只以「人间的手」存在',
    '老头':   '★★★★未禁｜然其瞒苏衍二十年，一开即收不回，宜留至出洞后且只开一次',
    '钱满':   '未禁',
    '刘二':   '未禁',
    '赵阙':   '⚠受限：只在已连接者之意识、梦与节点异象中现，不得有全知视角',
}

def gate5(chs):
    """★防「只走一条线」。其测二：①近N章之内至少一篇暗线章；②全书之欠账。"""
    mx = max(chs)
    win = [c for c in range(max(GATE5_FROM + 1, mx - DARK_EVERY + 1), mx + 1) if c in F]
    dk = [c for c in win if is_dark(c)]
    ok = (len(dk) >= 1) or (len(win) < DARK_EVERY)
    out = [('⑤·近%d章之暗线章' % DARK_EVERY, ok,
            '%d 篇／窗内%d章%s' % (len(dk), len(win), '' if ok else '⛔零篇：须插一篇第三人称暗线'))]
    # ★★★★★而欠账只自立闸之日起算（2026-08-16·第200章）
    # ★其由：前200章已封版，不可能回补；★★而一个永远修不好的红灯等于没有闸——
    # ★★★因为往后每回全测都被它拦，而人就会习惯绕行。
    # ★★★★而此正是本书自己的法：192—199八章之闸①皆记「补执」，其由为闸立於其后。
    allc = [c for c in sorted(F) if c > GATE5_FROM]
    tot = sum(1 for c in allc if is_dark(c))
    need = len(allc) // DARK_EVERY
    out.append(('⑤之b·自第%d章起之暗线章' % (GATE5_FROM + 1), tot >= need,
                '%d 篇／应有 %d 篇（前%d章为立闸前，记欠账不拦停）' % (tot, need, GATE5_FROM)))
    return out

# ───────── 闸② 脉象不相犯 ─────────
MAI = {
    'E1': '土层、墓气、强接边界',
    'E2': '干燥死气、断流结构、满城枯骨',
    'E3': '从活人身上抽的活气',
    'E4': '水压、浑流、低氧',
    'E5': '暴露地表、风蚀错流（无墓）',
    'E6': '材料与工程校准',
    'E7': '周期性反向流（潮汐）',
    'E8': '现代城市工程接通',
}

def gate2():
    """★防「站与站重复」。逐对并排，看其脉象之词有无相犯。"""
    ks = list(MAI); out = []
    def toks(s): return set(re.findall(r'[\u4e00-\u9fa5]{2,}', s))
    bad = 0
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            a, b = toks(MAI[ks[i]]), toks(MAI[ks[j]])
            same = a & b
            if same:
                bad += 1
                out.append(('②·%s↔%s' % (ks[i], ks[j]), False, '相犯：%s' % '、'.join(same)))
    out.insert(0, ('②·八脉象逐对并排（%d 对）' % (len(ks) * (len(ks) - 1) // 2), bad == 0,
                   '零相犯' if bad == 0 else '%d 对相犯' % bad))
    return out

# ───────── 闸③ 谜底之距 ─────────
E7_START = 316   # ★依重排：收E3(201-230)+E4(40)+E5(25)+E6(25) → E7自316起
def gate3(c):
    """★防「谜底吊太久」。其设二级：①距E7逾100章即须查；②而当段若有谜底碎片，则一级不报。
    ★★而此二级之序为2026-08-15头一跑时当场订正——★★★先前之写法令二级已过而一级仍报，
    ★★★★而其误在：把「距远」本身当成了伤；★★★★★而距远不是伤，距远而无碎片才是伤。"""
    d = E7_START - c
    if d <= 100:
        return [('③·距E7（复流原理）', True, '%d 章（在限内）' % d)]
    b = body(c)
    # ★碎片之形：本章有无关於「那个人／复流／抽逆成放」之新判
    sh = sum(b.count(k) for k in ['那个人', '不到一年', '近路', '塞住', '拔了塞子', '还要回来'])
    return [('③·距E7 %d 章（逾100，查碎片）' % d, sh > 0,
             '★碎片 %d 处，二级已过' % sh if sh > 0 else '⛔无碎片：须在本段内先给一块')]

# ───────── 闸④ 主线之距 ─────────
# ★★★★★2026-08-16 立·其由：191章末已见「章级之闸看不见一样东西在数十章里慢慢漂掉」，
# ★而其时立CHAR-191A（沈鸢·限210）、CHAR-191B（苏衍·限214）二笔账逮之；
# ★★然账只在到期那一章咬人，中间九十九章无人管——★★★故须一闸每章都测。
# ★★★★而其所测者有二：①二主角之线末次回切；②三反派之出场令有无违。
MAIN = {
    # 名: (末见之章, 限, 其由)
    # ★★★★★2026-08-16：沈鸢已於第200章回切（依191章末之令·只为念不为见）
    '沈鸢': (200, 80, '★CHAR-191A限210｜★★而200章之回切为「她在外头／而她那四十四天我连一行也没有」'),
    '苏衍·第三人称之名': (101, 999, '★★而苏衍为第一人称主角，每章皆在；此项只测「他人称其名」之距，不作硬限'),
}
# ★三反派之出场令（圣经原文·2026-08-16取）
FAN = {
    '黎东来': ('卷四起每卷至少1篇其视角', 4, '★而今在卷三，故未违；★★入卷四即须起算'),
    '霍钧':   ('与苏衍正面照面不早於卷六末、不晚於卷七开头', 6, '★★★而其身份须分层揭露，不得一篇交尽'),
    '赵阙':   ('只在已连接者之意识、梦与节点异象中出现', 99, '★★★★不得有随时读遍天下之全知视角'),
}
CUR_JUAN = 3  # ★今在卷三（E3青溪）

def gate4(c):
    """★防「主线漂掉」。其测二事：①二主角之线末次回切；②三反派之出场令有无违。
    ★★而其立之由：191章末之二笔账只在到期那一章咬人，中间九十九章无人管。"""
    out = []
    for who, (last, lim, why) in MAIN.items():
        d = c - last
        if lim >= 999:
            out.append(('④·%s 末见第%d章' % (who, last), True, '距 %d 章（不作硬限：%s）' % (d, why[:24])))
        else:
            out.append(('④·%s 末见第%d章' % (who, last), d <= lim,
                        '★距 %d 章（限%d）%s' % (d, lim, '' if d <= lim else '⛔已漂，须在当段内回切')))
    for who, (rule, jn, why) in FAN.items():
        ok = (CUR_JUAN < jn)
        out.append(('④之b·%s' % who, ok if not ok else True,
                    '★%s｜今卷%d：%s' % (rule[:22], CUR_JUAN, '未到其时 ✓' if CUR_JUAN < jn else '★★已入其卷，须查配额')))
    return out


def run(chs):
    print('=' * 62)
    print('  质量五闸 · 见 设定/02_全书之约_逐站事数表.md')
    print('=' * 62)
    bad = 0
    for c in chs:
        if c not in F:
            print('  ⛔ 第%d章未见' % c); bad += 1; continue
        print('\n【第%d章】' % c)
        for name, ok, msg in gate1(c) + gate3(c) + gate4(c) + gate4b(c):
            print('   %s %-28s %s' % ('✓' if ok else '⛔', name, msg))
            if not ok: bad += 1
    print('\n【全书·闸②⑤】')
    for name, ok, msg in gate2() + gate5(chs):
        print('   %s %-28s %s' % ('✓' if ok else '⛔', name, msg))
        if not ok: bad += 1
    # ★段之回测（每站写满十章后）
    if len(chs) >= 10:
        ws = [net(body(c)) for c in chs if c in F]
        avg = sum(ws) / len(ws)
        laws = []
        for c in chs:
            t = lunji(c)
            laws.append(len(re.findall(r'由此立|由此并记|故补一句|本轮所立', t)))
        la = sum(laws) / len(laws) if laws else 0
        print('\n【段之回测·%d—%d 共%d章】' % (chs[0], chs[-1], len(chs)))
        print('   %s 均净重≥5500                  %.0f 字' % ('✓' if avg >= 5500 else '⛔', avg))
        print('   %s 新立之法≥12条/章              %.1f 条' % ('✓' if la >= 12 else '⛔', la))
        if avg < 5500 or la < 12:
            bad += 1
            print('   ★★★★★而任一掉了 → 当场压章，且记其因於轮记')
    print('\n' + '=' * 62)
    print('  %s' % ('✓ 三闸皆过。' if bad == 0 else '⛔ 五闸报 %d 处，须修。' % bad))
    print('=' * 62)
    return 0 if bad == 0 else 2

if __name__ == '__main__':
    a = sys.argv[1:]
    if a and a[0] == '--段' and len(a) >= 3:
        sys.exit(run(list(range(int(a[1]), int(a[2]) + 1))))
    elif a:
        sys.exit(run([int(x) for x in a]))
    else:
        mx = max(F)
        sys.exit(run([mx]))
