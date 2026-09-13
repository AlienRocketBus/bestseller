# -*- coding: utf-8 -*-
"""负测·净重对表 · 2026-09-08 立（与 工具/净重对表.py 同日·令§六③）
　★要害在四样：
　　①**以旧式回灌**：拿 `db520882`（此器立成之前）之施工表灌回去，须逐行逮出那 17 处；
　　②**非陪跑**：**旧式对同一份原物零报**——立此器之前，全书没有一道器拿锁定行之净重回正文量过
　　　（`grep -rn 净重 工具/*.py` 之下，只有 书级体检 与 全测 在自己算自己的，无一处回表复量）；
　　③**非挖空**：今版须全绿，且其群不得塌（26 章），并须证「把一行改坏立刻逮得出」；
　　④**不吃盘**：此器只读不写（`--补` 例外，本负测不跑它），跑完诸档逐字原样。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import io, os, sys, subprocess, hashlib

根 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(根, '工具'))
import 净重对表 as J                                      # noqa: E402
from 亮点对表 import 诸章                                  # noqa: E402

过 = []
def t(名, 实, 期):
    过.append((名, 实 == 期, 实, 期))

章 = 诸章()
锚 = 'db520882'      # 此器立成之前——那 17 行尚未补
守 = [os.path.join(根, '设定', '01_镇冢秘术_逐章施工与伏笔回收表.md')] + list(章.values())
sha0 = {p: hashlib.sha256(io.open(p, 'rb').read()).hexdigest() for p in 守}

# ①旧物回灌：拿立器之前的施工表，须逮出 17 处
r = subprocess.run(['git', '-C', 根, 'show', '%s:设定/01_镇冢秘术_逐章施工与伏笔回收表.md' % 锚],
                   capture_output=True)
旧表 = r.stdout.decode('utf-8')
红旧, 群旧 = J.量(表文=旧表)
# ★2026-09-08 改：原钉死 17，而 17 是「立器之日尚未补的行数」——
# 旧表是死的，正文是活的：正文每改一章，旧表对得上的行就再少一行，17 自己会长。
# 一个会随日子长的数钉成常数，隔一天就自己变红（此即机制总审§二十六之病：桩一走味就成下一个坑）。
# 今改为「不得少於 17」，并把当日实数印在格名里，谁跑谁看得见它长到了几。
t('①回灌 %s 之施工表，逐行逮出 ≥17 处不符（今 %d 处；17 是立器之日之数，只许增不许减）' % (锚, len(红旧)),
  len(红旧) >= 17, True)
t('①之二·其群不变（26 章自书净重）', 群旧, 26)
# ★2026-09-08 二改（与格①同一族之病·机制总审§二十八）：
# 原式把 (283, 记3499, 实3481) 整个钉死，而**「实」是活的**——正文一改它就变（今日 #32 治 283，实成 3484）。
# 头一回改只扫了格①，把这一格留下了；**同一族之病，改一格不够，得把整器扫一遍。**
# 今只钉死物那一半：旧表上 283 那一行自书 3499（这是 db520882 之死数），
# 而「实」印出来给人看，不入判。
_283 = [(n, a, b) for _, n, a, b in 红旧 if n == 283]
t('①之三·旧表 283 自书 3499 且此器逮得着它（今实 %s；实数是活的，故不入判）'
  % (_283[0][2] if _283 else '未逮着'),
  [(n, a) for n, a, _ in _283], [(283, 3499)])

# ②非陪跑：立此器以前，无一道器拿锁定行之净重回正文量过。
#   ★怎么算「拿它量过」：一道器要量它，非得在同一处**既认锁定行、又取净重**不可。
#   故逐档逐行看：别器里有没有一行同时含「锁定」与「净重」。
#   ★★而 全测.py 里也有这样的行——那是**本器自己的接线与器注**，不算别器；
#     故它们必须**全落在 chk_net_weight_table 那一函数之内**。落在函数外，即是别处也在读它，此格该红。
全码 = io.open(os.path.join(根, '工具', '全测.py'), encoding='utf-8').read().split('\n')
起 = next(i for i, l in enumerate(全码) if l.startswith('def chk_net_weight_table'))
止 = next(i for i in range(起 + 1, len(全码)) if 全码[i].startswith('def '))
# ★★★★2026-09-13 收窄（0913 立 `负测_净重取形` 之後当场报红，其四行皆係器注）：
#   ⛔**旧式逐行只看字，遂把「器注」也数成了「别器在量」**——
#   **而本格自己的注早写着「那是本器自己的接线与器注，不算别器」**：
#   **它只把这一免给了 `全测.py` 里那一函之内，别处的注一概没免。**
#   ★**今把这一免写成通例**：**注不是量**——
#   **凡井号之注、凡串之内（模块与函数之说明、多行串里的字），一概不算**；
#   ⛔**而真码里同时读这两样者，照旧红**（其牙见②之四）。
#   ★★**其法不靠认字，靠 `ast` 把串与注的行号先标出来**——**认字必再漏。**
def _注与串之行(路):
    """返回该档中「井号之注」与「串之内」所占之行号（1 起）。"""
    import ast as _ast
    s = io.open(路, encoding='utf-8').read()
    行 = s.split('\n')
    出 = set()
    for i, l in enumerate(行, 1):
        if l.lstrip().startswith('#'):
            出.add(i)
    try:
        tree = _ast.parse(s)
    except Exception:
        return 出
    # ⛔**立日自栽一回，其局即下头②之四**：**头一版把「凡串之内」一概免了**——
    #   **而真去量它的那一行，正是拿串在比**（`if '锁定' in 行 and '净重' in 行:`）；
    #   **於是这一免把牙一并拔了，②之四当场报「得 0 期 1」。**
    #   ★**今只免「说明之串」（模块／函数／类之首句）与井号之注**——**注不是量，而串是。**
    for node in _ast.walk(tree):
        if isinstance(node, (_ast.Module, _ast.FunctionDef,
                             _ast.AsyncFunctionDef, _ast.ClassDef)):
            body = getattr(node, 'body', None)
            if not body:
                continue
            first = body[0]
            if (isinstance(first, _ast.Expr)
                    and isinstance(getattr(first, 'value', None), _ast.Constant)
                    and isinstance(first.value.value, str)):
                a0 = getattr(first, 'lineno', None)
                b0 = getattr(first, 'end_lineno', a0)
                if a0:
                    出.update(range(a0, (b0 or a0) + 1))
    return 出


犯 = []
for f in sorted(os.listdir(os.path.join(根, '工具'))):
    if not f.endswith('.py') or f in ('净重对表.py', '负测_净重对表.py'):
        continue
    _p = os.path.join(根, '工具', f)
    _skip = _注与串之行(_p)
    for i, ln in enumerate(io.open(_p, encoding='utf-8'), 1):
        if '锁定' in ln and '净重' in ln:
            if i in _skip:
                continue        # ★注不是量
            if f == '全测.py' and 起 < i <= 止:
                continue        # 本器之接线，不算别器
            犯.append('%s:%d' % (f, i))
t('②非陪跑：除本器之接线外，别处无一行同时读「锁定」与「净重」（故那 17 处一器也报不出）', 犯, [])
t('②之三·而本器之接线确在（不是靠删干净换来的绿）',
  any('锁定' in l and '净重' in l for l in 全码[起:止]), True)
# ②之二·而 全测.py 确实提过「净重」——提的是别的账（回执对台账、全书净重中位、台账之版比），
#   非施工表之锁定行；此格证「提过」不等于「量过」。
全 = io.open(os.path.join(根, '工具', '全测.py'), encoding='utf-8').read()
t('②之二·全测提过净重（故此非「谁都没提过」，是「提过而没回表量过」）', '净重' in 全, True)

# ②之四⛔证「注不是量」这一免没把牙拔掉：造一份假档，
#   其注里写一行、其真码里写一行——注那一行须放过，码那一行须逮着。
import tempfile as _tf
_假 = '''# -*- coding: utf-8 -*-
"""本注里提「锁定」与「净重」两样，而它只是注，不是量。"""
# 此井号之注亦同时提「锁定」与「净重」。
def 假量(行):
    if '锁定' in 行 and '净重' in 行:
        return 1
    return 0
'''
_fd, _tp = _tf.mkstemp(suffix='.py', dir=os.path.join(根, '工具'))
os.close(_fd)
io.open(_tp, 'w', encoding='utf-8').write(_假)
try:
    _skip2 = _注与串之行(_tp)
    _hit = [i for i, ln in enumerate(io.open(_tp, encoding='utf-8'), 1)
            if '锁定' in ln and '净重' in ln and i not in _skip2]
    t('②之四·注那两行放过、真码那一行照旧逮着（证此免未把牙拔掉）',
      len(_hit), 1)
finally:
    os.unlink(_tp)

# ③非挖空
红今, 群今 = J.量()
t('③今版零处不符', [(n, a, b) for _, n, a, b in 红今], [])
# ★★★★★2026-09-08 订·306封版席（其立器之日为同日）：
#   ★病灶：此格自书「其群**不得塌**」，而其码写的是 `群今 == 26`——**一个下限被写成了等号**。
#   ★★其果：306之锁定行一立（自书净重2690，且经 `净重对表.py` 复量相符），群由26涨到27，**本格当场判红**；
#     ★★★而它红的不是一处崩，是「这本书又多了一章有净重的锁定行」——**闸把一件对的事判成了错。**
#   ★★★★故改作下限（`>= 26`）：**塌了才红，涨了不红**；26 仍是立器之日之数，只许增不许减，与①之格同律。
基线群 = 26
t('③之二·其群不得塌（基线 %d 章·今 %d 章）' % (基线群, 群今), 群今 >= 基线群, True)
文 = io.open(守[0], encoding='utf-8').read()
坏 = None
for line in 文.split('\n'):
    m = J.锁.match(line)
    if m and J.数.search(line) and int(m.group(1)) in 章:
        坏 = line
        break
假 = 文.replace(坏, J.数.sub('净重1', 坏, count=1), 1)
r4, _ = J.量(表文=假)
t('③之三·把一行之数改作 1，当场逮出（这个绿不是一律放行换来的）',
  len(r4) == 1 and r4[0][2] == 1, True)

# ④不吃盘
sha1 = {p: hashlib.sha256(io.open(p, 'rb').read()).hexdigest() for p in 守}
t('④跑完施工表与诸章逐字原样', sha1, sha0)

print('════ 负测·净重对表 ════')
for 名, ok, 实, 期 in 过:
    print(('  ✓ ' if ok else '  ⛔ ') + 名 + ('' if ok else '｜得 %r 期 %r' % (str(实)[:70], str(期)[:70])))
好 = sum(1 for _, o, _, _ in 过 if o)
print('  ── 负测·净重对表 %d/%d %s ──' % (好, len(过), '全通' if 好 == len(过) else '有败'))
sys.exit(0 if 好 == len(过) else 1)
