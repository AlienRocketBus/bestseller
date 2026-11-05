# -*- coding: utf-8 -*-
"""负测 · 核轮（2026-09-24 立·令§一⑤）

⛔**其所以非有此测不可**：`核轮::judge` 被治过一回（**第102批**），
  **而那一回治的正是「其义反了」**——旧式作 `not is_last`，
  **遂令末章一到十轮满即判未竟，在十三轮制下每章必红三轮**。
★**一个被治反过一回的判，最该有一份负测钉着它**：⛔**不然下一坐再把它反回去，盘上照旧全绿。**
★★**本测所钉者四样**：**封版之判**｜**十轮满之判（末章放、非末章拦）**｜
  **未起轮不拦**｜**在跑之章（非末章而轮未满）须拦**。
⛔本负测一律造局（自造之状），⛔**不读真盘一个字去下判**；末二格方点一回真盘作注。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, io, re
import importlib.util as _u

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _器():
    s = _u.spec_from_file_location('核轮', os.path.join(ROOT, '工具', '核轮.py'))
    m = _u.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def _状(轮, 十一轮=False, 回执=False):
    return {'章': 0, '轮': list(轮), '十一轮': 十一轮, '回执': 回执,
            '开镜卡': True, '净重': 2800}


def 跑():
    m = _器()
    R = []
    J = m.judge

    # ① 封版者过（十一轮＋回执二样俱在）
    st, ok = J(_状(range(1, 14), True, True), False)
    R.append(('①封版者（十一轮✓回执✓）过，且其状作「封版」', ok and '封版' in st))
    R.append(('①之二·十一轮在而回执不在者⛔不算封版',
              '封版' not in J(_状(range(1, 14), True, False), False)[0]))
    R.append(('①之三·回执在而十一轮不在者⛔不算封版',
              '封版' not in J(_状(range(1, 14), False, True), False)[0]))

    # ②⛔第102批那一治·**其义反了**：末章十轮满係正常在跑，⛔不该拦
    R.append(('②⛔末章十轮满不拦（**此即第102批所治·旧式 `not is_last` 其义反了**）',
              J(_状(range(1, 11)), True)[1] is True))
    R.append(('②之二·非末章十轮满须拦（⛔证②不是一路放行）',
              J(_状(range(1, 11)), False)[1] is False))
    # ②之三·⛔**真的旧式回灌**：把那一行照旧式（`not is_last`）重演一回，
    #   **同一份状（末章·十轮满）旧式当场拦，新式放**——**二者判得不一样，本格方不是陪跑**。
    def _旧judge(r, is_last):
        n = len(r['轮'])
        if r['十一轮'] and r['回执']:
            return '✓封版', True
        if n == 0:
            return '—未起轮', True
        if n >= 10:
            return '⚠十轮满·待十一轮', not is_last      # ⛔旧式在此
        if not is_last:
            return '⛔未竟（跑到一半停了）', False
        return '·在跑', True
    R.append(('②之三·⛔旧式回灌：`not is_last` 之下末章十轮满当场被拦，而新式放',
              _旧judge(_状(range(1, 11)), True)[1] is False
              and J(_状(range(1, 11)), True)[1] is True))
    R.append(('②之四·⛔而旧式反把「非末章十轮满」放了——**其义确係反的**',
              _旧judge(_状(range(1, 11)), False)[1] is True
              and J(_状(range(1, 11)), False)[1] is False))

    # ③未起轮者不拦（⛔一章还没开始，不是「跑到一半停了」）
    R.append(('③未起轮者不拦，其状作「未起轮」',
              J(_状([]), False)[1] is True and '未起轮' in J(_状([]), False)[0]))

    # ④非末章而轮未满十者，係「跑到一半停了」，须拦——⛔本器立法之由即此
    st4, ok4 = J(_状(range(1, 6)), False)
    R.append(('④非末章·第5轮而止，须拦（⛔本器立法之由：防跳去写下一章）',
              ok4 is False and '未竟' in st4))
    R.append(('④之二·末章·第5轮而止，不拦（★那是正在跑）',
              J(_状(range(1, 6)), True)[1] is True))

    # ⑤⛔轮之数由「有记之轮」数，⛔不由其末号推（缺号者不许当满）
    R.append(('⑤⛔缺号者不算满：轮记只有 1—9 与 13（共10笔）——**本器数的是笔数**',
              J(_状([1, 2, 3, 4, 5, 6, 7, 8, 9, 13]), False)[0].startswith('⚠十轮满')))
    R.append(('⑤之二·只有 1—9（9笔）者，非末章即判未竟',
              '未竟' in J(_状(range(1, 10)), False)[0]))

    # ⑥ 章号之解（汉数）
    R.append(('⑥章号自名解得出（第三百六十三章→363）',
              m.cn('正文/镇冢秘术_第三百六十三章_半分.md') == 363))
    R.append(('⑥之二·十位之解（第四十章→40）', m.cn('x_第四十章_y.md') == 40))
    R.append(('⑥之三·解不出者判 -1（⛔不许当作第0章混进来）', m.cn('README.md') == -1))

    # ⑦⛔码上那一治之痕须在（⛔下一坐把它反回去，此格当场红）
    src = io.open(os.path.join(ROOT, '工具', '核轮.py'), encoding='utf-8').read()
    R.append(('⑦⛔码上十轮满那一行作 `return ..., is_last`（⛔不是 `not is_last`）',
              re.search(r"return '⚠十轮满·待十一轮', is_last", src) is not None))
    # ⛔**本格连问错两回，两回都是「问得太宽」**：
    #   ★头一版 grep 整段，而那一段之注正记着「原作 `not is_last`」——**那一行是碑，该留**；
    #   ★★第二版褪去注再 grep，而行 79 那一句 `if not is_last:` **係另一支之正用**
    #     （非末章而轮未满十者判未竟）——**把它也一并禁掉，等於要本器连好的那一半也拆了**。
    #   ★★★**故只许问那一支**：**十轮满那一行之後，不许跟 `not is_last`。**
    #   ⛔**记因**：**一个负测问得太宽，逼出来的不是治，是把对的东西改掉。**
    支 = src.split("if n >= 10:")[1].split("return")[1].split("\n")[0]
    R.append(('⑦之二·⛔只禁十轮满那一支之 `not is_last`（★行79那一句係另一支之正用，该留）',
              'not is_last' not in 支 and 'is_last' in 支
              and any('if not is_last:' in l for l in src.split('\n'))))

    # ⑧真盘（⛔只作注）：无未竟之章
    R.append(('⑧真盘·核轮 --静 报「无未竟之章」（⛔此係今日之实，逐日会变，只作注）',
              m.run(sorted(m.F)[-10:], True) == 0))

    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    过 = sum(1 for _, o in R if o)
    print('  ── 负测·核轮 %d/%d %s ──' % (过, len(R), '全通' if 过 == len(R) else '⛔未过'))
    return 过 == len(R)


if __name__ == '__main__':
    sys.exit(0 if 跑() else 1)
