#!/usr/bin/env python3
"""工作流账（0930·作者令「GitHub 为唯一之记忆；已做者绝不重做、不覆盖；中断可无缝续；要有一个机制保证」）

账在 设定/工作流账.json：每一件有 id、名、目的、状态（未始／进行／已成）、产出、验、续之令、依。
本器：
  python3 工具/工作流账.py            # 印：已成／进行／可开（依已满）／待依，与每件之续之令——每回会话开头先跑它
  python3 工具/工作流账.py --查       # 核：凡「已成」者，产出逐件核在（目录够数、档在、收束之语在档尾）；核不过即红（入全测）
  python3 工具/工作流账.py --标 W04 已成   # 改状态（标「已成」前先自核，核不过拒标）
  python3 工具/工作流账.py --自测
⛔「已成」须真成：档在不算，收束之语在档尾才算（0930 病册第八册被截断而误报全成之教）。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys, json, glob, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
账档 = os.path.join('设定', '工作流账.json')


def 读(root=ROOT):
    return json.load(open(os.path.join(root, 账档), encoding='utf-8'))


def 核件(件, root=ROOT):
    缺 = []
    for p in 件.get('产出', []):
        if '目录' in p:
            d = os.path.join(root, p['目录'])
            n = len([x for x in glob.glob(os.path.join(d, '*')) if os.path.isfile(x)]) if os.path.isdir(d) else 0
            if n < p.get('至少', 1):
                缺.append('%s 只 %d 档（须 ≥%d）' % (p['目录'], n, p.get('至少', 1)))
        if '档' in p:
            f = os.path.join(root, p['档'])
            if not os.path.exists(f):
                缺.append('%s 不在' % p['档']); continue
            if p.get('收束'):
                尾 = open(f, encoding='utf-8', errors='replace').read()[-3000:]
                if p['收束'] not in 尾:
                    缺.append('%s 档尾无收束「%s」（疑未写完）' % (p['档'], p['收束']))
    return 缺


def 查(root=ROOT):
    红 = []
    for 件 in 读(root)['件']:
        if 件['状态'] == '已成':
            缺 = 核件(件, root)
            if 缺:
                红.append('%s %s：%s' % (件['id'], 件['名'], '；'.join(缺)))
    return 红


def 印(root=ROOT):
    账 = 读(root)
    成 = {x['id'] for x in 账['件'] if x['状态'] == '已成'}
    print('════ 工作流账 ════（GitHub 为唯一之记忆；已成者⛔重做）')
    print('宗旨：' + 账['宗旨'])
    for 类, 条 in (('✓ 已成', lambda x: x['状态'] == '已成'),
                  ('▶ 进行中（先续它）', lambda x: x['状态'] == '进行'),
                  ('○ 可开（依已满）', lambda x: x['状态'] == '未始' and set(x.get('依', [])) <= 成),
                  ('… 待依', lambda x: x['状态'] == '未始' and not set(x.get('依', [])) <= 成)):
        组 = [x for x in 账['件'] if 条(x)]
        if not 组:
            continue
        print('\n' + 类)
        for x in 组:
            print('  %s %s——%s' % (x['id'], x['名'], x['目的']))
            if x['状态'] != '已成' or 类.startswith('✓') is False:
                print('     续之令：' + x['续之令'])
            if x['状态'] == '未始' and not set(x.get('依', [])) <= 成:
                print('     待：' + '、'.join(sorted(set(x['依']) - 成)))
    红 = 查(root)
    print('\n' + ('⛔ 已成而核不过：' + '｜'.join(红) if 红 else '✓ 凡已成者皆核过'))


def 标(i, 态, root=ROOT):
    p = os.path.join(root, 账档)
    账 = json.load(open(p, encoding='utf-8'))
    for x in 账['件']:
        if x['id'] == i:
            if 态 == '已成':
                缺 = 核件(x, root)
                if 缺:
                    print('⛔ 拒标已成：' + '；'.join(缺)); return False
            x['状态'] = 态
            json.dump(账, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            print('✓ %s → %s' % (i, 态)); return True
    print('⛔ 无此件：' + i); return False


def 自测():
    ok = 共 = 0
    t = tempfile.mkdtemp()
    try:
        os.makedirs(os.path.join(t, '设定'))
        账 = {'宗旨': '测', '件': [{'id': 'A', '名': '甲', '目的': '测', '状态': '已成', '产出': [{'档': '设定/甲.md', '收束': '总判'}], '续之令': '无', '依': []}]}
        json.dump(账, open(os.path.join(t, 账档), 'w'), ensure_ascii=False)
        共 += 1; ok += (len(查(t)) == 1)                                  # 档不在 → 红
        open(os.path.join(t, '设定', '甲.md'), 'w').write('写到一半')
        共 += 1; ok += (len(查(t)) == 1 and '收束' in 查(t)[0])           # 截断 → 红
        open(os.path.join(t, '设定', '甲.md'), 'a').write('\n## 总判\n完')
        共 += 1; ok += (查(t) == [])
        账['件'][0]['状态'] = '进行'; 账['件'][0]['产出'] = [{'档': '设定/乙.md', '收束': '毕'}]
        json.dump(账, open(os.path.join(t, 账档), 'w'), ensure_ascii=False)
        共 += 1; ok += (标('A', '已成', t) is False)                         # 未成拒标
    finally:
        shutil.rmtree(t)
    print('工作流账·自测 %d/%d' % (ok, 共))
    return ok == 共


if __name__ == '__main__':
    a = sys.argv[1:]
    if a == ['--自测']:
        sys.exit(0 if 自测() else 1)
    if a == ['--查']:
        红 = 查()
        if 红:
            print('⛔ 工作流账：已成而核不过 %d 件：%s' % (len(红), '｜'.join(红))); sys.exit(1)
        print('✓ 工作流账：凡已成者，产出皆在且收束俱全'); sys.exit(0)
    if len(a) == 3 and a[0] == '--标':
        sys.exit(0 if 标(a[1], a[2]) else 1)
    印()
