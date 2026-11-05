# -*- coding: utf-8 -*-
"""负测·硬闸单一真源（2026-09-01 立·全书审计第二层 2-5）

★立此测之由：硬项之集先前散在跑轮／预检／检察官三处，各记各的，遂成两本账。
　★★实测：一段含 `? ! ;`、九鼎、赵阙、「那个那个」之稿跑预检，只报「英文」与「段间空行」⛔。
★★★而令§六③曰：改闸必同日立负测，且须以旧式回灌验。
　★★★★故本测之要害有二：①新格该认的认；②**旧有之十三格一格不许走样**——
　　★一个把老账改坏了的新账，比两本账更坏。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, '工具'))
from 硬闸 import 硬项, 永禁词, 硬项之处, 处之印   # noqa: E402

# ★旧式（改之前跑轮那一份，逐字抄下作回灌之据）
def 旧式(txt):
    prose = txt.split('【本章亮点】')[0]
    body = re.sub(r'^.*?第.+?章[^\n]*\n', '', prose, count=1, flags=re.S)
    hl = txt[txt.find('【本章亮点】'):] if '【本章亮点】' in txt else ''
    sents = re.split(r'(?<=[。！？…])', txt)
    return {
        '破折': txt.count('—'), '半角逗': txt.count(','), '半角冒': txt.count(':'),
        '半角引号': txt.count('"'),
        '五逗句': sum(1 for s in sents if s.count('，') >= 5),
        '英文': len(re.findall(r'[A-Za-z]', txt)),
        '章号入正文': len(re.findall(r'[一二三四五六七八九十百]+章', body)),
        '禁抖': body.count('抖'),
        '永禁词': sum(body.count(w) for w in ['哆嗦', '僵尸']),
        '段间空行病': len(re.findall(r'。\n(?!\n)[^\n]', body)),
        '亮点段破折': hl.count('—'),
        '亮点段五逗': sum(1 for s in re.split(r'(?<=[。！？…])', hl) if s.count('，') >= 5),
        '亮点段半角': hl.count(',') + hl.count('"'),
    }


# ①新格该认者（旧式一格也认不出）
新格须认 = [
    ('半角问', '他问：你去哪儿?\n'),
    ('半角叹', '真的!\n'),
    ('半角分', '又一句;还有下文。\n'),
    ('半角撇', "他说的是'那一样'。\n"),
    ('叠词粘连', '他把那个那个记号又描了一遍。\n'),
    ('永禁词', '鼎心在底下。鼎心没来。\n'),   # ★旧表只四词，认不出这二词（0927 九鼎、赵阙解封，样本改用仍封之词）
    ('段间空行病', '真的！\n下一段紧挨着。\n'),     # ★2026-09-05：旧式只认「。\n」，叹号／问号／引号後之漏空行认不出
    ('段间空行病', '＊\n下一拍紧挨着分节符。\n'),   # ★2026-09-05：245章实有一处，旧式与检察官皆漏
    ('章号入正文', '《镇冢秘术》\n\n第九百九十九章　试\n\n第37章那天他没来。\n'),   # ★2026-09-05：阿拉伯章号旧式放行（须带章题行，否则此句被当作章题剥去）
    ('禁抖', '他的手颤了一下。\n'),                 # ★2026-09-05：F107 明列「颤」而旧式只数「抖」
    # ★2026-09-09·308第13轮：亮点段永禁（旧式无此格，白文之永禁格亦扫不到骨记）。
    #   此串係 308 骨记②治前之原文，逐字回灌：旧式报 0，新式须报红。
    ('亮点段永禁', '《镇冢秘术》\n\n第九百九十九章　试\n\n她把册子合上。\n\n【本章亮点】本席落笔後逐拍对过一遍，鼎心一处，今为零处。\n'),
]

# ②不许认者（皆取自正文原场，是好话）
不许认 = [
    ('叠词粘连', '他把五个罐子一个一个提起来掂了掂。\n'),
    ('叠词粘连', '七个减到两个，中间那五个是一个一个少下去的。\n'),
]

# ③旧有之格一格不许走样（拿全书回灌）
def _旧格不走样():
    import glob
    坏 = []
    for f in sorted(glob.glob(os.path.join(ROOT, '正文', '*.md'))):
        t = io.open(f, encoding='utf-8').read()
        a, b = 旧式(t), 硬项(t)
        for k in a:
            if k in ('永禁词', '段间空行病', '禁抖', '章号入正文'):
                # ★此二格有意扩式（永禁词 4→25词；段间空行病 2026-09-05 由「。\n」扩为 [。！？”＊]\n），只许增不许减
                if b[k] < a[k]:
                    坏.append('%s·%s 由 %d 减到 %d' % (os.path.basename(f)[:20], k, a[k], b[k]))
            elif a[k] != b[k]:
                坏.append('%s·%s 旧%d 新%d' % (os.path.basename(f)[:20], k, a[k], b[k]))
    return 坏


# ④硬项之处（1024·省审 seats 三）：每格之条数＝硬项()之数（全书回灌），且白文／骨记、同句二格、行号皆对
def _处之对():
    import collections, glob, subprocess, tempfile
    坏 = []
    for f in sorted(glob.glob(os.path.join(ROOT, '正文', '*.md'))):
        t = io.open(f, encoding='utf-8').read()
        c = collections.Counter(x[0] for x in 硬项之处(t))
        for k, v in 硬项(t).items():
            if c.get(k, 0) != v:
                坏.append('%s·%s 硬项%d 处%d' % (os.path.basename(f)[:20], k, v, c.get(k, 0)))
    样 = ('《镇冢秘术》\n\n第九百九十九章　试\n\n“好。”\n\n他走了，走了，又走，再走，还走，终于停了。\n\n'
          '【本章亮点】一，二，三，四，五，六。\n')
    印 = 处之印(硬项之处(样))
    跨 = 处之印(硬项之处('第一章　题\n\n甲，乙，丙，\n丁，戊，己。\n'))
    if 跨 != ['  白文 L3 五逗句：甲，乙，丙，⏎丁，戊，己。']:   # 跨行之句⛔断其行（--量 一处一行）
        坏.append('跨行之句走样：%s' % 跨)
    if 印 != ['  白文 L7 五逗句：他走了，走了，又走，再走，还走，终于停了。',
             '  骨记 L9 五逗句＝亮点段五逗（同一句，计二格）：【本章亮点】一，二，三，四，五，六。']:
        坏.append('处之印走样：%s' % 印)
    with tempfile.NamedTemporaryFile('w', suffix='.md', delete=False, encoding='utf-8') as g:
        g.write(样)
    try:
        o = subprocess.run([sys.executable, os.path.join(ROOT, '工具', '净重对表.py'), '--量', g.name],
                           capture_output=True, text=True).stdout.splitlines()
    finally:
        os.unlink(g.name)
    if o[1:] != 印 or not o or not o[0].startswith('净重 ') or '五逗句 2、亮点段五逗 1' not in o[0]:
        坏.append('净重对表 --量 未印其处：%s' % o)
    return 坏


def 跑():
    坏, 回灌漏 = [], 0
    for 格, s in 新格须认:
        if not 硬项(s).get(格):
            坏.append('新式漏认 %s：%s' % (格, s.strip()))
        o = 旧式(s)
        if not o.get(格, 0):
            回灌漏 += 1
    for 格, s in 不许认:
        if 硬项(s).get(格):
            坏.append('新式误认 %s（是好话，不是病）：%s' % (格, s.strip()))
    走样 = _旧格不走样()
    if 走样:
        坏.append('★旧格走样 %d 处（新账把老账改坏了）：%s' % (len(走样), 走样[0]))
    处坏 = _处之对()
    if 处坏:
        坏.append('★硬项之处 %d 处不对：%s' % (len(处坏), 处坏[0]))
    if 回灌漏 == 0:
        坏.append('★此测在旧式下亦全过——陪跑之测，不算数。')
    n = len(新格须认) + len(不许认) + 2
    if 坏:
        print('✗ 负测·硬闸 %d/%d' % (n - len(坏), n))
        for x in 坏:
            print('   ⛔ ' + x)
        return 1
    print('✓ 负测·硬闸 %d/%d 全通｜永禁词 %d 词｜旧十三格全书回灌一格未走样｜硬项之处逐格同数｜旧式漏认 %d 项，故非陪跑'
          % (n, n, len(永禁词()), 回灌漏))
    return 0


if __name__ == '__main__':
    sys.exit(跑())
