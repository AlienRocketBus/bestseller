# -*- coding: utf-8 -*-
"""负测 · 冷眼轮签核之认（2026-09-18 立·随 `开轮六检::_cold_done` 三治同日落）

⛔**其病三样，皆 346 封版之後自逮**：
①**一处「说起它」，被当成了一笔「签了它」**——
　`回执_…第346章…` 之内有一句在说那六个字该怎么写：
　「**其销须书「342章冷眼轮」「344章冷眼轮」，与本章之号一无干涉**」；
　⛔**而旧式读的是那六个字之在与不在，遂当场把 `COLD-342`／`COLD-344` 两笔判作已执。**
　★★**此害比误报重得多：误报只是吵；这一处是替两笔真账签了字。**
②**候选取「章号最大之回执」，而「光提起它」也算候选**——
　⛔**一份在後之回执只要提一句，便压过一份在前之真签。**
③**解名**：`第(\d+)章` 解不出「第73至74章」「第243_244章」，二份真回执皆落作章 0。

★**回灌全书 269 笔：终判有变者只 342／344 两笔，余 267 笔一笔未动。**
⛔**而本坐头两版之式各扫掉 27 笔旧账（COLD-73—99）**，皆係断句断错
（那几处签核写在 `## 标题` 里，其前无句号，遂把上文一整段吞进来）；**那两版一版也没有落盘。**
★★**故本测之要害，是压住这一改不许扫着旧账**：**②之组逐笔验其仍为已执。**
"""
import io, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import 开轮六检 as K

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def 跑():
    局 = []

    # ①那两笔假签，须判未执
    局.append(('①COLD-342 不许因 346 那一句「说式子」而判已执', K._cold_done(342) is False))
    局.append(('①之b COLD-344 同', K._cold_done(344) is False))
    # ⛔而其反面：342 之六字全书只 346 一份写过，且其句正是说式子那一句
    _t = io.open(os.path.join(ROOT, '设定', '回执_20260918_第346章作业单.md'),
                 encoding='utf-8', errors='replace').read()
    局.append(('①之c 其凭：那六个字确在 346 之回执里（⛔故本测非因「找不着」而绿）',
               '342章冷眼轮' in _t and '一无干涉' in _t))

    # ②⛔不许扫着旧账：那二十七笔（本坐头两版各扫掉一回）逐笔仍须已执
    旧 = [n for n in range(73, 100)]
    坏 = [n for n in 旧 if not K._cold_done(n)]
    局.append(('②旧账 COLD-73—99 共 27 笔，逐笔仍判已执（⛔本坐头两版在此各栽一回）',
               坏 == []))
    if 坏:
        print('     ⛔被扫着者：%s' % 坏)
    局.append(('②之b COLD-305 仍已执（本坐第一版曾扫着它）', K._cold_done(305) is True))

    # ③解名：多章之名须取其最大者
    def _ch(name):
        _ns = re.findall(r'第(\d+)(?:[至_\-—～~](\d+))?章', name)
        _all = [int(a) for a, b in _ns] + [int(b) for a, b in _ns if b]
        return max(_all) if _all else 0
    局.append(('③解名·「第73至74章」→74', _ch('回执_20260722_第73至74章作业单.md') == 74))
    局.append(('③之b 解名·「第243_244章」→244', _ch('回执_20260821_第243_244章作业单.md') == 244))
    局.append(('③之c 解名·寻常之名照旧', _ch('回执_20260918_第346章作业单.md') == 346))
    局.append(('③之d ⛔而无章号之档（立设之回执）须仍作 0，不许乱认',
               _ch('回执_20260717_伏笔审计.md') == 0))
    局.append(('③之e COLD-74（其真签在「第73至74章」那一份）仍判已执',
               K._cold_done(74) is True))

    # ④否决照旧压过签核（前两治之力不许被本治减去）
    局.append(('④否决记之力未减：COLD-343 已判废，其 done 须为否（⛔非因本治）',
               K._cold_done(343) is False and K._cold_void(343) is True))

    红 = 0
    print('════ 负测 · 冷眼轮签核之认（%d 局）════' % len(局))
    for 名, 果 in 局:
        print('  %s %s' % ('✓' if 果 else '⛔', 名))
        if not 果:
            红 += 1
    print('  ── %d/%d ──' % (len(局) - 红, len(局)))
    return 红


if __name__ == '__main__':
    sys.exit(1 if 跑() else 0)
