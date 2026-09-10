#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
可逆册（2026-08-30 立·作者令「我给你授权，但要留下记录，随时可以复原」）

★其立之由：五造§〇之二原有一条例外——凡不可复原者不落刀，改走可逆之路。
★★而作者今日授权：不可复原之事亦可做，**其条件是它变成可复原的**。
★★★故此器之职只一样：**把「不可逆」改造成「可逆」**——落刀之前先把原物整份存下来，
   ★★★★存的是文件本身（不是 git 历史），故 force-push 改写历史之后它照旧在；
   ★而其存处在仓库之内，一并推上 GitHub，故「完好无损存在 GitHub」这一条由推送保证。

用法：
    python3 工具/可逆.py --存 "其由" 路径1 [路径2 ...]   # 落刀之前跑；印复原之法
    python3 工具/可逆.py --存枝 "其由"                    # force-push 之前跑；造备份枝并记两端之号
    python3 工具/可逆.py --复原 R0001                     # 复原，并逐件验 sha256
    python3 工具/可逆.py --册                             # 逐条列
    python3 工具/可逆.py --验                             # 验全库完好（供全测调用）
    python3 工具/可逆.py --自测                           # 负测（供全测调用）
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import sys, os, json, glob, shutil, hashlib, subprocess, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.join(ROOT, '版本', '_可逆库')
CE = os.path.join(ROOT, '设定', '可逆册.md')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 16), b''):
            h.update(b)
    return h.hexdigest()


def _now():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M')


def _git(*a):
    try:
        r = subprocess.run(['git'] + list(a), cwd=ROOT, capture_output=True,
                           text=True, timeout=60)
        return r.stdout.strip() if r.returncode == 0 else None
    except Exception:
        return None


def _next_id():
    os.makedirs(LIB, exist_ok=True)
    ns = []
    for d in glob.glob(os.path.join(LIB, 'R*')):
        b = os.path.basename(d)
        if len(b) >= 5 and b[1:5].isdigit():
            ns.append(int(b[1:5]))
    return 'R%04d' % ((max(ns) + 1) if ns else 1)


def _rel(p):
    # ★2026-08-30 治（负测头一跑即逮出）：先前以 cwd 解相对路径，
    #   ★★而本器之路径一律以仓库根为准——换个目录跑即全部解错，且错法是「路径不在」，
    #   ★★★那正是最坏的一种：它会在落刀之前拒绝存档，看着像在护你，实则是它自己算错了地方。
    p = p if os.path.isabs(p) else os.path.join(ROOT, p)
    return os.path.relpath(os.path.abspath(p), ROOT).replace(os.sep, '/')


def 存(由, 路径):
    """★落刀之前把原物整份存下来。★★存不下来即不许落刀（返非零）。"""
    路径 = [p for p in 路径 if p]
    if not 路径:
        print('⛔ 未指路径，无物可存。')
        return 2
    缺 = [p for p in 路径 if not os.path.exists(os.path.join(ROOT, _rel(p)))]
    if 缺:
        print('⛔ 这些路径不在：%s' % '、'.join(缺))
        print('   ★存不下来即不许落刀——先查路径，再落刀。')
        return 2
    rid = _next_id()
    d = os.path.join(LIB, '%s_%s' % (rid, datetime.datetime.now().strftime('%Y%m%d')))
    os.makedirs(d, exist_ok=False)
    件 = []
    for p in 路径:
        r = _rel(p)
        src = os.path.join(ROOT, r)
        dst = os.path.join(d, '原', r)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.isdir(src):
            shutil.copytree(src, dst)
            for f in sorted(glob.glob(os.path.join(dst, '**', '*'), recursive=True)):
                if os.path.isfile(f):
                    件.append({'路': _rel(os.path.join(src, os.path.relpath(f, dst))),
                               'sha256': sha(f), '字节': os.path.getsize(f)})
        else:
            shutil.copy2(src, dst)
            件.append({'路': r, 'sha256': sha(src), '字节': os.path.getsize(src)})
    单 = {'号': rid, '时': _now(), '类': '文件', '其由': 由,
          '所存': [_rel(p) for p in 路径], '件': 件,
          'HEAD': _git('rev-parse', 'HEAD'), '枝': _git('rev-parse', '--abbrev-ref', 'HEAD')}
    with open(os.path.join(d, '_单.json'), 'w', encoding='utf-8') as f:
        f.write(json.dumps(单, ensure_ascii=False, indent=1))
    _记册(单)
    print('███ 可逆册 · %s ███' % rid)
    print('  存：%d 件｜%s' % (len(件), '、'.join(单['所存'])[:100]))
    print('  由：%s' % 由)
    print('  库：版本/_可逆库/%s/' % os.path.basename(d))
    print('  ★复原之法：python3 工具/可逆.py --复原 %s' % rid)
    print('  ★★而此库须与本次落刀同一笔提交推上 GitHub，否则「随时可复原」不成立。')
    return 0


