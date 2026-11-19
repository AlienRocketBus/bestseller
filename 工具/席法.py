#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""席法——**诸席之 .js 写法闸**：专防本坐在写席时反复踩的那几样。

【其立之由（2026-09-09）】本坐一日之内在同一形上犯了**四回**：
  ①`一章.js` 之 schema 键写成中文 → API 400，**六个席一个也没起来，一个字都没写**；
  ②五庭之提示里把命令用反引号括起来 → 工作流解析当场拒；
  ③第12/13轮必答表之提示，同形；④封版席里 `mk695e@gmail.com` 之反引号，同形。
★**而四回都被拦住了，一次也没混过去**——拦它的是工作流之解析与 API，**不是本仓的任何一道闸**。
★★**其病之形**：提示自己活在反引号里，而写提示的人习惯拿反引号括命令——
  **两层反引号撞在一处，外层当场断掉。**
★★★**而 `node --check` 量不出它**：断掉之後那一段仍是合法的 JS（只是意思全变了）——
  **一把量不出这个病的尺，用了四回还在用，这本身才是要治的那一样。**

【它认哪几样，本书同类共几样（令§六④）】
  认 `工具/席/*.js` **全部**（今 6 样，判据之源律：当场 glob，不写死）。两路：
  甲·**schema 键须 ASCII**：API 之 `input_schema.properties` 只收 `^[a-zA-Z0-9_.-]{1,64}$`。
  乙·**模板串内之反引号须转义**：凡在 `agent(\\`…\\`)` 之模板串里出现未转义之 `` ` ``，即红。

【其限（§一⑤）】本闸只认这两样；**它不保证一份席跑得起来**，只保证不因这两样跑不起来。

用法：
    python3 工具/席法.py
    python3 工具/席法.py <稿.js> [...]   # 〔1119 坑10 复踩〕Workflow 之稿：先写於 scratchpad、过本闸、再以 scriptPath 开
    python3 工具/席法.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os
import re
import sys
import glob
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _读(p):
    with open(p, encoding='utf-8', errors='ignore') as f:
        return f.read()


def 查一(t):
    """返 (schema键之红, 反引号之红)。"""
    键红 = [k for k in re.findall(r'([^\s:,{}\'"`]+)\s*:\s*\{\s*type:', t)
            if not re.fullmatch(r'[A-Za-z0-9_.\-]{1,64}', k)]
    # ★立器当日砍掉一路·记此**免下一坐再造它**：初版另有一路「数反引号之奇偶，未闭合即红」，
    #   而它把 `//` 注释里的反引号也数了进去，当场对 `一章.js` 报假红——
    #   **一个会喊狼的核对器比没有更糟**（本仓旧律），故砍。
    # ★★**其限须直说**（§一⑤）：本器只逮「模板串里拿反引号括命令」这一形，
    #   逮不出别的形之反引号相撞；**逮不出的那些，靠工作流解析当场拒**——
    #   而那一道是有效的：本坐今日四回同形，四回皆被它拦下，一次也没混过去。
    引红 = []
    # ★★★2026-09-09 补一形·**它刚让本坐跑废一次，而本器当时印「诸席俱合」——那是一次假绿**：
    #   heredoc 里写 `\\\\``（双转义）落到档上即成「反斜杠＋反引号」，
    #   **JS 读作「一个字面反斜杠」＋「模板串就此结束」**——外层当场断掉，而 node --check 照旧过。
    #   ★其判得死：模板串里出现 `\\\\`` 者，一律红（真要写一个字面反斜杠加反引号，本仓无此需）。
    for m in re.finditer(r'\\\\`', t):
        引红.append('第%d行附近：双转义之 \\\\`（heredoc 写多了一层）——'
                    'JS 读作「字面反斜杠」＋「模板串结束」，外层当场断掉，而 node --check 照旧过'
                    % (t[:m.start()].count('\n') + 1))
    # 另一路·更实：模板串内出现「`cmd`」之形（一对反引号夹着 python3/grep/awk/ls/git）
    for m in re.finditer(r'(?<!\\)`\s*(python3|grep|awk|sed|ls|git|node)\b', t):
        引红.append('第%d行附近：未转义之 `%s …（提示里的命令须写作 \\\\`）'
                    % (t[:m.start()].count('\n') + 1, m.group(1)))
    return 键红, sorted(set(引红))


