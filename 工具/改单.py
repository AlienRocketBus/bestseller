# -*- coding: utf-8 -*-
"""改单——**一切皆可改；改的前提只一条：让这本书更好。每一改必立单、必记改前之笔、可追溯。**

【其立之由（2026-09-25·作者令，逐字之意）】
  「规矩是死的，人是活的。圣经的设定、小说中的剧情，一切皆可改——但改的前提只有一个：让小说质量更高。
   否则完全没有必要改。改了之後要有修改清单，每一次改都有备份，方便後续追溯和核查。
   设立一个机制，叫一切皆可改，并且这个机制必须要运行起来。」

【一把尺（总编辑定）】改之前只答一问：**改了之後，这本书哪里更好了？**——须说得出具体：
  消了哪一处崩／哪一拍更狠／哪条线更连／读者哪里更放不下。**答不出「更好在哪」者，不改。**
【三步】
  ①立单：`python3 工具/改单.py --立 "改什么" "改了更好在哪" <档1> <档2> …`
     → 发单号（如 G0925-01），**记改前之提交 sha**（单之「改前」；取回走 `git show <sha>:<档>`，⛔再拷整档——1027·执行之审 #112：
       git 即逐字之全记，旧之 `设定/改单备份/` 319 档 1.8 亿字节係同功两处之劣者，已删；1027 前之单其备份在 db52f247 之树），并记入 `设定/修改清单.md`。
       档有未提交之改者照立而印 ⚠（改前之凭只到该提交；⛔误拦）。
  ②改：照常改；提交说明里写「改单#<单号>」。
  ③结单：`python3 工具/改单.py --毕 <单号> "改完一句（改了几处·验过哪几道闸）"`
【其牙（全测·改单）】
  甲·自本器立日起，凡提交**改动已有之正文章**（非新添）或圣经／canon／人物状态册，而提交说明无「改单#」者 → **红**。
  丙·改前之凭（1027·#112）：新单之「改前」须为 git 所有之提交；1027 前之单（无「改前」）其 `设定/改单备份/<号>/` 须在 db52f247 之树——缺即**红**（浅克隆寻不着者 ⚠）。
     ★例外唯一：新章封版之追记（圣经入册、状态册同步、施工表锁定行），提交说明标「封版#N」——那是添，不是改。
  乙·单立而七日未结 → 黄。
【施单（W60·X11 立）】席⛔亲改诸档，只交一份「改之单」（JSON 之列 [{档, 原, 新, 由}]），主环以本器施之：
  `python3 工具/改单.py --施单 <单.json> [--落] [--号 <单号>] [--根 <仓根>]`
  默认只验并印每条之 diff，⛔写；--落 方写。每条：原须在档中恰一见（重叠之见亦计；0 或 ≥2 即⛔并指出其行）、⛔跨行；
  新⛔含换行（⛔改行数——要添者以行内接写）、⛔同原、施後须恰一见。一条不过，全单⛔写。
  档⛔：出仓、.git、正文/（列二稿账）、剧情庭之裁档 设定/剧情庭_*.md、改单账、修改清单、单档本身、未在之档。
  --落：照 --立 之法以改前之提交为凭（带 --号 者即其单之「改前」，所动之档补登入单；无 --号 则印 HEAD 之 sha），⛔拷整档；
        验後写前再核盘上未变（他席并写即⛔）；写後再读盘逐条验新恰一见、行数未变。--根：以他目录为仓根（试於副本）。
  --自测 另渲染 工具/席/剧情庭.js 式段之令（node·假交）验其与本器之约：题档首行之认、单之四键、自验 --施单、守原写空单。
用法：--立 ｜ --毕 ｜ --查 ｜ --单（列清单）｜ --施单 ｜ --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, re, sys, json, time, shutil, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
账档 = os.path.join(ROOT, '设定', '改单账.json')
清单 = os.path.join(ROOT, '设定', '修改清单.md')
立日 = '2026-09-25 12:00'
# ★1027·执行之审 #111：人物百科卡汰（章号止於 341，诸器无一读之；人物之态归 人物状态册.json 与 人物链）——出管档之式
管 = re.compile(r'^(正文/|设定/00_镇冢秘术_唯一总圣经\.md|设定/canon事实库\.json|设定/人物状态册\.json|设定/镇冢秘术_作者版设定圣经\.md)')
# ★1027·执行之审 #112：改前之凭＝提交之 sha（⛔拷整档）。1027 前之单之整份备份已随其目删，取回：git show db52f247:设定/改单备份/<号>/<档>
旧备之笔 = 'db52f247'
旧备之目 = '设定/改单备份'


def _git(*a, 根=None):
    try:
        r = subprocess.run(['git', '-c', 'core.quotepath=off'] + list(a), cwd=根 or ROOT, capture_output=True, text=True)
        return r.returncode, r.stdout
    except Exception as e:
        return 1, str(e)


def 改前之笔(档们):
    """→ (sha12 或 None, 脏们)：HEAD 之提交即改前之凭；档们中未踪或有未提交之改者列入「脏」（照立、印 ⚠）。"""
    rc, out = _git('rev-parse', 'HEAD')
    if rc != 0:
        return None, []
    脏 = []
    for p in 档们:
        rel = os.path.relpath(os.path.join(ROOT, p) if not os.path.isabs(p) else p, ROOT).replace(os.sep, '/')
        if not os.path.exists(os.path.join(ROOT, rel)):
            continue
        rc1, _ = _git('ls-files', '--error-unmatch', '--', rel)
        _, st = _git('status', '--porcelain', '--', rel)
        if rc1 != 0 or st.strip():
            脏.append(rel)
    return out.strip()[:12], 脏


def 改前之凭(单们=None, 旧笔=None):
    """→ (坏, 黄)：每单之改前须可取回——新单「改前」之 sha 须为提交；旧单（无「改前」）其备份目须在 旧笔（默 db52f247）之树。"""
    单们 = 读()['单'] if 单们 is None else 单们
    旧笔 = 旧笔 or 旧备之笔
    坏, 黄 = [], []
    浅 = _git('rev-parse', '--is-shallow-repository')[1].strip() == 'true'
    旧在 = None
    for x in 单们:
        if x.get('改前'):
            if _git('cat-file', '-e', '%s^{commit}' % x['改前'])[0] != 0:
                (黄 if 浅 else 坏).append('%s 之改前 %s 非 git 所有之提交%s' % (x['号'], x['改前'], '（浅克隆·未验）' if 浅 else ''))
            continue
        if not x.get('档'):
            continue
        if 旧在 is None:
            rc, out = _git('ls-tree', '--name-only', '%s:%s' % (旧笔, 旧备之目))
            旧在 = set(out.split()) if rc == 0 else False
        if 旧在 is False:
            (黄 if 浅 else 坏).append('旧单之备份之笔 %s 寻不着（%s）' % (旧笔, '浅克隆·未验' if 浅 else '其树无 %s' % 旧备之目))
            break
        if x['号'] not in 旧在:
            坏.append('%s 无改前之凭：无「改前」之 sha，%s:%s/%s 亦不在' % (x['号'], 旧笔, 旧备之目, x['号']))
    return 坏, 黄


def 读():
    try:
        return json.load(open(账档, encoding='utf-8'))
    except Exception:
        return {'单': []}


def 写(d):
    t = 账档 + '.tmp'
    json.dump(d, open(t, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    os.replace(t, 账档)


def 立(何, 由, 档们):
    if len(由) < 10:
        print('⛔「改了更好在哪」须说具体（消了哪一处崩／哪一拍更狠／哪条线更连）——答不出，不改'); return None
    d = 读()
    日 = time.strftime('%m%d')
    n = 1 + sum(1 for x in d['单'] if x['号'].startswith('G' + 日))
    号 = 'G%s-%02d' % (日, n)
    笔, 脏 = 改前之笔(档们)
    if not 笔:
        print('⛔ 取不得改前之提交（非 git 之仓？）——改单以其 sha 为凭，⛔立'); return None
    存 = [os.path.relpath(os.path.join(ROOT, p) if not os.path.isabs(p) else p, ROOT).replace(os.sep, '/')
         for p in 档们 if os.path.exists(os.path.join(ROOT, p) if not os.path.isabs(p) else p)]
    d['单'].append({'号': 号, '立': time.strftime('%Y-%m-%d %H:%M'), '何': 何, '更好在哪': 由, '档': 存, '改前': 笔, '状': '开'})
    写(d)
    with open(清单, 'a', encoding='utf-8') as f:
        f.write('\n## %s ｜ %s\n- **改什么**：%s\n- **改了更好在哪**：%s\n- **改前之笔**：`%s`（取回 `git show %s:<档>`；%s）\n- **状**：开\n'
                % (号, time.strftime('%Y-%m-%d %H:%M'), 何, 由, 笔, 笔, '、'.join(存) or '无档'))
    if 脏:
        print('⚠ %s 有未提交之改（或未踪）——改前之凭只到 %s，其後未提交之改亦算入本单之差' % ('、'.join(脏), 笔))
    print('✓改单已立：%s｜改前之笔 %s（%d 档；取回 git show %s:<档>）｜提交说明须写「改单#%s」' % (号, 笔, len(存), 笔, 号))
    return 号


def 补登(号, 提交们):
    """事後补登：已立之单点名其所覆之提交（该提交当时未写单号）。⛔补登也须先 --立（有其由、有改前之笔）。"""
    d = 读()
    for x in d['单']:
        if x['号'] == 号:
            x.setdefault('覆', []).extend(提交们)
            写(d)
            with open(清单, 'a', encoding='utf-8') as f:
                f.write('- **%s 补登**：覆提交 %s（当时未写单号，事後补登）\n' % (号, '、'.join(提交们)))
            print('✓%s 补登覆 %s' % (号, '、'.join(提交们))); return True
    print('⛔无此单：%s' % 号); return False


def 毕(号, 句):
    d = 读()
    for x in d['单']:
        if x['号'] == 号:
            # ★1014：单改了正文即当场同步阅读器（G1014-02 改 384 骨记而未同，推时检察官自测、医生、全书检三红一根）
            _器 = os.path.join(ROOT, '工具', '同步全本阅读器.py')
            if os.path.exists(_器) and any(str(p).startswith('正文/') for p in x.get('档', [])):   # 器不在（自测之沙盘）即不跑
                r = subprocess.run([sys.executable, _器], cwd=ROOT, capture_output=True, text=True)
                print('  · 单涉正文，已同步阅读器：%s' % ((r.stdout.strip().split('\n') or [''])[-1] if r.returncode == 0 else '⛔同步败（rc=%d）' % r.returncode))
                if r.returncode != 0:
                    print('⛔ 阅读器未同步，⛔结单'); return False
            x['状'] = '毕'; x['毕'] = time.strftime('%Y-%m-%d %H:%M'); x['结'] = 句
            写(d)
            with open(清单, 'a', encoding='utf-8') as f:
                f.write('- **%s 结单**（%s）：%s\n' % (号, x['毕'], 句))
            print('✓%s 结单' % 号); return True
    print('⛔无此单：%s' % 号); return False


def 查(印=True):
    坏, 黄 = [], []
    try:
        out = subprocess.run(['git', '-c', 'core.quotepath=off', 'log', '--since=' + 立日, '--diff-filter=M',
                              '--name-only', '--format=@@%h %s%n%b'], cwd=ROOT, capture_output=True, text=True).stdout
    except Exception:
        out = ''
    覆 = {c for x in 读()['单'] for c in x.get('覆', [])}   # 补登：事後立单、点名所覆之提交（须有其由，入修改清单）
    for 块 in out.split('@@')[1:]:
        行 = 块.strip().split('\n')
        头 = 行[0]; 文 = '\n'.join(行)
        档 = [l for l in 行[1:] if 管.match(l)]
        if 档 and any(头.startswith(c[:7]) for c in 覆):
            continue
        if 档 and '改单#' not in 文 and '封版#' not in 文:   # 新章封版之追记（圣经入册、状态册同步、锁定行）係添不係改，标「封版#N」
            坏.append('%s 改了 %s 而无改单' % (头[:40], '、'.join(档[:3])))
    凭坏, 凭黄 = 改前之凭()
    坏 += 凭坏
    黄 += 凭黄
    for x in 读()['单']:
        if x['状'] == '开':
            t = time.mktime(time.strptime(x['立'], '%Y-%m-%d %H:%M'))
            if time.time() - t > 7 * 86400:
                黄.append('%s 立七日未结' % x['号'])
    if 印:
        for x in 坏:
            print('  ⛔ ' + x)
        for x in 黄:
            print('  ⚠ ' + x)
        if not 坏:
            print('  ✓ 改单：凡改必有单、单单有改前之凭。')
    return not 坏, 坏


# ★W60·X11：施单——391 段裁席亲改十一档 164 回 $20.94（复盘 1015_W43），今裁席只交单、本器施
_键 = ('档', '原', '新', '由')
_断行 = '\n\r\x0b\x0c\x1c\x1d\x1e\x85\u2028\u2029'   # str.splitlines 所认之断行俱⛔


def _窗(行文, 起, 长, 宽=36):
    """行文中 [起, 起+长) 一段，前後各带 宽 字，过长者以 … 截。"""
    a, b = max(0, 起 - 宽), min(len(行文), 起 + 长 + 宽)
    return ('…' if a > 0 else '') + 行文[a:b] + ('…' if b < len(行文) else '')


def _见数(t, s):
    """s 在 t 中之见数——**重叠之见亦计**（逐位步一而 find）。⛔str.count：它只数不相重叠者，「哈哈」於「哈哈哈」只算 1 见，实则 0、1 两处俱见。"""
    n, i = 0, t.find(s)
    while i >= 0:
        n += 1; i = t.find(s, i + 1)
    return n


def _行号们(t, s):
    """s 在 t 中所见之行（同行多见者记「×n」；至多列八行）。"""
    数, i, 前, n = {}, t.find(s), 0, 1
    while i >= 0 and len(数) <= 8:   # 逐见累计行号（⛔每见从头数——三兆之圣经、常字千见即卡）
        n += t.count('\n', 前, i); 前 = i
        数[n] = 数.get(n, 0) + 1; i = t.find(s, i + 1)
    出 = ['%d%s' % (n, '×%d' % k if k > 1 else '') for n, k in list(数.items())[:8]]
    return 出 + (['…'] if len(数) > 8 else [])


_禁施 = re.compile(r'^\.git(/|$)')
_禁施_正文 = re.compile(r'^正文/')
_禁施_裁档 = re.compile(r'^设定/剧情庭_[^/]*\.md$')


def _档路(p, 禁=()):
    """单之「档」→ (仓根相对路径, 绝对路径, 错)。⛔出仓、⛔.git、档须已在（⛔新立档）；
    ⛔正文/（正文之改列入二稿账）、⛔剧情庭之裁档（设定/剧情庭_*.md：裁席自写，⛔以单改）、
    ⛔改单账／修改清单（--号 之补登写之，单再写即覆其登）、⛔单档本身（禁：诸绝对路）。"""
    根 = os.path.realpath(ROOT)
    a = os.path.realpath(p if os.path.isabs(p) else os.path.join(根, p))
    if a != 根 and not a.startswith(根 + os.sep):
        return None, None, '出仓（%s）' % p
    rel = os.path.relpath(a, 根).replace(os.sep, '/')
    if _禁施.match(rel):
        return None, None, '⛔施於 %s' % rel
    if _禁施_正文.match(rel):
        return None, None, '⛔施於正文（%s）——正文之改列入二稿账，⛔入单' % rel
    if _禁施_裁档.match(rel):
        return None, None, '⛔施於剧情庭之裁档（%s）——裁档裁席自写，⛔入单' % rel
    if a in {os.path.realpath(账档), os.path.realpath(清单)} or rel in ('设定/改单账.json', '设定/修改清单.md'):
        return None, None, '⛔施於改单之账（%s）——账与清单只由本器之 --立／--号 登，⛔入单' % rel
    if a in 禁:
        return None, None, '⛔施於单档本身（%s）' % rel
    if not os.path.isfile(a):
        return None, None, '档不在（%s）——单只改已有之档，⛔新立' % rel
    return rel, a, None


def _读文(a):
    with open(a, encoding='utf-8', newline='') as f:   # newline='' 守其原之行尾
        return f.read()


def _写文(a, t):
    tmp = a + '.施单tmp'
    with open(tmp, 'w', encoding='utf-8', newline='') as f:
        f.write(t)
    shutil.copymode(a, tmp)
    os.replace(tmp, a)


def 施单(单档, 落=False, 号=None, _写後=None, _验後=None):
    """验（并於 落 时写）一份改之单。→ True／False。_写後、_验後：自测之钩（写後再验前／验毕落前调之）。"""
    try:
        with open(单档, encoding='utf-8') as f:
            单 = json.load(f)
    except FileNotFoundError:
        print('⛔ 单不在：%s' % 单档); return False
    except Exception as e:
        print('⛔ 单非合法 JSON（%s）：%s' % (单档, e)); return False
    if not isinstance(单, list):
        print('⛔ 单须是 JSON 之列 [{档, 原, 新, 由}]，今为 %s' % type(单).__name__); return False
    if not 单:
        print('✓ 单空（0 条），无可施'); return True
    错, 原文, 内, 记 = [], {}, {}, []
    for i, x in enumerate(单, 1):
        名 = '第%d条' % i
        if not isinstance(x, dict):
            错.append('%s 非对象' % 名); continue
        缺 = [k for k in _键 if not isinstance(x.get(k), str) or x.get(k) == '' or (k in ('档', '由') and not x[k].strip())]
        多 = sorted(set(x) - set(_键))
        if 缺 or 多:
            错.append('%s 键%s%s（须恰 档／原／新／由 四键，俱非空之串）' % (名, ('缺或空：' + '、'.join(缺)) if 缺 else '', ('；多：' + '、'.join(多)) if 多 else '')); continue
        rel, a, e = _档路(x['档'], 禁={os.path.realpath(单档)})
        if e:
            错.append('%s %s' % (名, e)); continue
        名 = '%s %s' % (名, rel)
        原, 新 = x['原'], x['新']
        if any(c in 原 for c in _断行):
            错.append('%s 原跨行（⛔：原只许一行之内）' % 名); continue
        if any(c in 新 for c in _断行):
            错.append('%s 新含换行（⛔改行数：要添者以行内接写）' % 名); continue
        if 原 == 新:
            错.append('%s 新同原' % 名); continue
        if rel not in 内:
            try:
                原文[rel] = 内[rel] = _读文(a)
            except Exception as e2:
                错.append('%s 读不动（%s）' % (名, e2)); continue
        t = 内[rel]
        n = _见数(t, 原)
        if n != 1:
            错.append('%s 原%s（须恰一见）：「%s」%s' % (名, '零见' if n == 0 else ' %d 见' % n, 原[:40] + ('…' if len(原) > 40 else ''),
                                             ('於行 ' + '、'.join(map(str, _行号们(t, 原)))) if n else ''))
            continue
        p = t.index(原)
        行 = t.count('\n', 0, p) + 1
        头 = t.rfind('\n', 0, p) + 1
        尾 = t.find('\n', p); 尾 = len(t) if 尾 < 0 else 尾
        前行 = t[头:尾]
        内[rel] = t[:p] + 新 + t[p + len(原):]
        後行 = 内[rel][头:尾 - len(原) + len(新)]
        记.append({'i': i, 'rel': rel, 'a': a, '行': 行, '由': x['由'], '新': 新,
                   '前': _窗(前行, p - 头, len(原)), '後': _窗(後行, p - 头, len(新))})
    for rel in 内:
        if 内[rel].count('\n') != 原文[rel].count('\n') or len(内[rel].splitlines()) != len(原文[rel].splitlines()):
            错.append('%s 行数变（%d→%d）' % (rel, len(原文[rel].splitlines()), len(内[rel].splitlines())))
    for r in 记:   # 施後之新须恰一见（後条覆了前条之新、或新本就撞他处者⛔）
        n = _见数(内[r['rel']], r['新'])
        if n != 1:
            错.append('第%d条 %s 新於施後 %d 见（须恰一见：带足上下文；同一处之改并作一条）' % (r['i'], r['rel'], n))
    for r in 记:
        print('@@ %s:%d ｜第%d条｜由：%s' % (r['rel'], r['行'], r['i'], r['由']))
        print('- ' + r['前'])
        print('+ ' + r['後'])
    诸档 = sorted(内)
    if 错:
        for e in 错:
            print('⛔ ' + e)
        print('⛔ 施单：%d 条，⛔ %d 处——一条不过，全单⛔写' % (len(单), len(错)))
        return False
    if not 落:
        print('✓ 施单（只验）：%d 条俱过，%d 档（%s）；行数俱守——加 --落 方写' % (len(单), len(诸档), ' '.join(诸档)))
        return True
    # —— 落 ——
    if _验後:
        _验後()
    d = 读()
    单记 = None
    if 号:
        单记 = next((x for x in d['单'] if x['号'] == 号), None)
        if not 单记:
            print('⛔ 无此改单：%s（先 --立）——⛔写' % 号); return False
    for rel in 诸档:   # 验後盘上又变者⛔（并跑之席正写）
        if _读文(os.path.join(ROOT, rel)) != 原文[rel]:
            print('⛔ %s 验後盘上已变——⛔写，重跑验' % rel); return False
    # ★1027·#112：改前之凭＝提交之 sha（⛔拷整档）——带 --号 者用其单之「改前」（无则补记 HEAD），无 --号 者印 HEAD
    笔, 脏 = 改前之笔(诸档)
    if 单记 is not None:
        if not 单记.get('改前') and 笔:
            单记['改前'] = 笔
        笔 = 单记.get('改前') or 笔
        添 = [rel for rel in 诸档 if rel not in 单记.setdefault('档', [])]
        单记['档'].extend(添)
        写(d)
        if 添:
            with open(清单, 'a', encoding='utf-8') as f:
                f.write('- **%s 施单补登**：%s（改前之笔 `%s`；单 `%s`）\n' % (号, '、'.join(添), 笔, os.path.relpath(os.path.abspath(单档), ROOT)))
        脏 = [rel for rel in 脏 if rel in 添]   # 已在单者之未提交之改係本单前回之施，⛔报
    if 脏:
        print('⚠ %s 有未提交之改（或未踪）——改前之凭只到 %s，其後未提交之改亦算入本单之差' % ('、'.join(脏), 笔 or '（无 HEAD）'))
    for rel in 诸档:
        _写文(os.path.join(ROOT, rel), 内[rel])
    if _写後:
        _写後()
    坏 = []
    for rel in 诸档:   # 再验：读盘
        t = _读文(os.path.join(ROOT, rel))
        if len(t.splitlines()) != len(原文[rel].splitlines()):
            坏.append('%s 行数变' % rel)
    for r in 记:
        n = _见数(_读文(r['a']), r['新'])
        if n != 1:
            坏.append('第%d条 %s 新於盘上 %d 见' % (r['i'], r['rel'], n))
    if 坏:
        import tempfile
        存 = tempfile.mkdtemp(prefix='施单之原_')   # 改前原文存仓外（⛔入仓），供逐档核之
        for rel in 诸档:
            with open(os.path.join(存, rel.replace('/', '__')), 'w', encoding='utf-8', newline='') as f:
                f.write(原文[rel])
        for e in 坏:
            print('⛔ 再验：' + e)
        print('⛔ 施单已写而再验不过——改前原文存於 %s（仓外）；或 git show %s:<档>，逐档核之' % (存, 笔 or 'HEAD')); return False
    print('✓ 施单已落：%d 条於 %d 档；改前之笔 %s（取回 git show %s:<档>）；再验 %d/%d%s' % (
        len(单), len(诸档), 笔 or '（无）', 笔 or 'HEAD', len(记), len(记),
        '' if 号 else '｜⚠未带 --号：提交说明仍须写「改单#」（先 --立）'))
    return True


# 剧情庭.js 式段之令与本器之约（W60·X11 驳後立：剧情庭.js 无自测，其令以 node 渲染、诸席以假交代之——
#   验题席之交，以其令中之命令真跑 bash 而得，非手编之首行）
_庭器 = r"""
const fs = require('fs'), cp = require('child_process')
const [, , 档, 案档] = process.argv
const src = fs.readFileSync(档, 'utf8').replace(/^export const meta/m, 'const meta')
const AF = Object.getPrototypeOf(async function () {}).constructor
const 出 = []
;(async () => {
  for (const c of JSON.parse(fs.readFileSync(案档, 'utf8'))) {
    const 令 = [], logs = []
    const 验 = (prompt) => {
      const m = /`(f='[^`]*)`/.exec(prompt)
      const o = cp.execFileSync('bash', ['-c', m[1]], { cwd: c.cwd, encoding: 'utf8' })
      if (/^题档不在$/m.test(o)) return { topic_exists: false, first_line: '', liao_path: '', liao_exists: false }
      const 首 = (/^首行=(.*)$/m.exec(o) || [, ''])[1], 料 = /^料=(.*) (有|无)$/m.exec(o) || [, '', '无']
      return { topic_exists: true, first_line: 首, liao_path: 料[1], liao_exists: 料[2] === '有' }
    }
    const 案 = n => ({ name: n, plan: 'p', why_better: 'w', soundness: 's' })
    const agent = async (prompt, o) => {
      令.push({ label: o.label, prompt, phase: o.phase })
      if (o.label === '验题·首行') return c.首 || 验(prompt)
      if (o.label.startsWith('出案')) return c.keep ? { current_judgement: 'x', current_appeal: 9, current_sound: 9, keep: true, proposals: [] }
        : { current_judgement: 'x', current_appeal: 7, current_sound: 7, keep: false, proposals: [案('a'), 案('b'), 案('c')] }
      if (o.label === '刺·并攻') return { attacks: ['小说家1', '小说家2', '小说家3', '剧本师1', '剧本师2', '剧本师3'].map(id => ({ id, flaw: 'f', level: '轻', better_claim_true: 'y' })) }
      if (o.label.startsWith('复评')) return { scores: ['小说家1', '小说家2', '小说家3', '剧本师1', '剧本师2', '剧本师3'].map(id => ({ id, appeal: id === '剧本师1' ? 9 : 6, sound: 8, beats_current: id === '剧本师1', reason: 'r' })), current_appeal: 7, first_choice: '剧本师1' }
      return '摘要'
    }
    let r = null, err = null
    try { r = await new AF('args', 'agent', 'parallel', 'phase', 'log', src)(c.args, agent, async ts => Promise.all(ts.map(f => f())), () => {}, m => logs.push(m)) }
    catch (e) { err = String(e && e.message || e) }
    出.push({ err, r, 令, logs })
  }
  process.stdout.write(JSON.stringify(出))
})().catch(e => { process.stderr.write(String(e && e.stack || e)); process.exit(3) })
"""


def _庭单之约():
    """→ [(名, 合否)]。剧情庭.js 式段：①题档首行之认（真题档逐一、带／不带反引号、缺、段料不在、题不在、无 W）；
    ②段裁令与本器之约（单之四键＝_键、自验 --施单、⛔亲改、⛔诸册同步之旧句、⛔grep -c）；③守原之支写空单。"""
    import tempfile
    js = os.path.join(ROOT, '工具', '席', '剧情庭.js')
    if not os.path.isfile(js):
        return [('㉕约·剧情庭.js 不在（%s）' % js, False)]
    if not shutil.which('node'):
        return [('㉕约·node 不在——剧情庭.js 之令渲染不起（⛔以不跑作过）', False)]
    沙 = tempfile.mkdtemp()
    os.makedirs(os.path.join(沙, '设定', '剧情庭题')); os.makedirs(os.path.join(沙, '设定', '段案'))
    open(os.path.join(沙, '设定', '段案', '_料_1-10.md'), 'w', encoding='utf-8').write('料\n')
    首们 = {'无反引号': '料：设定/段案/_料_1-10.md（段料.py 所汇）', '带反引号': '料：`设定/段案/_料_1-10.md`（段料.py 所汇）',
           '无料': '# 剧情庭题·势·第 1—10 段', '料不在': '料：`设定/段案/_料_11-20.md`'}
    for k, 首 in 首们.items():
        open(os.path.join(沙, '设定', '剧情庭题', k + '.md'), 'w', encoding='utf-8').write(首 + '\n正文\n')
    真题 = []
    目 = os.path.join(ROOT, '设定', '剧情庭题')
    for f in sorted(os.listdir(目)) if os.path.isdir(目) else []:
        p = os.path.join(目, f)
        if f.endswith('.md') and os.path.isfile(p):
            with open(p, encoding='utf-8') as fh:
                if fh.readline().startswith('料'):
                    真题.append('设定/剧情庭题/' + f)
    段 = lambda 题, **k: dict({'题': 题, '名': '试', '式': '段', 'W': 'W99'}, **k)
    案 = [{'cwd': ROOT, 'args': 段(x), 'keep': False} for x in 真题]
    案 += [{'cwd': 沙, 'args': 段('设定/剧情庭题/%s.md' % k), 'keep': False} for k in 首们]
    案 += [{'cwd': 沙, 'args': 段('设定/剧情庭题/无此题.md'), 'keep': False},
          {'cwd': 沙, 'args': {'题': '设定/剧情庭题/无反引号.md', '名': '试', '式': '段'}, 'keep': False},
          {'cwd': 沙, 'args': 段('设定/剧情庭题/带反引号.md'), 'keep': True},
          {'cwd': 沙, 'args': 段('设定/剧情庭题/无反引号.md'), 'keep': False,   # 验题席所报之段料路与首行所点不合（席抄错）⛔认
           '首': {'topic_exists': True, 'first_line': 首们['无反引号'], 'liao_path': '设定/段案/_料_2-3.md', 'liao_exists': True}}]
    案档 = os.path.join(沙, '案.json'); 器 = os.path.join(沙, '器.js')
    open(案档, 'w', encoding='utf-8').write(json.dumps(案, ensure_ascii=False)); open(器, 'w', encoding='utf-8').write(_庭器)
    try:
        o = subprocess.run(['node', 器, js, 案档], capture_output=True, text=True, timeout=60)
        果 = json.loads(o.stdout) if o.returncode == 0 else None
    except Exception as e:
        o, 果 = e, None
    shutil.rmtree(沙, ignore_errors=True)
    if not 果:
        return [('㉕约·剧情庭.js 渲染不起：%s' % str(getattr(o, 'stderr', o))[:300], False)]
    真, 无引, 带引, 无料, 料缺, 无题, 无W, 守, 错路 = 果[:len(真题)], *果[len(真题):]
    开 = lambda x, 料='设定/段案/_料_1-10.md': not x['err'] and x['r'] and x['r'].get('料') == 料 and x['r'].get('单') == '设定/_草/W99/剧情庭单.json'
    闭 = lambda x, 句: bool(x['err']) and '⛔式段不开' in x['err'] and 句 in x['err'] and [c['label'] for c in x['令']] == ['验题·首行']
    裁令 = next((c['prompt'] for c in 带引['令'] if c['label'] == '裁'), '')
    守令 = next((c['prompt'] for c in 守['令'] if c['label'] == '裁·守原'), '')
    键 = '{%s}' % ','.join('"%s"' % k for k in _键)
    return [
        ('㉕约·真题档首行点段料者俱开庭（%s）' % '、'.join(os.path.basename(x) for x in 真题),
         bool(真题) and all(not x['err'] and x['r'] and (x['r'].get('料') or '').startswith('设定/段案/_料_') for x in 真)),
        ('㉖约·首行之认：带／不带反引号俱开；无料、段料不在、题不在、验题席报路不合俱⛔开且只派验题一席；无 W ⛔开、一席不派',
         开(无引) and 开(带引) and 闭(无料, '首行须写') and 闭(料缺, '段料不在') and 闭(无题, '题档不在') and 闭(错路, '不合')
         and bool(无W['err']) and 'args.W' in 无W['err'] and not 无W['令']),
        ('㉗约·段裁令：单之四键＝本器之键、自验 --施单、⛔亲改、⛔立改单；旧「须同步更新圣经」「当场」「grep -c -F」⛔见',
         键 in 裁令 and 'python3 工具/改单.py --施单 设定/_草/W99/剧情庭单.json' in 裁令 and '⛔亲改圣经' in 裁令
         and '⛔`python3 工具/改单.py --立`' in 裁令 and '须同步更新圣经' not in 裁令 and '当场以' not in 裁令 and '当场改' not in 裁令
         and 'grep -c -F' not in 裁令 and '★段料（题档首行所点）：`设定/段案/_料_1-10.md`' in 裁令),
        ('㉘约·式段守原之支：带段料、单写空列 []、返回单与料', '单写空列 `[]`' in 守令 and '★段料（题档首行所点）' in 守令
         and '须同步更新圣经' not in 守令 and 守['r'] and 守['r'].get('结') == '守原' and 守['r'].get('单') == '设定/_草/W99/剧情庭单.json'),
    ]


def _凭之回灌():
    """→ [(名, 合否)]：丙·改前之凭於真仓回灌——1027 前诸单於 db52f247 俱有其备份目（✓）；以无其目之树（根之笔）作旧备之笔即俱红。"""
    if _git('cat-file', '-e', '%s^{commit}' % 旧备之笔)[0] != 0:
        浅 = _git('rev-parse', '--is-shallow-repository')[1].strip() == 'true'
        return [('㉙凭·回灌真仓：%s 寻不着%s' % (旧备之笔, '（浅克隆·略）' if 浅 else ''), 浅)]
    旧单 = [x for x in 读()['单'] if not x.get('改前') and x.get('档')]
    坏, 黄 = 改前之凭(旧单)
    根 = _git('rev-list', '--max-parents=0', 'HEAD')[1].split()
    坏2, _ = 改前之凭(旧单, 旧笔=根[0] if 根 else 'HEAD')
    return [('㉙凭·回灌真仓：1027 前之单 %d 份於 %s 俱有改前之备（✓）' % (len(旧单), 旧备之笔), bool(旧单) and not 坏 and not 黄),
            ('㉚凭·回灌真仓：以无其目之树（根之笔）作旧备之笔即红（⛔空验）', bool(坏2))]


def 自测():
    import tempfile
    global 账档, 清单, ROOT
    r = _凭之回灌()                 # 真仓（ROOT 未换）
    旧 = (账档, 清单, ROOT)
    t = tempfile.mkdtemp(); ROOT = t
    os.makedirs(os.path.join(t, '设定')); os.makedirs(os.path.join(t, '正文'))
    账档 = os.path.join(t, '设定', 'z.json'); 清单 = os.path.join(t, '设定', 'q.md')
    open(os.path.join(t, '正文', 'a.md'), 'w', encoding='utf-8').write('改前原文')
    _git('init', '-q')
    for k, v in (('user.name', 't'), ('user.email', 't@t'), ('commit.gpgsign', 'false')):
        _git('config', k, v)

    def 提(msg):
        _git('add', '--', '正文', '设定')
        return _git('commit', '-q', '-m', msg)[0] == 0
    提('始')
    头 = _git('rev-parse', 'HEAD')[1].strip()[:12]
    r.append(('①说不出更好在哪不立', 立('x', '更好', ['正文/a.md']) is None))
    号 = 立('改一句', '消了第一章与九十三章之抵，读者不再疑', ['正文/a.md'])
    单0 = [x for x in 读()['单'] if x['号'] == 号]
    r.append(('②立单发号', bool(号)))
    r.append(('③改前之笔＝立时之 HEAD（⛔拷整档：改单备份之目不立）', bool(单0) and 单0[0].get('改前') == 头
              and not os.path.exists(os.path.join(t, '设定', '改单备份'))))
    open(os.path.join(t, '正文', 'a.md'), 'w', encoding='utf-8').write('改後之文')
    r.append(('③之二 改前原文以 git show <改前>:<档> 取回', _git('show', '%s:正文/a.md' % 头)[1] == '改前原文'))
    import io, contextlib
    o = io.StringIO()
    with contextlib.redirect_stdout(o):
        号脏 = 立('改脏档', '档已改而未提交，照立而印警，⛔误拦', ['正文/a.md'])
    r.append(('③之三 档有未提交之改：照立（⛔误拦）而印 ⚠', bool(号脏) and '⚠ 正文/a.md 有未提交之改' in o.getvalue()))
    r.append(('④入修改清单（带改前之笔）', 号 in open(清单, encoding='utf-8').read() and ('改前之笔**：`%s`' % 头) in open(清单, encoding='utf-8').read()))
    r.append(('⑤结单', 毕(号, '改一处·过硬闸')))
    坏, _ = 改前之凭([{'号': 'G0000-01', '档': ['正文/a.md'], '改前': 头}])
    坏2, _ = 改前之凭([{'号': 'G0000-02', '档': ['正文/a.md'], '改前': 'deadbeef0000'}])
    r.append(('㉛凭·新单之改前係提交即过；伪 sha 即红', not 坏 and bool(坏2) and 'G0000-02' in 坏2[0]))
    os.makedirs(os.path.join(t, '设定', '改单备份', 'G0000-03'))
    open(os.path.join(t, '设定', '改单备份', 'G0000-03', '正文__a.md'), 'w', encoding='utf-8').write('旧备')
    提('旧备')
    旧笔 = _git('rev-parse', 'HEAD')[1].strip()
    坏3, _ = 改前之凭([{'号': 'G0000-03', '档': ['正文/a.md']}], 旧笔=旧笔)
    坏4, _ = 改前之凭([{'号': 'G0000-04', '档': ['正文/a.md']}], 旧笔=旧笔)
    坏5, _ = 改前之凭([{'号': 'G0000-05', '档': []}], 旧笔=旧笔)
    r.append(('㉜凭·旧单（无改前）其目在旧备之笔即过、不在即红；无档之单免', not 坏3 and bool(坏4) and 'G0000-04' in 坏4[0] and not 坏5))
    # —— 施单（W60·X11）——
    import io, contextlib
    def 写档(rel, s):
        p = os.path.join(t, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w', encoding='utf-8', newline='').write(s); return p
    def 读档(rel):
        return open(os.path.join(t, rel), encoding='utf-8', newline='').read()
    n单 = [0]
    def 单(条, 生=None):
        n单[0] += 1; p = os.path.join(t, '设定', '单%d.json' % n单[0])
        open(p, 'w', encoding='utf-8').write(生 if 生 is not None else json.dumps(条, ensure_ascii=False)); return p
    def 跑(*a, **k):
        o = io.StringIO()
        with contextlib.redirect_stdout(o):
            v = 施单(*a, **k)
        return v, o.getvalue()
    甲 = '设定/甲.md'; 甲文 = '第一行：老头在梁上。\n第二行：钱满收皮子。\n第三行：老头在梁下。\n'
    写档(甲, 甲文)
    条 = {'档': 甲, '原': '钱满收皮子', '新': '钱满当面成交', '由': '据 剧情庭_试·一'}
    v, o = 跑(单([条]))
    r.append(('⑥施单·原恰一见则验过、印其 diff', v and '@@ 设定/甲.md:2' in o and '- 第二行：钱满收皮子。' in o and '+ 第二行：钱满当面成交。' in o))
    r.append(('⑦施单·无 --落 不写', 读档(甲) == 甲文))
    v, o = 跑(单([dict(条, 原='老头在梁')]), 落=True)
    r.append(('⑧施单·原不唯一（2 见）⛔并指其行、不写', not v and '2 见' in o and '於行 1、3' in o and 读档(甲) == 甲文))
    v, o = 跑(单([dict(条, 原='霍钧')]), 落=True)
    r.append(('⑨施单·原零见⛔、不写', not v and '零见' in o and 读档(甲) == 甲文))
    v, o = 跑(单([dict(条, 新='钱满当面成交。\n新添一行')]), 落=True)
    r.append(('⑩施单·新含换行（行数变）⛔、不写', not v and '新含换行' in o and 读档(甲) == 甲文))
    v, o = 跑(单([dict(条, 原='收皮子。\n第三行')]), 落=True)
    r.append(('⑪施单·原跨行⛔', not v and '原跨行' in o and 读档(甲) == 甲文))
    v, o = 跑(单(None, 生='[{"档": "设定/甲.md", "原": "钱满"'), 落=True)
    v2, o2 = 跑(单({'档': 甲, '原': '钱满', '新': '钱', '由': 'x'}), 落=True)
    v3, o3 = 跑(单([{'档': 甲, '原': '钱满收皮子', '新': '钱满当面成交'}]), 落=True)
    r.append(('⑫施单·坏 JSON／非列／缺键⛔、不写', not v and '非合法 JSON' in o and not v2 and '须是 JSON 之列' in o2
              and not v3 and '缺或空：由' in o3 and 读档(甲) == 甲文))
    v, o = 跑(单([条, dict(条, 原='梁下', 新='梁下\n')]), 落=True)
    r.append(('⑬施单·一条不过全单⛔写', not v and 读档(甲) == 甲文))
    v, o = 跑(单([dict(条, 新='老头在梁')]))
    r.append(('⑭施单·新於施後不恰一见⛔', not v and '新於施後 3 见' in o))
    v, o = 跑(单([dict(条, 档='../外.md')]))
    v2, o2 = 跑(单([dict(条, 档='设定/无此档.md')]))
    r.append(('⑮施单·出仓／档不在⛔', not v and '出仓' in o and not v2 and '档不在' in o2))
    号2 = 立('施单之试', '391 裁席亲改十一档 164 回，今交单器施，裁席不再碎改', [])
    v, o = 跑(单([条, {'档': 甲, '原': '梁下', '新': '梁下（据 剧情庭_试·二）', '由': '二'}]), 落=True, 号=号2)
    后 = '第一行：老头在梁上。\n第二行：钱满当面成交。\n第三行：老头在梁下（据 剧情庭_试·二）。\n'
    r.append(('⑯施单·--落 依序施两条、行数守、再验过', v and 读档(甲) == 后 and '再验 2/2' in o))
    单2 = [x for x in 读()['单'] if x['号'] == 号2][0]
    r.append(('⑰施单·所动之档补登入其单、改前之凭仍係其单之 sha（⛔拷整档）', 甲 in 单2['档'] and bool(单2.get('改前'))
              and '施单补登' in open(清单, encoding='utf-8').read() and not os.path.exists(os.path.join(t, '设定', '改单备份', 号2))))
    写档(甲, 后)   # 再施一回（改他处）：单之改前⛔变
    v, o = 跑(单([{'档': 甲, '原': '第一行', '新': '首行', '由': '三'}]), 落=True, 号=号2)
    r.append(('⑱施单·再施同单，改前之笔⛔变', v and [x for x in 读()['单'] if x['号'] == 号2][0].get('改前') == 单2.get('改前')))
    def 撞():
        with open(os.path.join(t, 甲), 'a', encoding='utf-8') as f:
            f.write('又：老头在梁下（据 剧情庭_试·四）')
    v, o = 跑(单([{'档': 甲, '原': '梁下（据 剧情庭_试·二）', '新': '梁下（据 剧情庭_试·四）', '由': '四'}]), 落=True, 号=号2, _写後=撞)
    r.append(('⑲施单·写後再验（盘上新不恰一见）⛔', not v and '再验' in o and '新於盘上 2 见' in o))
    乙 = '设定/乙.md'; 写档(乙, 'a甲\r\nb乙\r\n')
    v, o = 跑(单([{'档': 乙, '原': 'b乙', '新': 'b乙丙', '由': '五'}]), 落=True)
    r.append(('⑳施单·无 --号 印改前之笔（HEAD）、守 CRLF、⛔立备份之目', v and 读档(乙) == 'a甲\r\nb乙丙\r\n'
              and '改前之笔 ' + _git('rev-parse', 'HEAD')[1].strip()[:12] in o and not os.path.exists(os.path.join(t, '设定', '改单备份', '施单_'))
              and not any(d.startswith('施单_') for d in os.listdir(os.path.join(t, '设定')))))
    v, o = 跑(单([]))
    v2, o2 = 跑(单([{'档': 乙, '原': 'a甲', '新': 'a甲丁', '由': '六'}]), 落=True, 号='G0000-99')
    r.append(('㉑施单·单空即过；--号 不在⛔、不写', v and not v2 and '无此改单' in o2 and 读档(乙) == 'a甲\r\nb乙丙\r\n'))
    # —— W60·X11 驳後所补 ——
    丙 = '设定/丙.md'; 丙文 = '第一行：哈哈哈。\n'; 写档(丙, 丙文)
    戊 = '设定/戊.md'; 戊文 = '第一行：甲哈乙。\n'; 写档(戊, 戊文)
    v, o = 跑(单([{'档': 丙, '原': '哈哈', '新': '嘿嘿', '由': '七'}]), 落=True)
    v2, o2 = 跑(单([{'档': 戊, '原': '甲', '新': '哈哈', '由': '八'}]), 落=True)   # 施後「哈哈哈乙」：新「哈哈」重叠两见（str.count 只算 1）
    r.append(('㉒施单·重叠之见亦计：原「哈哈」於「哈哈哈」⛔（2 见）、新施後重叠两见⛔，俱不写',
              not v and '原 2 见' in o and '於行 1×2' in o and not v2 and '新於施後 2 见' in o2 and 读档(丙) == 丙文 and 读档(戊) == 戊文))
    丁 = '设定/丁.md'; 丁文 = '一：老井。\n二：新坟。\n'; 写档(丁, 丁文)
    def 并写():
        with open(os.path.join(t, 丁), 'a', encoding='utf-8') as f:
            f.write('三：他席并写之行。\n')
    v, o = 跑(单([{'档': 丁, '原': '老井', '新': '老井（据 剧情庭_试·九）', '由': '九'}]), 落=True, _验後=并写)
    r.append(('㉓施单·验後盘上已变（他席并写）⛔写，盘上留他席之文', not v and '验後盘上已变' in o
              and 读档(丁) == 丁文 + '三：他席并写之行。\n'))
    写档('正文/第1章.md', '老井在村东。\n'); 写档('设定/剧情庭_势_第1段.md', '裁：守原。\n'); 写档('设定/修改清单.md', '清单\n')
    open(账档, 'a', encoding='utf-8').close()
    自单 = os.path.join(t, '设定', '自指单.json')
    open(自单, 'w', encoding='utf-8').write(json.dumps([{'档': '设定/自指单.json', '原': '自指单', '新': '他单', '由': 'x'}], ensure_ascii=False))
    禁果 = {}
    for 档, 期 in (('正文/第1章.md', '施於正文'), ('设定/剧情庭_势_第1段.md', '剧情庭之裁档'), (os.path.relpath(账档, t), '改单之账'),
                   ('设定/修改清单.md', '改单之账')):
        原 = {'正文/第1章.md': '老井', '设定/剧情庭_势_第1段.md': '守原', '设定/修改清单.md': '清单'}.get(档, '单')
        before = 读档(档)
        v, o = 跑(单([{'档': 档, '原': 原, '新': 原 + '甲', '由': 'x'}]), 落=True)
        禁果[档] = (not v and 期 in o and 读档(档) == before)
    v, o = 跑(自单, 落=True)
    禁果['单档本身'] = not v and '单档本身' in o
    r.append(('㉔施单·正文／剧情庭裁档／改单账／修改清单／单档本身俱⛔、不写', all(禁果.values()) and len(禁果) == 5))
    账档, 清单, ROOT = 旧
    shutil.rmtree(t, ignore_errors=True)
    r += _庭单之约()
    for n, v in r:
        print(('  ✓ ' if v else '  ⛔ ') + n)
    print('负测·改单 %d/%d' % (sum(v for _, v in r), len(r)))
    return all(v for _, v in r)


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--自测' in a:
        sys.exit(0 if 自测() else 1)
    if '--施单' in a:
        def _参(k):
            if k not in a:
                return None
            i = a.index(k)
            if i + 1 >= len(a) or a[i + 1].startswith('--'):
                print('⛔ %s 须带其值' % k); sys.exit(2)
            return a[i + 1]
        单档 = _参('--施单')
        根 = _参('--根')
        if 根:
            ROOT = os.path.realpath(根)
            账档 = os.path.join(ROOT, '设定', '改单账.json'); 清单 = os.path.join(ROOT, '设定', '修改清单.md')
        sys.exit(0 if 施单(单档, 落='--落' in a, 号=_参('--号')) else 1)
    if '--查' in a:
        sys.exit(0 if 查()[0] else 1)
    if '--立' in a:
        i = a.index('--立'); sys.exit(0 if 立(a[i + 1], a[i + 2], a[i + 3:]) else 1)
    if '--补登' in a:
        i = a.index('--补登'); sys.exit(0 if 补登(a[i + 1], a[i + 2:]) else 1)
    if '--毕' in a:
        i = a.index('--毕'); sys.exit(0 if 毕(a[i + 1], a[i + 2]) else 1)
    for x in 读()['单']:
        print('%s ｜%s｜%s｜更好在哪：%s' % (x['号'], x['状'], x['何'], x['更好在哪'][:50]))
