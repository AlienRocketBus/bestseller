#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""复核台账——1096 项 REVIEW 逐条建账、逐条判、跨会话可续。

【批116·立】病灶：REVIEW 自立项起从未被拆开看过，只以「1789」一个总数挂着。
  一查即见此数不干净：1789 行 = 真·待判项 1096 ＋ 证据续行 641 ＋ 截断提示 52；
  且截断提示自称尚有 265 处例句未列出。**既高报又低报，从来不是 1789 个问题。**
  此活须跨多次会话，而上下文压缩必然发生（P22）——无台账则今日所判明日尽忘，
  故先立账后动手。

判语只四种：
  未判 / 改（已改，须记改法）/ 判合（不改，须记因）/ 待定（须记待何事）
**判合与待定皆须记因；无因之判视同未判**（--进度 会把它揪出来）。

用法：
    python3 工具/复核台账.py --建账          # 自检察官抽取全量，增量并入（不覆盖已判）
    python3 工具/复核台账.py --进度          # 总进度＋各类目进度＋无因之判
    python3 工具/复核台账.py --抽样 近距重复 12   # 抽样，供先测后判（P24：n<5不得支撑断言）
    python3 工具/复核台账.py --列 未判 近距重复 20
    python3 工具/复核台账.py --判 <id> 判合 "记因"
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
import json
import glob
import random
import hashlib
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEDGER = os.path.join(ROOT, '设定', 'REVIEW台账.json')
VERDICTS = ('未判', '改', '判合', '待定')


def _iid(ch, item):
    """【批117·修】id 须对措辞稳定。
    病灶：初版以整条消息文本入哈希，故检察官一改告警措辞（如为「分量」加上分位数诊断），
    44 条已判之项即因哈希变动而变成新的未判项——账被措辞重开。
    今改为只取「章＋类目＋条内关键内容」：关键内容优先取「」中之引串，
    无引串则取消息中之首个定量特征（数字＋量词），再无则取类目后前12字。
    如此告警措辞可自由改进而账不动。"""
    t = item.strip()
    cat = re.match(r'\[([^\]]+)\]', t)
    cat = cat.group(1) if cat else '无类目'
    body = t[len(cat) + 2:] if cat != '无类目' else t
    keys = re.findall(r'「([^」]{2,})」', body)
    if keys:
        key = '｜'.join(sorted(set(keys)))
    else:
        m = re.search(r'"([^"]+)"\s*(\d+)\s*处', body)
        if m:
            key = m.group(1)
        else:
            m2 = re.search(r'(全章仅|均段长|没有一段≥)', body)
            key = m2.group(1) if m2 else re.sub(r'[\d０-９]+', 'N', body)[:12]
    return hashlib.sha256(('%d|%s|%s' % (ch, cat, key)).encode('utf-8')).hexdigest()[:12]


def _load():
    if os.path.exists(LEDGER):
        return json.load(open(LEDGER, encoding='utf-8'))
    return {'立账': datetime.datetime.now().strftime('%Y-%m-%d'), '项': []}