def 起得来(f):
    """★★★★★2026-09-11 立·**本器今日之最大一次假绿，其代价是四个半钟头全书停摆**：
    `工具/席/一章.js` 里有一整段（103 行）被复制成两份，於是 `const 庭` 重声明，
    **工作流当场拒：Identifier '庭' has already been declared**——**一章也开不了**；
    ★而那四个半钟头里，每小时那个自走 Routine 各起过一坐，**每一坐跑到派席那一步都撞同一个错**，
      **於是每一坐都白起**；★★**而本器那一刻印的是「✓ 诸席俱合」。**
    ★★★**其病之根一句话**：本器查的是**写法**（schema 键／反引号），**从来没问过一句「它跑得起来吗」**。
      **一份跑都跑不起来的席，在写法上可以是完美的。**
    ★★★★故补此路：**拿 `node --check` 真去解析一遍**——**它逮不出的形另有其它路，
      而它逮得出的这一形（重声明／括号不闭／落了半截），正是「改席」最常摔的那一跤。**
    ⛔**并记其限，不许含糊**：`node --check` 按 CommonJS 解析，**与工作流那一层的解析不尽同**；
      **故它过了不等於工作流一定收**——**但它不过，工作流一定不收。**
      **本路只守後一半：不过即红。**
    """
    # ★★★★★★0911 当日立此路时**又栽了一跤，须逐字记下**：
    #   头一版写的是 `node --check <档>.js`——**而它对今日那份真坏局照旧印绿**。
    #   ★其由：`.js` 之副档名令 node 按 **CommonJS script** 解析，而工作流那一层按 **ESM** 解析；
    #     **同名 const 声明两遍这一形，只在 ESM 之下当场报错**。
    #   ★★即：**头一版的丙路，逮不住那个把全书停摆四个半钟头的东西**——
    #     **一道照着病立起来而逮不住那个病的闸，比没有更坏（它会让人以为已经防住了）。**
    #   ★★★故改：拷一份作 `.mjs` 再 check，**与工作流同一种解析**。
    #     实测：同一档 `--check x.js` 印绿，`--check x.mjs` 当场印
    #     「const 庭 = [ ^ SyntaxError: Identifier '庭' has already been declared」。
    # ★★★★★★★而头一版之 .mjs 又立刻栽了第二跤（0911 同日·须一并记下）：
    #   直接把席当 ESM 去 check，**十份席里十份报红**——其红皆在同一形：`return out.filter(Boolean)`。
    #   ★其由：**工作流把整份脚本包在一个 async 函数里跑**，故席里写 top-level `return`／`await` 是合法的；
    #     而裸 ESM 之下二者皆非法。★★**於是那一版丙路把「本来就该这么写」的十份席全判成坏的**——
    #     **一个会喊狼的核对器比没有更糟**（本仓旧律，今日第三次用上）。
    #   ★★★故今照工作流那一层之形包一层再 check：`export const meta` → `const meta`，
    #     其余整份包进 `async function _w(){ … }`——**这才是与它同一种解析**。
    import shutil
    import tempfile
    码 = _读(f)
    码 = re.sub(r'^export\s+const\s+meta', 'const meta', 码, count=1, flags=re.M)
    i = 码.find('\n', 码.find('const meta'))
    # 自 meta 之後整块包起来（meta 之块以第一处 '\n}' 收）
    j = 码.find('\n}', i)
    j = (j + 2) if j > 0 else i
    码 = 码[:j] + '\nasync function _w() {\n' + 码[j:] + '\n}\n'
    d = tempfile.mkdtemp(prefix='席法check_')
    m = os.path.join(d, os.path.basename(f).rsplit('.', 1)[0] + '.mjs')
    try:
        open(m, 'w', encoding='utf-8').write(码)
        r = subprocess.run(['node', '--check', m], capture_output=True, text=True)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    if r.returncode == 0:
        return None
    语 = (r.stderr or r.stdout).strip().split('\n')
    要 = [x for x in 语 if x.strip() and not x.strip().startswith('at ')][:3]
    return ' ｜ '.join(x.strip() for x in 要)[:200]


