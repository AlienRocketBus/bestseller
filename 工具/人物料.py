#!/usr/bin/env python3
"""人物料（1015 立·W34·作者令「每个角色都要有独特的一面、让读者记住；⛔反智；照灭霸之反派、红楼梦之群像，写时不停地看人物设计得完美没有」）——零 token。

为何立：审一个人物要翻五处——全书记忆/人物.md 之节、人物状态册之条、圣经「七、人物唯一档案」之节、
  三百多份章记里此人之拍与要句、总纲与余章总案里此人之将来；席逐档翻找即坑㉚（席以零碎之活办多档）。
  本器把一人之五处汇成一档，审人之席一回读毕；每回大审之人物之审亦用之。
⛔限：只汇、⛔判；逐字抄自盘上之档（档:行可查）；逾限之行照实印其数（⛔静默截）。

用法：
  python3 工具/人物料.py 名 [--出 目录]      # → 设定/_草/人物料/<名>.md
  python3 工具/人物料.py --全 [--出 目录]    # 主要诸人
  python3 工具/人物料.py --全 --薄           # 只前四处（历章由人物链代之）
  python3 工具/人物料.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, re, glob, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
记 = os.path.join('设定', '全书记忆')
圣经 = os.path.join('设定', '00_镇冢秘术_唯一总圣经.md')
默出 = os.path.join('设定', '_草', '人物料')
限 = 140 * 1024

# 名：(章记里认此人之称、圣经「七、人物唯一档案」之节首式、人物.md 之节首式、状态册之名)
主要 = {
    '苏衍': (['苏衍', '衍娃子', '苏记者'], r'### 1\. 苏衍', r'### 苏衍', '苏衍'),
    '老头': (['老头', '独眼'], r'### 3\. 独眼老头', r'### 老头', '老头'),
    '钱满': (['钱满'], r'### 10\. 钱满', r'### 钱满', '钱满'),
    '刘二': (['刘二'], r'### 12\. 刘二', r'### 刘二', '刘二'),
    '东头': (['东头'], r'### 13\. 东头', r'### 东头', '东头'),
    '沈鸢': (['沈鸢'], r'### 2\. 沈鸢', r'### 沈鸢', '沈鸢'),
    '床上那人': (['床上那', '阿禾'], r'### 14\. 床上那人', r'### 床上那人', '床上那个人（暗线）'),
    '霍钧': (['霍钧'], r'### 8\. 霍钧', r'### 霍钧', '霍钧'),
    '黎东来': (['黎东来'], r'### 9\. 黎东来', r'### 黎东来', '黎东来'),
    '赵阙': (['赵阙', '门後', '门后之物'], r'### 7\. 赵阙', r'- \*\*门後之物', '赵阙'),
    '测绘那个年轻人': (['测绘'], None, r'### 测绘', '测绘那个年轻人'),
}


def 读(p, root=ROOT):
    p = os.path.join(root, p)
    return open(p, encoding='utf-8').read() if os.path.exists(p) else ''


def 节(文, 首式, 止式=r'^#{2,3} '):
    """自合首式之行起，至下一个同级以上之节首止（其间之 #### 小节属之）；带行号。"""
    if not 首式:
        return ''
    L = 文.split('\n')
    for i, l in enumerate(L):
        if re.match(首式, l):
            出 = ['%d｜%s' % (i + 1, l)]
            for k in range(i + 1, len(L)):
                if re.match(止式, L[k]) or (首式.startswith('- ') and L[k].startswith('- **')):
                    break
                出.append('%d｜%s' % (k + 1, L[k]))
            return '\n'.join(出).rstrip()
    return ''