def _save(d):
    json.dump(d, open(LEDGER, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def _harvest():
    """自检察官取全量 REVIEW，只收真·待判项（[类目]开头者）。
    证据续行与截断提示不入账——它们是凭据，不是待判之事。"""
    import importlib.util as u
    sys.argv = ['x']
    sp = u.spec_from_file_location('_insp', os.path.join(ROOT, '工具', '小说检察官.py'))
    m = u.module_from_spec(sp)
    sp.loader.exec_module(m)
    files = m._chapters()
    rows, ev = [], {}
    for n in sorted(files):
        issues, _, _ = m.check_file(files[n][0])
        issues += m.intra_repeat(files[n][2])
        cur = None
        for it in issues:
            if it.lstrip().startswith('['):
                cur = (n, it)
                rows.append(cur)
                ev[_iid(n, it)] = []
            elif cur is not None:
                ev[_iid(*cur)].append(it.strip())
    return rows, ev


def build():
    rows, ev = _harvest()
    d = _load()
    have = {x['id']: x for x in d['项']}
    add = 0
    seen = set()
    for n, it in rows:
        i = _iid(n, it)
        seen.add(i)
        if i in have:
            have[i]['证据'] = ev.get(i, [])
            continue
        cat = re.match(r'\[([^\]]+)\]', it.lstrip())
        d['项'].append({'id': i, '章': n, '类目': cat.group(1) if cat else '无类目',
                        '项': it.strip(), '证据': ev.get(i, []),
                        '判': '未判', '记因': '', '时': ''})
        add += 1
    gone = [x for x in d['项'] if x['id'] not in seen]
    auto = [x for x in gone if x['判'] == '未判']   # 仅未判而消失者方为自动销
    for x in gone:
        if x['判'] == '未判':
            x['判'] = '判合'
            x['记因'] = '正文已改，该项自检察官消失（%s 自动销）' % \
                datetime.datetime.now().strftime('%m-%d')
            x['时'] = datetime.datetime.now().strftime('%m-%d %H:%M')
    _save(d)
    print('  建账完毕：新增 %d 项；现存 %d 项；已判而消失 %d 项；未判而消失（自动销）%d 项'
          % (add, len(d['项']), len(gone) - len(auto), len(auto)))
    return 0


def progress():
    d = _load()
    it = d['项']
    if not it:
        print('  台账为空，请先跑 --建账')
        return 1
    from collections import Counter
    tot = len(it)
    done = [x for x in it if x['判'] != '未判']
    print('\n████ REVIEW 复核台账 ████')
    print('  总项 %d｜已判 %d（%.1f%%）｜未判 %d'
          % (tot, len(done), 100.0 * len(done) / tot, tot - len(done)))
    v = Counter(x['判'] for x in it)
    print('  判语分布：' + '｜'.join('%s %d' % (k, v[k]) for k in VERDICTS if v[k]))
    print('\n  ── 各类目进度 ──')
    cat = Counter(x['类目'] for x in it)
    catdone = Counter(x['类目'] for x in done)
    for k, n in cat.most_common():
        bar = '█' * int(20.0 * catdone[k] / n) + '·' * (20 - int(20.0 * catdone[k] / n))
        print('   %-8s %s %3d/%3d' % (k, bar, catdone[k], n))
    bad = [x for x in it if x['判'] in ('判合', '待定') and not x['记因'].strip()]
    if bad:
        print('\n  ⛔无因之判 %d 项（判合／待定须记因，无因视同未判）：' % len(bad))
        for x in bad[:8]:
            print('     %s 第%d章 %s' % (x['id'], x['章'], x['项'][:50]))
        return 1
    print('\n  ✓无因之判：0')
    return 0


def sample(cat, k=12):
    d = _load()
    pool = [x for x in d['项'] if x['类目'] == cat]
    if not pool:
        print('  无此类目：%s' % cat)
        return 1
    random.seed(20260804)
    pick = random.sample(pool, min(k, len(pool)))
    print('\n██ 抽样 · %s（总 %d，抽 %d）██' % (cat, len(pool), len(pick)))
    print('  【P24】先测后判：抽样评估可行率，再决定逐条办还是类目裁定；类目裁定须附此抽样为凭。')
    for x in pick:
        print('\n  [%s] 第%d章 判=%s' % (x['id'], x['章'], x['判']))
        print('   %s' % x['项'][:180])
        for e in x['证据'][:3]:
            print('     · %s' % e[:110])
    return 0


def lst(verdict='未判', cat=None, k=20):
    d = _load()
    pool = [x for x in d['项'] if x['判'] == verdict and (not cat or x['类目'] == cat)]
    print('  %s%s：%d 项，列前 %d' % (verdict, ('·' + cat) if cat else '', len(pool), min(k, len(pool))))
    for x in pool[:k]:
        print('   [%s] 第%d章 %s' % (x['id'], x['章'], x['项'][:120]))
    return 0


def judge(iid, verdict, reason=''):
    if verdict not in VERDICTS:
        print('  判语须为：%s' % '／'.join(VERDICTS))
        return 1
    if verdict in ('判合', '待定') and not reason.strip():
        print('  ⛔%s 须记因——无因之判视同未判。' % verdict)
        return 1
    d = _load()
    for x in d['项']:
        if x['id'] == iid:
            x['判'] = verdict
            x['记因'] = reason
            x['时'] = datetime.datetime.now().strftime('%m-%d %H:%M')
            _save(d)
            print('  ✓[%s] 第%d章 → %s｜%s' % (iid, x['章'], verdict, reason[:60]))
            return 0
    print('  ✗未找到 id=%s' % iid)
    return 1


def judge_bulk(cat, verdict, reason, chapters=None):
    """类目批判。**须附抽样凭据于记因**，否则即是无凭之裁（P24）。"""
    if verdict in ('判合', '待定') and not reason.strip():
        print('  ⛔须记因。')
        return 1
    d = _load()
    n = 0
    for x in d['项']:
        if x['类目'] == cat and x['判'] == '未判':
            if chapters and x['章'] not in chapters:
                continue
            x['判'] = verdict
            x['记因'] = reason
            x['时'] = datetime.datetime.now().strftime('%m-%d %H:%M')
            n += 1
    _save(d)
    print('  ✓类目批判：%s ×%d → %s' % (cat, n, verdict))
    return 0


def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__)
        return 1
    c = a[0]
    if c == '--建账':
        return build()
    if c == '--进度':
        return progress()
    if c == '--抽样':
        return sample(a[1], int(a[2]) if len(a) > 2 else 12)
    if c == '--列':
        return lst(a[1] if len(a) > 1 else '未判',
                   a[2] if len(a) > 2 else None,
                   int(a[3]) if len(a) > 3 else 20)
    if c == '--判':
        return judge(a[1], a[2], a[3] if len(a) > 3 else '')
    if c == '--类判':
        return judge_bulk(a[1], a[2], a[3] if len(a) > 3 else '')
    print(__doc__)
    return 1


if __name__ == '__main__':
    sys.exit(main())
