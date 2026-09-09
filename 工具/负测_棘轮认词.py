# -*- coding: utf-8 -*-
"""负测·棘轮之四字三现·认词（DEBT-298A·298第12轮立·限307·於307封版之序结清）

所治之伤（到期账 items::DEBT-298A 逐字）：
    **「预检.py::棘轮之『四字三现』认的是四字之窗，不是词；故一句被数两遍」**——
    298第12轮实数：19样之中「那一圈水印」×3 出「那一圈水」＋「一圈水印」两条、
    「门口那只碗」出「门口那只」＋「口那只碗」、「她一回也没」出「她一回也」＋「一回也没」、
    「宽的那一半」出「宽的那一」＋「的那一半」——**四句生八条**。
★即：**一句五个字的重出，在这把尺上算两处；六个字的算三处**——句子越长它被罚得越重，而它其实只重了一回。
★★而 298 当章一行代码不动此尺（令§六★★★★：不许为了让自己那一笔过去而挖空闸），故其治拖到 307：
   **不改旧式，另立一个认词之变式**；旧式照旧管棘轮之判，新式只报，供人裁。

本测所验（其头一项断言即其档所命，逐字照办）：
  ①**以298v38回灌，旧式报20而新式须报15上下**；
  ②**且二者之差须逐条指得出是哪四句被数了两遍**——四句逐句点名，一句也不许含糊；
  ③旧式对同一份原物照旧报20（不改旧式·非陪跑之凭）；
  ④新式不许把不同的重出合成一处（合并只许沿重叠，不许跨句）；
  ⑤新式之数不许高於旧式（认词只会少，不会多）；
  ⑥其口在 棘轮预检.py --项 四字三现·认词，且只认这一项。
"""
import io, os, re, sys
import importlib.util as iu

_D = os.path.dirname(os.path.abspath(__file__))
_R = os.path.dirname(_D)
案 = []


def chk(名, 得, 期):
    案.append((名, 得 == 期, '得%r 期%r' % (得, 期)))


def _mod(名, 档):
    sp = iu.spec_from_file_location(名, os.path.join(_D, 档))
    m = iu.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


_tj = _mod('_tj', '十轮精进.py')

_V38 = os.path.join(_R, '版本', '第298章', 'v38.md')
chk('〇·298v38 在（此测之原物）', os.path.exists(_V38), True)
_txt = io.open(_V38, encoding='utf-8').read()
_body = _tj.body_of(_txt)

# ①旧式之数（其档所命：旧式报20）
_seen = {}
for i in range(len(_body) - 3):
    k = _body[i:i + 4]
    if re.match(r'^[一-龥]{4}$', k):
        _seen[k] = _seen.get(k, 0) + 1
_旧 = sorted(k for k, v in _seen.items() if v >= 3)
_h, _sf = _tj.score(_txt)
chk('③旧式对同一份原物照旧报20（不改旧式·非陪跑之凭）', _sf['四字串三现'], 20)
chk('③之b 旧式之窗表亦为20（score 与逐窗重算同口径）', len(_旧), 20)

# ①新式之数
_新数, _新串 = _tj.rep3_by_word(_body)
chk('①以298v38回灌·新式须报15上下（今16）', 14 <= _新数 <= 17, True)
chk('⑤新式不高於旧式（认词只会少，不会多）', _新数 <= _sf['四字串三现'], True)

# ②二者之差须逐条指得出是哪四句被数了两遍
_四句 = ['那一圈水印', '门口那只碗', '她一回也没', '宽的那一半']
_窗 = {
    '那一圈水印': ('那一圈水', '一圈水印'),
    '门口那只碗': ('门口那只', '口那只碗'),
    '她一回也没': ('她一回也', '一回也没'),
    '宽的那一半': ('宽的那一', '的那一半'),
}
for 句 in _四句:
    a, b = _窗[句]
    chk('②「%s」旧式确出两条窗（%s＋%s）' % (句, a, b), a in _旧 and b in _旧, True)
    chk('②之b「%s」新式只作一条' % 句, _新串.count(句), 1)
    chk('②之c「%s」新式不再另留其两条窗' % 句, (a in _新串) or (b in _新串), False)
chk('②之d 二式之差恰为四（四句各省一条）', _sf['四字串三现'] - _新数, 4)

# ④合并只许沿重叠，不许跨句：新式每一串须真在文里出现≥3次
chk('④新式每一串皆真出现≥3次（不许凭合并造出一个文里没有的串）',
    all(_body.count(x) >= 3 for x in _新串), True)
chk('④之b 新式无一串被别的串整个含住（含住者即重复计一句）',
    all(not any(x in y and x != y for y in _新串) for x in _新串), True)

# ⑥其口
_pj = io.open(os.path.join(_D, '棘轮预检.py'), encoding='utf-8').read()
chk('⑥其口在 棘轮预检.py --项 四字三现·认词', '四字三现·认词' in _pj, True)
chk('⑥之b 且只认这一项（别的项名当场拒）', '本口只认「四字三现·认词」一项' in _pj, True)
chk('⑥之c 旧式仍在棘轮所judge之列（不许因立新式而把旧式撤了）',
    "'四字串三现'" in io.open(os.path.join(_D, '十轮精进.py'), encoding='utf-8').read(), True)

坏 = [x for x in 案 if not x[1]]
for 名, 过, 详 in 案:
    print(('  ✓ ' if 过 else '  ⛔ ') + 名 + ('' if 过 else '　' + 详))
print('\n★负测·棘轮认词 %d 项，过 %d，坏 %d' % (len(案), len(案) - len(坏), len(坏)))
sys.exit(1 if 坏 else 0)
