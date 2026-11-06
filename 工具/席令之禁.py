# -*- coding: utf-8 -*-
"""席令之禁 · 每一份席令里，有没有写着「席在跑时不许动整个工作区」（2026-09-24 立）

⛔**其所由来·0924·363 救章**：**一席误跑 `git checkout`，把正文退回 HEAD**，幸当场自 v20 复原并自报。
★**而其根不在那一席**：**律⑮（席在跑时不许 checkout／stash／reset／clean／add -A）只印在 `自走.py` 里**——
  **真正动手的那十二份席令，一次都没有禁 `git checkout`，`救章.js` 连一样都没禁。**
⛔**即：一条规矩，没有走到真正动手的那个地方**——与「读者之判没走到落笔之前」同一个形。

★**本器只问一件，判得死**：**`工具/席/*.js` 每一份，都带着那一段禁令，且七样命令一样不少。**
⛔**它判不了「那一席读没读、守没守」**——**後一件归 `全测::负测留字`（跑前跑後逐档比 sha256）去逮。**
★1027 执行之核（#84）：禁样添 `git commit`、`git push`（总章 §五「席⛔ git 写」）——旧只五样，剧情庭.js、大审.js 之禁文无此二样而照绿。
★1027 执行之核（#33）：每份之共令首段须带「五大主义」五行（虫洞、虹吸、完美、丝滑、执行·作者令「每次必读必须要明白这五大主义」）；
  造章.js 只 N≥411 带之（N≤410 一字不变·负测_造章令 之 sha 钉），本器只验其段在档。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, io, glob, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
标 = '律⑮·动盘之禁'
标20 = '律⑳·总编辑之权'
五样 = ('git checkout', 'git stash', 'git reset --hard', 'git clean', 'git add -A', 'git commit', 'git push')   # 1027 #84：添 commit、push（名仍「五样」·⛔改其引）
标五大 = '【六大主义'   # 1106：进化主义入（六大主义·六行）
五主 = ('虫洞', '虹吸', '完美', '丝滑', '执行', '进化')
旧笔 = 'db52f247'          # 1027 #84 #33 之前之树：剧情庭.js、大审.js 之禁文缺 commit／push、三份俱无五大主义——回灌须红


def 查(档们=None):
    """→ [(档, 缺什么)]。"""
    档们 = 档们 or sorted(glob.glob(os.path.join(ROOT, '工具', '席', '*.js')))
    坏 = []
    for f in 档们:
        t = io.open(f, encoding='utf-8', errors='replace').read()
        坏 += [(os.path.basename(f), x) for x in 查文(t)]
    return 坏


def 查文(t):
    """一份席令之文 → [缺什么]。"""
    坏 = []
    if 标 not in t:
        坏.append('无禁令之段')
    else:
        段 = t[t.index(标):t.index(标) + 900].replace('\\`', '`')
        缺 = [x for x in 五样 if x not in 段]
        if 缺:
            坏.append('禁令缺：' + '、'.join(缺))
    # ★0924 补：律⑳（总编辑之权：不许「交作者裁」而停）须逐份在——⛔此段一抽，席又会停下来等作者
    if 标20 not in t:
        坏.append('无律⑳·总编辑之权')
    # ★1027 #33：五大主义之段（五行·五名俱在）
    if 标五大 not in t:
        坏.append('无六大主义之段')
    else:
        段五 = t[t.index(标五大):t.index(标五大) + 520]
        缺五 = [x for x in 五主 if x not in 段五]
        if 缺五 or len(re.findall(r'(?m)^[1-6]\.\s*\S', 段五)) < 6:
            坏.append('六大主义之段不全：' + ('缺' + '、'.join(缺五) if 缺五 else '不足六行'))
        # ★1106 作者令「每次开写也要读到、严格执行」：段首一行须带唯一之的之文与自决（律⑳）——三纲同在缓存之首
        首行 = 段五.split('\n', 1)[0]
        if '中国第一' not in 首行 or '自决' not in 首行:
            坏.append('六大主义之首行缺唯一之的或自决（三纲：唯一之的→自决→六大主义）')
    # ★1027 #84（复核补）：席令⛔令席提交——禁文写「⛔ git commit」而令文又令「git add 并 commit（末两行：Co-Authored-By…）」，
    #   席照令文即 git 写（剧情庭.js 式新、式改、式验之裁旧如此）。提交之尾、「并 commit」在席令即红；「⛔不提交（主环提交）」放。
    if re.search(r'Co-Authored-By|Claude-Session:|并\s*commit', t):
        坏.append('令席提交（席令里有提交之尾或「并 commit」之令——席⛔ git 写：提交归主环）')
    return 坏


def 报():
    档们 = sorted(glob.glob(os.path.join(ROOT, '工具', '席', '*.js')))
    坏 = 查(档们)
    if 坏:
        print('⛔ 席令之禁：%d 处不合：%s' % (len(坏), '；'.join('%s（%s）' % x for x in 坏)))
        return False
    print('✓ 席令之禁：%d 份席令逐份带着禁令（七样命令一样不少）、律⑳、六大主义之段' % len(档们))
    return True


def 自测():
    import tempfile, shutil
    R = []
    d = tempfile.mkdtemp(prefix='席令_')
    五大段 = '%s·仅次於唯一之的「镇冢秘术成中国第一」·遇事自决】\n%s\n' % (标五大, '\n'.join('%d. %s：某' % (i + 1, x) for i, x in enumerate(五主)))
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
            '%s`%s：%s`\n%s\n' % (五大段, 标, '／'.join('\\`%s\\`' % x for x in 五样), 标20))
        R.append(('③七样、律⑳、五大主义俱在者过（⛔证本器不是一律判否·放行之反例）', 查([全]) == []))
        无20 = os.path.join(d, '无20.js')
        io.open(无20, 'w', encoding='utf-8').write(
            '%s`%s：%s`\n' % (五大段, 标, '／'.join('\\`%s\\`' % x for x in 五样)))
        R.append(('③之二·缺律⑳者红（⛔抽掉它，席又会停下来等作者）',
                  any('律⑳' in x[1] for x in 查([无20]))))
        五 = os.path.join(d, '五.js')        # 1027 #84：旧之五样（无 commit／push）
        io.open(五, 'w', encoding='utf-8').write(
            '%s`%s：%s`\n%s\n' % (五大段, 标, '／'.join('\\`%s\\`' % x for x in 五样[:5]), 标20))
        r五 = 查([五])
        R.append(('⑤之一·禁文只旧五样（缺 git commit、git push）者红（1027 #84：席⛔ git 写）',
                  len(r五) == 1 and 'git commit' in r五[0][1] and 'git push' in r五[0][1]))
        无五 = os.path.join(d, '无五.js')     # 1027 #33：无五大主义之段
        io.open(无五, 'w', encoding='utf-8').write('`%s：%s`\n%s\n' % (标, '／'.join('\\`%s\\`' % x for x in 五样), 标20))
        四 = os.path.join(d, '四.js')         # 五大主义之段缺一名（丝滑）
        io.open(四, 'w', encoding='utf-8').write(五大段.replace('丝滑', '某某') + '`%s：%s`\n%s\n' % (标, '／'.join('\\`%s\\`' % x for x in 五样), 标20))
        R.append(('⑤之二·无五大主义之段者红；段缺一名（丝滑）者红（1027 #33）',
                  any('无六大主义' in x[1] for x in 查([无五])) and any('缺丝滑' in x[1] for x in 查([四]))))
        旧首 = os.path.join(d, '旧首.js')     # 1106 前之首行（只「仅次於唯一之的」、无其文、无自决）
        io.open(旧首, 'w', encoding='utf-8').write(五大段.replace('「镇冢秘术成中国第一」·遇事自决', '') + '`%s：%s`\n%s\n' % (标, '／'.join('\\`%s\\`' % x for x in 五样), 标20))
        R.append(('⑤之三·六大主义之首行缺唯一之的之文或自决者红（1106 作者令「每次开写也要读到、严格执行」）',
                  any('首行缺唯一之的' in x[1] for x in 查([旧首]))))
        令提 = os.path.join(d, '令提.js')     # 1027 #84 复核补：禁文俱在而令文又令席提交
        io.open(令提, 'w', encoding='utf-8').write(io.open(全, encoding='utf-8').read()
                                                + '把该档 git add（明路径）并 commit（末两行：\nCo-Authored-By: x\nClaude-Session: y），⛔不推。\n')
        主提 = os.path.join(d, '主提.js')     # 放行之反例：⛔不提交（主环提交）
        io.open(主提, 'w', encoding='utf-8').write(io.open(全, encoding='utf-8').read() + '⛔不提交、⛔git add（主环提交）。\n')
        R.append(('⑦令席提交者红（禁文俱在而令文令「git add 并 commit（末两行：Co-Authored-By…）」）；「⛔不提交（主环提交）」放',
                  any('令席提交' in x[1] for x in 查([令提])) and 查([主提]) == []))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    # ⑥回灌旧树（1027 #84 #33 之前·db52f247）：剧情庭.js、大审.js 缺 commit／push；三份俱无五大主义——须红（⛔空验）
    旧红 = {}
    for 名 in ('剧情庭.js', '大审.js', '造章.js'):
        r = subprocess.run(['git', 'show', '%s:工具/席/%s' % (旧笔, 名)], cwd=ROOT, capture_output=True, text=True)
        if r.returncode == 0:
            旧红[名] = 查文(r.stdout)
    if 旧红:
        R.append(('⑥回灌 %s（改前之树）：剧情庭、大审之禁文缺 git commit／push、三份俱无五大主义 → 俱红' % 旧笔,
                  all(any('git commit' in x for x in 旧红[k]) for k in ('剧情庭.js', '大审.js') if k in 旧红)
                  and all(any('无六大主义' in x for x in v) for v in 旧红.values())
                  and not any('git commit' in x for x in 旧红.get('造章.js', []))))
        R.append(('⑥之二 回灌 %s：剧情庭.js 令裁席 git add 并 commit → 红；大审.js、造章.js 无此令 → ⛔红（放行）' % 旧笔,
                  any('令席提交' in x for x in 旧红.get('剧情庭.js', []))
                  and not any('令席提交' in x for k in ('大审.js', '造章.js') for x in 旧红.get(k, []))))
    else:
        print('  · ⑥ 改前之树 %s 不在（浅克隆）——回灌以 ⑤ 之坏例代' % 旧笔)
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
