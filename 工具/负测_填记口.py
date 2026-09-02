# -*- coding: utf-8 -*-
"""负测·填记口（批131·吞记闸第二形）
所治之伤：`--验收 N` 之说明亦係位置参数；不写即自动存版并落一行占位说明。
        而落完之後正文与末版逐字相同，空轮闸遂拦住 --存版 与 --补存——
        **那一行占位说明再也改不掉了**；真轮数轮号数的正是这一行。
        即：一轮真跑过了，而账上说不出它跑了什么。（同族：第十九犯·记录之路上有一个洞，走过去了自己不知道）
本测所验者为不变量，非快照：
  ①填记只填得了占位那一格，覆盖不了任何一行真说明（不论其文如何）；
  ②填完须留「原说明」之痕（一行後填的，不许看起来像当场写的）；
  ③说明以「--」起手者当场拦（与吞记闸同律）；
  ④验收无说明之时须当场出声，并印出唯一的修法；
  ⑤而其洞未被堵死——占位那一行仍存在（不许把闸改成「不落占位」了事，
    那样账上就少了一版，比说不清更坏）。
"""
import io, os, sys, json, shutil, tempfile, subprocess
_D = os.path.dirname(os.path.abspath(__file__))
_R = os.path.dirname(_D)
案 = []
def chk(名, 得, 期):
    案.append((名, 得 == 期, '得%r 期%r' % (得, 期)))

占位 = '（本轮说明未填，须在回执补记开庭与真伤级别）'

# ── 一·实跑：另起一间沙盘，不动真账 ──
tmp = tempfile.mkdtemp()
try:
    os.makedirs(os.path.join(tmp, '工具'))
    for f in ('跑轮.py',):
        shutil.copy(os.path.join(_D, f), os.path.join(tmp, '工具', f))
    vd = os.path.join(tmp, '版本', '第999章')
    os.makedirs(vd)
    led = os.path.join(vd, '_台账.json')
    io.open(led, 'w', encoding='utf-8').write(json.dumps({'章': 999, '版本': [
        {'版': 'v01', '说明': '第1轮·感官庭：真说明一行', 'hard': {}, 'soft': {}},
        {'版': 'v02', '说明': 占位, 'hard': {}, 'soft': {}},
    ]}, ensure_ascii=False, indent=1))

    def 跑(*a):
        p = subprocess.run([sys.executable, os.path.join(tmp, '工具', '跑轮.py')] + list(a),
                           cwd=tmp, capture_output=True, text=True)
        return p.returncode, (p.stdout or '') + (p.stderr or '')

    rc, out = 跑('--填记', '999', 'v02', '第2轮·四堂会审：所改何事')
    chk('①占位那一格·填得进', rc, 0)
    obj = json.load(io.open(led, encoding='utf-8'))
    行 = {x['版']: x for x in obj['版本']}
    chk('①之b 填进去的是真说明', '第2轮·四堂会审' in 行['v02']['说明'], True)
    chk('②须留「原说明」之痕', 行['v02'].get('原说明'), 占位)
    chk('②之b 且其说明须自带「填记」二字（见得出非当场所存）', 行['v02']['说明'].endswith('·填记'), True)

    rc, out = 跑('--填记', '999', 'v01', '想把这一行真说明改掉')
    chk('③真说明·不许覆盖', rc, 2)
    chk('③之b 且须说出为什么（账是用来查的）', '不许覆盖' in out and '另存一版' in out, True)
    chk('③之c 而那一行原样未动', json.load(io.open(led, encoding='utf-8'))['版本'][0]['说明'],
        '第1轮·感官庭：真说明一行')

    rc, out = 跑('--填记', '999', 'v02', '想把刚填的再改一遍')
    chk('③之d 填过一回之後亦不许再覆盖（填记不是一把万能改笔）', rc, 2)

    io.open(led, 'w', encoding='utf-8').write(json.dumps({'章': 999, '版本': [
        {'版': 'v01', '说明': 占位, 'hard': {}, 'soft': {}}]}, ensure_ascii=False, indent=1))
    rc, out = 跑('--填记', '999', 'v01', '--记')
    chk('④说明以「--」起手·当场拦（与吞记闸同律）', rc, 2)
    chk('④之b 并印出正确写法', '位置参数' in out, True)
    rc, out = 跑('--填记', '999', 'v01', '')
    chk('④之c 空说明亦拦（不许拿空字符串把洞抹平）', rc, 2)
    rc, out = 跑('--填记', '999', 'v99', '无此版')
    chk('④之d 无此版·须报现有版号，不许静默', rc == 2 and 'v01' in out, True)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# ── 二·验收口须当场出声 ──
_jc = io.open(os.path.join(_D, '小说检察官.py'), encoding='utf-8').read()
# ★★★★★2026-09-02·293第3轮·**此三项之断言今日被翻，须把翻它的由头写在这里，
#   不许悄悄改一行断言了事**（令§十一③：留底之档里的错因会被下一坐当成场）。
#   ★**原⑤之c 断的是**：「占位仍照落——**不许改成「不落这一版」，账上少一版比说不清更坏**」；
#     ★★**而今日翻它，其据有二，皆是数**：
#     ①**账上并不少一版**——不带说明那一次只是查，**其後带说明那一存照旧把同一段文存进去**；
#       **所失者不是一版，是那一行占位说明的含糊**；
#     ②**其代价已量得出**：**全书台账 3,352 版，占位行旧史只 1 行（第101章 v03）**，
#       **而今日一坐造出 8 行**——★★★**每一行都要回头 --填记，且每一行都先把带说明那一存拦在空轮闸上。**
#   ★★★★**故其判反过来**：**一行读不出自己跑的是哪一轮的账，不如不落。**
#   ★而本组三项遂改断新法，**且第③项反过来断「不许再落占位」**——
#     **一个被翻过的断言，若只是删掉，日後谁也不知道它曾经断过相反的话。**
chk('⑤验收无说明·须当场出声（其语今为「只查不存」）',
    'if not note:' in _jc and '说明未填：**本次只查不存**' in _jc, True)
