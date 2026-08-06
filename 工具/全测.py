#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全测——一条命令跑完全部回归，一个结论定去留。

【批115·立】病灶：此前验证须分四次调用（检察官 --selftest／--doctor／全书检、十轮精进 --自测），
  四段输出各看各的，遂有「改一处而不知碰坏他处」之隙；本会话已两度自证——
  ZM_REOPEN 所写空 soft 记录令存版必崩、同名夹具后者覆盖前者令二测名义在跑而实测旧局，
  皆是「改bug时造bug」而当时四段输出俱绿。
  故立全测：一条命令、一个退出码；并由 pre-push 钩子强制，不过不许推。

用法：
    python3 工具/全测.py            # 全跑
    python3 工具/全测.py --快        # 略过全书检（仅自检层，供频繁调用）
"""
import os
import re
import sys
import ast
import glob
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV = dict(os.environ, ZM_STREAM=os.environ.get('ZM_STREAM', 'streamA-cli'))


def run(desc, args, timeout=900):
    try:
        r = subprocess.run([sys.executable] + args, cwd=ROOT, env=ENV,
                           capture_output=True, text=True, timeout=timeout)
        return r.stdout + r.stderr
    except subprocess.TimeoutExpired:
        return '__TIMEOUT__'
    except Exception as e:
        return '__ERR__%s' % e


def chk_selftest():
    out = run('检察官自测', ['工具/小说检察官.py', '--selftest'])
    m = re.search(r'规则回归:(\d+)/(\d+)；契约负测:(\d+)/(\d+)；项目接线:(\S+?)；末章硬闸:(\S+)', out)
    if not m:
        return False, '未取到自测结论行'
    a, b, c, d, e, f = m.groups()
    ok = (a == b and c == d and e == '通过' and f.startswith('通过'))
    return ok, '规则回归%s/%s 契约负测%s/%s 接线%s 末章硬闸%s' % (a, b, c, d, e, f)


def chk_doctor():
    out = run('医生', ['工具/小说检察官.py', '--doctor'])
    m = re.search(r'医生结论: ERROR=(\d+)', out)
    if not m:
        return False, '未取到医生结论'
    return m.group(1) == '0', 'ERROR=%s' % m.group(1)


def chk_shilun():
    out = run('十轮精进负测', ['工具/十轮精进.py', '--自测'])
    m = re.search(r'负测（含端到端真跑）：(\d+)/(\d+)', out)
    if not m:
        m = re.search(r'负测：(\d+)/(\d+)', out)
    if not m:
        return False, '未取到负测结论'
    return m.group(1) == m.group(2), '%s/%s' % m.groups()


def chk_book():
    out = run('全书检', ['工具/小说检察官.py'])
    m = re.search(r'全书仪表盘:ERROR=(\d+)', out)
    if not m:
        return False, '未取到全书仪表盘'
    return m.group(1) == '0', 'ERROR=%s' % m.group(1)


def chk_dup_defs():
    """重名定义扫描。
    病灶实证：批113所加之 s_withlog／s_nolog／s_reopen 落在批114替换区之外而与新写者重名，
    后定义者覆盖前者，令二条负测名义在跑而实测旧局。此类错不报错、不崩、静默改变行为，
    非专测不可得。"""
    bad = []
    for f in sorted(glob.glob(os.path.join(ROOT, '工具', '*.py'))):
        try:
            tree = ast.parse(open(f, encoding='utf-8').read())
        except SyntaxError as e:
            bad.append('%s 语法错误 %s' % (os.path.basename(f), e))
            continue
        for node in ast.walk(tree):
            body = getattr(node, 'body', None)
            if not isinstance(body, list):
                continue
            seen = {}
            for st in body:
                if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if st.name in seen:
                        bad.append('%s: %s 于同一作用域重复定义（行%d 覆盖 行%d）'
                                   % (os.path.basename(f), st.name, st.lineno, seen[st.name]))
                    seen[st.name] = st.lineno
    return not bad, ('；'.join(bad) if bad else '工具目录内无重名定义')


def chk_zishu():
    """字数对齐探测器之回归。
    此规则住在 check_file 内，而检察官 138 条自测只跑 canon 正则（hits 不经 check_file），
    故其从来无回归——批117 修其二处误报时才发现。修探测器最忌静默削弱，
    故正测（真错须报）与负测（误报须不报）并立。"""
    import tempfile, importlib.util as u, sys
    sys.argv = ['x']
    sp = u.spec_from_file_location('_i2', os.path.join(ROOT, '工具', '小说检察官.py'))
    m = u.module_from_spec(sp)
    sp.loader.exec_module(m)

    def flagged(body):
        d = tempfile.mkdtemp()
        f = os.path.join(d, '镇冢秘术_第七章_测.md')
        open(f, 'w', encoding='utf-8').write('《镇冢秘术》\n\n第七章　测\n\n' + body + '\n')
        iss, _, _ = m.check_file(f)
        return any(x.startswith('[字数对齐]') for x in iss)

    POS = [   # 真错，必须报
        ('前向·数在前引在后', '过了几步他说了四个字。\n\n“今天你对了。”\n\n他点了点头。'),
        ('后向·引在前数在后', '“不知道。”\n\n这两个字从他嘴里出来，我心里咯噔一下。'),
        ('换行·引在前数在后', '“留给回来的人。”\n\n这四个字他说得很平。'),
    ]
    NEG = [   # 误报，必须不报
        ('数指前句非后句', '“等。”他说。\n\n就一个字。\n\n“等天黑。”'),
        ('数指前句非后句·二', '“不信。”\n\n就两个字。\n\n“那你来干什么。”'),
        ('数指前句非后句·三', '“摸。”\n\n一个字。\n\n“我先过。”'),
        ('两句合计报数', '“发烫，就回来。”\n\n他看着我。\n\n“灯灭。莫回头。”\n\n十个字，一个不差。'),
        ('数与引全合', '他说了五个字。\n\n“水一直在流。”'),
    ]
    bad = []
    for name, body in POS:
        if not flagged(body):
            bad.append('漏报:' + name)
    for name, body in NEG:
        if flagged(body):
            bad.append('误报:' + name)
    n = len(POS) + len(NEG)
    return not bad, ('；'.join(bad) if bad else '正测%d/负测%d 全通' % (len(POS), len(NEG)))


def chk_rhythm():
    """节奏方差闸之回归（批119）。
    此闸为第153章起之硬错，若静默失效则新章之方差塌缩无人拦，
    而其病正是「机器一直在报却没人当真」（P26）——故正负测并立。"""
    import importlib.util as u, sys
    sys.argv = ['x']
    sp = u.spec_from_file_location('_i3', os.path.join(ROOT, '工具', '小说检察官.py'))
    m = u.module_from_spec(sp)
    sp.loader.exec_module(m)
    hdr = '《镇冢秘术》\n\n第一百五十三章　测\n\n'
    short = '\n\n'.join(['他站住了。', '风从右边来。', '我数到三。'] * 12)
    longp = '这一段要连着跑到一百二十字以上，不断行，不换气，' \
            '把该慢下来的地方慢足了：他把手按在壁上，先是掌心，' \
            '再是掌根，最后是整只手贴上去，土从指缝里往下掉，' \
            '掉到鞋面上，又从鞋面上滑下去，落地没有声音，' \
            '因为地上原本就铺着一层同样的土；他就那么按着，' \
            '按到掌心底下那一块也凉了，才把手收回来。'
    mid = '\n\n'.join(['他把灯举起来又放下，举的时候手是稳的，放的时候手抖了一下，抖不是怕，是举得久了。'] * 8)
    V = m.rhythm_violation
    bad = []
    # 正测：新章违规须报
    if not V(hdr + short, 153):
        bad.append('漏报:全短段之新章')
    if not V(hdr + short + '\n\n' + mid, 153):
        bad.append('漏报:90分位不足30字')
    # 负测：不得误报
    if V(hdr + mid + '\n\n' + longp + '\n\n' + mid, 153):
        bad.append('误报:有长段且90分位达标')
    if V(hdr + short, 152):
        bad.append('误报:历史章(第152章)不受此闸')
    if V(hdr + short, 153, exempt=True):
        bad.append('误报:已登记节奏豁免者')
    return not bad, ('；'.join(bad) if bad else '正测2/负测3 全通')


def chk_lunci():
    """轮次完整性诸闸之回归（批121）。
    病灶（作者亲报，本会话第153章第7轮亲犯）：十轮常只跑七八轮／轮次跳号。
    链条：某轮存版被拦而未察→轮记按台账末版标错号→正文与末版脱节→带病连跑数轮。
    此测守三口：发轮前置闸、轮记版未到闸、封版十轮不满闸。"""
    import importlib.util as u, sys, tempfile, json, os as _o, io, contextlib
    sys.argv = ['x']
    sp = u.spec_from_file_location('_i4', os.path.join(ROOT, '工具', '十轮精进.py'))
    m = u.module_from_spec(sp)
    sp.loader.exec_module(m)
    sp2 = u.spec_from_file_location('_i5', os.path.join(ROOT, '工具', '小说检察官.py'))
    m2 = u.module_from_spec(sp2)
    sp2.loader.exec_module(m2)
    bad = []
    _R, _J = m.ROOT, m.JJ_DIR
    tmp = tempfile.mkdtemp(prefix='zm_lc_')
    try:
        _o.makedirs(_o.path.join(tmp, '正文'))
        _o.makedirs(_o.path.join(tmp, '设定'))
        m.ROOT, m.JJ_DIR = tmp, _o.path.join(tmp, '版本')
        f = _o.path.join(tmp, '正文', '镇冢秘术_第七章_测.md')
        d = _o.path.join(tmp, '版本', '第7章')
        _o.makedirs(d)
        open(f, 'w', encoding='utf-8').write('《镇冢秘术》\n\n第七章　测\n\n原始\n')
        open(_o.path.join(d, 'v01.md'), 'w', encoding='utf-8').write(
            open(f, encoding='utf-8').read())
        json.dump({'章': 7, '版本': [{'版': 'v01', '时': 'x', '说明': '第1轮·甲',
                   'hard': {}, 'soft': {'净重': 9}, '全书章数': 1}]},
                  open(_o.path.join(d, '_台账.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc_clean = m.nextround(7)                       # 正文与末版一致→须发轮
        open(f, 'w', encoding='utf-8').write('《镇冢秘术》\n\n第七章　测\n\n改过了\n')
        buf2 = io.StringIO()
        with contextlib.redirect_stdout(buf2):
            rc_drift = m.nextround(7)                       # 正文已偏→须拒发轮
        if rc_clean == 2:
            bad.append('误拦:正文与末版一致时不得拒发轮')
        if rc_drift != 2:
            bad.append('漏拦:上一轮未落台账仍发新轮')
        # 轮记版未到闸
        json.dump({'时': 'x', '正文sha': 'a', '末版sha': 'a', '目标轮': 5},
                  open(_o.path.join(d, '_领轮.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        buf3 = io.StringIO()
        with contextlib.redirect_stdout(buf3):
            rc_lj = m.lunji_append(7, '测')                 # 所领第5轮而台账末版第1轮→须拒
        if rc_lj != 2:
            bad.append('漏拦:轮记比版先到')
        if _o.path.exists(_o.path.join(d, '_轮记.md')):
            bad.append('漏拦:拒写轮记却仍落了盘')
    finally:
        m.ROOT, m.JJ_DIR = _R, _J
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
    if not hasattr(m2, '_rounds_full'):
        bad.append('缺:封版十轮不满闸未接线')

    # ── 拦停旗（批122）：漏读一次拦停不得等于走得过去 ──
    tmp2 = tempfile.mkdtemp(prefix='zm_flag_')
    try:
        _o.makedirs(_o.path.join(tmp2, '正文'))
        _o.makedirs(_o.path.join(tmp2, '设定'))
        m.ROOT, m.JJ_DIR = tmp2, _o.path.join(tmp2, '版本')
        f2 = _o.path.join(tmp2, '正文', '镇冢秘术_第七章_测.md')
        d2 = _o.path.join(tmp2, '版本', '第7章')
        _o.makedirs(d2)
        open(f2, 'w', encoding='utf-8').write('《镇冢秘术》\n\n第七章　测\n\n甲\n')
        open(_o.path.join(d2, 'v01.md'), 'w', encoding='utf-8').write(
            open(f2, encoding='utf-8').read())
        json.dump({'章': 7, '版本': [{'版': 'v01', '时': 'x', '说明': '第1轮·甲',
                   'hard': {}, 'soft': {'净重': 9}, '全书章数': 1}]},
                  open(_o.path.join(d2, '_台账.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        b3 = io.StringIO()
        with contextlib.redirect_stdout(b3):
            no_flag = m.flag_block(7, '发轮')
        if no_flag:
            bad.append('误拦:无旗时不得拒办')
        m.raise_flag(7, '测试之由', '第2轮·测')
        b4 = io.StringIO()
        with contextlib.redirect_stdout(b4):
            has_flag = m.flag_block(7, '发轮')
            rc_nr = m.nextround(7)
            rc_lj = m.lunji_append(7, '测')
        if not has_flag:
            bad.append('漏拦:有旗仍放行')
        if rc_nr != 2:
            bad.append('漏拦:有旗仍发轮')
        if rc_lj != 2:
            bad.append('漏拦:有旗仍写轮记')
        if _o.path.exists(_o.path.join(d2, '_轮记.md')):
            bad.append('漏拦:有旗仍落了轮记')
        # 一次成功存版须销旗
        open(f2, 'w', encoding='utf-8').write('《镇冢秘术》\n\n第七章　测\n\n甲乙丙\n')
        json.dump({'时': 'x', '正文sha': m._sha(open(_o.path.join(d2, 'v01.md'), encoding='utf-8').read()),
                   '末版sha': m._sha(open(_o.path.join(d2, 'v01.md'), encoding='utf-8').read()),
                   '目标轮': 2},
                  open(_o.path.join(d2, '_领轮.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        open(_o.path.join(d2, '_轮记.md'), 'w', encoding='utf-8').write('\n## 第1轮|v01|x|净重9\n所见\n')
        b5 = io.StringIO()
        with contextlib.redirect_stdout(b5):
            rc_ok = m.save(7, '第2轮·四堂会审')
        if rc_ok != 0:
            bad.append('误拦:清白之存版被旗拦（旗当由此次成功销去）')
        elif m.read_flag(7) is not None:
            bad.append('漏销:存版成功而旗未销')
    finally:
        m.ROOT, m.JJ_DIR = _R, _J
        import shutil as _sh
        _sh.rmtree(tmp2, ignore_errors=True)

    # ── 第十一轮总核（批123）──
    tmp3 = tempfile.mkdtemp(prefix='zm_zh_')
    try:
        _o.makedirs(_o.path.join(tmp3, '正文'))
        _o.makedirs(_o.path.join(tmp3, '设定'))
        m.ROOT, m.JJ_DIR = tmp3, _o.path.join(tmp3, '版本')
        f3 = _o.path.join(tmp3, '正文', '镇冢秘术_第七章_测.md')
        d3 = _o.path.join(tmp3, '版本', '第7章')
        _o.makedirs(d3)
        SOFT = {'净重': 100, '段数': 9, '均段': 11, '长段数': 1, '嗅': 3, '听': 4, '触': 7,
                '视': 2, '老头': 1, '钱满': 1, '沈鸢': 0, '四字串三现': 0, '顿悟起手': 0}
        def build(rounds, logs, same=None):
            vs = []
            for k, r in enumerate(rounds, 1):
                vn = 'v%02d' % k
                body = '《镇冢秘术》\n\n第七章　测\n\n' + ('同一段' if (same and k in same) else '第%d段内容' % k) + '\n'
                open(_o.path.join(d3, vn + '.md'), 'w', encoding='utf-8').write(body)
                vs.append({'版': vn, '时': 'x', '说明': r, 'hard': {}, 'soft': dict(SOFT), '全书章数': 1})
            json.dump({'章': 7, '版本': vs}, open(_o.path.join(d3, '_台账.json'), 'w', encoding='utf-8'), ensure_ascii=False)
            open(f3, 'w', encoding='utf-8').write(
                open(_o.path.join(d3, 'v%02d.md' % len(rounds)), encoding='utf-8').read())
            open(_o.path.join(d3, '_轮记.md'), 'w', encoding='utf-8').write(logs)
            for z in ('_总核.json', '_拦停.json'):
                if _o.path.exists(_o.path.join(d3, z)):
                    _o.remove(_o.path.join(d3, z))
        # 必答表自正文抽出，故须先有正文，_log 方取得到（否则 duty_list 返回空表）
        open(f3, 'w', encoding='utf-8').write('《镇冢秘术》\n\n第七章　测\n\n三天两头十三天四个人五样两副三圈\n')

        def _log(i):
            try:
                duties = m.duty_list(7, i)[0]
            except Exception:
                duties = []
            return ('\n## 第%d轮|v%02d|x|净重100\n**镜头**：%s\n**必答逐项**：%s\n'
                    '**真伤**：一根，已改。%s\n'
                    % (i, i, '｜'.join(m.LENS_KEY[i]),
                       '；'.join(duties) if duties else '本轮无可机抽之必答项',
                       '补白之句' * 40))
        full_log = ''.join(_log(i) for i in range(1, 11))
        # 正测：十轮齐、记齐、无空轮 → 须过
        build(['第%d轮·甲' % i for i in range(1, 11)], full_log)
        b6 = io.StringIO()
        with contextlib.redirect_stdout(b6):
            rc_full = m.zonghe(7)
        if rc_full != 0:
            bad.append('误拦:十轮齐备之章总核应过（%s）' % b6.getvalue()[-160:].replace('\n', ' '))
        elif not _o.path.exists(_o.path.join(d3, '_总核.json')):
            bad.append('漏写:总核过而未出凭据')
        # 负测一：缺第10轮
        build(['第%d轮·甲' % i for i in range(1, 10)],
''.join(_log(i) for i in range(1, 10)))
        with contextlib.redirect_stdout(io.StringIO()):
            if m.zonghe(7) != 2:
                bad.append('漏拦:缺第10轮仍判总核过')
        # 负测二：版齐而轮记缺一轮
        build(['第%d轮·甲' % i for i in range(1, 11)],
''.join(_log(i) for i in range(1, 11) if i != 4))
        with contextlib.redirect_stdout(io.StringIO()):
            if m.zonghe(7) != 2:
                bad.append('漏拦:缺一轮之轮记仍判总核过')
        # 负测三：空轮而未记判不补
        build(['第%d轮·甲' % i for i in range(1, 11)], full_log, same={5, 6})
        with contextlib.redirect_stdout(io.StringIO()):
            if m.zonghe(7) != 2:
                bad.append('漏拦:空轮未记判不补仍判总核过')
        # 负测四：轮记过简
        build(['第%d轮·甲' % i for i in range(1, 11)],
              ''.join('\n## 第%d轮|v%02d|x|净重100\n真伤：无\n' % (i, i) for i in range(1, 11)))
        with contextlib.redirect_stdout(io.StringIO()):
            if m.zonghe(7) != 2:
                bad.append('漏拦:轮记过简仍判总核过')
        # 负测六：抄清单而不裁（提及100%而裁定0%）——批125之核心
        def _naked_log(i):
            try:
                du = m.duty_list(7, i)[0]
            except Exception:
                du = []
            return ('\n## 第%d轮|v%02d|x|净重100\n**镜头**：%s\n'
                    '本轮所涉：%s\n段数9 长段1\n%s\n'
                    % (i, i, '｜'.join(m.LENS_KEY[i]),
                       '、'.join(du) if du else '无', '补白之句' * 40))
        build(['第%d轮·甲' % i for i in range(1, 11)],
              ''.join(_naked_log(i) for i in range(1, 11)))
        with contextlib.redirect_stdout(io.StringIO()):
            if m.zonghe(7) != 2:
                bad.append('漏拦:抄清单而不逐项裁定仍判总核过（批125之核心）')
        # 负测七：对数对不上（轮记不含台账所记之数）
        def _nonum_log(i):
            try:
                du = m.duty_list(7, i)[0]
            except Exception:
                du = []
            return ('\n## 第%d轮|v%02d|x|净重甚多\n**镜头**：%s\n'
                    '%s\n**真伤**：一根，已改核合。%s\n'
                    % (i, i, '｜'.join(m.LENS_KEY[i]),
                       '；'.join('%s：已核判合' % x for x in du) if du else '无',
                       '补白之句' * 40))
        build(['第%d轮·甲' % i for i in range(1, 11)],
              ''.join(_nonum_log(i) for i in range(1, 11)))
        with contextlib.redirect_stdout(io.StringIO()):
            if m.zonghe(7) != 2:
                bad.append('漏拦:轮记之数对不上台账仍判总核过')
        # 负测八：轮轮判合、全章无真伤
        def _nohurt_log(i):
            try:
                du = m.duty_list(7, i)[0]
            except Exception:
                du = []
            return ('\n## 第%d轮|v%02d|x|净重100\n**镜头**：%s\n段数9 长段1\n'
                    '%s\n**本轮真伤无，判不补。**%s\n'
                    % (i, i, '｜'.join(m.LENS_KEY[i]),
                       '；'.join('%s：已核判合' % x for x in du) if du else '无',
                       '补白之句' * 40))
        build(['第%d轮·甲·判不补' % i for i in range(1, 11)],
              ''.join(_nohurt_log(i) for i in range(1, 11)))
        with contextlib.redirect_stdout(io.StringIO()):
            if m.zonghe(7) != 2:
                bad.append('漏拦:全章十轮皆无真伤仍判总核过（产出基线）')
        # 负测五：拦停旗未销
        build(['第%d轮·甲' % i for i in range(1, 11)], full_log)
        m.raise_flag(7, '测', '第9轮')
        with contextlib.redirect_stdout(io.StringIO()):
            if m.zonghe(7) != 2:
                bad.append('漏拦:拦停旗未销仍判总核过')
    finally:
        m.ROOT, m.JJ_DIR = _R, _J
        import shutil as _s2
        _s2.rmtree(tmp3, ignore_errors=True)
    if not hasattr(m2, '_zonghe_ok'):
        bad.append('缺:封版总核闸未接线')
    # ── 检察官侧第十一轮五检（批126）──
    # ── 回执闸之在跑判（批130）──
    if not hasattr(m2, '_in_progress'):
        bad.append('缺:回执闸在跑判未接线')
    else:
        # 【批130·修】原测断言「第157章须判在跑」——**而此为会变之状态**：
        #   其母章十轮一满，157即不再在跑，该测遂红。批127已立此戒（负测不得钉在会变的状态上，
        #   须钉在不变的契约上），而立批130之负测时又犯，此其第二回。
        # 今只测不变之契约：不存在之章与已封版之章一律非在跑；返回值须为 bool。
        try:
            for ch in (999999, 152, 100):
                v = m2._in_progress(ch)
                if not isinstance(v, bool):
                    bad.append('在跑判返回值非bool(第%d章)' % ch)
                elif v:
                    bad.append('误判:第%d章（不存在或已封版）竟判在跑' % ch)
        except Exception as e:
            bad.append('在跑判运行失败:%s' % e)
    if not hasattr(m2, 'round11_audit'):
        bad.append('缺:检察官侧第十一轮未接线')
    elif not hasattr(m2, '_round11_main'):
        bad.append('缺:第十一轮两眼齐审总入口未接线')
    else:
        try:
            # 【批127·修】原测断言「第153章须有硬项」，而那是写测当日之临时状态；
            # 该章补齐之后此测反红——**负测不得钉在会变的状态上，须钉在不变的契约上**。
            o, h, sf = m2.round11_audit(153)
            if not (isinstance(o, list) and isinstance(h, list) and isinstance(sf, list)):
                bad.append('检察官侧第十一轮返回值不合约（须为三列表）')
            keys = ('圣经', '到期账', '回述', '病号', '翻页')
            if not all(any(k in x for x in o) for k in keys):
                bad.append('检察官侧第十一轮之五检要目不全（应出圣经／到期账／回述／病号／翻页五节）')
            o2, h2, _ = m2.round11_audit(999999)
            if not h2:
                bad.append('漏拦:不存在之章竟无硬项')
        except Exception as e:
            bad.append('检察官侧第十一轮运行失败:%s' % e)

    return not bad, ('；'.join(bad) if bad else '正测3/负测23 全通')


def chk_hookspath():
    """钩子须挂上：容器每次重建后 .git 皆新，故 hooksPath 须指向受版本管理之目录。"""
    want = '工具/githooks'
    try:
        r = subprocess.run(['git', 'config', '--get', 'core.hooksPath'],
                           cwd=ROOT, capture_output=True, text=True, timeout=30)
        cur = r.stdout.strip()
    except Exception as e:
        return False, '读取失败 %s' % e
    hook = os.path.join(ROOT, want, 'pre-push')
    if not os.path.exists(hook):
        return False, '缺 %s' % want + '/pre-push'
    if cur != want:
        subprocess.run(['git', 'config', 'core.hooksPath', want],
                       cwd=ROOT, capture_output=True, text=True, timeout=30)
        return True, '原为「%s」，已自动挂回 %s' % (cur or '未设', want)
    if not os.access(hook, os.X_OK):
        os.chmod(hook, 0o755)
        return True, '已挂，并补回执行位'
    return True, '已挂 %s' % want


def main():
    quick = '--快' in sys.argv
    items = [('重名定义扫描', chk_dup_defs), ('钩子挂载', chk_hookspath),
             ('字数对齐回归', chk_zishu),
             ('节奏方差闸回归', chk_rhythm),
             ('轮次完整性回归', chk_lunci),
             ('检察官自测', chk_selftest), ('医生', chk_doctor),
             ('十轮精进负测', chk_shilun)]
    if not quick:
        items.append(('全书检', chk_book))
    print('\n████ 全测 · %d 项 ████' % len(items))
    fails = []
    for name, fn in items:
        ok, detail = fn()
        print('  %s %-14s %s' % ('✓' if ok else '✗', name, detail))
        if not ok:
            fails.append(name)
    if fails:
        print('\n  ⛔全测未过：%s' % '、'.join(fails))
        print('  【批115】不过不许推——pre-push 钩子据此拦停。')
        return 1
    print('\n  ✓全测通过%s。' % ('（快测，未含全书检）' if quick else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main())
