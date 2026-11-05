# -*- coding: utf-8 -*-
"""一事几陈（2026-09-02·293第12轮立·第二十七犯之治）

★所治之伤：**查重之尺量的是字，而一部书里最贵的重复是命题。**
★★其实（293）：「浅／轻，是我手上停了，不是那天有事」这一判，全章说了三回——
   拍17「手上先停了一下，落下去就轻」｜拍27「浅不是那天有什么事。浅是那两下我手上停了」｜
   拍36旧「停手那一下是我手上出的，不是这件事出的」；★★★**三处两两之字面近似 0.24—0.32，
   俱低於0.60之槛**，故第8、第9两轮之查重扫一处也没报——**而三处说的是同一句话。**

★★★★**故此器不判，也不机化成硬闸**（令§十三②·「同一命题」无字面之据，机器判不了；
   强判者必大量假红，而假红多的闸终被绕，绕过的闸等於没有）。
   ★**它只办一件事**：把「本章之一事」里的实词取出来，**列出全章凡含其二者以上之拍**，
   **把那几句摆在一起**——★★**三句摆在一起，一眼看得出第三句是多的；
   三句散在七十拍里，看九轮也看不见。**

★而它认哪几样（令§六④）：
  ①认「一事」之实词（自 _开镜卡.md 或亮点段「本章之一事」取，去虚词）；
  ②列凡含其中二个以上实词之拍——**故它列的是候选，不是判决**；
  ③**不认者**：换了一整套词说同一件事而一个实词也不共用者（如「浅」对「轻」）——
    ★★★**故须人把同义之词补进 --词 里再跑一回**；**不许把它的绿读成「本章无重陈」。**

用法：
    python3 工具/一事几陈.py 293
    python3 工具/一事几陈.py 293 --词 浅,轻,停,手
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io
import os
import re
import sys
import importlib.util as _iu

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_sp = _iu.spec_from_file_location('_bd', os.path.join(ROOT, '工具', '比带.py'))
_mb = _iu.module_from_spec(_sp)
_sp.loader.exec_module(_mb)

_虚 = set('的了是不在他我她它这那一个么什和与而就都也还又有没把被从对以及其之为所')


def 一事之词(n):
    """★自开镜卡或亮点段取「本章之一事」，去虚词，返其实词。"""
    src = ''
    kj = os.path.join(ROOT, '版本', '第%d章' % n, '_开镜卡.md')
    if os.path.exists(kj):
        t = io.open(kj, encoding='utf-8', errors='replace').read()
        m = re.search(r'本章之一事[^\n]*\n?([^\n]*)', t)
        if m:
            src = m.group(0)
    if len(src) < 20:
        for f in os.listdir(os.path.join(ROOT, '正文')):
            if '第%s章' % _han(n) in f or ('_第%d' % n) in f:
                pass
        raw = _正文(n)
        m = re.search(r'本章之一事[^\n]*', raw or '')
        if m:
            src = m.group(0)
    return [w for w in set(re.findall(r'[一-鿿]', src)) if w not in _虚]


def _han(n):
    return str(n)


def _正文(n):
    for f in sorted(os.listdir(os.path.join(ROOT, '正文'))):
        p = os.path.join(ROOT, '正文', f)
        try:
            t = io.open(p, encoding='utf-8', errors='replace').read()
        except Exception:
            continue
        if re.search(r'^第[一二三四五六七八九十百零]+章', t, re.M) and \
           _序(t) == n:
            return t
    return ''


def _序(t):
    m = re.search(r'第([一二三四五六七八九十百零]+)章', t)
    if not m:
        return -1
    s, num, unit, tot = m.group(1), 0, 1, 0
    d = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
         '六': 6, '七': 7, '八': 8, '九': 9}
    for ch in s:
        if ch in d:
            num = d[ch]
        elif ch == '十':
            tot += (num or 1) * 10
            num = 0
        elif ch == '百':
            tot += (num or 1) * 100
            num = 0
    return tot + num


def 陈(n, 词=None):
    b = _mb._白(n)
    ps = _mb._拍(b)
    ws = 词 or 一事之词(n)
    if not ws:
        print('  ⛔取不着「本章之一事」——先立开镜卡，或以 --词 明给。')
        return 1
    hit = []
    for i, p in enumerate(ps, 1):
        k = [w for w in ws if w in p]
        if len(k) >= 2:
            hit.append((i, len(k), p))
    hit.sort(key=lambda x: -x[1])
    print('\n── 一事几陈 · 第%d章 ──' % n)
    print('  一事之实词（%d个）：%s' % (len(ws), '　'.join(sorted(ws))))
    print('  凡含其二者以上之拍：%d 拍' % len(hit))
    for i, k, p in hit[:14]:
        print('   拍%-4d 中%d词  %s' % (i, k, p[:56]))
    print('\n  ★本器不判。★★须逐拍答一句：**「少这一句，本章断什么」**——')
    print('     ★★★答得出即留，答不出即删；**而三句摆在一起才看得见第三句是多的。**')
    print('  ★而它认不着换一整套词说同一件事者（浅对轻）——**补进 --词 再跑一回。**')
    return 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__.strip())
        raise SystemExit(1)
    _n = int(sys.argv[1])
    _w = None
    if '--词' in sys.argv:
        _w = [x for x in re.split(r'[,，]', sys.argv[sys.argv.index('--词') + 1]) if x]
    raise SystemExit(陈(_n, _w))
