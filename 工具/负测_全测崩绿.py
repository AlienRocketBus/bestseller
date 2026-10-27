# -*- coding: utf-8 -*-
"""负测·全测崩绿（2026-09-05·机制总审·八路之陪跑闸审第1、2、11条所立）

★所测者一句话：**一件器崩了，全测那一行还绿不绿。**
★★其红在哪一行（八路之复现，本坐上磁盘再核）：chk_big_questions／chk_person_ledger／chk_two_ledger／
   chk_grand_audit／chk_huixiu／chk_duiwei／chk_object_roll_all 七项，皆只在印里找「⛔」或某个数——
   ★★★以一段 traceback 灌之，旧式 run()（原样返 stdout＋stderr）之下 **7/7 返 True**。
   ⛔1027：chk_huixiu、chk_duiwei 随回修、对位汰；换入 chk_outside_voice（旧式亦只认其数——今补索其自印之头），今六项。
★★★★而一份在旧式下也全过的测就是陪跑（令§六③）——**故其要害在①：旧式回灌须六项俱绿，方证此洞是真的。**
★★★★★另测第11条：旧式超时以 SIGKILL 杀子进程，子进程之 finally 不跑——负测在真仓库上改的档留在盘上。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import importlib.util
import io
import os
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TB = ('Traceback (most recent call last):\n  File "工具/大问表.py", line 1, in <module>\n'
      "    import nothing_here\nModuleNotFoundError: No module named 'nothing_here'\n")
HOOKS = ('chk_big_questions', 'chk_person_ledger', 'chk_two_ledger', 'chk_grand_audit',
         'chk_outside_voice', 'chk_object_roll_all')
K = len(HOOKS)


def _load():
    spec = importlib.util.spec_from_file_location('quance', os.path.join(ROOT, '工具', '全测.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def run():
    R = []
    q = _load()
    real_run = q.run

    # ①旧式回灌·以改前之 全测.py（钉在 a73c8836：乙一之前末一笔提交，非 HEAD）灌 traceback 之印，七项须 7/7 绿——证此洞是真的
    #   ★2026-09-05 改：旧断以「今之 hook＋旧之 run」为旧式；而今各 hook 亦已加「器印之头」之验，旧式须整档取旧，方不自绿。
    import subprocess, tempfile
    旧源 = subprocess.run(['git', 'show', 'a73c8836:工具/全测.py'], cwd=ROOT, capture_output=True, text=True).stdout
    旧 = None
    if 旧源:
        fd, tmp = tempfile.mkstemp(prefix='quance_old_', suffix='.py', dir=os.path.join(ROOT, '工具'))
        os.close(fd)
        io.open(tmp, 'w', encoding='utf-8').write(旧源)
        try:
            spec = importlib.util.spec_from_file_location('quance_old', tmp)
            旧 = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(旧)
        finally:
            os.remove(tmp)
    if 旧 is not None:
        旧.run = lambda *a, **k: TB
        old_green = sum(1 for h in HOOKS if getattr(旧, h)()[0])
        旧.run = lambda *a, **k: '（某器改了标签）一切都好\n'
        old_green2 = sum(1 for h in HOOKS if getattr(旧, h)()[0])
    else:
        old_green = old_green2 = -1
    R.append(('①旧式回灌·改前（a73c8836）之全测以 traceback 灌诸项，绿 %d/%d；以无头之印灌，绿 %d/%d（须皆满·证二洞）' % (old_green, K, old_green2, K),
              old_green == K and old_green2 == K))

    # ②新式·run() 遇子进程 traceback 返 None
    q.run = real_run
    r2 = q.run('崩', ['-c', 'raise RuntimeError("boom")'])
    R.append(('②新式·子进程 traceback → run() 返 None', r2 is None))

    # ③新式·run 返 None 时诸项须俱红
    q.run = lambda *a, **k: None
    new_red = sum(1 for h in HOOKS if not getattr(q, h)()[0])
    q.run = real_run
    R.append(('③新式·run 返 None，诸项红 %d/%d（须满）' % (new_red, K), new_red == K))

    # ④超时·先 SIGINT，子进程之 finally 得跑（旧式 SIGKILL 下 finally 不跑，档留 MUTATED）
    fd, tmp = tempfile.mkstemp(prefix='zm_crash_', suffix='.txt')
    os.close(fd)
    io.open(tmp, 'w', encoding='utf-8').write('MUTATED')
    t0 = time.time()
    r4 = q.run('超时', ['-c', ('import time,sys\ntry:\n    time.sleep(30)\nfinally:\n'
                                '    open(sys.argv[1],"w").write("RESTORED")'), tmp], timeout=1)
    dt = time.time() - t0
    got = io.open(tmp, encoding='utf-8').read()
    os.remove(tmp)
    R.append(('④超时·返 None 且子进程 finally 已跑（档=%s，用时 %.1fs）' % (got, dt),
              r4 is None and got == 'RESTORED' and dt < 20))

    # ⑤不误伤·器正常印「⛔」者照旧原样返印（返非空且含⛔）
    r5 = q.run('正常', ['-c', 'print("⛔ 试")'])
    R.append(('⑤不误伤·正常之印原样返（含⛔）', bool(r5) and '⛔' in r5))

    # ⑥不误伤·器返非零而无 traceback（如开轮六检查出即返2）仍返印
    r6 = q.run('返2', ['-c', 'import sys; print("⛔ 查出"); sys.exit(2)'])
    R.append(('⑥不误伤·返码非零而无 traceback 者仍返印', bool(r6) and '查出' in r6))

    # ⑦自陈在册·run() 之注写明它只认「崩」，不认「印错」（§一⑤）
    src = io.open(os.path.join(ROOT, '工具', '全测.py'), encoding='utf-8').read()
    R.append(('⑦自陈在册·run() 注明只认「崩」不认「印错」', '本函只认「崩」' in src and '仍须各 hook 自验其项名' in src))

    # ⑧留字之查·在 版本/ 下临时留一档，快照之差须报其名；删去後须归零
    snap = q._留字快照()
    tmpf = os.path.join(ROOT, '版本', '_负测留字_临时.txt')
    io.open(tmpf, 'w', encoding='utf-8').write('留字')
    _变, _增, _失 = q._留字之差(snap)
    os.remove(tmpf)
    _变2, _增2, _失2 = q._留字之差(snap)
    R.append(('⑧留字之查·留一档即报其名（增 %d）；删去归零（%d/%d/%d）' % (len(_增), len(_变2), len(_增2), len(_失2)),
              _增 == ['版本/_负测留字_临时.txt'] and not _变 and not _失 and not (_变2 or _增2 or _失2)))

    # ⑨印错之路（八路·陪跑闸审「治了一半」所指）：器不崩而印错（无其自印之头），诸项须俱红——旧式（只索⛔或某数）俱绿
    q.run = lambda *a, **k: '（某器改了标签）一切都好\n'
    bogus_red = sum(1 for h in HOOKS if not getattr(q, h)()[0])
    q.run = real_run
    R.append(('⑨印错之路·无自印之头之印灌诸项，红 %d/%d（须满）' % (bogus_red, K), bogus_red == K))

    # ⑩⑪⑫ 吞红之路（2026-09-09·307封版席所逮·当日治·见 全测.py::_六检之败）：
    #   ★`开轮六检.py --静` 把当日所有之红以「；」串成**一行**，
    #     ★★而旧式 `_bad` 逐**行**判：见行内有「⑭」即整行跳过——**同行之别的红一并被吞**。
    #   ★★★本日之实（磁盘逐字）：`开轮六检.py 307 --静` 印⑨与⑭二红，rc=2，
    #     而全测印「✓ 开轮十六检　两头俱过」——**⑨从来没有进过 fails，推闸连开都没开。**
    #   ★★★★故此三条之要害在⑩：**旧式回灌须真绿**，方证此洞不是编的。
    实印307 = ('⑨·领轮之号 ⛔基线里无「目标轮」（领了轮而没记所领之号）；'
               '⑭·已封版之章 ⛔第307章已封版（十一轮✓／回执✓｜末章第307章）：'
               '★而封版之章不得再跑十轮——★★再跑会覆盖其回执与轮记。'
               '★★★而今之末章为第307章；★★★★下一章为第308章。')

    def 旧式(_t, _skip14):
        _b = []
        for _ln in (_t or '').splitlines():
            _x = _ln.strip()
            if not _x or '开轮十六检通过' in _x:
                continue
            if _skip14 and ('⑭' in _x or '已封版' in _x):
                continue
            _b.append(_x)
        return _b

    旧 = 旧式(实印307, True)
    R.append(('⑩旧式回灌·307之真印（⑨＋⑭同行）灌旧式，得 %d 条（须0·证此洞是真的）' % len(旧),
              len(旧) == 0))
    # ★1027：⑭随十三轮汰、「免⑭」之参随去——拆法照旧：断在「；」而其後紧接检号之处
    新 = q._六检之败(实印307)
    R.append(('⑪新式·同一份印得 %d 条，首为⑨（%s）、次为⑭' % (len(新), (新[0][:12] if 新 else '无')),
              len(新) == 2 and 新[0].startswith('⑨') and 新[1].startswith('⑭')))
    单十四 = q._六检之败(实印307.split('；', 1)[1])
    R.append(('⑫新式不误伤·⑭独在时得 %d 条（其文内亦有「；」，不许生假条；须1）' % len(单十四), len(单十四) == 1))

    bad = [x for x, o in R if not o]
    for x, o in R:
        print('   %s %s' % ('✓' if o else '✗', x))
    print('  负测·全测崩绿 %d/%d %s' % (len(R) - len(bad), len(R), '全通' if not bad else '⛔未通'))
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(run())