def 册条(名, root=ROOT):
    try:
        册 = json.load(open(os.path.join(root, '设定', '人物状态册.json'), encoding='utf-8'))
    except Exception:
        return ''
    for v in 册.get('人物') or []:
        if isinstance(v, dict) and v.get('名') == 名:
            态 = sorted([x for x in v if re.match(r'\d+态$', x)], key=lambda x: int(re.match(r'\d+', x).group()))
            体 = {k: v[k] for k in v if not re.match(r'\d+态$', k)}
            出 = json.dumps(体, ensure_ascii=False, indent=1)
            for x in 态[-3:]:
                出 += '\n%s：%s' % (x, str(v[x])[:900])
            return 出 + ('\n（态 %d 条，此印末三）' % len(态) if 态 else '')
    return ''


def 章记之行(称们, root=ROOT, 每章=4, 每行=200):
    """每章记里提此人之行：先「一句之要」「要句」，再「发生了什么」。→ [(章, 级, 行)]"""
    出 = []
    for f in glob.glob(os.path.join(root, 记, '第*章.md')):
        m = re.search(r'第(\d+)章\.md$', f)
        if not m:
            continue
        n = int(m.group(1)); t = open(f, encoding='utf-8').read()
        段们 = {}
        for 名, 体 in re.findall(r'^## ([^\n]+)\n(.*?)(?=^## |\Z)', t, re.M | re.S):
            段们[名.split('（')[0].strip()] = 体
        取 = []
        for 段名, 级 in (('一句之要', 0), ('要句', 0), ('发生了什么', 1), ('本章之新知', 1)):
            for l in (段们.get(段名) or '').split('\n'):
                l = l.strip()
                if l and any(c in l for c in 称们):
                    取.append((级, 段名, l[:每行]))
        取.sort(key=lambda x: x[0])
        for 级, 段名, l in 取[:每章]:
            出.append((n, 级, '%s·%s' % (段名, l)))
    return sorted(出)


def 将来之行(称们, root=ROOT, 最多=60, 每行=320):
    出 = []
    for p in (os.path.join('设定', '02_余章之势_总纲.md'), os.path.join('设定', '剧情庭_余章总案.md')):
        L = 读(p, root).split('\n'); k = 0
        for i, l in enumerate(L):
            if any(c in l for c in 称们):
                出.append('%s:%d｜%s' % (os.path.basename(p), i + 1, l.strip()[:每行])); k += 1
                if k >= 最多:
                    出.append('（%s 尚有提此人之行，未印）' % os.path.basename(p)); break
    return '\n'.join(出)