def 二代之检(t):
    """1013·造式二代（设定/方法升级_造式二代.md §九3；坑②④）：席之令须带「回数之限」与「只读章料」。
    判法：一档立了 const 限 与 const 料律 者，即二代之席——其每一份以「`${令}」起之令，至其模板串之末，须含「${限(」；
    除盲读（⛔读章料）外须含「${料律}」。⛔限：只认以「`${令}」起之令与「盲读令」，不解析 JS 全文。"""
    if not re.search(r'const\s+限\s*=', t) or not re.search(r'const\s+料律\s*=', t):
        return []
    坏 = []
    for m in re.finditer(r'`\$\{令\}', t):
        e = t.find('`', m.end())
        身 = t[m.end():e if e > 0 else len(t)]
        首 = 身.strip().split('\n')[0][:30]
        if '${限(' not in 身:
            坏.append('二代之令缺「回数之限」（${限(n)}）：「%s…」' % 首)
        if '${料律}' not in 身:
            坏.append('二代之令缺「只读章料」（${料律}）：「%s…」' % 首)
    m = re.search(r'const\s+盲读令\s*=\s*\(\)\s*=>\s*`', t)
    if m:
        e = t.find('`', m.end())
        if '${限(' not in t[m.end():e]:
            坏.append('二代之盲读令缺「回数之限」')
    return 坏


def 查(印=True, fs=None):
    # 〔1119 坑10 复踩·W907/W908 三席 400〕fs 可由参给：Workflow 之稿（总编辑写於 scratchpad 之 .js）开跑前亦须过本闸
    fs = sorted(fs) if fs else sorted(glob.glob(os.path.join(ROOT, '工具', '席', '*.js')))
    红 = []
    for f in fs:
        k, b = 查一(_读(f))
        rp = os.path.relpath(f, ROOT) if os.path.abspath(f).startswith(ROOT) else f
        # ★丙路先於甲乙印：**跑不起来这一件，比写法上的任何一处都大**
        c = 起得来(f)
        if c:
            红.append('丙·%s：**node --check 不过**——%s'
                      '｜★**一份跑不起来的席，写法上可以是完美的**：'
                      '0911 之 一章.js 即因一整段被复制成两份而重声明，'
                      '**全书停摆四个半钟头，而本器那时印「诸席俱合」。**' % (rp, c))
        for x in k:
            红.append('甲·%s：schema 键非 ASCII「%s」——API 只收 ^[a-zA-Z0-9_.-]{1,64}$，'
                      '写中文则 400，**诸席一个也起不来**。' % (rp, x))
        for x in b:
            红.append('乙·%s：%s' % (rp, x))
        for x in 二代之检(_读(f)):
            红.append('丁·%s：%s' % (rp, x))
    if 印:
        print('════ 席法 ════（认 %d 份席·三路：**跑得起来（node --check）**／schema键须ASCII／模板串内反引号须转义）' % len(fs))
        for x in 红:
            print('  ⛔ ' + x)
        print('  ✓ 诸席俱合。' if not 红 else '  ⛔ %d 处。' % len(红))
    return 红


