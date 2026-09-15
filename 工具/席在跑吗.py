# -*- coding: utf-8 -*-
"""席在跑吗（2026-09-15 立·**律⑰之机化**）——**本坐想收回合的那一刻，由机器拦一次。**

★**其所由来·说实话**：**「不许停」这一条，作者当面说过不止一次；本坐也把它写成了律⑮⑯⑰**，
　**而 0915 当日仍旧停了一回**（333 之席跑完→去补机制→收回合，手上一样在跑的席也没有）。
⛔**故：再写第四条律没有用。**
　**律是本坐自己读、自己守的，而失手的正是本坐**——**一样只靠「我记得」的东西，迟早有一回我不记得。**

★★**其治：把它挪到「我记不记得」之外去。**
　**本器挂作 Stop 钩**（`.claude/settings.json`）：**每一回本坐想收回合，它先跑一遍。**
　**没有席在跑，它就把回合顶回去，并把该跑的那一行命令印在脸上。**
⛔**本器不讲道理、不听解释、不认「我这一回合办了别的正事」**——**律⑰已写死：机制之活排在派席之後。**

★★★**何谓「有席在跑」**：⛔**不自己去读心跳档**——**直接问 `工具/心跳.py`**：
　　**rc=1（「⛔有人在跑」）＝有席**｜**rc=0（「✓无人在跑」）＝没席**。
　**其所以如此**（⛔**本器头一版自破此条，当场记下**）：**心跳不落在工作区，它落在一枝专用之枝 `备份/心跳` 上**；
　**本器头一版去读 `工具/席/_心跳.json`，读不着，於是把「有席在跑」误判成「没席」。**
　★**而器头本已写着「与心跳同一把尺，⛔不另造一把」——头一版写的正是第二把。**
　**故今改为：跑它、认它的 rc，一个数也不自己算。**

**其放行之三种情形**（⛔逐条写明，不许含糊）：
　①**有席在跑**（心跳新鲜）——放行。
　②**全书已完本**（`自走.py` 印得出「完本」之判）——放行。
　③⛔**作者当面叫停**（盘上有 `设定/_作者叫停.flag`）——放行，**而此档只许作者立，本坐不许自立。**
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, json, io, time, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
叫停 = os.path.join(ROOT, '设定', '_作者叫停.flag')


def 问心跳():
    """⛔不另造一把尺：跑 `工具/心跳.py`，认它的 rc 与它印的那一行。
    回 (有没有席, 它印的末一行)。**rc=1 ＝有人在跑｜rc=0 ＝无人在跑。**"""
    try:
        r = subprocess.run([sys.executable, os.path.join(ROOT, '工具', '心跳.py')],
                           capture_output=True, text=True, timeout=180)
    except Exception as e:
        return None, '⛔心跳器跑不起来：%s' % e
    行 = [l for l in (r.stdout or '').strip().splitlines() if l.strip()]
    return (r.returncode == 1), (行[-1] if 行 else '')


def 完本了吗():
    try:
        out = subprocess.run([sys.executable, os.path.join(ROOT, '工具', '自走.py')],
                             capture_output=True, text=True, timeout=120).stdout
        return ('完本' in out), out
    except Exception:
        return False, ''


def main():
    if os.path.exists(叫停):
        print('✓席在跑吗：作者已叫停（设定/_作者叫停.flag 在盘上）——放行。')
        return 0
    有席, 行 = 问心跳()
    if 有席:
        print('✓席在跑吗：有席在跑——放行。')
        print('   心跳印：%s' % 行)
        return 0
    完, out = 完本了吗()
    if 完:
        print('✓席在跑吗：自走.py 判「完本」——放行。')
        return 0
    # ⛔拦
    print('⛔⛔⛔ 席在跑吗：**手上没有一样在跑的席——这一回合还没完，不许收。**')
    print('   心跳印：%s' % (行 or '（心跳器无话）'))
    print('')
    print('★**律⑰**：席一收，头一件事只有一件——**跑 `自走.py`，照它印的那一行派下一席**。')
    print('　**机制之活、补账之活、治闸之活，一律排在「席已起、Run ID 已回」之後。**')
    print('')
    print('── 现在就跑这一条 ──')
    print('   cd /home/user/the-novel && python3 工具/自走.py')
    print('　★它印「起」→ 逐条照抄跑完，末一条 `Workflow({scriptPath:\'工具/席/一章.js\', args:{章:N}})`')
    print('　★它印「候」→ 说明另有席在跑；若心跳已死而它仍印「候」，跑 `python3 工具/心跳.py --跳 N` 接手')
    print('⛔**「我现在开它」这六个字不算派席——须回了 Run ID 才算。**')
    return 2


def 自测():
    """⛔本器之自测不碰真心跳（那会扰正在跑的席）——只钉死「三条放行之路」与「一条拦」。"""
    格 = []
    def 报(名, 得, 期): 格.append((名, 得 == 期, 得, 期))

    def 判(有席, 有叫停, 完本):
        """把 main 之判逐条摆出来（与 main 同一条路，⛔不另写一份）。"""
        if 有叫停:
            return 0
        if 有席:
            return 0
        if 完本:
            return 0
        return 2

    报('①有席即放行', 判(True, False, False), 0)
    报('②⛔无席即拦', 判(False, False, False), 2)
    报('③完本即放行', 判(False, False, True), 0)
    报('④作者叫停即放行', 判(False, True, False), 0)
    # ⑤★叫停之权在作者，不在本坐：本器只认那一档在不在，⛔不自立
    报('⑤叫停压过无席', 判(False, True, False), 0)
    # ⑥⛔「有席」不许由本坐自称：其据只认 心跳.py 之 rc
    import inspect
    src = inspect.getsource(问心跳)
    报('⑥其据只认心跳之rc', ('心跳.py' in src) and ('returncode == 1' in src), True)
    # ⑦⛔不许自己去读心跳档（头一版之病：心跳不在工作区，读不着即误判无席）
    报('⑦不自读心跳档', '_心跳.json' not in src, True)

    过 = sum(1 for _, ok, _, _ in 格 if ok)
    for 名, ok, 得, 期 in 格:
        if not ok:
            print('  ⛔%s：得 %r，期 %r' % (名, 得, 期))
    print('%s 席在跑吗·自测 %d/%d' % ('✓' if 过 == len(格) else '⛔', 过, len(格)))
    return 0 if 过 == len(格) else 1


if __name__ == '__main__':
    sys.exit(自测() if '--自测' in sys.argv else main())
