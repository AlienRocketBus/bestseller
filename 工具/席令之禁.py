# -*- coding: utf-8 -*-
"""席令之禁 · 每一份席令里，有没有写着「席在跑时不许动整个工作区」（2026-09-24 立）

⛔**其所由来·0924·363 救章**：**一席误跑 `git checkout`，把正文退回 HEAD**，幸当场自 v20 复原并自报。
★**而其根不在那一席**：**律⑮（席在跑时不许 checkout／stash／reset／clean／add -A）只印在 `自走.py` 里**——
  **真正动手的那十二份席令，一次都没有禁 `git checkout`，`救章.js` 连一样都没禁。**
⛔**即：一条规矩，没有走到真正动手的那个地方**——与「读者之判没走到落笔之前」同一个形。

★**本器只问一件，判得死**：**`工具/席/*.js` 每一份，都带着那一段禁令，且五样命令一样不少。**
⛔**它判不了「那一席读没读、守没守」**——**後一件归 `全测::负测留字`（跑前跑後逐档比 sha256）去逮。**
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, io, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
标 = '律⑮·动盘之禁'
标20 = '律⑳·总编辑之权'
五样 = ('git checkout', 'git stash', 'git reset --hard', 'git clean', 'git add -A')


def 查(档们=None):
    """→ [(档, 缺什么)]。"""
    档们 = 档们 or sorted(glob.glob(os.path.join(ROOT, '工具', '席', '*.js')))
    坏 = []
    for f in 档们:
        t = io.open(f, encoding='utf-8', errors='replace').read()
        if 标 not in t:
            坏.append((os.path.basename(f), '无禁令之段'))
            continue
        段 = t[t.index(标):t.index(标) + 900].replace('\\`', '`')
        缺 = [x for x in 五样 if x not in 段]
        if 缺:
            坏.append((os.path.basename(f), '禁令缺：' + '、'.join(缺)))
        # ★0924 补：律⑳（总编辑之权：不许「交作者裁」而停）须逐份在——⛔此段一抽，席又会停下来等作者
        if 标20 not in t:
            坏.append((os.path.basename(f), '无律⑳·总编辑之权'))
    return 坏


def 报():
    档们 = sorted(glob.glob(os.path.join(ROOT, '工具', '席', '*.js')))
    坏 = 查(档们)
    if 坏:
        print('⛔ 席令之禁：%d 份席令不带「席在跑时不许动整个工作区」：%s'
              % (len(坏), '；'.join('%s（%s）' % x for x in 坏)))
        return False
    print('✓ 席令之禁：%d 份席令逐份带着禁令，五样命令一样不少' % len(档们))
    return True


def 自测():
    import tempfile, shutil
    R = []
    d = tempfile.mkdtemp(prefix='席令_')
    try:
        旧 = os.path.join(d, '旧.js')
        io.open(旧, 'w', encoding='utf-8').write('const 令 = `工作目录 /home/user/the-novel。动笔。`\n')
        R.append(('①⛔旧式回灌：0924 之前之席令（无禁令之段）当场红', bool(查([旧]))))
        缺 = os.path.join(d, '缺.js')
        io.open(缺, 'w', encoding='utf-8').write('`%s：\\`git stash\\`／\\`git reset --hard\\``\n' % 标)
        r = 查([缺])
        R.append(('②有禁令而缺 checkout 者红（⛔363 那一席跑的正是 checkout）',
                  bool(r) and 'git checkout' in r[0][1]))
        全 = os.path.join(d, '全.js')
        io.open(全, 'w', encoding='utf-8').write(
            '`%s：%s`\n%s\n' % (标, '／'.join('\\`%s\\`' % x for x in 五样), 标20))
        R.append(('③五样俱在者过（⛔证本器不是一律判否）', 查([全]) == []))
        无20 = os.path.join(d, '无20.js')
        io.open(无20, 'w', encoding='utf-8').write(
            '`%s：%s`\n' % (标, '／'.join('\\`%s\\`' % x for x in 五样)))
        R.append(('③之二·缺律⑳者红（⛔抽掉它，席又会停下来等作者）',
                  any('律⑳' in x[1] for x in 查([无20]))))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    R.append(('④真盘·诸份席令（当场 glob）逐份过', 查() == []))
    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    过 = sum(1 for _, o in R if o)
    print('  ── 席令之禁·自测 %d/%d %s ──' % (过, len(R), '全通' if 过 == len(R) else '⛔未过'))
    return 过 == len(R)


if __name__ == '__main__':
    if '--自测' in sys.argv:
        sys.exit(0 if 自测() else 1)
    sys.exit(0 if 报() else 1)
