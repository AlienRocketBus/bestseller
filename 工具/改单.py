# -*- coding: utf-8 -*-
"""改单——**一切皆可改；改的前提只一条：让这本书更好。每一改必立单、必备份、可追溯。**

【其立之由（2026-09-25·作者令，逐字之意）】
  「规矩是死的，人是活的。圣经的设定、小说中的剧情，一切皆可改——但改的前提只有一个：让小说质量更高。
   否则完全没有必要改。改了之後要有修改清单，每一次改都有备份，方便後续追溯和核查。
   设立一个机制，叫一切皆可改，并且这个机制必须要运行起来。」

【一把尺（总编辑定）】改之前只答一问：**改了之後，这本书哪里更好了？**——须说得出具体：
  消了哪一处崩／哪一拍更狠／哪条线更连／读者哪里更放不下。**答不出「更好在哪」者，不改。**
【三步】
  ①立单：`python3 工具/改单.py --立 "改什么" "改了更好在哪" <档1> <档2> …`
     → 发单号（如 G0925-01），**先把诸档之改前原文整份备份**到 `设定/改单备份/<单号>/`，并记入 `设定/修改清单.md`。
  ②改：照常改；提交说明里写「改单#<单号>」。
  ③结单：`python3 工具/改单.py --毕 <单号> "改完一句（改了几处·验过哪几道闸）"`
【其牙（全测·改单）】
  甲·自本器立日起，凡提交**改动已有之正文章**（非新添）或圣经／canon／人物状态册，而提交说明无「改单#」者 → **红**。
     ★例外唯一：新章封版之追记（圣经入册、状态册同步、施工表锁定行），提交说明标「封版#N」——那是添，不是改。
  乙·单立而七日未结 → 黄。
用法：--立 ｜ --毕 ｜ --查 ｜ --单（列清单）｜ --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, re, sys, json, time, shutil, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
账档 = os.path.join(ROOT, '设定', '改单账.json')
清单 = os.path.join(ROOT, '设定', '修改清单.md')
备份 = os.path.join(ROOT, '设定', '改单备份')
立日 = '2026-09-25 12:00'
管 = re.compile(r'^(正文/|设定/00_镇冢秘术_唯一总圣经\.md|设定/canon事实库\.json|设定/人物状态册\.json|设定/镇冢秘术_作者版设定圣经\.md|设定/人物百科卡)')


def 读():
    try:
        return json.load(open(账档, encoding='utf-8'))
    except Exception:
        return {'单': []}


def 写(d):
    t = 账档 + '.tmp'
    json.dump(d, open(t, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    os.replace(t, 账档)


def 立(何, 由, 档们):
    if len(由) < 10:
        print('⛔「改了更好在哪」须说具体（消了哪一处崩／哪一拍更狠／哪条线更连）——答不出，不改'); return None
    d = 读()
    日 = time.strftime('%m%d')
    n = 1 + sum(1 for x in d['单'] if x['号'].startswith('G' + 日))
    号 = 'G%s-%02d' % (日, n)
    目 = os.path.join(备份, 号)
    os.makedirs(目, exist_ok=True)
    存 = []
    for p in 档们:
        a = os.path.join(ROOT, p) if not os.path.isabs(p) else p
        if os.path.exists(a):
            dst = os.path.join(目, os.path.relpath(a, ROOT).replace('/', '__'))
            shutil.copy2(a, dst)
            存.append(os.path.relpath(a, ROOT))
    d['单'].append({'号': 号, '立': time.strftime('%Y-%m-%d %H:%M'), '何': 何, '更好在哪': 由, '档': 存, '状': '开'})
    写(d)
    with open(清单, 'a', encoding='utf-8') as f:
        if os.path.getsize(清单) == 0 if os.path.exists(清单) else True:
            pass
        f.write('\n## %s ｜ %s\n- **改什么**：%s\n- **改了更好在哪**：%s\n- **改前备份**：`设定/改单备份/%s/`（%s）\n- **状**：开\n'
                % (号, time.strftime('%Y-%m-%d %H:%M'), 何, 由, 号, '、'.join(存) or '无档'))
    print('✓改单已立：%s｜备份 %d 档於 设定/改单备份/%s/｜提交说明须写「改单#%s」' % (号, len(存), 号, 号))
    return 号


def 补登(号, 提交们):
    """事後补登：已立之单点名其所覆之提交（该提交当时未写单号）。⛔补登也须先 --立（有其由、有备份）。"""
    d = 读()
    for x in d['单']:
        if x['号'] == 号:
            x.setdefault('覆', []).extend(提交们)
            写(d)
            with open(清单, 'a', encoding='utf-8') as f:
                f.write('- **%s 补登**：覆提交 %s（当时未写单号，事後补登）\n' % (号, '、'.join(提交们)))
            print('✓%s 补登覆 %s' % (号, '、'.join(提交们))); return True
    print('⛔无此单：%s' % 号); return False


def 毕(号, 句):
    d = 读()
    for x in d['单']:
        if x['号'] == 号:
            x['状'] = '毕'; x['毕'] = time.strftime('%Y-%m-%d %H:%M'); x['结'] = 句
            写(d)
            with open(清单, 'a', encoding='utf-8') as f:
                f.write('- **%s 结单**（%s）：%s\n' % (号, x['毕'], 句))
            print('✓%s 结单' % 号); return True
    print('⛔无此单：%s' % 号); return False


def 查(印=True):
    坏, 黄 = [], []
    try:
        out = subprocess.run(['git', '-c', 'core.quotepath=off', 'log', '--since=' + 立日, '--diff-filter=M',
                              '--name-only', '--format=@@%h %s%n%b'], cwd=ROOT, capture_output=True, text=True).stdout
    except Exception:
        out = ''
    覆 = {c for x in 读()['单'] for c in x.get('覆', [])}   # 补登：事後立单、点名所覆之提交（须有其由，入修改清单）
    for 块 in out.split('@@')[1:]:
        行 = 块.strip().split('\n')
        头 = 行[0]; 文 = '\n'.join(行)
        档 = [l for l in 行[1:] if 管.match(l)]
        if 档 and any(头.startswith(c[:7]) for c in 覆):
            continue
        if 档 and '改单#' not in 文 and '封版#' not in 文:   # 新章封版之追记（圣经入册、状态册同步、锁定行）係添不係改，标「封版#N」
            坏.append('%s 改了 %s 而无改单' % (头[:40], '、'.join(档[:3])))
    for x in 读()['单']:
        if x['状'] == '开':
            t = time.mktime(time.strptime(x['立'], '%Y-%m-%d %H:%M'))
            if time.time() - t > 7 * 86400:
                黄.append('%s 立七日未结' % x['号'])
    if 印:
        for x in 坏:
            print('  ⛔ ' + x)
        for x in 黄:
            print('  ⚠ ' + x)
        if not 坏:
            print('  ✓ 改单：凡改必有单。')
    return not 坏, 坏


def 自测():
    import tempfile
    global 账档, 清单, 备份, ROOT
    旧 = (账档, 清单, 备份, ROOT)
    t = tempfile.mkdtemp(); ROOT = t
    os.makedirs(os.path.join(t, '设定')); os.makedirs(os.path.join(t, '正文'))
    账档 = os.path.join(t, '设定', 'z.json'); 清单 = os.path.join(t, '设定', 'q.md'); 备份 = os.path.join(t, '设定', 'b')
    open(os.path.join(t, '正文', 'a.md'), 'w', encoding='utf-8').write('改前原文')
    r = []
    r.append(('①说不出更好在哪不立', 立('x', '更好', ['正文/a.md']) is None))
    号 = 立('改一句', '消了第一章与九十三章之抵，读者不再疑', ['正文/a.md'])
    r.append(('②立单发号', bool(号)))
    r.append(('③改前原文整份备份', open(os.path.join(备份, 号, '正文__a.md'), encoding='utf-8').read() == '改前原文'))
    r.append(('④入修改清单', 号 in open(清单, encoding='utf-8').read()))
    r.append(('⑤结单', 毕(号, '改一处·过硬闸')))
    账档, 清单, 备份, ROOT = 旧
    for n, v in r:
        print(('  ✓ ' if v else '  ⛔ ') + n)
    print('负测·改单 %d/%d' % (sum(v for _, v in r), len(r)))
    return all(v for _, v in r)


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--自测' in a:
        sys.exit(0 if 自测() else 1)
    if '--查' in a:
        sys.exit(0 if 查()[0] else 1)
    if '--立' in a:
        i = a.index('--立'); sys.exit(0 if 立(a[i + 1], a[i + 2], a[i + 3:]) else 1)
    if '--补登' in a:
        i = a.index('--补登'); sys.exit(0 if 补登(a[i + 1], a[i + 2:]) else 1)
    if '--毕' in a:
        i = a.index('--毕'); sys.exit(0 if 毕(a[i + 1], a[i + 2]) else 1)
    for x in 读()['单']:
        print('%s ｜%s｜%s｜更好在哪：%s' % (x['号'], x['状'], x['何'], x['更好在哪'][:50]))
