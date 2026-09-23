# -*- coding: utf-8 -*-
"""合玉闸（2026-09-23·限359 立）——**`F026_合玉后完整态` 那一张卡之验码，今日方才有。**

★**其卡逐字**（`设定/canon事实库.json`）：
  `{"id": "F026_合玉后完整态", "level": "ERROR", "checker": "whole_jade_after_merge",
    "forbid": [], "except_ch": [1], "from_ch": 2}`
  **其 note**：「ch1守灵夜两块残玉已无缝合成完整古玉。ch2起当前时线中实物只能称完整古玉／那块玉；
  历史回忆『爷爷交给我的那半』可保留。**由语境守卫 whole_jade_after_merge 检查**」

⛔**而本坐今日 `grep` 全仓亲数**：**`whole_jade_after_merge` 一处代码也没有**——
  **那句「由语境守卫检查」指着的那个守卫，从来没有被写出来。**
  ★`设定/无闸之卡账.md` §五自书：「⛔**诸席历来只跑正则，未跑此码**；**此格至今未验，原样记着。**」
  ★★**记了八天，而它记的其实比实情轻**：**不是「没人跑那段码」，是「那段码不存在」。**

## ⛔本器不冒充能判事理

**那一张卡所禁者係「当前时线中把那件实物称作半块」**——**而「当前时线」与「历史回忆」之别，
机器分不出**（`无闸之卡账` §三之通例：**拿正则去查事理，查出来的是假绿，比不查更坏**）。
★**故本器只办两件事**：
  ①**把 `白文` 之内（⛔【本章亮点】之前）、第2章起、玉字所系之「半」逐处数出来**；
  ②**逐处须在 `设定/合玉闸账.md` 上有一行裁**（其章、其行、其判、其由）——
    ⛔**未裁者即红**；**裁作「犯」者亦红**；**裁作「回忆·许」者方过。**
★★**即本器判的不是「这一处对不对」，是「这一处有没有人看过」。**

## ⛔其所以要玉字所系

**旧念之式作 `那半块`**，**而 266／271 二章之「那半块**布**」当场入红**（本坐亲数 6 处）——
★**一件半块的布与一块半块的玉，在正则眼里一模一样。**
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import io, os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
账档 = os.path.join(ROOT, '设定', '合玉闸账.md')
起章 = 2          # ★卡自书 from_ch=2
_汉 = '零〇一二三四五六七八九十百'
# ★玉所系之「半」——⛔逐式皆须带玉字，免与「半块布」之属相撞
式 = re.compile(r'(半块玉|半玉|残玉|半片玉|半边玉|那半块古玉|两半玉|半块古玉)')


def 章号(f):
    m = re.search(r'第([%s]+)章' % _汉, os.path.basename(f))
    if not m:
        return None
    s, tot, cur = m.group(1), 0, 0
    for ch in s:
        if ch in '零〇':
            continue
        if ch == '十':
            cur = cur * 10 if cur else 10
        elif ch == '百':
            cur = (cur or 1) * 100
            tot += cur
            cur = 0
        else:
            d = '零一二三四五六七八九'.index(ch)
            cur = cur + d if cur and cur % 10 == 0 else d
    return tot + cur


def 白文(fp):
    """★只取【本章亮点】之前（⛔骨记与亮点段不在其辖·317、340 二处正在其後）。"""
    t = io.open(fp, encoding='utf-8', errors='replace').read()
    return t.split('【本章亮点】')[0]


def 逐处():
    """回 [(章, 行, 其句)]。⛔行号以整档计（便於 `awk 'NR==N'` 复核）。"""
    out = []
    for fp in glob.glob(os.path.join(ROOT, '正文', '*.md')):
        n = 章号(fp)
        if n is None or n < 起章:
            continue
        头 = 白文(fp)
        for i, ln in enumerate(头.split('\n'), 1):
            if 式.search(ln):
                out.append((n, i, ln.strip()))
    return sorted(out)


def 已裁():
    """读 `设定/合玉闸账.md`：{(章, 行): (判, 其由)}。⛔判须係「许」或「犯」。"""
    if not os.path.exists(账档):
        return {}
    out = {}
    for ln in io.open(账档, encoding='utf-8'):
        if not ln.startswith('|'):
            continue
        c = [x.strip() for x in ln.strip().strip('|').split('|')]
        if len(c) < 4 or not c[0].isdigit() or not c[1].isdigit():
            continue
        判 = re.sub(r'[*\s]', '', c[2])
        if 判 in ('许', '犯'):
            out[(int(c[0]), int(c[1]))] = (判, c[3])
    return out


def 查():
    处 = 逐处()
    裁 = 已裁()
    未裁 = [x for x in 处 if (x[0], x[1]) not in 裁]
    判犯 = [x for x in 处 if 裁.get((x[0], x[1]), ('', ''))[0] == '犯']
    return 处, 裁, 未裁, 判犯


def 全书():
    处, 裁, 未裁, 判犯 = 查()
    print('████ 合玉闸 ████（`F026_合玉后完整态` 之验码·2026-09-23 方才有）')
    print('  ★其辖：白文（⛔【本章亮点】之前）｜第%d章起｜玉字所系之「半」。' % 起章)
    print('  ★★本器判的不是「这一处对不对」，是**「这一处有没有人看过」**——'
          '⛔**事理之判机器做不了，故逐处须在 `设定/合玉闸账.md` 上有一行裁。**')
    print('  ── 今数 ──')
    print('  全书白文之内，第%d章起，玉字所系之「半」共 %d 处｜已裁 %d｜⛔未裁 %d｜⛔判犯 %d'
          % (起章, len(处), len(处) - len(未裁), len(未裁), len(判犯)))
    for n, i, s in 未裁:
        print('  ⛔未裁｜第%d章:%d｜%s' % (n, i, s[:60]))
    for n, i, s in 判犯:
        print('  ⛔判犯｜第%d章:%d｜%s' % (n, i, 裁[(n, i)][1][:70]))
    if 未裁 or 判犯:
        print('  ⛔ 合玉闸：未裁 %d 处、判犯 %d 处。' % (len(未裁), len(判犯)))
        return 1
    print('  ✓ 合玉闸：%d 处逐处有裁，且无一处判犯。' % len(处))
    return 0


def 自测():
    格 = []
    def 报(名, 得, 期): 格.append((名, 得 == 期, 得, 期))
    # ①⛔玉字所系方认（「半块布」不认·266／271 之真局）
    报('①「那半块布」不认', bool(式.search('我把那半块布从怀里掏出')), False)
    报('①之b「半块玉」认得', bool(式.search('爷爷把半块玉塞给我')), True)
    报('①之c「残玉」认得', bool(式.search('掌心还放着一块残玉')), True)
    报('①之d「另一半玉」之形', bool(式.search('它掌心那另一半玉')), True)
    # ②章号之算（⛔百位·三百四十）
    报('②章号·第二章', 章号('镇冢秘术_第二章_提灯人.md'), 2)
    报('②之b 第三百四十章', 章号('镇冢秘术_第三百四十章_十一步.md'), 340)
    报('②之c 第五十八章', 章号('镇冢秘术_第五十八章_血账.md'), 58)
    # ③⛔亮点段之後不入（317:311 与 340:224 皆在其後）
    报('③亮点段之後不入', '两半玉' in 白文(os.path.join(ROOT, '正文',
        '镇冢秘术_第三百一十七章_写小一号.md')), False)
    # ④第1章不辖（卡自书 except_ch=[1]／from_ch=2）
    报('④第1章不入其辖', [x for x in 逐处() if x[0] < 2], [])
    # ⑤⛔旧式回灌：不带玉字之式，266／271 当场假红
    _旧 = re.compile(r'那半块')
    _f = os.path.join(ROOT, '正文', '镇冢秘术_第二百六十六章_我早年压过.md')
    报('⑤旧式回灌·266 之「那半块布」在旧式之下入红',
       bool(_旧.search(白文(_f))) and not bool(式.search(白文(_f))), True)
    过 = sum(1 for _, ok, _, _ in 格 if ok)
    for 名, ok, 得, 期 in 格:
        if not ok:
            print('  ⛔%s：得 %r，期 %r' % (名, 得, 期))
    print('%s 合玉闸·自测 %d/%d' % ('✓' if 过 == len(格) else '⛔', 过, len(格)))
    return 0 if 过 == len(格) else 1


if __name__ == '__main__':
    sys.exit(自测() if '--自测' in sys.argv else 全书())
