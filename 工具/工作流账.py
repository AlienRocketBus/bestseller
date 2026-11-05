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
import os, sys, io, re, json, glob, tempfile, shutil

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
        if 件['状态'] != '已成' and not str(件.get('续之令', '')).strip():
            红.append('%s %s：缺续之令（断後无从续）' % (件['id'], 件['名']))
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
    try:   # ★1021 费哨（裁_1021_省律·七三之律）：每回会话开头先见钱落在哪
        import 费哨
        print(费哨.判(root)[1])
    except Exception as _e:
        print('费哨：跑不得（%s）' % _e)
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
                print('     续之令：' + x.get('续之令', '（缺——⛔见账红）'))
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
    # ★1009 坑⑭：作者之暂停令在盘上——在即拒开（⛔靠人记得）
    try:
        import 暂停令
        停在, 停由 = 暂停令.在(root)
    except Exception:
        停在, 停由 = False, ''
    if 停在:
        if 暂停令.许(i, root):
            print('⏸ 暂停令在，而 %s 有作者亲令之例外——只许此一回（开即销）' % i)
        else:
            print('⛔ 拒开：%s——作者令下方 `python3 工具/暂停令.py --解 "作者令：……"`，或单件 `--例外 %s "作者令：……"`' % (停由, i)); return False
    # ★1021 费哨（裁_1021_省律）：末十件写书之占 <七成时，非写书之件须带「挡路：」或「读者可见：」之由方开
    try:
        import 费哨
        _名 = next((x.get('名', '') for x in 读(root)['件'] if x['id'] == i), '')
        _许, _由 = 费哨.许开('%s·%s' % (i, _名), 有效之据, root)
    except Exception as _e:
        _许, _由 = True, '费哨跑不得（%s）——只报不拦' % _e
    if not _许:
        print('⛔ 拒开：' + _由); return False
    if _由:
        print('⚠ ' + _由)
    # ★1009 作者令「进化之时先看曾经踩过的坑，踩过的坑⛔在新法里再现」：开前逐坑过一遍，有效之据须写坑之检
    try:
        import 方法坑账 as 坑账
        诸坑 = 坑账.读(root)['坑']
    except Exception:
        诸坑 = []
    if 诸坑:
        print('── 坑账（开前逐坑过一遍：本法如何排除之）──')
        for k in 诸坑:
            print('  %s〔%s〕%s' % (坑账.圈(k['号']), k['状'], k['名'][:70]))
        if '坑' not in 有效之据:
            print('⛔ 拒开：有效之据须写「坑之检」——本法如何排除上列诸坑（或指其设计档之「## 坑之检」）'); return False
    # ★1009 作者令「每一环都要先精准确定它能做成，再去实施；⛔猜」：有 设定/方案/ 之盘，即验其 W 之方案（逐环确证、时、费、败则；未确证者⛔开）
    if os.path.isdir(os.path.join(root, '设定', '方案')):
        try:
            import 方案 as _方案
            案过, 案坏 = _方案.验(i, root)
        except Exception as _e:
            案过, 案坏 = False, ['方案器跑不起来：%s' % _e]
        if not 案过:
            print('⛔ 拒开：方案未过——\n  ' + '\n  '.join(案坏)); return False
    # ★1009 作者令「每做一件事先想最好的办法，先设计方法，⛔硬着头皮上」（坑⑳：W18 派十一个模型席去核机器能核之算术）
    if '零token之检' not in 有效之据.replace(' ', ''):
        print('⛔ 拒开：有效之据须写「零token之检：……」——此件哪些机器能办（归脚本、⛔开席）、哪些非模型不可、为何；先设计方法，再开'); return False
    账 = 读(root)
    for x in 账['件']:
        if x['id'] == i:
            x.update({'状态': '进行', '起': (今 or _今()).strftime('%Y-%m-%dT%H:%MZ'), '时限': 时限,
                      '停止线': 停止线.strip(), '换法': 换法.strip(), '有效之据': 有效之据.strip(), '预估': 预估.strip()})
            x.setdefault('裁', [])
            _存(账, root); print('✓ %s 开：时限 %g 时' % (i, 时限))
            if 停在:
                暂停令.销(i, root)
            return True
    print('⛔ 无此件：' + i); return False


def 有复盘(i, root=ROOT):
    """1009 作者令：每一回任务都要复盘——耗费、无用功、改进方案、坑四节俱在方许结案（坑节须点坑账之号或写「无新坑」，`工具/复盘.py --验` 守）。
    ★档名须 <日>_<W>_<题>.md 而精确认 W（旧以 *W1* 认，W1 会错认 W12 之复盘）。"""
    for f in glob.glob(os.path.join(root, '设定', '复盘', '*_%s_*.md' % i)):
        t = open(f, encoding='utf-8').read()
        if all(k in t for k in ('## 耗费', '## 无用功', '## 改进方案', '## 坑')) or all(k in t for k in ('## 耗费', '## 三问', '## 坑')):   # ★1021 简式
            return True
    return False


