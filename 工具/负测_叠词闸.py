# -*- coding: utf-8 -*-
"""负测·叠词粘连闸（2026-09-01 立·全书审计所逮）

★立此测之由：小说检察官之叠词闸写作 r'(那个|…)\\1'——
　★★r-string 里 `\\1` 是「反斜杠＋1」两个字面字符，不是反向引用；
　★★★故此闸自立起之日一次也没红过，而没人查过它红不红 ⛔。
★★★★而令§六③曰：改闸必同日立负测，且须以旧式回灌验。
　★故本测之要害只一条：**下列各句在旧式下全不认，在新式下该认的认、该放的放。**
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
旧式 = re.compile(r'(那包|那个|那块|那道|那把|那面|这个|这块|一个)\\1')


def _新式():
    src = io.open(os.path.join(ROOT, '工具', '小说检察官.py'), encoding='utf-8').read()
    m = re.search(r"re\.finditer\(r'(\(那包[^']*)',t\)", src)
    if not m:
        raise RuntimeError('取不到检察官之叠词式')
    return re.compile(m.group(1))


须认 = [
    '他把那个那个记号又描了一遍。',
    '绳搭在那块那块石头上。',
    '这个这个数我记不住。',
    '他拿那把那把刀刮了刮。',
]
# ★不许认者：皆取自正文原场，是好话，不是粘连
不许认 = [
    '他把五个罐子一个一个提起来掂了掂。',            # 111:33
    '他站在我们前头，一个一个点过去：我在前头。',      # 114:41
    '七个减到两个，中间那五个是一个一个少下去的。',    # 177:431
    '这一回他单填我一个，填得实。一个一个问，比一块儿点准。',  # 139:253
    '一队人，在一个不好走的地方，一个一个少下去。',    # 192:583
]


def 跑():
    新式 = _新式()
    坏, 回灌漏 = [], 0
    for s in 须认:
        if not 新式.search(s):
            坏.append('新式漏认：' + s)
        if not 旧式.search(s):
            回灌漏 += 1
    for s in 不许认:
        if 新式.search(s):
            坏.append('新式误认（「一个一个」是好话，不是粘连）：' + s)
    if 回灌漏 == 0:
        坏.append('★此测在旧式下亦全过——陪跑之测，不算数。')
    n = len(须认) + len(不许认)
    if 坏:
        print('✗ 负测·叠词闸 %d/%d' % (n - len(坏), n))
        for x in 坏:
            print('   ⛔ ' + x)
        return 1
    print('✓ 负测·叠词闸 %d/%d 全通（旧式回灌漏认 %d 项，故非陪跑）' % (n, n, 回灌漏))
    return 0


if __name__ == '__main__':
    sys.exit(跑())
