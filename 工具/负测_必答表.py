# -*- coding: utf-8 -*-
"""负测·必答表（第3轮逐数对表之抽数式）——2026-09-05·机制总审所立

★所测者一句话：**第3轮的必答表，认不认得着本书真拿来记数的那几个量词。**
★★其红在哪一行（上磁盘核，非设想）：**305 v13 拍61「前天那三处」对拍23「前天那四处」自相矛盾**——
   ★★★十二轮带器之轮一个没逮着，第13轮一遍通读撞上；★★★★而其所以没逮着：
   抽数之式只认 21 样量词，「处」「行」「道」「层」一个也不在其内——305 全章「N处」二十四见，入表者零。
★★★★★而一份在旧式下也全过的测就是陪跑（令§六③）——**故其要害在①：以旧式回灌 305，须证其一个「处」也抽不着。**
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import importlib.util
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, '工具', name + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _old_third(body):
    """★旧式（2026-09-05 改前之第三条抽数式，逐字照录）——只作回灌，不许再用。"""
    raw = set(re.findall(r'[二两三四五六七八九十百]+(?:个|下|回|段|样|类|把|条|根|卷|分)', body))
    return {x for x in raw if not re.fullmatch(r'一(个|下|回|段|样|类|口|层|把|条|根|卷|分|半)', x)}


def _body(p):
    return io.open(p, encoding='utf-8').read().split('【本章亮点')[0]


def _src_of(name, func):
    s = io.open(os.path.join(ROOT, '工具', name + '.py'), encoding='utf-8').read()
    m = re.search(r'\n(_数尾 = .*?\n)\n\ndef duty_list', s, re.S) if func == '_数项' else re.search(r'\ndef duty_list\(.*?\n(?=def |\Z)', s, re.S)
    return m.group(0) if m else None


def run():
    R = []
    pl = _load('跑轮')
    v13 = _body(os.path.join(ROOT, '版本', '第305章', 'v13.md'))
    v14 = _body(os.path.join(ROOT, '版本', '第305章', 'v14.md'))

    # ①旧式回灌·305 全章「N处」二十四见，旧式抽着几个——须为零（故此改非陪跑）
    old = _old_third(v14)
    n_chu = len(re.findall(r'[零〇一二两三四五六七八九十百]+处', v14))
    R.append(('①旧式回灌·305「N处」%d见，旧式入表 %d（须0）' % (n_chu, len([x for x in old if x.endswith('处')])),
              n_chu >= 20 and not any(x[-1] in '处行道层' for x in old)))

    # ②新式·305 之六处／三处／十一处／十道 皆入表
    it14, why14 = pl._数项(v14)
    R.append(('②新式·305 之 六处／三处／十一处／十道 入表', all(x in it14 for x in ('六处', '三处', '十一处', '十道'))))

    # ③真红回灌·305 v13 之同指对「前天那三处／前天那四处」须上表
    it13, _ = pl._数项(v13)
    R.append(('③真红·v13 同指对「前天那三处／前天那四处」上表', '前天那三处／前天那四处' in it13))

    # ④不误判·v14 已治，前天之对不再上表；而「昨天那三处／昨天那六处」（纸上对水里·不同物）仍作一问上表
    R.append(('④不误判·v14 无前天之对，而昨天之对仍作一问', not any('前天那' in x and '／' in x for x in it14)
              and '昨天那三处／昨天那六处' in it14))

    # ⑤无对不报·白文里无同指对者，表上无「／」
    plain = '今天我数了六处。他说三处。昨天那六处我记在本子上。'
    it5, _ = pl._数项(plain)
    R.append(('⑤无对不报·无同指对之白文表上无「／」', not any('／' in x for x in it5) and '六处' in it5 and '三处' in it5))

    # ⑥口语量词照旧不入表（一个／一下／一处／一行）
    it6, _ = pl._数项('一个人一下就走了一处，一行也没记。两个人走了三处。')
    R.append(('⑥口语量词不入表·一个／一下／一处／一行', not any(x in it6 for x in ('一个', '一下', '一处', '一行')) and '两个' in it6 and '三处' in it6))

    # ⑦序数·303 之「第三处、第四处、第五处」（305 拍20至22 串账之原场）入表
    it7, _ = pl._数项('我昨天在这一行上拿指甲搁过，第三处、第四处、第五处搁得进。')
    R.append(('⑦序数·「第三处」入表（305串账之原场係303此句）', '第三处' in it7 and '第五处' in it7))

    # ⑧双份同式·跑轮.py 与 十轮精进.py 之抽数式逐字同（「一处判，两份码」之旧伤所立）
    a, b = _src_of('跑轮', '_数项'), _src_of('十轮精进', '_数项')
    c, d = _src_of('跑轮', 'duty_list'), _src_of('十轮精进', 'duty_list')
    R.append(('⑧双份同式·跑轮.py 与 十轮精进.py 之 _数项 与 duty_list 逐字同', bool(a) and a == b and bool(c) and c == d))

    # ⑨自陈在册·「它认哪几样，本书同类共几样」与「不认只／指」写在器上
    s = io.open(os.path.join(ROOT, '工具', '跑轮.py'), encoding='utf-8').read()
    R.append(('⑨自陈在册·它认哪几样／不认「只」「指」／同指对之由', '它认哪几样' in s and '不认「只」「指」' in s and '同指对' in s
              and '只' not in pl._数尾 and '指' not in pl._数尾))

    # ⑩说明随表·第3轮之说明里写着同指对怎么裁
    R.append(('⑩说明随表·第3轮说明含「同指对」与「同一物即真伤」', '同指对' in why14 and '同一物即真伤' in why14))

    # ⑪回述词·旧式回灌：305 v13 含「前天」而旧式十样不认；新式认
    _old2 = re.compile(r'[^。！？\n]{0,26}(想起|记得|那天|那一回|昨天|前几天|早上|进来的时候|前十|二十七年前)[^。！？\n]{0,26}')
    old_hits = {m.group(1) for m in _old2.finditer(v13)}
    new_hits, why2 = pl._回述项(v13)
    R.append(('⑪回述词·v13 含「前天」：旧式不认（%s），新式认' % ('认' if '前天' in old_hits else '不认'),
              '前天' not in old_hits and '前天' in new_hits and '前天' in v13))

    # ⑫P36／P38 黑名单八词皆入式（这两天／前几天／这十来天／这几天｜那时候／那天／那一天／那会儿）
    黑 = ['这两天', '前几天', '这十来天', '这几天', '那时候', '那天', '那一天', '那会儿']
    got = [w for w in 黑 if w in pl._回述项('他说%s来过。' % w)[0]]
    R.append(('⑫黑名单八词皆入第2轮之式（%d/8）' % len(got), len(got) == 8))

    bad = [x for x, o in R if not o]
    for x, o in R:
        print('   %s %s' % ('✓' if o else '✗', x))
    print('  负测·必答表 %d/%d %s' % (len(R) - len(bad), len(R), '全通' if not bad else '⛔未通'))
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(run())
