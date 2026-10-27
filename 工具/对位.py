# -*- coding: utf-8 -*-
"""
对位闸（八造·2026-09-03 立）
─────────────────────────────────────────────────────────────
★立此器之由（作者令·2026-09-03）：「**我们所有的机制都得跑起来**……
  提示词一定要能够完美的让所有的机制都能够跑起来。」
★★而「跑起来」不是「码在仓库里」。一个器要算跑起来，须答得出三样：
  ①**谁调它**（有一条路从入口够得着它）；
  ②**它在哪一轮出声**（出声之时，文还改不改得动）；
  ③**它红得起来吗**（有没有一条负测，拿真犯过此项之原物回灌须报红）。
★★★三样缺一，它就不是机制，是摆设。

★立此器之实证（2026-09-03 逐条上磁盘核过，非设想）：
  ·**五钩（钩／新问／情绪波／危机升档／承诺推进）——本书唯一一件量「读者翻不翻页」的器**：
    其函数 `pageturn` 全仓只有一个调用点（小说检察官.py:4511），在 `ai_homework` 之内，
    而 `ai_homework` 只在 `--封版` 之下——**十三轮无一轮调得着它**。
    ★★更狠一层：`--封版 293` 实跑，其「收尾三段」印的是
    「★★★而其数：第一百零四天｜十层一样长…」——**那是封版之後贴在文件尾巴上的台账，
    不是小说的结尾**（293 真末句在第373行「而那一排点，明天还是六个。」）。
    **一件量结尾之钩的器，读的是台账。**
  ·**大问表**：其律自印「只报不拦」；以294计逾四十章者七样——
    血图缺234章、悬赏缺223章、地窖缺222章、寨里那些人缺186章、爷爷缺184章、
    走路的理由缺116章、听针缺92章。**二百三十四章之内没有一道闸因此拦过一次。**
  ·**负测覆盖**：全测 59 检项，其中 20 项（34%）无一条负测证明它红得起来——
    而令§一⑤★★★★已写「一项要进『所守』这一行，须其负测里有一条…」两造之久。
─────────────────────────────────────────────────────────────
用法：python3 工具/对位.py         逐器印其位
      python3 工具/对位.py --负测   只印负测覆盖
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, re, sys, io

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(ROOT, '工具')

# ── 入口：人自己会去跑的那几条命令（令§〇＋封版之序） ──
入口 = {
    '起草闸.py': '每章·起草前後（2026-09-06 立·作者令「把踩过的坑做成机制」）',
    '一坐.py': '每坐·起手',
    '全测.py': '每推之前',
    '跑轮.py': '每轮·存版',
    '预检.py': '每一刀之前',
    '可逆.py': '不可逆之事之前',
    '第零轮开镜庭.py': '开章·立卡',
    '自走.py': '每时·自走 Routine 唯一之令（2026-09-24 补入：自进化环／尺之校／未上库哨皆由它调）',
    '席/收尾.js': '收尾席之 Workflow（2026-09-24 补入）',
    '十轮精进.py': '（旧制之驱动·今由跑轮.py代）',
}

# ── 剧情之器：量「前后的剧情精彩程度」者，逐件declare其开关与其位 ──
#    （器名, 其所量, 其函数/其律之凭据, 其开关, 应在之位）
剧情之器 = [
    ('五钩',   '钩／新问／情绪波／危机升档／承诺推进', ('小说检察官.py', "args[0] == '--五钩'"), '--五钩（第7轮）', '第7轮·节奏（文还改得动之时）'),
    ('五钩·所读', '其「收尾三段」须是小说的结尾，不是封版台账', ('小说检察官.py', 'def _story_only'), '--五钩（第7轮）', '第7轮'),
    ('伏笔账本', '到期伏笔之接／展期／废',            ('小说检察官.py', 'def foreshadow_report'), '--五钩（第7轮）', '第7轮·时序'),
    ('大问表',  '读者挂着的旧问，末见第几章',          ('大问表.py', '逾上限'), '一坐.py', '每坐·起手'),
    ('FS闸',   '逾期伏笔本章回话了没有',             ('FS闸.py', ''), '全测.py', '每推之前'),
]


def _src(name):
    p = os.path.join(T, name)
    if not os.path.exists(p):
        return ''
    return io.open(p, encoding='utf-8').read()


LING = os.path.join(ROOT, '设定', '09_跑轮令_精简版.md')


def _ling():
    return io.open(LING, encoding='utf-8').read() if os.path.exists(LING) else ''


def _tools():
    out = []
    for f in sorted(os.listdir(T)):
        if not f.endswith('.py'):
            continue
        if f.startswith('负测_'):
            continue
        out.append(f)
    # ★0924 补：席之 Workflow（js）亦是调器之路——旧式只扫 .py，存底包等由席调者遂判孤器
    _x = os.path.join(T, '席')
    if os.path.isdir(_x):
        out += ['席/' + f for f in sorted(os.listdir(_x)) if f.endswith('.js')]
    return out


def _callers(name, tools):
    """谁调它：全仓（除它自己）出现 `工具/<name>` 者。"""
    key = '工具/' + name
    cs = []
    for t in tools:
        if t == name:
            continue
        _s = _src(t)
        # ★0924 补：自走.py 以 importlib 按档名载器（`'未上库哨.py'`），不书 `工具/` 之前缀——旧式遂看不见
        if key in _s or ("'%s'" % name) in _s:
            cs.append(t)
    return cs


def _reach(name, tools, seen=None):
    """自入口够不够得着它（逐层上溯，遇入口即止）。返回够得着它的那几个入口。"""
    if seen is None:
        seen = set()
    if name in seen:
        return set()
    seen.add(name)
    got = set()
    if name in 入口:
        got.add(name)
    for c in _callers(name, tools):
        got |= _reach(c, tools, seen)
    return got


def 负测覆盖():
    src = _src('全测.py')
    parts = re.split(r'^def (chk_\w+)', src, flags=re.M)
    funcs = {}
    for i in range(1, len(parts), 2):
        funcs[parts[i]] = parts[i + 1]
    withneg, bare = [], []
    for n, b in funcs.items():
        (withneg if re.search(r'负测_\w+\.py', b) else bare).append(n)
    return funcs, withneg, sorted(bare)


def main():
    只负测 = '--负测' in sys.argv
    tools = _tools()
    red = 0

    if not 只负测:
        print('════ 对位闸 ════')
        print('  【其律】一个器要算「跑起来」，须答得出三样：谁调它｜它在哪一轮出声｜它红得起来吗。')
        print()
        print('  ── 一·孤器（有器而无一条路够得着）──')
        ling = _ling()
        孤, 哑 = [], []
        for f in tools:
            if f.endswith('.js') and f not in 入口:   # js 只作调器之路，不作被查之器
                continue
            if f in 入口:
                continue
            got = _reach(f, tools)
            活 = {g for g in got if not 入口[g].startswith('（')}
            if 活:
                continue
            # 令里点名其命令者，其位即「令·人手跑」——令每坐原样重发，故它跑得着
            if ('工具/' + f) in ling:
                continue
            # 令里只提其事而不给命令者：有其事而无其命令，人一忙就漏
            名 = f[:-3]
            if 名 in ling or 名.replace('看官', '看官') in ling:
                哑.append((f, sorted(got)))
            else:
                孤.append((f, sorted(got)))
        for f, got in 哑:
            旧 = '｜只旧制入口：' + '、'.join(got) if got else ''
            print(f'   ⚠ {f}：**令里有其事而无其命令**{旧}——人一忙就漏，且漏了无声。')
        for f, got in 孤:
            旧 = '｜只旧制入口：' + '、'.join(got) if got else ''
            print(f'   ⛔ {f}{旧}')
        if 孤:
            print(f'   ⛔ 孤器 {len(孤)} 件——**码在仓库里，今日之路上一步也走不到。**')
            red += len(孤)
        if 哑:
            red += len(哑)
        if not 孤 and not 哑:
            print('   ✓ 无孤器、无哑器。')

        print()
        print('  ── 二·剧情之器（量「前后的剧情精彩程度」者）──')
        for 名, 所量, (器, 凭), 开关, 应位 in 剧情之器:
            s = _src(器)
            在 = (凭 in s) if 凭 else bool(s)
            if not 在:
                print(f'   ⛔ {名}：其凭据「{凭}」在 {器} 里找不着——**此表已陈，当日正之。**')
                red += 1
                continue
            # 其位：这个开关，是不是十三轮跑得着的
            晚 = 开关 in ('--封版',)
            # ★问的是它的**主口**拦不拦得动，不是它的档头里有没有「只报不拦」四个字
            #   （本闸头一版即栽在此：八造已把主口改成 sys.exit(1 if …)，
            #    而档头里那句「旧律『只报不拦』已废」还在，於是闸照旧报它只报不拦。）
            拦 = ('sys.exit(1 if' in s) if 器 == '大问表.py' else True
            mark = '⚠' if (晚 or not 拦) else '✓'
            why = []
            if 晚:
                why.append('**只在封版之下出声——出声之时，文已定**')
            if not 拦:
                why.append('**只报不拦**')
            print(f'   {mark} {名}（{所量}）')
            print(f'      其位：{开关}　｜应在：{应位}' + ('　← ' + '；'.join(why) if why else ''))
            if why:
                red += 1

    print()
    print('  ── 三·负测覆盖（令§一⑤★★★★：一项要进「所守」，须其负测里有一条回灌须报红）──')
    funcs, withneg, bare = 负测覆盖()
    print(f'   全测检项 {len(funcs)}｜有负测撑者 {len(withneg)}｜**赤手无负测者 {len(bare)}（{len(bare)*100//max(1,len(funcs))}%）**')
    if bare:
        print('   ⚠ 以下诸项之绿，本令之下一律记「未验」，不许记「已过」「全绿」：')
        for i in range(0, len(bare), 4):
            print('      ' + '　'.join(bare[i:i + 4]))
    print()
    if red:
        print(f'  ⛔ 对位闸：{red} 处未对位。')
        return 1
    print('  ✓ 对位闸：诸器各有其位。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