def 自测():
    ok, bad = 0, []

    def T(n, c, note=''):
        nonlocal ok
        if c:
            ok += 1
        else:
            bad.append(n + ('（%s）' % note if note else ''))

    T('①今局诸席俱合', not 查(印=False), '；'.join(查(印=False))[:120])

    # ★★★★★丙路之负测（0911 立·与其路同日）——**拿今日那份真让全书停摆四个半钟头的坏局回灌**
    #   ★其局之实：`git show 9c7b78a4:工具/席/一章.js` ——其内一整段（103 行）被复制成两份，
    #     `const 庭` 重声明；★★工作流当场拒「Identifier '庭' has already been declared」，
    #     **而本器那时印「✓ 诸席俱合」**（甲乙两路皆过：schema 键是 ASCII、反引号也都转义了）。
    #   ★★★**故这一格问的正是那一句**：**新路逮不逮得住「写法完美而跑不起来」。**
    import subprocess as _sp
    import tempfile as _tf

    def _坏(码):
        d = _tf.mkdtemp(prefix='席法负测_')
        f = os.path.join(d, 'x.js')
        open(f, 'w', encoding='utf-8').write(码)
        try:
            return 起得来(f)
        finally:
            try:
                os.remove(f)
                os.rmdir(d)
            except Exception:
                pass

    # ④·**今日之真局**：同一个 const 声明两遍（一整段被复制之形）
    T('④丙路·同名 const 声明两遍（0911 真局之形）须红',
      bool(_坏("const 庭 = [1]\nconst 庭 = [2]\n")))
    # ④之二·括号没闭（改席落了半截之形）
    T('④之二 丙路·括号未闭（改席落了半截）须红', bool(_坏("const a = {\n")))
    # ④之三·**好局不许红**（不然它就是一个会喊狼的核对器）
    T('④之三 丙路·好局不许红', not _坏("export const meta = {name:'x',description:'y'}\nconst a = 1\n"))
    # ④之四·**旧式回灌·证本路非陪跑**：坏局在甲乙两路之下**照旧全过**
    #   （schema 键是 ASCII、无未转义之反引号）——**即：没有丙路，它就是一次假绿。**
    _k, _b = 查一("const 庭 = [1]\nconst 庭 = [2]\n")
    T('④之四 旧式回灌·同一坏局在甲乙两路之下照旧全过（故丙路非陪跑）',
      not _k and not _b)
    # ④之六·★★**最要紧的一格·拿 0911 那份真坏局回灌**（`git show 9c7b78a4:工具/席/一章.js`）：
    #   **它是唯一一份「真的让全书停摆过四个半钟头」的局**——**本路若逮不住它，本路就是白立的。**
    # ★样本落在 `工具/席/_坏局样本/` 之内，**不落在 `工具/席/` 之下**——
    #   其由：查之 glob 係 `工具/席/*.js`，样本若与诸席同处，**本器每一回都会把这份标本判红**
    #   （0911 当日实见，一立即犯）；**一份负测之样本，不许把它守的那道闸自己拌倒。**
    _真坏 = os.path.join(ROOT, '工具', '席', '_坏局样本', '一章js_0911.js')
    if os.path.exists(_真坏):
        T('④之六 真坏局回灌·0911 那份让全书停摆四个半钟头的 一章.js 须红', bool(_坏(_读(_真坏))))
        _k6, _b6 = 查一(_读(_真坏))
        T('④之六之二 同一真坏局在甲乙两路之下照旧全过（故丙路非陪跑·此即当日那次假绿）',
          not _k6 and not _b6)
    else:
        bad.append('④之六 真坏局之样本不在（%s）——**没有样本的负测是空话**' % _真坏)
    # ④之七·**top-level return／await 不许被误判**（0911 同日第二跤：十份席全被判坏）
    T('④之七 top-level return 不许红（工作流把整份包在 async 函数里跑）',
      not _坏("export const meta = {name:'x',description:'y'}\nconst a = await f()\nreturn a\n"))
    # ④之五·**本路之限须写在测里**（§一⑤）：node --check 过不等於工作流一定收
    _s5 = open(os.path.join(ROOT, '工具', '席法.py'), encoding='utf-8').read().split('def 自测')[0]
    T('④之五 头注写明其限（过了不等於工作流一定收；不过则工作流一定不收）',
      '不过即红' in _s5 and '不尽同' in _s5)
    # ②旧局回灌·甲：中文 schema 键须当场逮出（此係 0909 之真局）
    k, _ = 查一("schema: { properties: { 锁定行: { type: 'string' } } }")
    T('②中文 schema 键照旧判红', k == ['锁定行'], str(k))
    T('②之二 ASCII 键不误伤', 查一("{ lock_row: { type: 'string' } }")[0] == [])
    # ③旧局回灌·乙：提示里未转义之命令反引号须逮出（0909 之真局·四回同形）
    _, b = 查一("const p = `跑一下 `python3 工具/全测.py` 看看`")
    T('③未转义之 `python3 照旧判红', any('python3' in x for x in b), str(b))
    # ★2026-09-09 改此格之样本·记其由：**这个样本自己就是双转义的**（写的是 \\\\`，不是 \\`）——
    #   它本想演示「写对的样子」，写出来的却正是本日新逮的那个病。**改样本，不改判据。**
    T('③之二 已转义者不误伤（单转义 \\`）', 查一("const p = `跑一下 \\`python3 x.py\\` 看看`")[1] == [],
      str(查一("const p = `跑一下 \\`python3 x.py\\` 看看`")[1]))
    # ③之三·**双转义须判红**（0909 新形：它让本坐跑废一次，而本器当时印「诸席俱合」）
    T('③之三 双转义 \\\\` 照旧判红',
      any('双转义' in x for x in 查一("const p = `读 \\\\`档名\\\\` 一遍`")[1]))
    # ④席之全集当场 glob（判据之源律）
    T('④席之全集当场读出（今 %d 份）' % len(glob.glob(os.path.join(ROOT, '工具', '席', '*.js'))),
      os.path.join(ROOT, '工具', '席', '造章.js') in glob.glob(os.path.join(ROOT, '工具', '席', '*.js')))   # ★409 囤灰四席彻删後只余三：⛔以份数为底，认派令之席在集中
    # ⑤本闸逮得出 node --check 逮不出的那一样（其立之由）
    T('⑤本闸之乙路非空判据（认命令词 7 样）', len(re.findall(r'python3\|grep', _读(os.path.join(ROOT, '工具', '席法.py')))) >= 1)
    # ⑨1013·二代之检：缺限、缺料律即红；全带者不红；非二代之席不查
    _好 = "const 限 = (n) => n\nconst 料律 = 'x'\nconst 甲 = () => `${令}\n你是甲\n${料律}\n${限(12)}`\nconst 盲读令 = () => `你是盲\n${限(8)}`"
    T('⑨二代之席令俱带限与料律 → 不红', 二代之检(_好) == [])
    T('⑨之二 缺限 → 红', any('回数之限' in x for x in 二代之检(_好.replace('${限(12)}', ''))))
    T('⑨之三 缺料律 → 红', any('只读章料' in x for x in 二代之检(_好.replace('\n${料律}\n', '\n'))))
    T('⑨之四 非二代之席（无 const 限）不查', 二代之检('const 甲 = () => `${令}\n你是甲`') == [])
    T('⑨之五 今仓 造章.js 俱合', 二代之检(_读(os.path.join(ROOT, '工具', '席', '造章.js'))) == [])
    # ⑩ 1119 坑10 复踩：Workflow 之稿（任意路之 .js）以参给即查——顶层 schema 键汉字须红、好稿⛔红
    _d = _tf.mkdtemp(prefix='席法参_')
    _f坏 = os.path.join(_d, 'w坏.js'); _f好 = os.path.join(_d, 'w好.js')
    open(_f坏, 'w', encoding='utf-8').write("export const meta = {name:'x',description:'y'}\nconst r = await agent('a', { schema: { type: 'object', properties: { 方案: { type: 'string' } }, required: ['方案'] } })\nreturn r\n")
    open(_f好, 'w', encoding='utf-8').write("export const meta = {name:'x',description:'y'}\nconst r = await agent('a', { schema: { type: 'object', properties: { plan: { type: 'string' } }, required: ['plan'] } })\nreturn r\n")
    try:
        T('⑩ 参给之 Workflow 稿·顶层 schema 键汉字须红', any('方案' in x for x in 查(印=False, fs=[_f坏])))
        T('⑩之二 参给之 Workflow 稿·ASCII 之键不许红', not 查(印=False, fs=[_f好]), '；'.join(查(印=False, fs=[_f好]))[:120])
    finally:
        for _x in (_f坏, _f好):
            try:
                os.remove(_x)
            except Exception:
                pass
        try:
            os.rmdir(_d)
        except Exception:
            pass
    print('── 负测·席法 %d/%d %s ──' % (ok, ok + len(bad), '全通' if not bad else '｜未过：' + '；'.join(bad)))
    return not bad


if __name__ == '__main__':
    if '--自测' in sys.argv:
        sys.exit(0 if 自测() else 1)
    _参 = [a for a in sys.argv[1:] if a.endswith('.js')]
    sys.exit(1 if 查(fs=_参 or None) else 0)
