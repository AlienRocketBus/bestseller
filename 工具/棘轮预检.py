# -*- coding: utf-8 -*-
"""棘轮预检 · 2026-09-01 立（LAW-289C·令§十一机化）
　病：改文之後直接 --存版，棘轮闸事後才报回退，遂须 --补存 补一版。
　　　289 第5轮（补身撞「是哪一样」）、第6轮（承前撞「馊压过甜」）连犯二回。
　法：**不另造一把尺**——直接 import 跑轮.score 与其 RATCHET_MIN/MAX，
　　　读同一份 _台账.json 算同一个「历来最优」；
　　　★故此器所报，与 --存版 之棘轮闸逐字同源，不会出现「预检绿而存版红」。
　用：python3 工具/棘轮预检.py N      ← 落盘之後、--存版 之前跑
　　　rc=0 放行｜rc=1 会回退｜rc=2 无此章
"""
import io, os, re, sys, json, glob

根 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(根, '工具'))
from 跑轮 import score, body_of, RATCHET_MIN, RATCHET_MAX, RATCHET_V01  # noqa: E402

CN = {'零':0,'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9}


def _号(s):
    m = re.search(r'第([零一二三四五六七八九十百]+)章', s)
    if not m:
        return None
    t = m.group(1)
    if t.startswith('十'):
        t = '一' + t
    n = cur = 0
    for ch in t:
        if ch == '百':
            n += (cur or 1) * 100; cur = 0
        elif ch == '十':
            n += (cur or 1) * 10; cur = 0
        else:
            cur = CN[ch]
    return n + cur


def 正文路径(n):
    for p in sorted(glob.glob(os.path.join(根, '正文', '*.md'))):
        if _号(os.path.basename(p)) == n:
            return p
    return None


def 起草版(n):
    """台账首个有 soft 之版——RATCHET_V01 之底（2026-09-02立）。"""
    f = os.path.join(根, '版本', '第%d章' % n, '_台账.json')
    if not os.path.exists(f):
        return {}
    for r in json.load(io.open(f, encoding='utf-8')).get('版本', []):
        sf = r.get('soft') or {}
        if sf:
            return sf
    return {}


def 最优(n):
    """与跑轮存版处逐行同式：只认台账里已记之 soft，缺键者不参与。"""
    f = os.path.join(根, '版本', '第%d章' % n, '_台账.json')
    if not os.path.exists(f):
        return {}
    led = json.load(io.open(f, encoding='utf-8'))
    best = {}
    for r in led.get('版本', []):
        sf = r.get('soft') or {}
        for k in RATCHET_MIN:
            if k in sf:
                best[k] = min(best.get(k, sf[k]), sf[k])
        for k in RATCHET_MAX:
            if k in sf:
                best[k] = max(best.get(k, sf[k]), sf[k])
        if '净重' in sf:
            best['净重'] = max(best.get('净重', sf['净重']), sf['净重'])
    return best


def 三现串(txt):
    b = body_of(txt)
    seen = {}
    for i in range(len(b) - 3):
        k = b[i:i + 4]
        if re.match(r'^[一-龥]{4}$', k):
            seen[k] = seen.get(k, 0) + 1
    return {k for k, v in seen.items() if v >= 3}


_感式 = {'嗅': r'味|气味|鼻|闻', '听': r'听|响|声|叫|吠',
        '触': r'凉|温|烫|硬|软|摸|按|贴', '视': r'灯|光|看|眼|见'}


def _四感删证(n, txt, 项):
    """★★★★★2026-09-05·305第8、9两轮所立（欠-305A之治·§十一③机化）。
    ★其红在哪一行（二组数·§六①）：
      · **305第8轮**：删拍71（「昨天那个十一是针听的…」——一处转述），器报「听 14→13」；
      · **305第9轮**：紧拍72（「一把说硬，一把说一响」——同一对尺之三陈），器报「听／触」又降。
      ★★二回所减者俱非一次真的感觉，是一句转述**；而器只印「听 14→13」，
        不印那一句是什么——**於是「所减者是不是一次真感觉」这一问，全靠人自己记得去问。**
    ★★★故此块只做一件事：**把「本轮删掉而含此感之字」的句子逐句摆出来**，判仍归人。
    ★★★★它认哪几样（§六④）：**四感四项，本书同类共四样**（嗅／听／触／视，与 RATCHET_V01 同源）；
      ★它认不着的两样：①改写而非整句删者（其残句仍在，不入此表）；②**「那一句算不算一次真感觉」——那一判器不下，人下。**"""
    vs = sorted(glob.glob(os.path.join(根, '版本', '第%d章' % n, 'v*.md')))
    if not vs:
        return []
    旧 = body_of(io.open(vs[-1], encoding='utf-8').read())
    新 = body_of(txt)
    切 = lambda t: [x for x in re.split(r'[。！？\n]', t) if x.strip()]
    有 = set(切(新))
    式 = _感式.get(项)
    if not 式:
        return []
    return [x.strip() for x in 切(旧)
            if x.strip() and x not in 有 and re.search(式, x)]


def 跑(n, 报=True):
    p = 正文路径(n)
    if not p:
        if 报:
            print('⛔ 第%d章之正文不在' % n)
        return 2
    txt = io.open(p, encoding='utf-8').read()
    _hard, soft = score(txt)
    best = 最优(n)
    worse = []
    for k in RATCHET_MIN:
        if k in best and soft[k] > best[k]:
            worse.append((k, best[k], soft[k], '升'))
    for k in RATCHET_MAX:
        if k in best and soft[k] < best[k]:
            worse.append((k, best[k], soft[k], '降'))
    v01 = 起草版(n)
    for k in RATCHET_V01:
        if k in v01 and k in soft and soft[k] < v01[k]:
            worse.append((k, v01[k], soft[k], '低於起草'))
    if 报:
        print('════ 棘轮预检 · 第%d章 ════' % n)
        if not best:
            print('  ℹ 台账无版可比（新章），棘轮无底，放行。')
            return 0
        print('  历来最优：' + '｜'.join('%s %s' % (k, best[k]) for k in sorted(best)))
        print('  当前正文：' + '｜'.join('%s %s' % (k, soft[k]) for k in sorted(best)))
        if not worse:
            print('  ✓ 此刻存版，棘轮不会报回退。')
        for k, a, b, d in worse:
            extra = ''
            if k in _感式:
                句 = _四感删证(n, txt, k)
                if 句:
                    extra = ('｜本轮删去而含「%s」之句 %d 条：' % (k, len(句))
                             + '｜'.join('「%s」' % x[:34] for x in 句[:3]))
                    if len(句) > 3:
                        extra += '｜…'
                else:
                    extra = '｜本轮无整句删去而含此感者——**故其降係改写所致，须逐处自看**'
            if k == '四字串三现':
                vs = sorted(glob.glob(os.path.join(根, '版本', '第%d章' % n, 'v*.md')))
                if vs:
                    新 = 三现串(txt) - 三现串(io.open(vs[-1], encoding='utf-8').read())
                    if 新:
                        extra = '｜所增之串：' + '、'.join(sorted(新))
            print('  ⛔ %s %d→%d(%s)%s' % (k, a, b, d, extra))
        if worse:
            print('  处方：先改回再 --存版。')
            print('  ★而其常犯之形有二：①补身之字落在旧物上，旧物之名已在章中（289第5轮）；')
            print('    ②承前之句引原场之词，而那词本章已用过两回（289第6轮）。')
    return 1 if worse else 0


if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('-')]
    if not a:
        print('用法：python3 工具/棘轮预检.py N'); sys.exit(2)
    sys.exit(跑(int(a[0])))
