#!/usr/bin/env python3
"""记料（1015 立·W33）——零 token：把记席九件事要翻的诸账之相关段一次汇成一档，记席一回读毕、⛔逐档翻找。

为何立：W24／W27／W31 三份复盘皆点「记席居诸席之首」（386 $5.26／45 回→387 $5.64／51 回→388 $6.09／63 回）；
  1015 量 388 记席之 63 回：取证与翻账 26、跑器 14、其他 14、写 6、读 3——四成回数花在逐份翻找
  「前章回执之式、施工表 N-1 之锁定行与悬账、全书记忆五档之相关段、轮记与行家评、圣经之锚、检察官之行、下一章之段案与总纲」，
  每翻一回重读整份上下文（坑㉚ 之同类：席以零碎之活办多档）。执笔有章料（一档汇齐），记席无——本器即记席之章料。
⛔限：只汇、⛔判；所汇皆逐字抄自盘上之档（章:行可查）；封版.py N --前 之印⛔汇（其有存版之副作用，记席自跑）。

用法：
  python3 工具/记料.py N          # → 版本/第N章/_记料.md
  python3 工具/记料.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, re, glob, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
表 = os.path.join('设定', '01_镇冢秘术_逐章施工与伏笔回收表.md')
记 = os.path.join('设定', '全书记忆')
限 = 150 * 1024


def 读(p, root=ROOT):
    p = os.path.join(root, p)
    return open(p, encoding='utf-8').read() if os.path.exists(p) else ''


def 行们(文, 式, 上=0, 下=0, 最多=None):
    """文里合式之行（连上下文），带行号。"""
    L = 文.split('\n'); 出 = []; 已 = set()
    for i, l in enumerate(L):
        if re.search(式, l):
            for k in range(max(0, i - 上), min(len(L), i + 下 + 1)):
                if k not in 已:
                    已.add(k); 出.append('%d｜%s' % (k + 1, L[k]))
            if 最多 and len(出) >= 最多:
                break
    return '\n'.join(出)


def 节(标, 体):
    return '\n## %s\n\n%s\n' % (标, 体.strip() or '（无）')


def 章白(n, root=ROOT):
    import 章料
    f = 章料.章档(n, root)
    if not f:
        return '', ''
    t = open(f, encoding='utf-8').read()
    return f, t.split('【本章亮点】')[0]


def 汇(N, root=ROOT):
    import 章料
    f, 白 = 章白(N, root)
    出 = ['# 记料·第%d章（零 token 所汇·工具/记料.py）' % N, '',
          '> 记席之九件事所要翻的诸账，於此一档；逐字抄自盘上（章:行可查）。⛔再逐档翻找——缺者方以 `sed -n` 补，并记其缺（交主环补器）。'
          '封版.py %d --前 之印⛔在此（其有存版之副作用），记席自跑。' % N]
    # 一、前章回执之式
    前回 = sorted(glob.glob(os.path.join(root, '设定', '回执_*_第%d章封版席.md' % (N - 1))))
    if 前回:
        t = open(前回[-1], encoding='utf-8').read()
        出.append(节('一·前章回执之式（%s：其节目与首二节；全文照此式写）' % os.path.relpath(前回[-1], root),
                    '\n'.join(l for l in t.split('\n') if l.startswith('#')) + '\n\n' + '\n'.join(t.split('\n')[:40])))
    # 二、施工表
    T = 读(表, root)
    出.append(节('二·施工表：N-1 之锁定行与悬账（式样）、本章与下一章之硬门槛（落笔处）',
                行们(T, r'^\| %d \| (锁定|悬账) \|' % (N - 1)) + '\n\n' +
                行们(T, r'^## 四、续写第 (%d|%d) 章前的硬门槛' % (N, N + 1), 0, 3)))
    # 三、创作记录与席记之式
    出.append(节('三·前章创作记录（首三十行）与席记（式样）',
                '\n'.join(读(os.path.join('版本', '第%d章' % (N - 1), '_创作记录.md'), root).split('\n')[:30]) + '\n\n' +
                读(os.path.join('版本', '第%d章' % (N - 1), '_席记.json'), root)))
    # 四、全书记忆
    用法 = '\n'.join(读(os.path.join(记, '用法.md'), root).split('\n')[:60])
    前章记 = 读(os.path.join(记, '第%d章.md' % (N - 1)), root)
    总览 = 读(os.path.join(记, '总览.md'), root)
    出.append(节('四·全书记忆：用法（首六十行）、前章之记（式样）、总览之首与索引之末',
                用法 + '\n\n〔第%d章.md〕\n' % (N - 1) + 前章记 + '\n\n〔总览·首十四行〕\n' + '\n'.join(总览.split('\n')[:14]) +
                '\n\n〔总览·「全书今之末」「下一章」与索引末五行〕\n' + 行们(总览, r'全书今之末|下一章', 0, 1, 12) + '\n' +
                '\n'.join('%d｜%s' % (i + 1, l) for i, l in list(enumerate(总览.split('\n')))[-8:])))
    # 五、在场之人：人物、状态册
    册 = {}
    try:
        册 = json.load(open(os.path.join(root, '设定', '人物状态册.json'), encoding='utf-8'))
    except Exception:
        pass
    人们 = []
    for v in (册.get('人物') or [] if isinstance(册, dict) else []):     # ★册之式：{"人物":[{名、别称、末见章、N态…}]}
        if not isinstance(v, dict):
            continue
        称们 = [v.get('名') or ''] + [x for x in re.split(r'[、，,／/\s]+', str(v.get('别称') or '')) if x]
        中 = [x for x in 称们 if len(x) >= 2 and x in 白]
        if 中:
            人们.append((v.get('名') or 中[0], 中, v))
    人物 = 读(os.path.join(记, '人物.md'), root)
    体 = []
    for 名, 中, v in 人们:
        体.append('### %s（白文所见之称：%s｜末见章 %s）' % (名, '、'.join(中), v.get('末见章')))
        体.append(行们(人物, r'^#+ .*%s' % re.escape(名), 0, 2, 3))
        态 = sorted([x for x in v if re.match(r'\d+态$', x)], key=lambda x: int(re.match(r'\d+', x).group()))[-1:]
        for x in 态:
            体.append('状态册·%s：%s' % (x, str(v[x])[:600]))
    出.append(节('五·本章白文里出现之人（人物.md 之节首、状态册之末态）——须添「%d态」者' % N, '\n'.join(体)))
    # 六、物件、悬线
    物件 = 读(os.path.join(记, '物件.md'), root)
    悬线 = 读(os.path.join(记, '悬线.md'), root)
    钉 = '|'.join(str(x) for x in range(N, N + 7))
    出.append(节('六·物件之末两块「N 之物」、悬线钉在 %d—%d 之行' % (N, N + 6),
                行们(物件, r'(%d|%d) 之物' % (N - 1, N - 2), 0, 6) + '\n\n' + 行们(悬线, r'(^|[^\d])(%s)([^\d]|$)' % 钉, 0, 0, 60)))
    # 七、轮记、行家评
    轮 = 读(os.path.join('版本', '第%d章' % N, '_轮记.md'), root)
    评 = 读(os.path.join('版本', '第%d章' % N, '_行家评.md'), root)
    出.append(节('七·本章轮记之节目与首十行、行家评之名次',
                '\n'.join(l for l in 轮.split('\n') if l.startswith('#')) + '\n\n' + '\n'.join(轮.split('\n')[:10]) + '\n\n' +
                行们(评, r'^#+ *名次|^\d+\. *稿|名次', 0, 2, 20)))
    # 八、圣经之锚、检察官之行、open_brief
    圣 = 读(os.path.join('设定', '00_镇冢秘术_唯一总圣经.md'), root)
    检 = 读(os.path.join('工具', '小说检察官.py'), root)
    try:
        canon = json.load(open(os.path.join(root, '设定', 'canon事实库.json'), encoding='utf-8'))
        ob = canon.get('open_brief') if isinstance(canon, dict) else None
    except Exception:
        canon, ob = {}, None
    出.append(节('八·圣经之锚与事件链之题、检察官里本章与下一章之行、open_brief（今之块）',
                行们(圣, r'第 (%d|%d) 章必须从|^## 十一、已写 1—|第 %d 章《' % (N, N + 1, N - 1), 0, 2, 12) + '\n\n' +
                行们(检, r'^ (%d|%d):' % (N, N + 1), 0, 0, 20) + '\n\n' +
                (json.dumps(ob, ensure_ascii=False, indent=1)[:4000] if ob else '（open_brief 不在）')))
    # 九、下一章：段案、总纲
    段 = ''
    for p in sorted(glob.glob(os.path.join(root, '设定', '段案', '*.md'))):
        t = open(p, encoding='utf-8').read()
        m = re.search(r'^## %d\n(.*?)(?=^## \d+|\Z)' % (N + 1), t, re.S | re.M)
        if m:
            段 = '〔%s〕\n## %d\n%s' % (os.path.relpath(p, root), N + 1, m.group(1).strip()); break
    纲 = 读(os.path.join('设定', '02_余章之势_总纲.md'), root)
    出.append(节('九·下一章（%d）：段案之节、总纲之行；开镜卡以「python3 工具/第零轮开镜庭.py --立 %d」起' % (N + 1, N + 1),
                (段 or '（段案无其节）') + '\n\n' + 行们(纲, r'\| *(%d|%d) *\|' % (N + 1, N + 2), 0, 0, 6)))
    # ★1015（391 记席「此法之缺」：同线前章之白文、在场之人之册行、canon 卡名，各自 awk／python 补约六回）
    import 造式验
    本线 = 造式验.线(N, root)
    同 = next((k for k in range(N - 1, N - 13, -1) if 本线 and 造式验.线(k, root) == 本线), None)
    if 同 and 同 != N - 1:
        _, 同白 = 章白(同, root)
        出.append(节('十·同线前章（第%d章）之白文——承前之判（开轮⑮）、极短段之比、收句之骨' % 同, 同白))
    行 = []
    for 名, 中, v in 人们:
        体2 = {k: v[k] for k in v if not re.match(r'\d+态$', k)}
        态2 = sorted([x for x in v if re.match(r'\d+态$', x)], key=lambda x: int(re.match(r'\d+', x).group()))[-2:]
        体2.update({x: v[x] for x in 态2})
        行.append(json.dumps(体2, ensure_ascii=False))
    if 行:
        出.append(节('十一·人物状态册之行（在场之人；去旧态、留末二态——添「%d态」照此式）' % N, '\n'.join(行)))
    try:
        卡们 = [c for c in ((canon or {}).get('state_canon') or []) if isinstance(c, dict)]
    except Exception:
        卡们 = []
    名们 = [x for _, 中, _ in 人们 for x in 中]
    近 = [c.get('what', '') for c in 卡们 if (isinstance(c.get('from'), int) and c['from'] >= N - 15) or any(x in str(c.get('what', '')) for x in 名们)]
    if 近:
        出.append(节('十二·canon state_canon 卡名（近十五章所立、或提在场之人者；open_brief 之 required_state_cards 照此择）', '\n'.join('- ' + x for x in 近[-80:])))
    return '\n'.join(出)


def 自测():
    ok = 共 = 0
    共 += 1; ok += 行们('a\nb 12\nc', r'12', 1, 1) == '1｜a\n2｜b 12\n3｜c'
    共 += 1; ok += 节('甲', '') == '\n## 甲\n\n（无）\n'
    t = 汇(388)
    共 += 1; ok += all(k in t for k in ('一·前章回执之式', '| 387 | 锁定 |', '四·全书记忆', '五·本章白文里出现之人', '九·下一章（389）'))
    共 += 1; ok += ('### 刘二' in t or '### 钱满' in t)                  # 在场之人认得出（册之式 1015 自测逮：旧当作 dict）
    共 += 1; ok += len(t.encode()) <= 限
    print('记料·自测 %d/%d（388 之记料 %d 字节）' % (ok, 共, len(t.encode())))
    return ok == 共


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--自测']:
        sys.exit(0 if 自测() else 1)
    if len(a) == 1 and a[0].isdigit():
        N = int(a[0]); t = 汇(N)
        p = os.path.join(ROOT, '版本', '第%d章' % N, '_记料.md')
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w', encoding='utf-8').write(t)
        b = len(t.encode())
        print('✓ 写 %s（%d KB）%s' % (os.path.relpath(p, ROOT), b // 1024, '' if b <= 限 else '　⛔逾 150KB（坑③）'))
        sys.exit(0 if b <= 限 else 1)
    print(__doc__); sys.exit(2)
