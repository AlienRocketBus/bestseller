# -*- coding: utf-8 -*-
"""负测 · 薄章之禁（2026-09-24 立·守 `设定/裁_0924_364与365之薄_换事不凑字.md` 之教）

⛔**其教（裁档「所以不取的三条路」）**：一章薄了，其治是换事，**不是**——
　①凑字；②⛔**事後补「短章豁免」**（闸让自己过）；③⛔**改认欠额／放宽界**（放宽闸）。
★凑字一路已有 `质量三闸.py`／`小说检察官.py` 守着；**②③两路只写在纸上，没有一道器问**——
　**而这两路恰是最省事的：一行施工表、一个常数，闸就绿了。**
★★故本测守②③，判得死：

　②**豁免须在落笔之前**：`分量闸.豁免之章()` 之中，凡不在 `旧集`（0924 立此测时盘上已有之 14 章，
　　皆 0924 之前所登，其由各在施工表，本测不追）者——
　　**其章之正文若已在盘上（git 里有其档之提交，或档已在而豁免尚未提交），
　　而那一行豁免之首次提交不早於正文之首次提交 → ⛔红：事後补豁免。**
　　⛔旧集只许缩（某章补厚销了豁免即自动出集），**不许往里添章以求绿**。
　③**界与额钉死**：`分量闸` 之 硬＝2500｜暗硬＝2300｜认欠上限＝1｜额破已裁 ⊆ {363, 365}——
　　⛔改任一个即红；**真要改，先在裁档里写明其由，再改本测之钉——两处同改，旁人一眼看得见。**

局（⛔每一局皆验其反面）：
　①沙盘：正文先、豁免後 → 红 ｜②沙盘：豁免先、正文後 → 不红（落笔之前之豁免是正路）
　③沙盘：正文在而豁免未提交 → 红 ｜④沙盘：旧集之章不追
　⑤真盘·②   ⑥真盘·③
"""
import io, os, re, sys, glob, subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
表 = '设定/01_镇冢秘术_逐章施工与伏笔回收表.md'
旧集 = {48, 49, 50, 63, 66, 67, 312, 317, 322, 327, 328, 341, 344, 350}
钉 = {'硬': 2500, '暗硬': 2300, '认欠上限': 1}
额破可 = {363, 365}


def _git(*a):
    try:
        return subprocess.run(['git'] + list(a), cwd=ROOT, capture_output=True,
                              text=True, timeout=120).stdout
    except Exception:
        return ''


def _正文档(n):
    try:
        import 器物点名 as _y      # ★1027：cn2i 自 一坐.py 移此
    except Exception:
        return None
    for f in glob.glob(os.path.join(ROOT, '正文', '*.md')):
        m = re.search(r'第([零一二三四五六七八九十百]+)章', os.path.basename(f))
        if m and _y.cn2i(m.group(1)) == n:
            return os.path.relpath(f, ROOT)
    return None


def _首提(args):
    out = _git('log', '--reverse', '--format=%ct', *args).split()
    return int(out[0]) if out else None


def 判(n, 正文时, 豁免时, 正文在):
    """回 None（不红）或红之语。正文时／豁免时：首次提交之时（None＝未提交）。"""
    if n in 旧集:
        return None
    if not 正文在 and 正文时 is None:
        return None                      # 未落笔：豁免在前，正路
    if 豁免时 is None:
        return '第%d章：正文已在而豁免未提交——事後补豁免' % n
    if 正文时 is not None and 豁免时 >= 正文时:
        return '第%d章：豁免首提於正文首提之後——事後补豁免' % n
    return None


def 真盘豁免():
    import 分量闸 as _fl
    红 = []
    for n in sorted(_fl.豁免之章()):
        if n in 旧集:
            continue
        f = _正文档(n)
        正文时 = _首提(['--', f]) if f else None
        豁免时 = _首提(['-G', r'第\s*%d\s*章短章豁免' % n, '--', 表])
        r = 判(n, 正文时, 豁免时, bool(f))
        if r:
            红.append(r)
    return 红


def 真盘钉():
    import 分量闸 as _fl
    红 = []
    for k, v in 钉.items():
        if getattr(_fl, k, None) != v:
            红.append('分量闸.%s＝%s，钉为 %s' % (k, getattr(_fl, k, None), v))
    多 = set(getattr(_fl, '额破已裁', set())) - 额破可
    if 多:
        红.append('分量闸.额破已裁 添了 %s（⛔只许 %s）' % (sorted(多), sorted(额破可)))
    return 红


def 跑():
    局 = []
    局.append(('①沙盘·正文先、豁免後 → 红', 判(999, 100, 200, True) is not None))
    局.append(('②沙盘·豁免先、正文後 → 不红（落笔之前是正路）', 判(999, 300, 200, True) is None))
    局.append(('②之二·豁免在而正文未写 → 不红', 判(999, None, 200, False) is None))
    局.append(('③沙盘·正文在而豁免未提交 → 红', 判(999, 100, None, True) is not None))
    局.append(('④沙盘·旧集之章不追', 判(341, 100, 200, True) is None))
    try:
        r2 = 真盘豁免()
        局.append(('⑤真盘·新豁免皆在落笔之前%s' % ('；⛔' + '｜'.join(r2) if r2 else ''), not r2))
    except Exception as e:
        局.append(('⑤真盘跑不成：%s' % e, False))
    try:
        r3 = 真盘钉()
        局.append(('⑥真盘·界与额钉死（硬2500／暗硬2300／认欠上限1／额破只363、365）%s'
                  % ('；⛔' + '｜'.join(r3) if r3 else ''), not r3))
    except Exception as e:
        局.append(('⑥真盘跑不成：%s' % e, False))

    红 = 0
    print('════ 负测 · 薄章之禁（%d 局）════' % len(局))
    for 名, 果 in 局:
        print('  %s %s' % ('✓' if 果 else '⛔', 名))
        if not 果:
            红 += 1
    print('  ── %d/%d ──' % (len(局) - 红, len(局)))
    return 红


if __name__ == '__main__':
    sys.exit(1 if 跑() else 0)
