# -*- coding: utf-8 -*-
"""负测·盲读之关（2026-09-25 立·作者令「每一章须写到最好，读者读了上瘾；不然就没有必要写」）。
★所守者：`工具/席/一章.js` 之盲读之关**在、有牙、牙没被拔**：
  ①盲读席不给任何一席之说，只给正文；②不过则重锻，至多二回、每回换新盲读席；
  ③二回仍不过，**封版席不派**（机制之牙，不靠案席自觉），且案席令里明写不许封版；
  ④结果随工作流交回（盲读·盲读过）。"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, sys
s = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '席', '一章.js'), encoding='utf-8').read()
案 = []
def chk(名, 过): 案.append((名, bool(过)))
chk('①盲读之关在', '七之二·盲读之关' in s)
chk('①之b 盲读席不许读任何席之说', '你不许读任何席的轮记' in s)
chk('②不过则重锻·至多二回', "回 <= 2" in s and '重锻席' in s)
chk('②之b 每回换五个新盲读者', "一轮盲读(回 + 1)" in s)
chk('⑥五个口味各异之读者，看多数（五中至少四过）', s.count("'读") >= 0 and "读者样 = [" in s and "filter(r => r.pass).length >= 4" in s)
chk('⑦只一问：放进这本书里配不配中国第一（作者0925令：无招胜有招）', '只有一问' in s and '不照任何清单打勾' in s)
chk('⑨重锻席亦禁硬造悬念', '不许为「让人想往下读」而硬造悬念' in s)
chk('③不过则封版席不派', "const 封 = !盲读过 ?" in s)
chk('③之b 案席令明写不许封版', '本章不许封版' in s)
chk('④结果随工作流交回', '盲读: 盲读记, 盲读过' in s)
chk('⑤拿不准即 false（宁严勿松）', '拿不准即 false' in s)
chk('⑩写章令不再逼「每章踢进下一章」', '把读者踢进下一章的那一脚' not in s and '把读者往下一章推不推' not in s)
chk('⑪写章令不另立刻意之规（刻意之疲只照镜不入令）', '工具/刻意之疲.py' not in s)
_q = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '全测.py'), encoding='utf-8').read()
_z = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '自走.py'), encoding='utf-8').read()
chk('⑫刻意之疲接进全测与自走（造了就要跑）', "('刻意之疲', chk_kexi)" in _q and '刻意之疲.py' in _z)
chk('⑬起草後另派抄袭之关亲跑（不靠自报），红则重写', '三之二·抄袭之关' in s and "抄.red && k <= 2" in s)
chk('⑭起草令首立「起草是最重要的一关·绝不许抄」', '起草是最重要的一关' in s and '绝不许抄前面的章节' in s)
_c = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '起草闸.py'), encoding='utf-8').read()
chk('⑮抄袭闸在起草闸甲层', "('抄袭闸', ['工具/抄袭闸.py'" in _c)
chk('⑯全测接抄袭闸', "('抄袭闸', chk_chaoxi)" in _q)
chk('⑰起草三稿各写（三位执笔·入口不同·同一魂）', "const 入口们 = [" in s and "执笔·' + x.名" in s)
chk('⑱动笔前须读前两章白文全文', '白文全文从头读到尾' in s)
chk('⑲写完自当读者读一遍、跑抄袭闸', '你自己当读者，从头到尾读一遍你写的' in s and '抄袭闸.py --档' in s)
chk('⑳五位盲读者比三稿，看多数择优', "label: '比稿·'" in s and '哪一稿放进这本书里最好' in s)
chk('㉑合稿只许嫁接多数所点之拍', '只许嫁接至少两位读者同点的他稿之拍' in s)
chk('㉒合稿令里无未定义之 JS 变量（0925 当场逮过 body.slice）', 'body.slice' not in s)
chk('㉓逻辑审席在（防崩·五类·须给原句为据）', '全书防崩之第一责任人' in s and '死而复生' in s and '能无来由' in s and '知不当知' in s)
chk('㉔起草後与封版前各审一回', "防崩('起草')" in s and "防崩('极限')" in s)
chk('㉕硬崩二回不净则封版席不派', "!封前之审.净 ?" in s)
chk('㉖回写只许改本章合前文，不许改前文或洗状态册', '不许改前文来迁就本章' in s and '不许改状态册来洗白' in s)
chk('㉗封版须同步人物状态册', '人物状态册.json' in s and '账不同步，下一章之防崩就是瞎的' in s)
chk('㉘崩坏闸在起草闸甲层', "('崩坏闸', ['工具/崩坏闸.py'" in _c)
chk('㉙盲读者须答「读到发生了什么」，读误席对开镜卡与状态册', "happened" in s and '读误席' in s and '作者写病重，读者读成死了' in s)
chk('㉚重锻删不许删到线之带以下', '删不许删到线之带以下' in s)
chk('㉛厚之关：合稿後另派一席亲量，低於带即派第二件事席（367、368 连两章之教训）', '三之三·厚之关' in s and "第二件事·' + k" in s and '厚.low && k <= 2' in s)
_j = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '席', '救章.js'), encoding='utf-8').read()
chk('㉜救章升格：均分<95即升格，升格係改得更好非补丁（作者0925令）', '均(评) < 95' in _j and '⛔不是在原句上缝补' in _j)
chk('㉝升格须盲比胜（三人中≥2判改後更好），否则退回', '赞新 < 2' in _j and "退回('救章_升格前_' + k)" in _j)
chk('㉞回归守：救章动字前先存原稿；每改之後专查新病，有即退回', "救章_起.md" in _j and "回归守('救章_起', '深掘无伤')" in _j and "守.new_issues.length" in _j)
chk('㉟进化：回归守所逮新病入救章回归账，升格席先读之（同类不许再犯）', '设定/救章回归账.md' in _j and "记病('升格' + k" in _j and '先读 \\`设定/救章回归账.md' in _j)
坏 = [x for x in 案 if not x[1]]
print('════ 负测·盲读之关 ════')
for 名, 过 in 案:
    print(('  ✓ ' if 过 else '  ⛔ ') + 名)
print('负测·盲读之关 %d/%d' % (len(案) - len(坏), len(案)))
sys.exit(1 if 坏 else 0)