def 存枝(由):
    """★force-push 之前跑：造一条备份枝，并记两端之号。
    ★★其要害：force-push 改写的是枝之指针，而备份枝指着旧头，旧头之物遂不失。"""
    head = _git('rev-parse', 'HEAD')
    枝 = _git('rev-parse', '--abbrev-ref', 'HEAD')
    if not head or not 枝:
        print('⛔ 取不到 HEAD 或枝名，不许落刀。')
        return 2
    rid = _next_id()
    bak = 'backup/%s_%s' % (rid, datetime.datetime.now().strftime('%Y%m%d'))
    if _git('branch', bak, head) is None:
        print('⛔ 造备份枝失败，不许落刀。')
        return 2
    远 = _git('ls-remote', 'origin', 枝)
    远头 = 远.split()[0] if 远 else None
    d = os.path.join(LIB, '%s_%s' % (rid, datetime.datetime.now().strftime('%Y%m%d')))
    os.makedirs(d, exist_ok=True)
    单 = {'号': rid, '时': _now(), '类': '枝', '其由': 由, '所存': [],
          '件': [], '枝': 枝, 'HEAD': head, '远端之头': 远头, '备份枝': bak}
    with open(os.path.join(d, '_单.json'), 'w', encoding='utf-8') as f:
        f.write(json.dumps(单, ensure_ascii=False, indent=1))
    _记册(单)
    print('███ 可逆册 · %s（枝）███' % rid)
    print('  枝：%s｜本地之头 %s｜远端之头 %s' % (枝, head[:12], (远头 or '无')[:12]))
    print('  备份枝：%s（已造，须一并推上 GitHub）' % bak)
    print('  ★复原之法：git push --force-with-lease origin %s:%s' % (bak, 枝))
    print('  ★★而备份枝须先推：git push -u origin %s' % bak)
    return 0


def _记册(单):
    新 = not os.path.exists(CE)
    with open(CE, 'a', encoding='utf-8') as f:
        if 新:
            f.write('# 可逆册（2026-08-30 立·作者令「我给你授权，但要留下记录，随时可以复原」）\n\n'
                    '> ★此册只记一样：**凡不可逆之事，落刀之前存了什么、怎么复原。**\n'
                    '> ★★而其存处为 `版本/_可逆库/`，存的是文件本身（非 git 历史），'
                    '故 force-push 改写历史之后它照旧在。\n'
                    '> ★★★`python3 工具/可逆.py --验` 逐件核 sha256；此验已接进全测，'
                    '**库一旦损，推送即拦**。\n\n'
                    '| 号 | 时 | 类 | 其由 | 所存 | 复原之法 |\n|---|---|---|---|---|---|\n')
        if 单['类'] == '枝':
            法 = '`git push --force-with-lease origin %s:%s`' % (单['备份枝'], 单['枝'])
            物 = '枝 %s @ %s' % (单['枝'], (单['HEAD'] or '')[:12])
        else:
            法 = '`python3 工具/可逆.py --复原 %s`' % 单['号']
            物 = '%d 件：%s' % (len(单['件']), '、'.join(单['所存'])[:60])
        f.write('| **%s** | %s | %s | %s | %s | %s |\n'
                % (单['号'], 单['时'], 单['类'], 单['其由'].replace('|', '／')[:80], 物, 法))


def _单之路(rid):
    for d in glob.glob(os.path.join(LIB, '%s_*' % rid)):
        p = os.path.join(d, '_单.json')
        if os.path.exists(p):
            return d, json.load(open(p, encoding='utf-8'))
    return None, None


def 复原(rid):
    d, 单 = _单之路(rid)
    if not 单:
        print('⛔ 册上无此号：%s' % rid)
        return 2
    if 单['类'] == '枝':
        print('★此笔为枝之备份，复原不由本器办，由 git 办：')
        print('   git push --force-with-lease origin %s:%s' % (单['备份枝'], 单['枝']))
        return 0
    坏 = []
    for x in 单['件']:
        src = os.path.join(d, '原', x['路'])
        if not os.path.exists(src):
            坏.append('%s（库中缺）' % x['路'])
        elif sha(src) != x['sha256']:
            坏.append('%s（库中已损）' % x['路'])
    if 坏:
        print('⛔ 库不完好，不许复原：%s' % '；'.join(坏[:5]))
        return 2
    for x in 单['件']:
        dst = os.path.join(ROOT, x['路'])
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(os.path.join(d, '原', x['路']), dst)
    错 = [x['路'] for x in 单['件'] if sha(os.path.join(ROOT, x['路'])) != x['sha256']]
    if 错:
        print('⛔ 复原之后 sha256 仍不符：%s' % '、'.join(错))
        return 2
    print('✓ 已复原 %s：%d 件，逐件 sha256 相符。' % (rid, len(单['件'])))
    for x in 单['件']:
        print('   · %s' % x['路'])
    print('  ★其由（当初落刀之由）：%s' % 单['其由'])
    return 0