def 登方法账(i, 由, root=ROOT, 今=None):
    """★1021 作者令「要有一条升级链」：--裁 W 取 即於 设定/方法账.md 末之「## 升级链」添一行（零 token；已登者⛔重登）。"""
    p = os.path.join(root, '设定', '方法账.md')
    文 = io.open(p, encoding='utf-8').read() if os.path.exists(p) else '# 方法账\n'
    if re.search(r'^\| %s·' % re.escape(i), 文, re.M):
        return False
    名 = next((x.get('名', '') for x in 读(root)['件'] if x['id'] == i), '')
    费 = 0.0
    try:
        for r in json.load(io.open(os.path.join(root, '设定', '费账.json'), encoding='utf-8')).get('行', []):
            if (r.get('名') or '').startswith(i + '·'):
                费 += float(r.get('美元') or 0)
    except (OSError, ValueError):
        pass
    清 = lambda t, n: re.sub(r'[|\n]', '／', t.strip())[:n]
    k = 由.find('所废'); j = 由.find('较旧')
    法 = 清(由[k:] if k >= 0 else 由, 100)
    旧 = 清(由[j:] if j >= 0 else '', 100) or '—'
    if '## 升级链' not in 文:
        文 = 文.rstrip('\n') + ('\n\n## 升级链（1021 立·`工具/工作流账.py --裁 W 取` 自添一行，零 token；作者令「升级之的只一：写出全中国最好看的小说」）\n\n'
                               '| 件 | 法（所废後） | 费 | 较旧 | 日 | 判 |\n|---|---|---|---|---|---|\n')
    日 = (今 or _今()).strftime('%m%d')
    文 = 文.rstrip('\n') + '\n| %s·%s | %s | %s | %s | %s | 取 |\n' % (i, 清(名, 40), 法, ('$%.2f' % 费) if 费 else '未记', 旧, 日)
    io.open(p, 'w', encoding='utf-8').write(文)
    return True


