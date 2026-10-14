#!/usr/bin/env python3
"""造式验（1013 立·造式二代·设定/方法升级_造式二代.md §五、§九）——诸机闸一次跑完，零 token。

为何立：一代之机闸、抄袭之关、厚之关三席以模型去跑十几个器（380 机闸一席 $9、抄袭与厚之关另席），
而「跑器、看 rc、印红处」是机器之活（零 token 等效之检）。今合稿席只跑本器一回，红了只治红处。

两类（其判据逐器实测过——1013 以已封版之 380 试跑，十七器俱绿、各器红时之形查过源码）：
  致命之器（⛔绿不许交）：起草闸（rc）｜硬闸（JSON 计数有 >0 即红）｜抄袭闸（rc）｜崩坏闸（rc）｜
                         厚（净重取 工具/净重对表.py 之尺；带底：总纲本章之行 主 2500／暗 2300）
  报之器（红即印其末行，治或写明其由）：棘轮预检、字数闸、数闸、含拍、亮点对表、亮点界、亮点在、息日链、日差哨、器物点名、外事尺 --度、比带、咬合哨
  （「对位」查诸器之位、非本章之事，单跑约 94 秒——在全测，⛔入本器。）

用法：
  python3 工具/造式验.py N           # 跑毕印逐器一行；致命之器有红 rc=1
  python3 工具/造式验.py N --json    # 另印 JSON
  python3 工具/造式验.py N --料      # 只验料全：开镜卡、章料（≤120KB）、前两章正文
  python3 工具/造式验.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, re, json, glob, time, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
致命 = [('起草闸', '{N}', 'rc'), ('硬闸', '{N}', '硬'), ('抄袭闸', '{N}', 'rc'), ('崩坏闸', '{N}', 'rc')]
报 = [('棘轮预检', '{N}'), ('字数闸', '{N}'), ('数闸', '{N}'), ('含拍', '{N}'), ('亮点对表', '{N}'), ('亮点界', '{N}'),
     ('亮点在', '{N}'), ('息日链', ''), ('日差哨', ''), ('器物点名', '{N}'), ('外事尺', '--度 {N}'), ('比带', '{N}'),
     ('咬合哨', '')]   # ★1014：381—385 无一章报咬合，推时方红（坑㉖）——合稿时即见
带底 = {'主': 2500, '暗': 2300}


def 正文档(n, root=ROOT):
    from 对账预筛 import 章号
    for f in glob.glob(os.path.join(root, '正文', '*.md')):
        if 章号(f) == n:
            return f
    return None


def 净重(路):
    """⛔另造一把尺（1013 实踩：自写之尺於 380 得 2581，仓之尺 2572）——直取 工具/净重对表.py 之 净重（与检察官同尺）。"""
    import 净重对表
    return 净重对表.净重(路)


def 线(n, root=ROOT):
    t = open(os.path.join(root, '设定', '02_余章之势_总纲.md'), encoding='utf-8').read()
    m = re.search(r'\|\s*%d\s*\|\s*(主|暗)·\d+\s*\|' % n, t)      # ★总纲两栏排（左 381、右 404）——整行逐栏认（1013 实踩：只认左栏，右栏之章认不出）
    return m.group(1) if m else None


def 跑(器, 参, n):
    a = [sys.executable, os.path.join(ROOT, '工具', 器 + '.py')] + 参.format(N=n).split()
    t = time.time()
    try:
        r = subprocess.run(a, cwd=ROOT, capture_output=True, text=True, timeout=300)
        out, rc = (r.stdout + r.stderr), r.returncode
    except subprocess.TimeoutExpired:
        out, rc = '（逾 300 秒未毕）', 124
    末 = [l for l in out.split('\n') if l.strip()]
    return rc, out, (末[-1].strip() if 末 else ''), time.time() - t


def 硬之红(out):
    try:
        d = json.loads(out[out.index('{'):out.rindex('}') + 1])
        return {k: v for k, v in d.items() if isinstance(v, (int, float)) and v > 0}
    except Exception:
        return {'硬闸之印读不出': 1}


def 验(n, root=ROOT):
    出 = []
    for 器, 参, 判 in 致命:
        rc, out, 末, 秒 = 跑(器, 参, n)
        if 判 == '硬':
            h = 硬之红(out)
            红 = bool(h) or rc != 0
            末 = '、'.join('%s %s' % kv for kv in h.items()) if h else '诸格俱零'
        else:
            红 = rc != 0
        出.append(dict(器=器, 类='致命', 红=红, rc=rc, 秒=round(秒, 1), 末=末))
    f = 正文档(n, root)
    if not f:
        出.append(dict(器='厚', 类='致命', 红=True, rc=1, 秒=0, 末='第%d章之正文不在 正文/' % n))
    else:
        w, l = 净重(f), 线(n, root)
        底 = 带底.get(l)
        出.append(dict(器='厚', 类='致命', 红=(底 is None or w < 底), rc=0, 秒=0,
                      末='净重 %d｜%s线带底 %s' % (w, l or '?', 底 if 底 else '（总纲无本章之行）')))
    for 器, 参 in 报:
        rc, out, 末, 秒 = 跑(器, 参, n)
        出.append(dict(器=器, 类='报', 红=rc != 0, rc=rc, 秒=round(秒, 1), 末=末[:200]))
    return 出


def 料全(n, root=ROOT):
    坏 = []
    d = os.path.join(root, '版本', '第%d章' % n)
    if not os.path.exists(os.path.join(d, '_开镜卡.md')):
        坏.append('无开镜卡')
    p = os.path.join(d, '_料.md')
    if not os.path.exists(p):
        坏.append('无章料（先跑 python3 工具/章料.py %d）' % n)
    elif os.path.getsize(p) > 120 * 1024:
        坏.append('章料 %d KB 逾 120KB（坑③）' % (os.path.getsize(p) // 1024))
    for k in (n - 1, n - 2):
        if not 正文档(k, root):
            坏.append('第%d章正文不在' % k)
    return 坏


def 自测():
    ok = 共 = 0
    f = 正文档(380)
    import 净重对表
    共 += 1; ok += (f is not None and 净重(f) == 净重对表.净重(f))                 # 一把尺
    共 += 1; ok += (硬之红('{\n "破折": 0,\n "英文": 2\n}') == {'英文': 2} and 硬之红('乱') == {'硬闸之印读不出': 1})
    共 += 1; ok += all(os.path.exists(os.path.join(ROOT, '工具', x[0] + '.py')) for x in 致命 + 报)
    共 += 1; ok += (线(381) == '暗' and 线(380) == '主' and 线(404) == '主' and 线(405) == '暗' and 线(999) is None)   # 右栏之章亦认
    print('造式验·自测 %d/%d' % (ok, 共))
    return ok == 共


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--自测']:
        sys.exit(0 if 自测() else 1)
    if not a or not a[0].isdigit():
        print(__doc__); sys.exit(2)
    n = int(a[0])
    if '--料' in a:
        坏 = 料全(n)
        print('✓ 第%d章之料全' % n if not 坏 else '⛔ 第%d章之料不全：%s' % (n, '；'.join(坏)))
        sys.exit(0 if not 坏 else 1)
    r = 验(n)
    for x in r:
        print('  %s %-6s %-5s %5.1fs  %s' % ('⛔' if x['红'] else '✓', x['器'], '（致命）' if x['类'] == '致命' else '', x['秒'], x['末']))
    红致 = [x['器'] for x in r if x['红'] and x['类'] == '致命']
    红报 = [x['器'] for x in r if x['红'] and x['类'] == '报']
    print('造式验·第%d章：致命之器%s｜报之器%s' % (n, '俱绿' if not 红致 else '有红（%s）——⛔交' % '、'.join(红致),
                                         '俱绿' if not 红报 else '有红（%s）——治或写明其由' % '、'.join(红报)))
    if '--json' in a:
        print(json.dumps(r, ensure_ascii=False))
    sys.exit(1 if 红致 else 0)
