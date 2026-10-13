#!/usr/bin/env python3
"""费审对拍（1009 立·作者令「确保计算 token 之方式绝对精准正确，一定要再三确定」；同日令「先设计最好的办法——机器核，费不了多少时间与 token」）。

为何立：算 token 与美元是确定之算术，机器核与模型核一样准——⛔派模型席去核（W18 之教，坑⑳）。
本器以与 `工具/费审.py` **结构全异之写法**重算一遍，逐单位对到 token 个位、美元到分以下：
  · 费审：逐行流读、dict 按 message.id 去重、Python 逐回计价。
  · 本器：每一行带 usage 者入 SQLite 一行（档、行号、id、时、模型、诸项），去重、合计、计价**全在 SQL**。
并核记录之义（费审之去重所恃之前提）：
  ① 同一 (档, message.id) 之诸行，usage 是否全同（若有演变，取末行是否对）；
  ② 同一 message.id 是否跨档重现（续跑之 Run 抄档则计重）；
  ③ 缓存写两档之和 ＝ 总；思考之 token ≤ 产出；
  ④ 价目里没有之模型。
单位：每个工作流 Run、每份非工作流子席、主会话全程。价目共用 `设定/价目.json`（其数另核於官方价目页，见 价目.json 之源与抓）。

用法：
  python3 工具/费审对拍.py            # 全会话对拍（单位数、不符数、记录之义之异常、合计）；不符即 rc=1
  python3 工具/费审对拍.py --自测      # 手算之金题（与费审之自测不同之数）
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, json, glob, sqlite3, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


活之界 = 900   # 秒：近十五分钟内改过之档作「活档」（席之一回工具至多十分钟不落笔）


def 快照之(fs, 快照, 今=None, 目录=None):
    """活档先抄一份，两边只算抄本（1013 实踩：推时之全测正逢 381 之席在写，两边先後读同一活档，读到之行数不同，报「不符 6 处」——⛔量器之差）。
    fs 中有一档在活之界内者：目录给了（工作流 Run）即整个目录抄去（费审.审 要读 meta）；否则逐档抄。→ 抄本之 fs（无活档则原样）。"""
    import time as _t
    今 = 今 or _t.time()
    if not any(今 - os.path.getmtime(f) < 活之界 for f in fs):
        return fs
    if 目录:
        到 = os.path.join(快照, os.path.basename(目录))
        shutil.copytree(目录, 到)
        return [os.path.join(到, os.path.relpath(f, 目录)) for f in fs]
    出 = []
    for f in fs:
        d = tempfile.mkdtemp(dir=快照)
        出.append(shutil.copy2(f, os.path.join(d, os.path.basename(f))))
    return 出


def 单位们(快照=None):
    """→ [(单位名, [档…])]：工作流 Run、非工作流子席、主会话。快照给了即活档先抄（见 快照之）。"""
    if 快照:
        return [(名, 快照之(fs, 快照, 目录=os.path.dirname(fs[0]) if 名.startswith('run:') else None)) for 名, fs in 单位们()]
    出 = []
    for 会 in sorted(glob.glob(os.path.expanduser('~/.claude/projects/*/*.jsonl'))):
        d = 会[:-len('.jsonl')]
        for run in sorted(glob.glob(os.path.join(d, 'subagents', 'workflows', 'wf_*'))):
            fs = sorted(glob.glob(os.path.join(run, 'agent-*.jsonl')))
            if fs:
                出.append(('run:' + os.path.basename(run), fs))
        for f in sorted(glob.glob(os.path.join(d, 'subagents', 'agent-*.jsonl'))):
            出.append(('子席:' + os.path.basename(f), [f]))
        出.append(('主会话:' + os.path.basename(会), [会]))
    return 出


def 入库(db, 单位, fs):
    for f in fs:
        with open(f, encoding='utf-8') as fh:
            for n, l in enumerate(fh, 1):
                try:
                    e = json.loads(l)
                except Exception:
                    continue
                m = e.get('message') or {}
                u = m.get('usage')
                if not isinstance(u, dict) or e.get('type') != 'assistant':
                    if isinstance(u, dict):
                        db.execute('INSERT INTO 外 VALUES (?,?,?,?)', (单位, f, n, e.get('type')))
                    continue
                cc = u.get('cache_creation') or {}
                od = u.get('output_tokens_details') or {}
                db.execute('INSERT INTO 行 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (
                    单位, f, n, m.get('id'), m.get('model') or '',
                    u.get('input_tokens') or 0, u.get('cache_creation_input_tokens') or 0,
                    cc.get('ephemeral_5m_input_tokens'), cc.get('ephemeral_1h_input_tokens'),
                    u.get('cache_read_input_tokens') or 0, u.get('output_tokens') or 0,
                    od.get('thinking_tokens'), u.get('speed') or '', u.get('inference_geo') or '',
                    ((u.get('server_tool_use') or {}).get('web_search_requests') or 0),
                    json.dumps(u, sort_keys=True), e.get('timestamp') or ''))


def 建库(价):
    db = sqlite3.connect(':memory:')
    db.execute('CREATE TABLE 行 (单位, 档, 号, id, 模型, 新, 建, 建5, 建1, 读, 出, 思, 速, 地, 搜, 全usage, 时)')
    db.execute('CREATE TABLE 外 (单位, 档, 号, 类)')
    db.execute('CREATE TABLE 价 (模型 PRIMARY KEY, 新, 写5, 写1, 读, 出)')
    for k, p in 价['模型'].items():
        db.execute('INSERT INTO 价 VALUES (?,?,?,?,?,?)', (k, p['新入'], p['缓存写5m'], p['缓存写1h'], p['缓存读'], p['产出']))
    db.execute('CREATE TABLE 快 (模型 PRIMARY KEY, 新, 出, 读倍)')
    for k, p in 价.get('快速', {}).items():
        db.execute('INSERT INTO 快 VALUES (?,?,?,?)', (k, p['新入'], p['产出'], 价['缓存倍数']['缓存读'].get(k, 价['缓存倍数']['缓存读']['余'])))
    return db


算SQL = """
WITH 末 AS (                         -- 去重：同一 (档, id) 取末行；无 id 者逐行各算一回
  SELECT r.* FROM 行 r
  WHERE r.id IS NULL OR r.号 = (SELECT MAX(号) FROM 行 x WHERE x.档 = r.档 AND x.id = r.id)
),
定 AS (
  SELECT 末.*,
    CASE WHEN 模型 = 'claude-haiku-5-5' AND 新 + 建 + 读 > :界 THEN 'claude-haiku-5-5>100k' ELSE 模型 END AS 价键,
    COALESCE(建5, CASE WHEN 建1 IS NULL THEN 建 ELSE 0 END) AS w5,
    COALESCE(建1, 0) AS w1
  FROM 末
),
金 AS (
  SELECT 定.单位, 定.新, 定.建, 定.读, 定.出, 定.模型,
    (CASE WHEN 定.新 + 定.建 + 定.读 + 定.出 = 0 THEN 0
          WHEN 定.速 = 'fast' AND 快.模型 IS NOT NULL THEN
            (定.新 * 快.新 + 定.w5 * 快.新 * :倍5 + 定.w1 * 快.新 * :倍1 + 定.读 * 快.新 * 快.读倍 + 定.出 * 快.出) / 1e6
          ELSE (定.新 * 价.新 + 定.w5 * 价.写5 + 定.w1 * 价.写1 + 定.读 * 价.读 + 定.出 * 价.出) / 1e6 END)
      * (CASE WHEN 定.地 = 'us' THEN :美 ELSE 1.0 END) + 定.搜 * :搜价 AS usd,
    CASE WHEN 定.新 + 定.建 + 定.读 + 定.出 > 0 AND 价.模型 IS NULL THEN 1 ELSE 0 END AS 未价
  FROM 定 LEFT JOIN 价 ON 价.模型 = 定.价键 LEFT JOIN 快 ON 快.模型 = 定.模型
)
SELECT 单位, COUNT(*), SUM(新), SUM(建), SUM(读), SUM(出), SUM(usd), SUM(未价) FROM 金 GROUP BY 单位
"""


def 算(db, 价):
    db.execute('CREATE INDEX IF NOT EXISTS 行_档id ON 行 (档, id, 号)')   # ★无此索引，去重之子查询逐行扫全表，十余万行跑十分钟不完
    参 = {'界': 价.get('海酷长档之界', 100000), '倍5': 价['缓存倍数']['缓存写5m'], '倍1': 价['缓存倍数']['缓存写1h'],
         '美': 价.get('地域', {}).get('us', 1.1), '搜价': 价.get('网搜每次', 0.01)}
    return {r[0]: dict(回=r[1], 新=r[2], 建=r[3], 读=r[4], 出=r[5], 金=r[6], 未价=r[7]) for r in db.execute(算SQL, 参)}


def 义(db):
    """记录之义之核 → [(名, 数, 例)]。"""
    q = lambda s: db.execute(s).fetchall()
    出 = []
    r = q("SELECT COUNT(*) FROM (SELECT 档, id FROM 行 WHERE id IS NOT NULL GROUP BY 档, id HAVING COUNT(DISTINCT 全usage) > 1)")
    出.append(('同 (档,id) 诸行之 usage 有演变（流式中途之数）', r[0][0]))
    # ★1009 实核：522 处演变俱是流式中途之数（只产出与附属字段变），末行恒为终值——取末行为对；末行若小於前行即真异
    r = q("""SELECT COUNT(*) FROM 行 m JOIN (SELECT 档, id, MAX(号) AS 末号, MAX(新) AS a, MAX(建) AS b, MAX(读) AS c, MAX(出) AS d
             FROM 行 WHERE id IS NOT NULL GROUP BY 档, id) g ON m.档 = g.档 AND m.id = g.id AND m.号 = g.末号
             WHERE m.新 < g.a OR m.建 < g.b OR m.读 < g.c OR m.出 < g.d""")
    出.append(('末行小於前行（取末行即错）', r[0][0]))
    r = q("SELECT COUNT(*) FROM (SELECT id FROM 行 WHERE id IS NOT NULL GROUP BY id HAVING COUNT(DISTINCT 档) > 1)")
    出.append(('同 id 跨档重现', r[0][0]))
    r = q("SELECT COUNT(*) FROM 行 WHERE (建5 IS NOT NULL OR 建1 IS NOT NULL) AND COALESCE(建5,0) + COALESCE(建1,0) != 建")
    出.append(('缓存写两档之和 ≠ 总', r[0][0]))
    r = q("SELECT COUNT(*) FROM 行 WHERE 建 > 0 AND 建5 IS NULL AND 建1 IS NULL")
    出.append(('缓存写无两档之分', r[0][0]))
    r = q("SELECT COUNT(*) FROM 行 WHERE 思 IS NOT NULL AND 思 > 出")
    出.append(('思考之 token > 产出', r[0][0]))
    r = q("SELECT COUNT(*) FROM 行 WHERE id IS NULL")
    出.append(('无 message.id 之行（逐行各算）', r[0][0]))
    r = q("SELECT COUNT(*) FROM 外")
    出.append(('非 assistant 而带 usage 之行（未计）', r[0][0]))
    r = q("SELECT COUNT(*) FROM 行 WHERE 速 = 'fast' OR 地 = 'us' OR 搜 > 0")
    出.append(('加价之回（快速／美区／网搜）', r[0][0]))
    return 出


def 对(甲, 乙, 容=1e-9):
    """甲：本器；乙：费审。→ 不符之单位。"""
    不符 = []
    for k in sorted(set(甲) | set(乙)):
        a, b = 甲.get(k), 乙.get(k)
        if not a or not b:
            不符.append((k, '一方无此单位')); continue
        for f in ('回', '新', '建', '读', '出'):
            if a[f] != b[f]:
                不符.append((k, '%s：本器 %s ≠ 费审 %s' % (f, a[f], b[f])))
        if abs(a['金'] - b['金']) > 容:
            不符.append((k, '美元：本器 %.6f ≠ 费审 %.6f' % (a['金'], b['金'])))
    return 不符


def 费审之数(单位们_):
    import 费审
    出 = {}
    for 名, fs in 单位们_:
        if 名.startswith('run:'):
            s = 费审.合(费审.审(os.path.dirname(fs[0])))
        else:
            r = 费审.审一(fs[0], 名)
            s = {k: r[k] for k in ('回', '新', '建', '读', '出', '金')}
        出[名] = {k: s[k] for k in ('回', '新', '建', '读', '出', '金')}
    return 出


def 跑():
    价 = json.load(open(os.path.join(ROOT, '设定', '价目.json'), encoding='utf-8'))
    快照 = tempfile.mkdtemp()
    try:
        us = 单位们(快照)
        db = 建库(价)
        for 名, fs in us:
            入库(db, 名, fs)
        甲 = 算(db, 价)
        乙 = 费审之数(us)
    finally:
        shutil.rmtree(快照, ignore_errors=True)
    不符 = 对(甲, 乙)
    计 = lambda p: sum(v['金'] for k, v in 甲.items() if k.startswith(p))
    print('════ 费审对拍 ════（本器：SQLite 去重合计计价；费审：Python 逐回）')
    print('  单位 %d（工作流 Run %d、非工作流子席 %d、主会话 %d）｜价目 抓於 %s' % (
        len(us), sum(1 for k, _ in us if k.startswith('run:')), sum(1 for k, _ in us if k.startswith('子席:')),
        sum(1 for k, _ in us if k.startswith('主会话:')), 价.get('抓')))
    print('  美元：工作流 $%.2f｜非工作流子席 $%.2f｜主会话 $%.2f｜合计 $%.2f' % (计('run:'), 计('子席:'), 计('主会话:'), sum(v['金'] for v in 甲.values())))
    print('  未价之回：%d' % sum(v['未价'] for v in 甲.values()))
    print('── 记录之义（费审之去重所恃之前提）──')
    for 名, n in 义(db):
        print('  %s %-30s %d' % ('✓' if n == 0 or 名.startswith(('无 message', '加价', '同 (档,id)')) else '⛔', 名, n))
    真异 = sum(n for 名, n in 义(db) if not 名.startswith(('无 message', '加价', '同 (档,id)')))
    if 真异:
        print('⛔ 记录之义有真异 %d 处——费审之去重前提不成立，须先查明' % 真异)
    if 不符:
        print('⛔ 对拍不符 %d 处：' % len(不符))
        for k, w in 不符[:30]:
            print('   %s：%s' % (k, w))
    else:
        print('✓ 对拍：%d 个单位，来回、四项 token 逐个相符，美元相差俱 < $0.000000001' % len(甲))
    print('  ⚠ 不可量（本地无记）：工具内部之小模型调用（如 WebFetch 之摘要、权限判别），不入转录；故上数是「转录所记」之全，非账单之全')
    return not 不符 and not 真异


def 自测():
    """金题：手算之数（与费审自测不同之数）。"""
    ok = 共 = 0
    价 = json.load(open(os.path.join(ROOT, '设定', '价目.json'), encoding='utf-8'))
    t = tempfile.mkdtemp()
    try:
        f = os.path.join(t, 'a.jsonl')
        def L(i, mid, model, u):
            return json.dumps({'type': 'assistant', 'timestamp': '2026-10-09T00:00:%02dZ' % i, 'message': {'id': mid, 'model': model, 'usage': u}}) + '\n'
        uA = {'input_tokens': 1000, 'cache_creation_input_tokens': 3000, 'cache_creation': {'ephemeral_5m_input_tokens': 1000, 'ephemeral_1h_input_tokens': 2000},
              'cache_read_input_tokens': 500000, 'output_tokens': 4000, 'output_tokens_details': {'thinking_tokens': 3000}}
        uB = {'input_tokens': 7, 'cache_creation_input_tokens': 0, 'cache_read_input_tokens': 0, 'output_tokens': 3, 'inference_geo': 'us'}
        uC = {'input_tokens': 200000, 'cache_creation_input_tokens': 0, 'cache_read_input_tokens': 0, 'output_tokens': 100}
        open(f, 'w', encoding='utf-8').write(L(1, 'm1', 'claude-opus-5-5', uA) * 3 + L(2, 'm2', 'claude-sonnet-5-5', uB) + L(3, 'm3', 'claude-haiku-5-5', uC)
                                              + json.dumps({'type': 'user', 'message': {'usage': uB}}) + '\n')
        db = 建库(价)
        入库(db, 'u', [f])
        r = 算(db, 价)['u']
        # 手算：m1（Opus 5.5）＝(1000×4 + 1000×5 + 2000×8 + 500000×0.20 + 4000×20)/1e6 ＝ 205000/1e6 ＝ $0.205
        #       m2（Sonnet 5.5，美区）＝(7×2 + 3×10)/1e6 ×1.1 ＝ 44×1.1/1e6 ＝ $0.0000484
        #       m3（Haiku 5.5，逾十万用长档）＝(200000×0.50 + 100×2.50)/1e6 ＝ $0.10025
        共 += 1; ok += (r['回'] == 3 and r['新'] == 201007 and r['读'] == 500000 and r['出'] == 4103)    # 三行同 id 只计一回
        共 += 1; ok += (abs(r['金'] - (0.205 + 0.0000484 + 0.10025)) < 1e-12 and r['未价'] == 0)
        义_ = dict(义(db))
        共 += 1; ok += (义_['同 (档,id) 诸行之 usage 有演变（流式中途之数）'] == 0 and 义_['非 assistant 而带 usage 之行（未计）'] == 1 and 义_['末行小於前行（取末行即错）'] == 0)
        # 流式中途之数：前行产出 5、末行 9 → 取末行；若末行反小即报真异
        g = os.path.join(t, 'b.jsonl')
        uP = dict(uB, output_tokens=5); uF = dict(uB, output_tokens=9)
        open(g, 'w', encoding='utf-8').write(L(1, 'n1', 'claude-sonnet-5-5', uP) + L(2, 'n1', 'claude-sonnet-5-5', uF) + L(3, 'n2', 'claude-sonnet-5-5', uF) + L(4, 'n2', 'claude-sonnet-5-5', uP))
        db2 = 建库(价); 入库(db2, 'v', [g]); r2 = 算(db2, 价)['v']; 义2 = dict(义(db2))
        共 += 1; ok += (r2['回'] == 2 and r2['出'] == 9 + 5 and 义2['同 (档,id) 诸行之 usage 有演变（流式中途之数）'] == 2 and 义2['末行小於前行（取末行即错）'] == 1)
        共 += 1; ok += (对({'x': dict(r)}, {'x': dict(r, 金=r['金'] + 0.01)}) and not 对({'x': dict(r)}, {'x': dict(r)}))   # 差一分即报
        # 活档之快照：活者抄、静者不抄；抄後原档再添行，抄本不变（两边算同一份）
        import time as _t
        快 = tempfile.mkdtemp(dir=t)
        os.utime(g, (_t.time() - 2 * 活之界, _t.time() - 2 * 活之界))
        共 += 1; ok += (快照之([g], 快) == [g])
        活 = os.path.join(t, 'c.jsonl'); open(活, 'w', encoding='utf-8').write(L(1, 'k1', 'claude-sonnet-5-5', uB))
        抄 = 快照之([活], 快)[0]
        open(活, 'a', encoding='utf-8').write(L(2, 'k2', 'claude-sonnet-5-5', uB))
        共 += 1; ok += (抄 != 活 and open(抄, encoding='utf-8').read().count('\n') == 1 and open(活, encoding='utf-8').read().count('\n') == 2)
    finally:
        shutil.rmtree(t)
    print('费审对拍·自测 %d/%d' % (ok, 共))
    return ok == 共


if __name__ == '__main__':
    if sys.argv[1:] == ['--自测']:
        sys.exit(0 if 自测() else 1)
    sys.exit(0 if 跑() else 1)
