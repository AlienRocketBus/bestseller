# -*- coding: utf-8 -*-
"""硬闸·单一真源（2026-09-01 立·全书审计第二层 2-5）

★立此器之由：硬项之集先前散在四处，各记各的，遂成两本账 ⛔——
　·跑轮.py 之表：破折／半角逗／半角冒／半角引号／五逗／英文／章号入正文／禁抖／永禁词（**只四个**）／段间空行／亮点三格；
　·小说检察官：`[,?!;:]` **五个**半角、canon 之 **22** 个永禁词、叠词粘连；
　·预检：跑轮之表。
　★★今日实测：一段含 `? ! ;`、九鼎、赵阙、「那个那个」之稿，预检只报「英文」与「段间空行」——
　　★★★三样硬伤一样也没认出来。而「预检说可落盘而它不可落盘」，正是287第3轮已犯二回之病（LAW-287A）。
★★★★而并集之前先量（令§六②·数其群）：全书287章
　　`? ! ; ' , :` 各 **0 章**；canon 22 个永禁词各 **0 章**；唯半角引号 8 章 144 处（跑轮本已在报）。
　★故此并集接上去，**不误伤任何一章已封版之文**——它只是把一直没人看的那几格补上。

【用法】
    from 硬闸 import 硬项
    hard = 硬项(全文)          # → {格名: 处数}
"""
import io, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ★永禁词取 canon 之表，不另抄一份——抄一份就是第二本账
_PF_CACHE = None


def 永禁词():
    global _PF_CACHE
    if _PF_CACHE is None:
        try:
            d = json.load(io.open(os.path.join(ROOT, '设定', 'canon事实库.json'), encoding='utf-8'))
            _PF_CACHE = [w for w in d.get('perm_forbidden', []) if isinstance(w, str) and w]
        except Exception:
            _PF_CACHE = []
        # ★而旧表所独有之四词（哆嗦／骊山／僵尸／点亮）须并进来，一个不许丢
        for w in ('哆嗦', '骊山', '僵尸', '点亮'):
            if w not in _PF_CACHE:
                _PF_CACHE.append(w)
    return _PF_CACHE


叠词式 = re.compile(r'(那包|那个|那块|那道|那把|那面|这个|这块)\1')
# ★不含「一个」：改对反向引用之後全书命中34处，尽是「一个一个」——那是好话不是粘连。


def 拆(txt):
    """★正文／亮点二分，并剥去章题那一行（照 跑轮.body_of 之例，一字不差）。

    ★★不剥即每一章都报「章号入正文 1 处」——那是题，不是正文入号 ⛔。"""
    prose = txt.split('【本章亮点】')[0]
    body = re.sub(r'^.*?第.+?章[^\n]*\n', '', prose, count=1, flags=re.S)
    hl = txt[txt.find('【本章亮点】'):] if '【本章亮点】' in txt else ''
    return body, hl


def 硬项(txt):
    body, hl = 拆(txt)
    sents = re.split(r'(?<=[。！？…])', txt)
    return {
        '破折': txt.count('—'),
        '半角逗': txt.count(','),
        '半角冒': txt.count(':'),
        '半角引号': txt.count('"'),
        '半角问': txt.count('?'),          # ★新·检察官有而跑轮无
        '半角叹': txt.count('!'),          # ★新
        '半角分': txt.count(';'),          # ★新
        '半角撇': txt.count("'"),          # ★新
        '五逗句': sum(1 for s in sents if s.count('，') >= 5),
        '英文': len(re.findall(r'[A-Za-z]', txt)),
        '章号入正文': len(re.findall(r'[一二三四五六七八九十百]+章', body)),
        '禁抖': body.count('抖'),
        '永禁词': sum(body.count(w) for w in 永禁词()),   # ★由四个补到 22＋4
        '叠词粘连': len(叠词式.findall(body)),             # ★新·检察官有而跑轮无
        '段间空行病': len(re.findall(r'。\n(?!\n)[^\n]', body)),
        '亮点段破折': hl.count('—'),
        '亮点段五逗': sum(1 for s in re.split(r'(?<=[。！？…])', hl) if s.count('，') >= 5),
        '亮点段半角': hl.count(',') + hl.count('"'),
    }


def 报(txt):
    h = 硬项(txt)
    return {k: v for k, v in h.items() if v}


if __name__ == '__main__':
    import glob
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--全书':
        红 = {}
        for f in sorted(glob.glob(os.path.join(ROOT, '正文', '*.md'))):
            for k, v in 报(io.open(f, encoding='utf-8').read()).items():
                红.setdefault(k, [0, 0])
                红[k][0] += 1
                红[k][1] += v
        print('════ 硬闸 · 全书回灌 ════')
        print('  永禁词共 %d 个（canon %d ＋旧表独有 4）' % (len(永禁词()), len(永禁词()) - 4))
        if not 红:
            print('  ✓ 十八格全零。')
        for k, v in sorted(红.items(), key=lambda x: -x[1][1]):
            print('  %-12s %3d 章｜%5d 处' % (k, v[0], v[1]))
    else:
        print(json.dumps(硬项(io.open(sys.argv[1], encoding='utf-8').read()) if len(sys.argv) > 1 else {},
                         ensure_ascii=False, indent=1))
