#!/usr/bin/env python3
"""工作流账（0930·作者令「GitHub 为唯一之记忆；已做者绝不重做、不覆盖；中断可无缝续；要有一个机制保证」）

账在 设定/工作流账.json：每一件有 id、名、目的、状态（未始／进行／已成）、产出、验、续之令、依。
本器：
  python3 工具/工作流账.py            # 印：已成／进行／可开（依已满）／待依，与每件之续之令——每回会话开头先跑它
  python3 工具/工作流账.py --查       # 核：凡「已成」者，产出逐件核在（目录够数、档在、收束之语在档尾）；核不过即红（入全测）
  python3 工具/工作流账.py --标 W04 已成   # 改状态（标「已成」前先自核，核不过拒标）
  python3 工具/工作流账.py --开 W16 8 "停止线" "重造之法" "有效之据" "预估"   # 开一件：先印 D6 之痛与开法四问，缺一拒开
  python3 工具/工作流账.py --裁 W15 取|重造|续 "由" [新时限]   # 到点必裁：达标则取；不达标则毁了重造（取其精华、换法、重起计时）；续至多一回
  python3 工具/工作流账.py --自测
★D6 之痛·止损闸（1008 作者令「三十小时零结果，永远的痛；必须有应对机制，灵活变通」）：
  凡「进行」之件须有 起、时限、停止线、换法（开法三问）；逾时限而未裁 → --查 红（入全测，推不上去），
  逼总编辑到点必裁：取（达标）／重造（毁了重造，取其精华）／续（至多一回）。⛔烂尾：没有「守原了事」「不干了」这一出口——
  问题必须解决；重造两回仍不达标 → 报作者商量新路，仍⛔撂下。⛔不裁而任其空转。
  ★防此病最要紧的一招在开头：造时就造到满分（作者 1008：垃圾再怎么修也修不好；大厦一开始就造到质量过硬，就不会塌）。
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


D6之痛 = ('⛔⛔ 永远的痛·D6 床上那人：三十多小时、三千多万 token、九轮，一事无成。'
          '病在方法——拿修去救骨子不行的旧案，同一个法子死跑九轮，没有一处到点必停、必裁、必换。'
          '防它最要紧的一招在开头：造时就造到满分、挑不出毛病；造出垃圾就毁了重造（取其精华），⛔修。'
          '其次：每开一法先答三问，到点必裁（取或重造，⛔烂尾），两次不成即换法，只看产出不看过程。')
开法三问 = ('①时限：几小时内必须出结果？②停止线：到哪一步、什么数就算成（取）？'
          '③重造之法：到点没成、或同法两次不成，怎么毁了重造（取其精华、换成什么法）？'
          '（先查 设定/方法账.md 同类最优者）④虫洞之律（选法第一原则）：此法是否效果更好、且花费更少？凭什么确定（有据，⛔凭感觉）？预估几时、多少 token？⛔笨办法——两样都满足才开'
          '（另问自己：这一回造出来的，是不是已经满分、挑不出毛病？是在造，还是在补一辆垃圾车？）')


def _时(s):
    import datetime as _d
    return _d.datetime.strptime(s, '%Y-%m-%dT%H:%MZ').replace(tzinfo=_d.timezone.utc)


def _今():
    import datetime as _d
    return _d.datetime.now(_d.timezone.utc)


def 已跑时(件, 今=None):
    return ((今 or _今()) - _时(件['起'])).total_seconds() / 3600


def 止损(件, 今=None):
    """→ 红之由（空串＝不红）。只管「进行」之件。"""
    if 件['状态'] != '进行':
        return ''
    缺 = [k for k in ('起', '时限', '停止线', '换法') if not 件.get(k)]
    if 缺:
        return '开法未答三问（缺 %s）' % '、'.join(缺)
    跑 = 已跑时(件, 今)
    if 跑 > float(件['时限']):
        return '已跑 %.1f 时，逾时限 %s 时而未裁——到点必裁：取／重造／续（续至多一回；⛔烂尾）' % (跑, 件['时限'])
    return ''


def 查(root=ROOT, 今=None):
    红 = []
    for 件 in 读(root)['件']:
        if 件['状态'] == '已成':
            缺 = 核件(件, root)
            if 缺:
                红.append('%s %s：%s' % (件['id'], 件['名'], '；'.join(缺)))
        由 = 止损(件, 今)
        if 由:
            红.append('%s %s：D6之痛·%s' % (件['id'], 件['名'], 由))
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
            if x['状态'] == '进行' and x.get('起') and x.get('时限'):
                跑 = 已跑时(x)
                print('     ⏱ 已跑 %.1f 时／时限 %s 时｜停止线：%s｜换法：%s%s' % (
                    跑, x['时限'], x.get('停止线', '（缺）'), x.get('换法', '（缺）'),
                    '　⛔⛔逾时——D6 之痛：到点必裁，⛔任其空转' if 跑 > float(x['时限']) else ''))
            if x['状态'] == '未始' and not set(x.get('依', [])) <= 成:
                print('     待：' + '、'.join(sorted(set(x['依']) - 成)))
    红 = 查(root)
    print('\n' + ('⛔ 账红：' + '｜'.join(红) if 红 else '✓ 凡已成者皆核过；凡进行者皆在时限内'))
    print(D6之痛)


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


def _存(账, root):
    json.dump(账, open(os.path.join(root, 账档), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def 开(i, 时限, 停止线, 换法, 有效之据='', 预估='', root=ROOT, 今=None):
    print(D6之痛); print('开法四问：' + 开法三问)
    try:
        时限 = float(时限)
    except (TypeError, ValueError):
        时限 = 0
    if 时限 <= 0 or not all((x or '').strip() for x in (停止线, 换法, 有效之据, 预估)):
        print('⛔ 拒开：四问未答全（时限须 >0 时；停止线、重造之法、有效之据、预估皆须写）'); return False
    账 = 读(root)
    for x in 账['件']:
        if x['id'] == i:
            x.update({'状态': '进行', '起': (今 or _今()).strftime('%Y-%m-%dT%H:%MZ'), '时限': 时限,
                      '停止线': 停止线.strip(), '换法': 换法.strip(), '有效之据': 有效之据.strip(), '预估': 预估.strip()})
            x.setdefault('裁', [])
            _存(账, root); print('✓ %s 开：时限 %g 时' % (i, 时限)); return True
    print('⛔ 无此件：' + i); return False


def 裁(i, 法, 由, 新时限=None, root=ROOT, 今=None):
    if 法 == '守原':
        print('⛔ 无「守原」之出口——作者 1008：留下烂摊子不干了即烂尾。原文果真已达标，以「取」裁之并写由；否则「重造」'); return False
    if 法 not in ('取', '重造', '续') or not (由 or '').strip():
        print('⛔ 裁须为 取／重造／续 之一，且须写由'); return False
    账 = 读(root)
    for x in 账['件']:
        if x['id'] != i:
            continue
        记 = x.setdefault('裁', [])
        今s = (今 or _今()).strftime('%Y-%m-%dT%H:%MZ')
        if 法 == '续':
            if any(r['法'] == '续' and r.get('起') == x.get('起') for r in 记):
                print('⛔ 已续过一回——D6 之痛：再续即空转。只许 取／重造'); return False
            try:
                加 = float(新时限)
            except (TypeError, ValueError):
                print('⛔ 续须给新加之时（时）'); return False
            x['时限'] = float(x.get('时限', 0)) + 加
        elif 法 == '重造':
            if sum(1 for r in 记 if r['法'] == '重造') >= 2:
                print('⛔ 已重造两回仍未达标——报作者商量新路（⛔撂下、⛔烂尾）'); return False
            try:
                x['时限'] = float(新时限)
            except (TypeError, ValueError):
                print('⛔ 重造须给新之时限（时）'); return False
            x['起'] = 今s; x['换法'] = 由.strip()
        else:
            x['状态'] = '已成'
        记.append({'时': 今s, '法': 法, '由': 由.strip(), '起': x.get('起')})
        _存(账, root); print('✓ %s 裁：%s' % (i, 法)); return True
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
        import datetime as _d
        T0 = _d.datetime(2026, 1, 1, 0, 0, tzinfo=_d.timezone.utc)
        H = lambda h: T0 + _d.timedelta(hours=h)
        共 += 1; ok += (len(查(t, H(0))) == 1 and '三问' in 查(t, H(0))[0])   # 进行而未答三问 → 红
        共 += 1; ok += (开('A', 0, '停', '换', '据', '估', t, H(0)) is False)    # 时限缺 → 拒开
        共 += 1; ok += (开('A', 6, '停', '换', '', '', t, H(0)) is False)        # 有效之据、预估缺 → 拒开
        共 += 1; ok += (开('A', 6, '停', '换', '据', '估', t, H(0)) is True and 查(t, H(5)) == [])   # 时限内不红
        共 += 1; ok += (len(查(t, H(7))) == 1 and '逾时限' in 查(t, H(7))[0])  # 逾时 → 红
        共 += 1; ok += (裁('A', '续', '由', 3, t, H(7)) is True and 查(t, H(8)) == [])   # 续一回
        共 += 1; ok += (裁('A', '续', '由', 3, t, H(8)) is False)               # 再续拒
        共 += 1; ok += (裁('A', '重造', '新法', 4, t, H(10)) is True and 查(t, H(13)) == [] and len(查(t, H(15))) == 1)
        裁('A', '重造', '又一法', 4, t, H(15))
        共 += 1; ok += (裁('A', '重造', '三法', 4, t, H(20)) is False)          # 重造两回後拒——报作者
        共 += 1; ok += (裁('A', '守原', '由', None, t, H(20)) is False)         # 无守原之出口（⛔烂尾）
        共 += 1; ok += (裁('A', '取', '达标', None, t, H(20)) is True and 读(t)['件'][0]['状态'] == '已成')
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
            print('⛔ 工作流账红 %d 件：%s' % (len(红), '｜'.join(红))); sys.exit(1)
        print('✓ 工作流账：凡已成者，产出皆在且收束俱全；凡进行者皆答三问、皆在时限内'); sys.exit(0)
    if len(a) == 7 and a[0] == '--开':
        sys.exit(0 if 开(a[1], a[2], a[3], a[4], a[5], a[6]) else 1)
    if len(a) in (4, 5) and a[0] == '--裁':
        sys.exit(0 if 裁(a[1], a[2], a[3], a[4] if len(a) == 5 else None) else 1)
    if len(a) == 3 and a[0] == '--标':
        sys.exit(0 if 标(a[1], a[2]) else 1)
    印()
