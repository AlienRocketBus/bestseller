# -*- coding: utf-8 -*-
"""负测 · 跨整章找东西的窗须挡换行（1103 立·X61·窗界哨之 ⛔待窗 十六处之治）

★立此测之由（`设定/窗界账.md` 0918 判错、挂作 ⛔待窗 之十六处，1103 落手）：
　`小说检察官.py` 之 ANTIPHYS／AWKWARD 跑在**整章之档**（`check_file` 之 text），
　CANON_FORBID 跑在**整章白文**（`b`），canon forbid 亦跑在**整章白文**（`_bai`）——
　**其窗意在一句之内，而旧界只挡「。」（或「，。」），⛔换行未挡**：
　**上一段末一个词接下一段头一个词（其间无句号，如段末作「——」「」」「？」），被缝成一句从来没有人写过的话。**
★其治：诸窗之界补 `\\n`；内嵌 canon（`_EMBEDDED_LIB`）与 `设定/canon事实库.json` 同笔补，F001／F004／F005 逐条同字。

五局（⛔每局皆带其牙：同一式不跨段者照旧须中）：
　①ANTIPHYS 「胡茬」段末＋「动」段首 → ⛔不许判物理反逻辑；同段者照判
　②AWKWARD 「胡茬」段末＋「抖」段首 → ⛔不许判文采病；同段者照判
　③CANON_FORBID 三式跨段 → ⛔不许中；同句者照中
　④外 canon F001／F004／F005 跨段 → ⛔不许中；同句者照中
　⑤内嵌 canon 诸 forbid 之窗皆挡换行，且 F001／F004／F005 与外 canon 逐条同字

用法：python3 工具/负测_窗界之换行.py [检察官.py 之路] [canon事实库.json 之路]
　（⛔二参供旧码回灌：`git show HEAD:…` 取於 /tmp 之副本验之，须红）
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import importlib.util, io, json, os, re, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_窗 = re.compile(r'\[\^([^\]]{1,24})\]\{0,\d+\}')


def _载(p):
    sp = importlib.util.spec_from_file_location('_检察官_负测', p)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def _查(m, 文):
    with tempfile.NamedTemporaryFile('w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(文)
        p = f.name
    try:
        return '\n'.join(m.check_file(p)[0])
    finally:
        os.unlink(p)


def _中(式, 文):
    return re.search(式, 文) is not None


def 跑(检=None, 库=None):
    检 = 检 or os.path.join(ROOT, '工具', '小说检察官.py')
    库 = 库 or os.path.join(ROOT, '设定', 'canon事实库.json')
    m = _载(检)
    ext = {f['id']: f for f in json.load(io.open(库, encoding='utf-8'))['facts']}
    局 = []

    _前 = '他抬起头。\n\n'
    跨 = _查(m, _前 + '风从坡上下来，吹着他的胡茬——\n\n动手的是老四。\n')
    同 = _查(m, _前 + '他的胡茬动了一下。\n')
    跨2 = _查(m, _前 + '额上的皱纹\n\n跳出来的是老四。\n')        # ★1103 W78 驳：皱纹之窗另守（旧只造胡茬之局）
    同2 = _查(m, _前 + '额上的皱纹跳了一下。\n')
    局.append(('①ANTIPHYS 跨段不判、同段照判（胡茬、皱纹二窗）', '[物理反逻辑]' not in 跨 and '[物理反逻辑]' in 同
               and '[物理反逻辑]' not in 跨2 and '[物理反逻辑]' in 同2))

    跨 = _查(m, _前 + '他摸了摸胡茬\n\n抖开那张纸的是老四。\n')
    同 = _查(m, _前 + '他的胡茬抖了抖。\n')
    def _文采胡茬(s):
        return '[文采病]' in s and '胡茬' in s.split('[文采病]')[1].split('\n')[0]
    局.append(('②AWKWARD 跨段不判、同段照判', not _文采胡茬(跨) and _文采胡茬(同)))

    _禁 = [p for p, _w, _e, _d in m.CANON_FORBID if '[^' in p]
    # ★1103 W78 驳：二窗之式，换行逐窗各落一例（旧只落其一窗，另一窗退回旧式仍绿）
    _例 = [(('钱满背着那一捆，说起十几年前——\n\n背不动了。', '钱满——\n\n说他十几年前背过'), '钱满说十几年前他背过。'),
           (('他往东头看——\n\n那副架子早没了。',), '东头那副架子立着。'),
           (('我们站在门口？\n\n在这寨子住了三个多月的人不多。', '我们在这儿——\n\n三个多月了'), '我们在这寨子住了三个多月。')]
    ok = len(_禁) == 3 and all(not any(_中(p, x) for x in 跨) and _中(p, 同) for p, (跨, 同) in zip(_禁, _例))
    局.append(('③CANON_FORBID 三式跨段不中、同句照中', ok))

    _外例 = {'F001_暗门机关': [('爷爷——\n\n教过我的那几样', '爷爷当年教过我'),
                             ('老宅的门——\n\n没有锁孔', '老宅那扇门没有锁孔')],
             'F004_浅纹初见': [('头一回——\n\n看见那道纹', '头一回看见那道纹'),
                             ('看见——\n\n纹路上那一下，头一回', '看见那纹，头一回')],
             'F005_手机手电': [('手机——\n\n灯的手电', '手机背面的手电')]}
    ok = True
    for k, 例 in _外例.items():
        for p, (跨, 同) in zip(ext[k]['forbid'] if k != 'F001_暗门机关'
                              else [x for x in ext[k]['forbid'] if '[^' in x], 例):
            ok = ok and not _中(p, 跨) and _中(p, 同)
    局.append(('④外 canon F001/F004/F005 跨段不中、同句照中', ok))

    emb = m._EMBEDDED_LIB
    缺 = [p for f in emb['facts'] for p in f.get('forbid', [])
          for c in _窗.findall(p) if '\n' not in c]
    同字 = all(next(f for f in emb['facts'] if f['id'] == k)['forbid'] == ext[k]['forbid']
             for k in ('F001_暗门机关', 'F004_浅纹初见', 'F005_手机手电'))
    局.append(('⑤内嵌 canon 窗皆挡换行（缺 %d）且 F001/F004/F005 与外 canon 同字' % len(缺),
               not 缺 and 同字))

    红 = 0
    print('════ 负测 · 窗界之换行（五局）════')
    for 名, 果 in 局:
        print('  %s %s' % ('✓' if 果 else '⛔', 名))
        红 += 0 if 果 else 1
    print('  ── %d/%d ──' % (len(局) - 红, len(局)))
    return 红


if __name__ == '__main__':
    a = sys.argv[1:]
    sys.exit(1 if 跑(*(a[:2])) else 0)