chk('⑤之b 并须印出正确之写法（带说明重跑），而非叫人事後去填一个洞',
    '--验收 %d "第N轮·某庭：所改何事"' in _jc and '带说明者照旧自动存版' in _jc, True)
chk('⑤之c 【此断今日翻了】不许再落占位——空说明之路须在 save 之前 return',
    _jc.find('本次只查不存') < _jc.find("_m.save(n, note or"), True)
chk('⑤之d 而带说明者照旧存版（翻的只是「空说明也存」这一路，不是整个入口）',
    "_m.save(n, note or" in _jc, True)
_pl = io.open(os.path.join(_D, '跑轮.py'), encoding='utf-8').read()
chk('⑥填记口须挂上命令面（写了函数而未接线，等於没写）', "cmd == '--填记'" in _pl, True)

# ── 三·死门闸（第三形：账房的旧门） ──
# 其形：十轮精进.py 係跑轮.py 之旧身，全工具箱无一处引它，而它写的是同一批真台账；
#      自改名以来加进跑轮的闸（吞记闸、趋阈闸、填记口…）它一个也没有。
_sl = os.path.join(_D, '十轮精进.py')
if not os.path.exists(_sl):
    chk('⑦旧身已不在（若日後删之，本组自然作废）', True, True)
else:
    _st = io.open(_sl, encoding='utf-8').read()
    chk('⑦旧身之写口须封（存版／补存／还原／下一轮／轮记／补记）',
        all(x in _st for x in ("_写口 = ('--存版'", "if cmd in _写口:")), True)
    def 跑旧(*a):
        p = subprocess.run([sys.executable, _sl] + list(a), cwd=_R, capture_output=True, text=True)
        return p.returncode, (p.stdout or '') + (p.stderr or '')
    for c in ('--存版', '--补存', '--下一轮'):
        rc, out = 跑旧(c, '292', '试')
        chk('⑦之b 旧门 %s·不许写' % c, rc == 2 and '死门闸' in out, True)
    rc, out = 跑旧('--验轮', '292')
    # 头一版写作 rc == 0，而验轮见拦停旗本就该返 2——那是它在干活，不是它跑不动。
    # 「读口通不通」验的是它有没有读出账来，不是它对那本账满不满意。
    chk('⑦之c 而读口照旧可跑（设定诸档仍按行号引它，封的是写不是读）',
        '真轮' in out and '死门闸' not in out, True)
    chk('⑧且旧身未被删（设定 11_全书审计 与 十轮精进机制_立法与操作 仍印其名与行号）',
        os.path.exists(_sl), True)
    # 不变量：凡跑轮有而旧身无之闸，旧身皆不许再开写路。此处只验「写路已封」，
    # 不列举闸名——列举即成快照，日後跑轮再加一道闸，本测须照旧成立。
    # 头一版查的是「吞记闸」三字，而我自己在死门闸的注里就写了这三字，遂自判其坏。
    # 查名逮的是话，查形逮的才是那道闸：故改查其真身（_记 之守门函）。
    chk('⑧之b 旧身确係缺闸者（若日後两器同步，本项自坏，正提醒人回头看这一条）',
        ('def _记(argv)' in io.open(os.path.join(_D, '跑轮.py'), encoding='utf-8').read())
        and ('def _记(argv)' not in _st), True)

# ── 四·领轮基线之销，只算认了轮号的那一存（293第2轮所逮·第二形之馀波） ──
# 其形：领轮闸自己认的是说明里那个「第N轮」（闸八）——说明一空，它整个不适用；
#      而基线之销从前不问说明，於是一次 `--验收 N`（不带说明）的自动存版
#      **既不受领轮闸管，又把领轮基线吃掉了**：不归它管的那一步，把归它管的那一步的凭据销了。
#      （今日一坐之内从这个口走过三回：292 v16/v17、293 v05，三回都得回头补领轮。）
_pl2 = io.open(os.path.join(_D, '跑轮.py'), encoding='utf-8').read()
chk('⑨基线之销须以「说明报了轮号」为条件',
    "if _round_of(note) and os.path.exists(_ling_path(n)):" in _pl2, True)
chk('⑨之b 而其销未被删（报轮号者照旧一领一存）',
    "os.remove(_ling_path(n))   # 一领一存" in _pl2, True)
chk('⑨之c 且其由与领轮闸同源（闸八认的也是那个「第N轮」）',
    "_r0 = _round_of(note)" in _pl2, True)

坏 = [x for x in 案 if not x[1]]
for 名, 过, 详 in 案:
    print(('  ✓ ' if 过 else '  ⛔ ') + 名 + ('' if 过 else '　' + 详))
print('\n★负测 %d 项，过 %d，坏 %d' % (len(案), len(案) - len(坏), len(坏)))
sys.exit(1 if 坏 else 0)
