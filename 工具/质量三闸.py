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
def gate1(c):
    """★防「一章塞多事」。其测有三：①轮记须有「本章之一事」一行；②净重须≥5500；③一章之日词须唯一。"""
    b = body(c); lj = lunji(c); out = []
    has = ('本章之一事' in lj)
    out.append(('①之a·轮记有「本章之一事」', has, '✓' if has else '⛔须於轮记之首写明'))
    w = net(b)
    out.append(('①之b·净重≥5500', w >= 5500, '%d 字' % w))
    # ★一章一日：章首之日词须唯一（第N天）
    days = set(re.findall(r'第([一二三四五六七八九十百]+)天头一件事', b))
    ok = (len(days) == 1)
    out.append(('①之c·一章一日（章首日词唯一）', ok, '%d 处' % len(days)))
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
    print('  质量四闸 · 见 设定/02_全书之约_逐站事数表.md')
    print('=' * 62)
    bad = 0
    for c in chs:
        if c not in F:
            print('  ⛔ 第%d章未见' % c); bad += 1; continue
        print('\n【第%d章】' % c)
        for name, ok, msg in gate1(c) + gate3(c) + gate4(c):
            print('   %s %-28s %s' % ('✓' if ok else '⛔', name, msg))
            if not ok: bad += 1
    print('\n【全书·闸②】')
    for name, ok, msg in gate2():
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
    print('  %s' % ('✓ 三闸皆过。' if bad == 0 else '⛔ 四闸报 %d 处，须修。' % bad))
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