def 册():
    单们 = _全单()
    if not 单们:
        print('★可逆册空：尚无一笔不可逆之事。')
        return 0
    print('███ 可逆册 · %d 笔 ███' % len(单们))
    for 单 in 单们:
        print('  %s｜%s｜%s｜%s' % (单['号'], 单['时'], 单['类'], 单['其由'][:56]))
    return 0


def _全单():
    out = []
    for d in sorted(glob.glob(os.path.join(LIB, 'R*'))):
        p = os.path.join(d, '_单.json')
        if os.path.exists(p):
            try:
                out.append(json.load(open(p, encoding='utf-8')))
            except Exception:
                out.append({'号': os.path.basename(d)[:5], '时': '?', '类': '⛔单坏',
                            '其由': '_单.json 读不出', '件': [], '所存': []})
    return out


def _未入库者(路径们):
    """★2026-08-30 补·作者令「所有的内容一定都要完好无损地存在 GitHub」：
    ★★sha256 只证库没烂，不证库上了 GitHub——一个没被 git 认下的库，
    ★★★下一个容器一起来就没了，而那时 sha256 照样报「完好」。
    ★★★★故加此一格：逐件问 git 认不认。返回未入库者之列。"""
    未 = []
    for r in 路径们:
        if _git('ls-files', '--error-unmatch', '--', r) is None:
            未.append(r)
    return 未


def 验(quiet=False):
    """★逐件核 sha256（库没烂）＋逐件核 git 认不认（库存得住）。
    ★★二者缺一，「随时可复原」即是空话。★★★此验接进全测。"""
    单们 = _全单()
    坏 = []
    件数 = 0
    库件 = []
    for 单 in 单们:
        if 单['类'] == '⛔单坏':
            坏.append('%s：单读不出' % 单['号'])
            continue
        if 单['类'] == '枝':
            if not _git('rev-parse', '--verify', 单.get('备份枝', '')):
                坏.append('%s：备份枝 %s 不在' % (单['号'], 单.get('备份枝')))
            continue
        d, _ = _单之路(单['号'])
        for x in 单['件']:
            件数 += 1
            src = os.path.join(d, '原', x['路'])
            if not os.path.exists(src):
                坏.append('%s：%s 库中缺' % (单['号'], x['路']))
            elif sha(src) != x['sha256']:
                坏.append('%s：%s 库中已损' % (单['号'], x['路']))
            else:
                库件.append(_rel(src))
        库件.append(_rel(os.path.join(d, '_单.json')))
    未 = _未入库者(库件)
    for r in 未:
        坏.append('未入 git：%s（★而未入 git 者，换个容器就没了）' % r)
    远 = _git('rev-parse', 'HEAD')
    未推 = None
    if 远 and not 未:
        枝 = _git('rev-parse', '--abbrev-ref', 'HEAD') or ''
        r = _git('ls-remote', 'origin', 枝)
        远头 = r.split()[0] if r else None
        if 远头 and 远头 != 远:
            未推 = '本地 %s ≠ 远端 %s' % (远[:12], 远头[:12])
    if quiet:
        print('可逆库完好' if not 坏 else '；'.join(坏[:3]))
        if not 坏 and 未推:
            print('  ⚠库已入 git 而尚未推：%s（推上去才算存在 GitHub）' % 未推)
    else:
        print('███ 可逆库之验 ███')
        print('  %d 笔｜%d 件｜入 git %d 件' % (len(单们), 件数, len(库件) - len(未)))
        if 未推:
            print('  ⚠尚未推：%s——★入了 git 只是存得住，推上去才算存在 GitHub。' % 未推)
        if 坏:
            for x in 坏:
                print('  ⛔ %s' % x)
            print('  ⛔ 库不完好——「随时可复原」不成立，推送须拦。')
        else:
            print('  ✓ 逐件 sha256 相符，且逐件皆已入 git——库完好且存得住。')
    return 0 if not 坏 else 2


if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    if '--自测' in sys.argv:
        sys.exit(subprocess.call([sys.executable, os.path.join(ROOT, '工具', '负测_可逆册.py')]))
    if '--存' in sys.argv:
        sys.exit(存(a[0] if a else '', a[1:]))
    if '--存枝' in sys.argv:
        sys.exit(存枝(a[0] if a else ''))
    if '--复原' in sys.argv:
        sys.exit(复原(a[0] if a else ''))
    if '--册' in sys.argv:
        sys.exit(册())
    if '--验' in sys.argv:
        sys.exit(验('--静' in sys.argv))
    print(__doc__)
    sys.exit(0)
