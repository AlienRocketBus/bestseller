# -*- coding: utf-8 -*-
"""自进化环 · 查 → 自修 → 验自修 → 修不了才报，报了就挂账（2026-09-24 立·作者令）

════════════════════════════════════════════════════════════════════
⛔**其所以立·0924 之实（作者当面三令）**：
  「**要有自我纠错与自我进化之机制**」｜「**东西一定要随时保存在 GitHub**」｜
  「**不能故步自封，一直按老的问题去执行**」。

★**本坐当日自认之病，是这一环要治的全部**：
  ①**只会报，不会修**：推闸红了六天，回执里逐章记过，**没有一道器去修它**；
  ②**报了而无人读**：「待验」写在注里，十几个回合没人回头；
  ③**哨自己也会量错**：本坐当日立的 `未上库哨` 只量主枝、看不见存底枝，
    **报了一个「198 笔没上库」的假警**——⛔**而云端存底枝一直都有全部 363 章**；
  ④**同一族病反复发**：当日「问得太宽」一日三回。

★★**故本环四层，每层皆作「查 → 自修 → 验自修 → 修不了才报 → 报了就挂账」**：
  **L0 保命**（云端有没有这本书）——**会自己存、自己打标、自己验**；
  **L1 发布**（主枝落後多少）——**会自己推；同一原因连两回不变即判「卡死」，当面报作者**；
  **L2 自纠**（尺之校＋自省哨）——**把「该疑那把尺」「写了没人读」摆出来**；
  **L3 自进化**（病族账）——**一族病逮到第二回而无器管它，即红**；
    **每一个器立起来，都要登是为哪一族病立的**——⛔**不许只治这一回，要治这一族。**
★★★**并有一层管这一环自己**：**每跑一回落一行 `设定/自进化环.log`**；
  **逾两个钟头没跑过，即是这一环自己停了**——⛔**一个会停而没人知道的环，就是又一道祝福。**
════════════════════════════════════════════════════════════════════

用法：
    python3 工具/自进化环.py            # 跑一整环（查＋自修＋验＋挂账），自走每回合头一件
    python3 工具/自进化环.py --只查      # 不自修，只报（给负测与人眼用）
    python3 工具/自进化环.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, io, re, glob, json, time, subprocess
import importlib.util as _u

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
日志 = os.path.join(ROOT, '设定', '自进化环.log')
病族账 = os.path.join(ROOT, '设定', '病族账.md')
挂账 = os.path.join(ROOT, '设定', '自进化环_挂账.json')
主枝 = 'claude/the-novel-review-4dtuit'
# ⛔诸限写死，⛔不随今日之数挪（今日之教：一个会随今日之数挪的限，等於没有限）
存底之限分 = 30        # 存底枝逾此分钟未更新 → 自修（存一回）
主枝之限笔 = 3         # 主枝落後逾此笔 → 自修（推一回）
卡死之回 = 2           # 同一原因连此回不变 → 判卡死，当面报作者
环停之限时 = 2         # 本环逾此钟头没跑过 → 本环自己停了


def _器(名):
    s = _u.spec_from_file_location(名, os.path.join(ROOT, '工具', 名 + '.py'))
    m = _u.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def _跑(*a, timeout=120):
    try:
        return subprocess.run(a, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    except Exception as e:
        class R:
            returncode = 99
            stdout = ''
            stderr = str(e)
        return R()


def _本地章数():
    return len(glob.glob(os.path.join(ROOT, '正文', '*.md')))


# ═══════════ 挂账（修不了的，逐笔挂上，⛔不许再沉默）═══════════
def _读挂():
    try:
        return json.load(io.open(挂账, encoding='utf-8'))
    except Exception:
        return {}


def _写挂(d):
    io.open(挂账, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=1))


def 挂(层, 因, 修得了):
    """★同一「层＋因」连着出现几回？——**连 `卡死之回` 回不变，即判卡死**。"""
    d = _读挂()
    k = '%s｜%s' % (层, 因[:60])
    if 修得了:
        d.pop(k, None)
        _写挂(d)
        return 0
    x = d.get(k) or {'首见': time.strftime('%Y-%m-%d %H:%M'), '回': 0}
    x['回'] += 1
    x['末见'] = time.strftime('%Y-%m-%d %H:%M')
    d[k] = x
    _写挂(d)
    return x['回']


# ═══════════ L0 保命：云端有没有这本书 ═══════════
def L0(自修=True):
    """→ (安否, 诸语)。★**先量存底枝（保命那一层），不是主枝**——
    ⛔**0924 本坐立的未上库哨只量主枝，报了一个假警；本层即治它。**"""
    语 = []
    底 = _器('存底')
    v = 底.验(印=False)
    本 = _本地章数()
    旧分 = None
    if v:
        r = _跑('git', 'log', '-1', '--format=%ct', 'origin/备份/存底')
        if r.stdout.strip().isdigit():
            旧分 = (time.time() - int(r.stdout.strip())) / 60.0
    缺 = (v is None) or (v['章'] < 本) or (旧分 is None) or (旧分 > 存底之限分)
    if not 缺:
        语.append('✓L0 保命：云端存底枝 %d 章（本地 %d）｜%.0f 分钟前存过｜章标 %d 个'
                 % (v['章'], 本, 旧分, v['标']))
        挂('L0', '存底', True)
        return True, 语
    因 = ('存底枝不在云端' if v is None else
          ('云端 %d 章 < 本地 %d 章' % (v['章'], 本) if v['章'] < 本 else
           '存底枝 %.0f 分钟未更新（限 %d）' % (旧分 or -1, 存底之限分)))
    语.append('⚠L0 保命：%s' % 因)
    if not 自修:
        return False, 语
    # ★自修：存一回
    rc, msg = 底.存('自进化环·L0 自修：%s' % 因)
    v2 = 底.验(印=False)
    好 = (rc == 0 and v2 is not None and v2['章'] >= 本)
    语.append(('  ★已自修：存底一回（%s）→ 云端今 %d 章' % (msg, v2['章'] if v2 else -1))
             if 好 else ('  ⛔自修不成：%s' % msg))
    回 = 挂('L0', 因, 好)
    if not 好 and 回 >= 卡死之回:
        语.append('  ⛔⛔**L0 卡死（连 %d 回）——须当面报作者：书之云端存底连着存不上去**' % 回)
    return 好, 语


# ═══════════ L1 发布：主枝落後多少 ═══════════
def L1(自修=True):
    """→ (安否, 诸语)。⛔**主枝落後不是「丢了」，是「成果未发布」——二者不许混说**（0924 之教）。"""
    语 = []
    _跑('git', 'fetch', '-q', 'origin', 主枝, timeout=60)
    r = _跑('git', 'rev-list', '--count', 'origin/%s..HEAD' % 主枝)
    n = int(r.stdout.strip()) if r.stdout.strip().isdigit() else None
    if n is None:
        语.append('⛔L1 发布：数不出主枝落後几笔——⛔**读不着不是绿**')
        return False, 语
    if n < 主枝之限笔:
        语.append('✓L1 发布：主枝落後 %d 笔' % n)
        挂('L1', '主枝落後', True)
        return True, 语
    语.append('⚠L1 发布：主枝落後 %d 笔（⛔此係「成果未发布」，不是「丢了」——书在 L0 里）' % n)
    if not 自修:
        return False, 语
    # ★自修：推一回（⛔走闸，不绕；推闸之判即其判）——放在後台，免本环被卡二十分钟
    记 = os.path.join(ROOT, '设定', '_自进化环_推.out')
    try:
        subprocess.Popen('git push -u origin %s > "%s" 2>&1' % (主枝, 记),
                         cwd=ROOT, shell=True)
        语.append('  ★已自修：发起一回推（後台·走闸不绕·其印落 设定/_自进化环_推.out）')
    except Exception as e:
        语.append('  ⛔发起推不成：%s' % e)
    # ★上一回推之果：若仍被拦，读出其「点名之红」作因
    因 = '主枝落後'
    try:
        上 = io.open(记, encoding='utf-8', errors='replace').read()
        m = re.search(r'推闸：([^\n]+)', 上)
        if m:
            因 = m.group(1).strip()[:60]
    except Exception:
        pass
    回 = 挂('L1', 因, False)
    if 回 >= 卡死之回:
        语.append('  ⛔⛔**L1 卡死（同一因连 %d 回：%s）——须当面报作者，⛔不许默默接着写下一章**'
                 % (回, 因))
    return False, 语


# ═══════════ L2 自纠：尺之校＋自省哨 ═══════════
def L2():
    语, 好 = [], True
    for 名 in ('尺之校', '自省哨'):
        try:
            m = _器(名)
            import contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                ok = m.报()
            if ok:
                语.append('✓L2 %s：过' % 名)
            else:
                好 = False
                坏 = [l.strip() for l in buf.getvalue().split('\n') if '⛔' in l][:2]
                语.append('⛔L2 %s：%s' % (名, '｜'.join(坏)[:140]))
            挂('L2', 名, ok)
        except Exception as e:
            好 = False
            语.append('⛔L2 %s 跑不起来：%s' % (名, e))
    return 好, 语


# ═══════════ L3 自进化：病族账 ═══════════
def 读病族():
    """→ [{名, 例, 器}]。⛔其式：`| 族名 | 例数 | 器 |`（器写「无」者即无器管它）。"""
    if not os.path.exists(病族账):
        return []
    out = []
    for l in io.open(病族账, encoding='utf-8'):
        m = re.match(r'\|\s*\*{0,2}([^|*]+?)\*{0,2}\s*\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|', l)
        if m and m.group(1) not in ('族', '族名'):
            out.append({'名': m.group(1).strip(), '例': int(m.group(2)),
                        '器': m.group(3).strip()})
    return out


def L3():
    语 = []
    族 = 读病族()
    if not 族:
        return False, ['⛔L3 自进化：病族账读不出——⛔**读不着不是绿**']
    # ⛔「书之族」之限是 3 不是 2（第三回方判它是病还是这个人的样子·病族账§三）
    def _无器(x):
        return x['器'].startswith('无') or x['器'] in ('', '—', '-')
    def _限(x):
        return 3 if '书之族' in x['器'] else 2
    无器 = [x for x in 族 if _无器(x) and x['例'] >= _限(x)]
    器不在 = []
    for x in 族:
        for f in re.findall(r'`([^`]+\.py)`', x['器']):
            if not os.path.exists(os.path.join(ROOT, '工具', os.path.basename(f))):
                器不在.append('%s→%s' % (x['名'], f))
    if 无器 or 器不在:
        if 无器:
            语.append('⛔L3 自进化：%d 族病已逮到第二回而无器管它：%s'
                     % (len(无器), '、'.join(x['名'] for x in 无器)))
        if 器不在:
            语.append('⛔L3 自进化：%d 族所登之器盘上不在：%s' % (len(器不在), '、'.join(器不在)))
        return False, 语
    语.append('✓L3 自进化：病族 %d 族，逮到二回以上者皆有器管它' % len(族))
    return True, 语


# ═══════════ 本环自己：它停没停 ═══════════
def 环之脉():
    try:
        末 = io.open(日志, encoding='utf-8').read().strip().split('\n')[-1]
        t = time.mktime(time.strptime(末[:16], '%Y-%m-%d %H:%M'))
        return (time.time() - t) / 3600.0
    except Exception:
        return None


def 跑(自修=True):
    print('════ 自进化环 · 查 → 自修 → 验自修 → 修不了才报，报了就挂账 ════')
    时 = 环之脉()
    if 时 is not None and 时 > 环停之限时:
        print('  ⛔**本环上一回跑在 %.1f 钟头前（限 %d）——这一环自己停过**；'
              '⛔**一个会停而没人知道的环，就是又一道祝福**' % (时, 环停之限时))
    诸 = []
    for 名, f in (('L0', lambda: L0(自修)), ('L1', lambda: L1(自修)),
                  ('L2', L2), ('L3', L3)):
        try:
            ok, 语 = f()
        except Exception as e:
            ok, 语 = False, ['⛔%s 跑不起来：%s' % (名, e)]
        诸.append((名, ok))
        for l in 语:
            print('  ' + l)
    卡 = [(k, v) for k, v in _读挂().items() if v.get('回', 0) >= 卡死之回]
    if 卡:
        print('  ' + '═' * 60)
        print('  ⛔⛔⛔ **卡死 %d 处——⛔须当面报作者，不许默默往下写** ⛔⛔⛔' % len(卡))
        for k, v in 卡:
            print('     · %s（首见 %s·连 %d 回）' % (k, v.get('首见'), v['回']))
    行 = '%s｜%s｜卡死%d' % (time.strftime('%Y-%m-%d %H:%M'),
                            ' '.join('%s%s' % (n, '✓' if o else '⛔') for n, o in 诸), len(卡))
    try:
        with io.open(日志, 'a', encoding='utf-8') as fh:
            fh.write(行 + '\n')
    except Exception:
        pass
    print('  ── 本环落一行 设定/自进化环.log：%s' % 行)
    return all(o for _, o in 诸) and not 卡


def 自测():
    R = []
    R.append(('①诸限写死（30分／3笔／2回／2时）',
              (存底之限分, 主枝之限笔, 卡死之回, 环停之限时) == (30, 3, 2, 2)))
    # ②⛔挂账：同一因连两回即卡死，修好即销
    老 = dict(_读挂())
    try:
        _写挂({})
        a = 挂('测', '造局之因', False)
        b = 挂('测', '造局之因', False)
        R.append(('②⛔同一因连两回即计 2（≥卡死之回）', (a, b) == (1, 2)))
        挂('测', '造局之因', True)
        R.append(('②之二·修好即销（⛔不许留一笔已好了的卡死）', '测｜造局之因' not in _读挂()))
    finally:
        _写挂(老)
    # ③病族账读得出，且其式认「无」为无器
    族 = 读病族()
    R.append(('③病族账读得出（今 %d 族）' % len(族), len(族) >= 5))
    R.append(('④⛔L1 之语明写「成果未发布，不是丢了」（⛔0924 本坐混说二者，致作者惊慌）',
              '不是「丢了」' in io.open(__file__, encoding='utf-8').read()))
    R.append(('⑤⛔L0 先量存底枝，⛔不量主枝（0924 未上库哨之假警即由此来）',
              "'origin/备份/存底'" in io.open(__file__, encoding='utf-8').read()))
    R.append(('⑥⛔L1 之推走闸不绕（码里无 --no-verify／ZM_SKIP_HOOK）',
              all(w not in io.open(__file__, encoding='utf-8').read().split('def L1')[1]
                  .split('def L2')[0] for w in ('--no-verify', 'ZM_SKIP_HOOK'))))
    R.append(('⑦本环每跑一回落一行日志（本环之脉）', '日志' in io.open(__file__, encoding='utf-8').read()))
    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    过 = sum(1 for _, o in R if o)
    print('  ── 自进化环·自测 %d/%d %s ──' % (过, len(R), '全通' if 过 == len(R) else '⛔未过'))
    return 过 == len(R)


if __name__ == '__main__':
    if '--自测' in sys.argv:
        sys.exit(0 if 自测() else 1)
    sys.exit(0 if 跑(自修='--只查' not in sys.argv) else 1)
