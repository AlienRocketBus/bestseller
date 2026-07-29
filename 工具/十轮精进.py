#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
十轮精进机制（批102立法／批103并入检察官）

**本文件是库，不是命令面。**
作者只说两句话：「续」→ 检察官 --开拍；「挑刺」→ 检察官 --验收（自动带存版＋棘轮闸＋满十轮横评）。
下列 CLI 仅供机器自检与负测，日常不用：
    python3 工具/十轮精进.py --存版 94 "第三轮·四堂会审"
    python3 工具/十轮精进.py --横评 94

立法要点：并行十版会丢弃已修好的真伤，故改为串行累积；
但每轮必存版打分，任何硬项劣于历史最优即棘轮闸拦停，末轮十版横评择优。
"""
import os
import re
import sys
import json
import glob
import datetime
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JJ_DIR = os.path.join(ROOT, '版本')
CN = {'零': 0, '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4,
      '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}


def chap_num(path):
    m = re.search(r'第([零〇一二三四五六七八九十百]+)章', os.path.basename(path))
    if not m:
        return -1
    s = m.group(1)
    total, num = 0, 0
    for ch in s:
        if ch in CN:
            num = CN[ch]
        elif ch == '十':
            total += (num or 1) * 10
            num = 0
        elif ch == '百':
            total += (num or 1) * 100
            num = 0
    return total + num


def find_chapter(n):
    for f in sorted(glob.glob(os.path.join(ROOT, '正文', '*.md'))):
        if chap_num(f) == n:
            return f
    return None


def paths(n):
    d = os.path.join(JJ_DIR, '第%d章' % n)
    return d, os.path.join(d, '_台账.json')


def body_of(txt):
    prose = txt.split('【本章亮点】')[0]
    return re.sub(r'^.*?第.+?章[^\n]*\n', '', prose, count=1, flags=re.S)


def score(txt):
    """机器可测之十七项。硬项须为0；量项供横评比对。"""
    body = body_of(txt)
    hl = txt[txt.find('【本章亮点】'):] if '【本章亮点】' in txt else ''
    sents = re.split(r'(?<=[。！？…])', txt)
    paras = [re.sub(r'\s', '', x) for x in body.split('\n') if x.strip()]
    lens = [len(x) for x in paras] or [0]

    def cnt(pat, s=body):
        return len(re.findall(pat, s))

    seen = {}
    for i in range(len(body) - 3):
        k = body[i:i + 4]
        if re.match(r'^[\u4e00-\u9fa5]{4}$', k):
            seen[k] = seen.get(k, 0) + 1
    rep3 = sum(1 for v in seen.values() if v >= 3)
    epi = sum(1 for x in paras
              if re.match(r'^(我忽然|我这才|我心里|我明白|我看出|我先以为|我在心里)', x))

    hard = {
        '破折': txt.count('—'),
        '半角逗': txt.count(','),
        '半角引号': txt.count('"'),
        '五逗句': sum(1 for s in sents if s.count('，') >= 5),
        '英文': len(re.findall(r'[A-Za-z]', txt)),
        '章号入正文': len(re.findall(r'[一二三四五六七八九十百]+章', body)),
        '禁抖': body.count('抖'),
        '永禁词': sum(body.count(w) for w in ['哆嗦', '骊山', '僵尸', '点亮']),
        '段间空行病': len(re.findall(r'。\n(?!\n)[^\n]', txt)),
        '亮点段破折': hl.count('—'),
        '亮点段五逗': sum(1 for s in re.split(r'(?<=[。！？…])', hl) if s.count('，') >= 5),
        '亮点段半角': hl.count(',') + hl.count('"'),
    }
    soft = {
        '净重': len(re.sub(r'\s', '', body)),
        '段数': len(paras),
        '均段': sum(lens) // max(len(lens), 1),
        '最长段': max(lens),
        '长段数': sum(1 for x in lens if x >= 90),
        '嗅': cnt(r'味|气味|鼻|闻'),
        '听': cnt(r'听|响|声|叫|吠'),
        '触': cnt(r'凉|温|烫|硬|软|摸|按|贴'),
        '视': cnt(r'灯|光|看|眼|见'),
        '老头': cnt('老头'),
        '钱满': cnt('钱满'),
        '沈鸢': cnt('沈鸢'),
        '四字串三现': rep3,
        '顿悟起手': epi,
    }
    return hard, soft


# 棘轮方向：min＝越小越好，max＝越大越好
RATCHET_MIN = ('四字串三现', '顿悟起手')
RATCHET_MAX = ('嗅', '沈鸢')


def save(n, note=''):
    d, led = paths(n)
    os.makedirs(d, exist_ok=True)
    src = find_chapter(n)
    if not src:
        print('  ✗未找到第%d章正文' % n)
        return 1
    txt = open(src, encoding='utf-8').read()
    hard, soft = score(txt)
    ledger = json.load(open(led, encoding='utf-8')) if os.path.exists(led) \
        else {'章': n, '版本': []}
    v = len(ledger['版本']) + 1
    open(os.path.join(d, 'v%02d.md' % v), 'w', encoding='utf-8').write(txt)

    print('\n███ 存版 v%02d · 第%d章 ███' % (v, n))
    hb = sum(hard.values())
    print('  硬项合计 %d %s' % (hb, '✓' if hb == 0 else '⛔须清零，非零不得为最终版'))
    if hb:
        print('   ', {k: x for k, x in hard.items() if x})
    print('  净重%d 段数%d 均段%d 长段%d | 嗅%d 听%d 触%d 视%d | 老%d 钱%d 沈%d | 四字三现%d 顿悟%d'
          % (soft['净重'], soft['段数'], soft['均段'], soft['长段数'],
             soft['嗅'], soft['听'], soft['触'], soft['视'],
             soft['老头'], soft['钱满'], soft['沈鸢'],
             soft['四字串三现'], soft['顿悟起手']))

    if ledger['版本']:
        best = {}
        for r in ledger['版本']:
            for k in RATCHET_MIN:
                best[k] = min(best.get(k, r['soft'][k]), r['soft'][k])
            for k in RATCHET_MAX:
                best[k] = max(best.get(k, r['soft'][k]), r['soft'][k])
            best['净重'] = max(best.get('净重', r['soft']['净重']), r['soft']['净重'])
        worse = []
        for k in RATCHET_MIN:
            if soft[k] > best[k]:
                worse.append('%s %d→%d(升)' % (k, best[k], soft[k]))
        for k in RATCHET_MAX:
            if soft[k] < best[k]:
                worse.append('%s %d→%d(降)' % (k, best[k], soft[k]))
        if soft['净重'] < best['净重'] * 0.92:
            worse.append('净重 %d→%d(减逾8%%)' % (best['净重'], soft['净重']))
        print('  ── 棘轮闸（与历史最优逐项比） ──')
        if worse:
            print('   ⚠回退项：' + '；'.join(worse))
            print('   减法轮之净重下降属正常，须于回执写明理由；其余回退须裁定或改回。')
        else:
            print('   ✓无回退')

    if not note.strip():
        print('  ⛔本轮说明为空——防假跑第2条：空说明视为该轮未做。')
    ledger['版本'].append({
        '版': 'v%02d' % v,
        '时': datetime.datetime.now().strftime('%m-%d %H:%M'),
        '说明': note, 'hard': hard, 'soft': soft})
    json.dump(ledger, open(led, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('  台账：%s（共%d版）' % (os.path.relpath(led, ROOT), v))
    print('  ⏳十轮精进：已%d轮，还差%d轮' % (v, 10 - v) if v < 10
          else '  ✓十轮已满，请跑 --横评 %d' % n)
    return 0


def compare(n):
    d, led = paths(n)
    if not os.path.exists(led):
        print('  ✗第%d章尚无版本台账，先跑 --存版 %d' % (n, n))
        return 1
    versions = json.load(open(led, encoding='utf-8'))['版本']
    print('\n███ 十版横评 · 第%d章（共%d版） ███' % (n, len(versions)))

    print('\n  ── 一·硬项（任一非零即不可为最终版） ──')
    clean = []
    for r in versions:
        hb = sum(r['hard'].values())
        print('   %s 硬项%-3d %s %s' % (r['版'], hb, '✓' if hb == 0 else '⛔', r['说明'][:34]))
        if hb == 0:
            clean.append(r)

    print('\n  ── 二·量项走势 ──')
    head = ('版', '净重', '段数', '长段', '嗅', '触', '沈鸢', '顿悟', '四字三现')
    print('   %-5s %-6s %-5s %-5s %-4s %-4s %-5s %-5s %-8s' % head)
    for r in versions:
        s = r['soft']
        print('   %-5s %-6d %-5d %-5d %-4d %-4d %-5d %-5d %-8d'
              % (r['版'], s['净重'], s['段数'], s['长段数'], s['嗅'],
                 s['触'], s['沈鸢'], s['顿悟起手'], s['四字串三现']))

    print('\n  ── 三·逐项冠军 ──')
    pool = clean or versions
    champs = {}
    for k, pick in [('净重', max), ('长段数', max), ('嗅', max), ('触', max),
                    ('沈鸢', max), ('四字串三现', min), ('顿悟起手', min)]:
        best_val = pick(r['soft'][k] for r in pool)
        holders = [r['版'] for r in pool if r['soft'][k] == best_val]
        # 【批104】并列修正：末版若同为最优即算持有，避免"首次达标版"误判为唯一冠军
        champs[k] = pool[-1]['版'] if pool[-1]['soft'][k] == best_val else holders[0]
        tie = '（并列%d版，末版持有）' % len(holders) if len(holders) > 1 and \
              pool[-1]['soft'][k] == best_val else ''
        print('   %-8s 最优值%-6d 持有 %s%s' % (k, best_val, champs[k], tie))

    print('\n  ── 四·择优裁定（机器只给候选，最终由AI四席定夺） ──')
    if not clean:
        print('   ⛔无硬项全清之版，不得择优；先清零再评。')
        return 1
    last = clean[-1]
    print('   机器候选＝%s（硬项全清之末版，承载全部累积修复）' % last['版'])
    dist = Counter(champs.values())
    print('   逐项冠军分布：%s' % dict(dist))
    if dist.most_common(1)[0][0] != last['版']:
        losing = [k for k, v in champs.items() if v != last['版']]
        print('   ⚠末版未持有以下项之最优值，须逐项核对是否在后续轮次被改坏：%s' % '、'.join(losing))
        print('     改回该项，而非退回旧版；若经裁定为必要代价，须在回执记因。')
    else:
        print('   ✓末版同时为多数项冠军，累积有效。')
    print('\n  【铁律】择优不是挑一版丢九版。取末版为底，逐项回补其余版之冠军项；')
    print('        任何回补须再跑 --存版 生成新版，且新版硬项须全清。')
    if len(versions) < 10:
        print('\n  ⏳尚未满十轮（%d/10），横评仅供中途参考。' % len(versions))
    return 0


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    cmd = sys.argv[1]
    n = int(sys.argv[2])
    if cmd == '--存版':
        return save(n, sys.argv[3] if len(sys.argv) > 3 else '')
    if cmd == '--横评':
        return compare(n)
    print(__doc__)
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
