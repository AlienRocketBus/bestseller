# -*- coding: utf-8 -*-
"""层census（2026-09-02·292第12轮之一疑所令·第13轮所立）
所答之问：**一章之骨，每一层在白文里占几拍？**

★其立之由：第12轮翻案三逮出「②係⑧之早半」，是我逐层读出来的；
  ★★而那一轮自己记着：**读一回只逮得着一根**——**一双眼睛读九层，读到第三层就开始认得出自己的话。**
  ★★★故其查不许再由人读：**令器把每一拍派给一层**，占拍少者当场提出来复问。

★★★★其法（不认词，认串）：逐拍与逐层求最长公共子串；
  ★≥MIN(默认8字)者即判此拍属此层；一拍可属数层，取其最长者为主。

⛔⛔⛔【立此器之日即验其不称职·须与器同存，不许删】（292第13轮）
  ★本器造出来是要答「每层占几拍」，而当日拿她自己四章回灌，**它答的不是这个**：
      章   覆盖率   一拍之层
      284    6%     ①②③④ 四层皆只占一拍
      286   17%     ①占0拍
      288   45%     ——
      290   ——      ①占2拍
      292   31%     六层在三拍以下
  ★★**284係已封版之章，其五层无人判过薄**；而本器判它四层皆「占一拍」。
  ★★★**即：本器量的是「亮点段抄白文抄得实不实」，不是「一层在白文里占几拍」**——
      **同一把尺在她自己五章上从6%摆到45%，摆的是我写亮点段的手，不是章的厚薄。**
  ★★★★**故其数不许用作「层薄」之凭**（令§一②：此器没印的数，不许说；
      而此器印的这个数，印的不是它名字上那一样）。
  ★**本器可用者只一样：亮点段之引实率**——**一章之骨记，是抄下来的，还是转述的。**
    转述不是错（284即通篇转述），**而转述之骨与白文对不上账，日後改文时逮不着它**
    （第十八犯：减法轮删掉的那一句判，在亮点段里还活着——那一犯正是引实率低时才犯得成）。

用法：python3 工具/层census.py 292 [最小串长]
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io, os, re, sys, glob


def _lcs(a, b):
    """最长公共子串之长（滚动一维）。"""
    if not a or not b:
        return 0
    prev = [0] * (len(b) + 1)
    best = 0
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        ai = a[i - 1]
        for j in range(1, len(b) + 1):
            if ai == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                if cur[j] > best:
                    best = cur[j]
        prev = cur
    return best


def census(n, minlen=8):
    fs = [f for f in glob.glob('正文/*.md') if _num(f) == n]
    if not fs:
        print('  ✗ 无第%d章正文' % n)
        return 2
    t = io.open(fs[0], encoding='utf-8').read()
    if '【本章亮点' not in t:
        print('  ✗ 第%d章无亮点段' % n)
        return 2
    bw, hl = t.split('【本章亮点')[0], t[t.find('【本章亮点'):]
    pai = [re.sub(r'\s', '', p) for p in bw.split('＊') if p.strip()]
    pai = [p for p in pai if p and not p.startswith('《')]
    blocks = re.findall(r'^([①-⑳])(.*?)(?=^[①-⑳]|\Z)', hl, flags=re.M | re.S)
    if not blocks:
        print('  ✗ 亮点段无骨层之号')
        return 2
    净 = [(k, re.sub(r'[*★（）()【】\s]', '', b)) for k, b in blocks]
    print('\n████ 层census · 第%d章 ████' % n)
    print('  ★其法：逐拍与逐层求最长公共子串，≥%d字即判此拍属此层（不认词，认串）。' % minlen)
    print('  ★★一拍可属数层，主属取其最长者；无一层认领者另报。\n')
    属 = {k: [] for k, _ in 净}
    孤 = []
    for i, p in enumerate(pai):
        best, bk = 0, None
        for k, b in 净:
            L = _lcs(p, b)
            if L > best:
                best, bk = L, k
        if best >= minlen:
            属[bk].append(i)
        else:
            孤.append(i)
    print('  层  抄实之拍  拍号')
    thin = []
    for k, _ in 净:
        v = 属[k]
        if len(v) <= 3:
            thin.append(k)
        print('  %s  %3d   %s' % (k, len(v), ','.join(str(x) for x in v[:16])))
    cov = len(pai) - len(孤)
    率 = 100.0 * cov / len(pai)
    print('\n  ── 本器之判：亮点段引实率 %.0f%%（%d拍／全章%d拍）──' % (率, cov, len(pai)))
    print('  ★其义：骨记里有多少是从白文原样抄下来的，多少是转述的。')
    print('  ★★校准（她自己四章·2026-09-02 回灌）：284 6%｜286 17%｜292 31%｜288 45%')
    print('     ——**同一把尺在五章之间从6%到45%**；')
    print('     ★★★故此数不许读作「层厚薄」，284係已封版之章而它判其四层皆占一拍。')
    if 率 < 15:
        print('  ⚠引实率低於15%：骨记多係转述——**转述之骨与白文对不上账，日後改文时逮不着它**')
        print('     （第十八犯：减法轮删掉的那一句判，在亮点段里还活着）。')
    else:
        print('  ✓引实率在校准之带内。')
    print('\n  ── 抄实为零或仅一拍之层（只报「此层几无原句」，不报「此层薄」）──')
    if thin:
        print('  %s —— ★须逐层回看一句：**它在白文里的那几拍，我抄得出来么？**' % '、'.join(thin))
        print('     ★★抄不出来，多半是这一层写在册子上而没写进章里。')
    else:
        print('  ✓无。')
    return 0


def _num(f):
    d = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}
    m = re.search(r'第(.+?)章', os.path.basename(f))
    if not m:
        return -1
    v, cur = 0, 0
    for ch in m.group(1):
        if ch in d:
            cur = d[ch]
        elif ch == '十':
            v += (cur or 1) * 10
            cur = 0
        elif ch == '百':
            v += (cur or 1) * 100
            cur = 0
    return v + cur


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__.strip())
        raise SystemExit(1)
    raise SystemExit(census(int(sys.argv[1]),
                            int(sys.argv[2]) if len(sys.argv) > 2 else 8))
