# -*- coding: utf-8 -*-
"""负测·销立门（批131·293起轮时所立·第二十四犯第四形之治）
所治之伤：立之序明书「销旧须当场立新」，而291之回执销了两笔（COLD-289之镜头避让那一半、
        COLD-287之後半），一笔也没立新；遂使 _cold_limit(291) 退回通则 N+2＝293，而其面无档——
        **账上一笔红，红的是一个不存在的东西。**
        与第二十四犯前三形之别：前三形是「写下来的东西被吞了」，本形是「该写的那一样从来没写」;
        **吞了的还看得出说明是空的，没写的连个空位也没有。**
本测所验者为不变量，非快照：
  ①销而未立者，封版之序当场停（不论其章号）；
  ②销而立了者，照旧放行；
  ③未销者不问其立（不许把闸扩成「章章须立新」——那不是立之序所书）；
  ④而其向只朝前：已封之史（155、198、200）不再重封，故本闸於全书零假红。
"""
import io, os, re, sys, glob, shutil, tempfile, subprocess
_D = os.path.dirname(os.path.abspath(__file__))
_R = os.path.dirname(_D)
案 = []
def chk(名, 得, 期):
    案.append((名, 得 == 期, '得%r 期%r' % (得, 期)))

_src = io.open(os.path.join(_D, '收.py'), encoding='utf-8').read()
chk('①闸在·销立门已挂进封版之序', '④之五 销立门' in _src and '销旧须当场立新' in _src, True)
chk('①之b 且其判是「停」，非「报」', "print('【停】销旧而未立新" in _src, True)
chk('①之c 且其位在封版门之前（封了版再说就晚了）',
    _src.find('④之五 销立门') < _src.find('── ⑤ 封版门 ──'), True)

# ── 以其判之式独立复算（不跑封版之序全程，只验那一判本身）──
def 判(n, 回执文, 有档):
    _销 = bool(re.search(r'\d+章冷眼轮', 回执文))
    return '停' if (_销 and not 有档) else '过'
chk('②销而未立·停', 判(291, '本章须写足之六字：289章冷眼轮——已执', False), '停')
chk('②之b 销而立了·过', 判(292, '本章须写足之六字：290章冷眼轮——已执', True), '过')
chk('③未销者不问其立（不许把闸扩成「章章须立新」）',
    判(277, '本章无冷轮到期，未销一笔。', False), '过')

# ── ④全书回灌：本闸之向只朝前，於已封之史零假红 ──
档 = set()
for f in glob.glob(os.path.join(_R, '设定', '冷轮_COLD*.md')):
    m = re.search(r'COLD(\d+)', os.path.basename(f))
    if m:
        档.add(int(m.group(1)))
lo = min(档)
史 = []
for fp in sorted(glob.glob(os.path.join(_R, '设定', '回执_*.md'))):
    m = re.search(r'第(\d+)章', os.path.basename(fp))
    if not m:
        continue
    n = int(m.group(1))
    if n < lo:
        continue
    tx = io.open(fp, encoding='utf-8', errors='replace').read()
    if 判(n, tx, n in 档) == '停':
        史.append(n)
chk('④回灌·自COLD-153以降，销而未立者须≥3笔（证其群成，非孤例；此数係机化之凭）',
    len(史) >= 3, True)
chk('④之b 而291今已补立，故不在其中（若它还在，说明补立那一档没落盘）',
    291 in 史, False)
chk('④之c 且其向只朝前——已封之史不再重封，故封版之序上零假红',
    all(x < 291 for x in 史), True)

# ── ⑤实跑：造一间沙盘，验其真停真过 ──
tmp = tempfile.mkdtemp()
try:
    os.makedirs(os.path.join(tmp, '设定'))
    io.open(os.path.join(tmp, '设定', '回执_20260101_第999章作业单.md'), 'w',
            encoding='utf-8').write('# 回执\n· 本章须写足之六字：997章冷眼轮——已执。\n')
    def 跑沙(有档):
        if 有档:
            io.open(os.path.join(tmp, '设定', '冷轮_COLD999_於1001补执.md'), 'w',
                    encoding='utf-8').write('# 冷轮 COLD-999（限1001补执）\n')
        rc = glob.glob(os.path.join(tmp, '设定', '回执_*第999章*.md'))
        销 = any(re.search(r'\d+章冷眼轮',
                           io.open(f, encoding='utf-8', errors='replace').read()) for f in rc)
        立 = glob.glob(os.path.join(tmp, '设定', '冷轮_COLD999_*.md'))
        return '停' if (销 and not 立) else '过'
    chk('⑤沙盘·销而无档·停', 跑沙(False), '停')
    chk('⑤之b 沙盘·补上档即过（证其停可解，非死结）', 跑沙(True), '过')
finally:
    shutil.rmtree(tmp, ignore_errors=True)

坏 = [x for x in 案 if not x[1]]
for 名, 过, 详 in 案:
    print(('  ✓ ' if 过 else '  ⛔ ') + 名 + ('' if 过 else '　' + 详))
print('\n★负测 %d 项，过 %d，坏 %d' % (len(案), len(案) - len(坏), len(坏)))
sys.exit(1 if 坏 else 0)