def 汇(名, root=ROOT, 薄=False):
    称们, 圣首, 人首, 册名 = 主要[名]
    人物 = 读(os.path.join(记, '人物.md'), root)
    圣 = 读(圣经, root)
    出 = ['# 人物料·%s（零 token 所汇·工具/人物料.py）' % 名, '',
          '> 一人之五处於此一档：人物.md 之节、状态册之条、圣经「七、人物唯一档案」之节、章记里此人之拍与要句、总纲与余章总案里此人之将来。'
          '逐字抄自盘上（档:行可查）。要读白文，照章号取 `正文/` 之档（⛔通读全书）。']
    出.append('\n## 一·全书记忆/人物.md 之节（至今之状）\n\n' + (节(人物, 人首) or '（无）'))
    出.append('\n## 二·人物状态册之条\n\n' + (册条(册名, root) or '（无）'))
    圣节 = 节(圣, 圣首) if 圣首 else ''
    圣他 = []
    for i, l in enumerate(圣.split('\n')):
        if any(c in l for c in 称们) and not (圣节 and ('%d｜' % (i + 1)) in 圣节):
            圣他.append('%d｜%s' % (i + 1, l.strip()[:300]))
    出.append('\n## 三·圣经之节（设定）\n\n' + (圣节 or '（圣经「七」无此人之节）') +
             '\n\n### 圣经他处提此人之行（各截 300 字）\n\n' + '\n'.join(圣他[:80]) +
             ('\n（尚有 %d 行未印）' % (len(圣他) - 80) if len(圣他) > 80 else ''))
    出.append('\n## 四·将来：总纲、余章总案提此人之行\n\n' + (将来之行(称们, root) or '（无）'))
    if 薄:                       # ★W34 再换法：历章由人物链（工具/人物链.py --并记，全书无舍）代之
        出.append('\n## 五·历章\n\n见人物链：`设定/全书记忆/人物链/%s.md`（自第 1 章至末章，章记「在场之人」零 token 所并，⛔舍）' % 名)
        return '\n'.join(出)
    行们 = 章记之行(称们, root)
    章们 = sorted({n for n, _, _ in 行们})
    头 = '\n'.join(出)
    # ★先「一句之要」「要句」（级 0），再「发生了什么」「新知」（级 1）按章轮取——满限则舍级 1 之後轮，⛔舍後头之章（1015 自测逮：旧按章序填，主角诸人 300 章後全舍）
    次 = {}; 序 = []
    for n, 级, l in 行们:
        次[(n, 级)] = 次.get((n, 级), 0) + 1
        序.append((级, 次[(n, 级)], n, l))
    序.sort(key=lambda x: (x[0], x[1], -x[2]))        # 同轮先近章（早章已缩在人物.md 之节）
    取 = []; 已 = len(头.encode()) + 600; 舍 = 0
    for 级, k, n, l in 序:
        s = '%d｜%s' % (n, l)
        if 已 + len(s.encode()) + 1 > 限:
            舍 += 1; continue
        取.append((n, 级, k, s)); 已 += len(s.encode()) + 1
    体 = [x[3] for x in sorted(取)]
    出.append('\n## 五·历章：章记里此人之行（%d 章：%s）\n\n' % (len(章们), _段(章们)) + '\n'.join(体) +
             ('\n\n（逾 140KB 之限，舍 %d 行——要者照章号取 `设定/全书记忆/第N章.md`）' % 舍 if 舍 else ''))
    return '\n'.join(出)


def _段(ns):
    """[1,2,3,7,8] → 1—3、7—8"""
    出 = []; i = 0
    while i < len(ns):
        j = i
        while j + 1 < len(ns) and ns[j + 1] == ns[j] + 1:
            j += 1
        出.append(str(ns[i]) if i == j else '%d—%d' % (ns[i], ns[j])); i = j + 1
    return '、'.join(出)


def 写(名, 出目, root=ROOT, 薄=False):
    t = 汇(名, root, 薄)
    p = os.path.join(root, 出目, '%s.md' % 名)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8').write(t)
    return p, len(t.encode())


def 自测():
    ok = 共 = 0
    共 += 1; ok += _段([1, 2, 3, 7, 8, 10]) == '1—3、7—8、10'
    共 += 1; ok += 节('# 甲\n### 1. 乙\n一\n#### 丙\n二\n### 2. 丁\n三', r'### 1\. 乙') == '2｜### 1. 乙\n3｜一\n4｜#### 丙\n5｜二'
    t = 汇('黎东来')
    共 += 1; ok += all(k in t for k in ('第二个秦始皇', '## 五·历章', '277'))       # 圣经之核、章记之镜章俱在
    t2 = 汇('刘二')
    共 += 1; ok += ('说话之式' in t2 and '183' in t2)
    共 += 1; ok += max(len(汇(n).encode()) for n in ('苏衍', '老头')) <= 限
    print('人物料·自测 %d/%d' % (ok, 共))
    return ok == 共


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--自测']:
        sys.exit(0 if 自测() else 1)
    出目 = a[a.index('--出') + 1] if '--出' in a else 默出
    名们 = list(主要) if '--全' in a else [x for x in a if x in 主要]
    if not 名们:
        print(__doc__); print('主要：' + '、'.join(主要)); sys.exit(2)
    for 名 in 名们:
        p, b = 写(名, 出目, 薄='--薄' in a)
        print('✓ %s（%d KB）' % (os.path.relpath(p, ROOT), b // 1024))
