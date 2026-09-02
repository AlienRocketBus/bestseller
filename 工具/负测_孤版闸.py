# -*- coding: utf-8 -*-
"""负测·孤版（批131·293第1轮自逮·第二十四犯之第五形）
所治之伤：`save()` 之快照落盘写在诸闸之前，而趋阈闸／棘轮闸拦停时 return——
        **快照落了盘，台账没落**；且当场印一句「⛔存版已拦停，未写入任何文件」，**那是假话**。
        其果有二：①磁盘上多一个无账之孤版；②**空轮闸原比「磁盘上最後一个 vNN.md」**，
        於是那个孤版恰与正文逐字相同，**空轮闸把「上一次被拦」读成「本轮零改动」**，
        此後同一段文再也存不进去——**一道闸拦了我一回，然後把门锁上了。**
        （今日之实：293第1轮补感官毕，趋阈闸拦一回，此後 --补存 一律被空轮闸拦死。）
本测所验者为不变量，非快照：
  ①快照之写须在台账之写旁（账上有它，磁盘才有它）；
  ②空轮闸之比须比「台账所记之末版」，不比「磁盘上最後一个文件」；
  ③而空轮闸未被挖空：正文与台账末版逐字相同者，照旧拦；
  ④其判以旧式回灌须相反（证非陪跑）。
"""
import io, os, re, sys, json, glob, shutil, tempfile
_D = os.path.dirname(os.path.abspath(__file__))
案 = []
def chk(名, 得, 期):
    案.append((名, 得 == 期, '得%r 期%r' % (得, 期)))

_src = io.open(os.path.join(_D, '跑轮.py'), encoding='utf-8').read()

# ①快照之写与台账之写须相邻（其间不许再有 return）
_i = _src.find("open(os.path.join(d, 'v%02d.md' % v), 'w', encoding='utf-8').write(txt)")
_j = _src.find("json.dump(ledger, open(led, 'w', encoding='utf-8')")
chk('①快照之写在·且只此一处',
    _src.count("open(os.path.join(d, 'v%02d.md' % v), 'w', encoding='utf-8').write(txt)"), 1)
chk('①之b 快照之写须在台账之写之前一步（二者同落）', 0 < _j - _i < 200, True)
chk('①之c 而其间不许再有 return（有则又是一个孤版）',
    'return' in _src[_i:_j], False)

# ②空轮闸之比，须取台账所记之末版
chk('②空轮闸比的是台账之末版，不是磁盘之末档',
    "_vs = ledger.get('版本') or []" in _src and "'v%02d.md' % len(_vs)" in _src, True)
chk('②之b 旧式（比 sorted(glob) 之末）须已不在',
    "same_as_last = bool(snaps)" in _src, False)

# ③④以两式独立复算，验其判相反
def 新式(账数, 磁盘, 正文):
    last = 'v%02d' % 账数 if 账数 else ''
    return bool(last) and last in 磁盘 and 磁盘[last].strip() == 正文.strip()
def 旧式(账数, 磁盘, 正文):
    ks = sorted(磁盘)
    return bool(ks) and 磁盘[ks[-1]].strip() == 正文.strip()
磁 = {'v01': '甲', 'v02': '乙', 'v03': '丙'}   # v03 係孤版（台账只两行）
chk('③孤版在而台账只两行·新式判「非空轮」（放行）', 新式(2, 磁, '丙'), False)
chk('④旧式於同一局面判「空轮」（拦死）——两式相反，证非陪跑', 旧式(2, 磁, '丙'), True)
chk('③之b 而真空轮照旧拦：正文与台账末版逐字相同', 新式(2, 磁, '乙'), True)
chk('③之c 台账为空者不判空轮（新章头一版）', 新式(0, {}, '甲'), False)

# ⑤实跑：造一间沙盘，验「拦一回之後还存得进去」
tmp = tempfile.mkdtemp()
try:
    os.makedirs(os.path.join(tmp, '工具'))
    shutil.copy(os.path.join(_D, '跑轮.py'), os.path.join(tmp, '工具', '跑轮.py'))
    d = os.path.join(tmp, '版本', '第997章'); os.makedirs(d)
    io.open(os.path.join(d, '_台账.json'), 'w', encoding='utf-8').write(json.dumps(
        {'章': 997, '版本': [{'版': 'v01', '说明': '第1轮·起草', 'hard': {}, 'soft': {'净重': 2000}}]},
        ensure_ascii=False, indent=1))
    io.open(os.path.join(d, 'v01.md'), 'w', encoding='utf-8').write('旧文\n')
    io.open(os.path.join(d, 'v02.md'), 'w', encoding='utf-8').write('新文\n')   # ← 孤版
    磁2 = {f[:-3]: io.open(os.path.join(d, f), encoding='utf-8').read()
           for f in sorted(os.listdir(d)) if re.match(r'v\d\d\.md$', f)}
    _vs = json.load(io.open(os.path.join(d, '_台账.json'), encoding='utf-8'))['版本']
    chk('⑤沙盘·孤版 v02 在而台账只一行·新式放行（此正是今日那把锁）',
        新式(len(_vs), 磁2, '新文'), False)
    chk('⑤之b 而旧式在此锁死', 旧式(len(_vs), 磁2, '新文'), True)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

坏 = [x for x in 案 if not x[1]]
for 名, 过, 详 in 案:
    print(('  ✓ ' if 过 else '  ⛔ ') + 名 + ('' if 过 else '　' + 详))
print('\n★负测 %d 项，过 %d，坏 %d' % (len(案), len(案) - len(坏), len(坏)))
sys.exit(1 if 坏 else 0)