def 裁(i, 法, 由, 新时限=None, root=ROOT, 今=None):
    if 法 == '守原':
        print('⛔ 无「守原」之出口——作者 1008：留下烂摊子不干了即烂尾。原文果真已达标，以「取」裁之并写由；否则「重造」'); return False
    if 法 not in ('取', '重造', '续') or not (由 or '').strip():
        print('⛔ 裁须为 取／重造／续 之一，且须写由'); return False
    # ★1017 作者铁律「淘汰之律」：取一新法，须同时说出它淘汰了哪一样旧法——「所废：<旧法与其删处>」；
    #   真係新增而无所替者写「所废：无（<由>）」。⛔只添不汰（老旧冗杂之法留在路上拖後腿）。
    if 法 == '取' and '所废' not in 由:
        print('⛔ 取须写「所废：……」——此法淘汰了哪一样旧法、删在哪（真无所替写「所废：无（由）」）——1017 作者铁律·淘汰之律'); return False
    # ★1017 作者铁律·采用之准（大哥大之喻）：同价而效更好（B）、或同效而费更省（C）方许取；最好者效如 B 而费如 C。
    #   取之由须含「较旧：效…；费…」——效与费各写升／平／降与其数（真係新增而无旧可比写「较旧：无（新增）」）。
    if 法 == '取' and '较旧' not in 由:
        print('⛔ 取须写「较旧：效…；费…」——与所废之旧法比，效（升／平）与费（降／平）各带其数；效降或费升而效不升者⛔取（1017 作者铁律·采用之准）'); return False
    if 法 in ('取', '重造') and not 有复盘(i, root):
        print('⛔ 无复盘不许结案（1009 作者令·每任务必复盘）：须先立 设定/复盘/<日>_%s_<题>.md，含「## 耗费」（实耗：token、时、席、来回——`工具/费审.py <Run ID>`）、「## 无用功」（哪里花了大量 token 与时却无实果）、「## 改进方案」（具体到改哪档哪条、下回照办之验）——`python3 工具/复盘.py %s <Run ID…>` 起草' % (i, i)); return False
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
        _存(账, root); print('✓ %s 裁：%s' % (i, 法))
        if 法 == '取':
            try:
                登方法账(i, 由, root, 今)
            except Exception as e:
                print('⚠ 升级链未登：%s' % e)
        return True
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
        共 += 1; ok += (开('A', 6, '停', '换', '据；零token之检：须模型', '估', t, H(0)) is True and 查(t, H(5)) == [])   # 时限内不红
        # 1009：有坑账则有效之据须写坑之检；暂停令在即拒开
        json.dump({'坑': [{'号': 1, '名': '甲坑', '状': '已守'}]}, open(os.path.join(t, '设定', '方法坑账.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        import io as _io, contextlib as _cl
        with _cl.redirect_stdout(_io.StringIO()):
            r1 = 开('A', 6, '停', '换', '据', '估', t, H(0))
            r0 = 开('A', 6, '停', '换', '据；坑之检：①已排除', '估', t, H(0))          # ⑳：缺零token之检 → 拒
            r2 = 开('A', 6, '停', '换', '据；坑之检：①已排除；零token之检：须模型', '估', t, H(0))
            open(os.path.join(t, '设定', '交.md'), 'w', encoding='utf-8').write('> 暂停令\n')
            json.dump({'令': '作者令：停', '据': '设定/交.md:1', '解': None}, open(os.path.join(t, '设定', '暂停令.json'), 'w', encoding='utf-8'), ensure_ascii=False)
            r3 = 开('A', 6, '停', '换', '据；坑之检：①已排除；零token之检：须模型', '估', t, H(0))
            import 暂停令 as _停
            _停.例外('A', '作者令：A 可开', t)
            r4 = 开('A', 6, '停', '换', '据；坑之检：①已排除；零token之检：须模型', '估', t, H(0))
            r5 = 开('A', 6, '停', '换', '据；坑之检：①已排除；零token之检：须模型', '估', t, H(0))   # 例外用即销，二回拒
        os.remove(os.path.join(t, '设定', '暂停令.json')); os.remove(os.path.join(t, '设定', '方法坑账.json'))
        # 1009：有方案之盘则须方案过——无方案拒、方案好则开
        os.makedirs(os.path.join(t, '设定', '方案'))
        with _cl.redirect_stdout(_io.StringIO()):
            r6 = 开('A', 6, '停', '换', '据；零token之检：须模型', '估', t, H(0))
            open(os.path.join(t, '设定', '方案', 'A.md'), 'w', encoding='utf-8').write(
                '## 逐环\n| 环 | 做什么 | 谁办 | 确证 | 时 | 费 | 败则 |\n|---|---|---|---|---|---|---|\n'
                '| 1 | 对拍 | 脚本：工具/费审对拍.py | 自测 5/5 | 1 分 | $0 | 停 |\n## 未确证\n- 无\n## 合计\n- 时：1 分；费：$0；据：自测\n')
            r7 = 开('A', 6, '停', '换', '据；零token之检：须模型', '估', t, H(0))
        共 += 1; ok += (r6 is False and r7 is True)
        共 += 1; ok += (r0 is False and r1 is False and r2 is True and r3 is False and r4 is True and r5 is False)
        共 += 1; ok += (len(查(t, H(7))) == 1 and '逾时限' in 查(t, H(7))[0])  # 逾时 → 红
        共 += 1; ok += (裁('A', '续', '由', 3, t, H(7)) is True and 查(t, H(8)) == [])   # 续一回
        共 += 1; ok += (裁('A', '续', '由', 3, t, H(8)) is False)               # 再续拒
        共 += 1; ok += (裁('A', '重造', '新法', 4, t, H(10)) is False)          # 无复盘不许重造（1009）
        os.makedirs(os.path.join(t, '设定', '复盘'), exist_ok=True)
        open(os.path.join(t, '设定', '复盘', '1009_A_测.md'), 'w').write('## 耗费\n## 无用功\n## 改进方案\n## 坑\n无新坑\n')
        open(os.path.join(t, '设定', '复盘', '1009_A1_测.md'), 'w').write('## 耗费\n## 无用功\n## 改进方案\n## 坑\n无新坑\n')
        共 += 1; ok += (有复盘('A', t) is True and 有复盘('A2', t) is False)    # 精确认 W：A1 之复盘⛔算 A 的，A2 无
        共 += 1; ok += (裁('A', '重造', '新法', 4, t, H(10)) is True and 查(t, H(13)) == [] and len(查(t, H(15))) == 1)
        裁('A', '重造', '又一法', 4, t, H(15))
        共 += 1; ok += (裁('A', '重造', '三法', 4, t, H(20)) is False)          # 重造两回後拒——报作者
        共 += 1; ok += (裁('A', '守原', '由', None, t, H(20)) is False)         # 无守原之出口（⛔烂尾）
        共 += 1; ok += (裁('A', '取', '达标', None, t, H(20)) is False)   # ★1017 淘汰之律：取而无「所废」即拒
        共 += 1; ok += (裁('A', '取', '达标；所废：无（新增）', None, t, H(20)) is False)   # 缺「较旧」即拒
        共 += 1; ok += (裁('A', '取', '达标；所废：无（新增）；较旧：无（新增）', None, t, H(20)) is True and 读(t)['件'][0]['状态'] == '已成')
        _链 = io.open(os.path.join(t, '设定', '方法账.md'), encoding='utf-8').read()   # ★1021 升级链：取即自登一行、⛔重登
        共 += 1; ok += ('## 升级链' in _链 and _链.count('| A·甲 |') == 1 and 登方法账('A', '再', t) is False)
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
