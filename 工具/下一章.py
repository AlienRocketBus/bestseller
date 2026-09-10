#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""下一章——**任何一次新开的会话，跑这一条就知道该干什么。**

【其立之由（2026-09-08·作者问「完全不需要我操作，可以吗」）】
  可以，但有一个前提：**这本书的进度不许只活在某一次会话的脑子里。**
  会话会被压缩、会断、会重开；**凡只记在上下文里的，断一次就没了**（P22 断层续手）。
  ★故立此器：它只读盘上的东西，印出三样——
    ①下一章是第几章；②它起草之前必须先办的是哪几件；③上一章有没有留下未了之事。
  **一个新会话读完它的印，就能接着写，不必问任何人。**

用法：
    python3 工具/下一章.py          # 印下一章之号与其前置
    python3 工具/下一章.py --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os
import re
import sys
import glob
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_汉 = '零一二三四五六七八九'


def _汉数(n):
    """章号转汉字，与本书档名逐字同。
    ★两处坑，皆立器之日踩过：
      ①**百位之後的十位不许省「一」**：110 是「一百一十」，不是「一百十」——
        本书档名 `第一百一十章_一个记号.md` 为凭；而十位以下（10—19）单独用时才是「十」「十九」。
      ②**四位以上不许硬转**：原式 `_汉[n // 100]` 遇 9999 当场 IndexError。
        本书章数不会过千，故 ≥1000 一律返空串，令 glob 找不着而返 None（明摆着的假章号，不许假装认得）。"""
    if n < 0 or n >= 1000:
        return ''
    if n < 10:
        return _汉[n]
    if n < 20:
        return '十' + (_汉[n % 10] if n % 10 else '')
    if n < 100:
        return _汉[n // 10] + '十' + (_汉[n % 10] if n % 10 else '')
    s = _汉[n // 100] + '百'
    r = n % 100
    if r == 0:
        return s
    if r < 10:
        return s + '零' + _汉[r]
    return s + _汉[r // 10] + '十' + (_汉[r % 10] if r % 10 else '')


def 正文档(n):
    g = glob.glob(os.path.join(ROOT, '正文', '*第%s章_*.md' % _汉数(n)))
    return g[0] if g else None


def 末章():
    """自正文逐章上数，返最末一章之号。"""
    n = 0
    while 正文档(n + 1):
        n += 1
    return n


def 席记全(n):
    p = os.path.join(ROOT, '版本', '第%d章' % n, '_席记.json')
    if not os.path.isfile(p):
        return False, '无 _席记.json'
    try:
        j = json.load(open(p, encoding='utf-8'))
    except Exception as e:
        return False, '读不动：%s' % e
    八段 = ['定位', '三魂', '起草', '机闸', '读席', '修席', '极限', '案席']
    缺 = [x for x in 八段 if x not in (j.get('段') or {})]
    return (not 缺), ('缺段：' + '／'.join(缺) if 缺 else '八段俱全')


def 门槛(n):
    """自 02_余章之势_总纲 与 01_施工表 取本章之硬门槛（逐行原文，不转述）。"""
    出 = []
    for 档, 头 in (('设定/02_余章之势_总纲.md', '总纲'),
                   ('设定/01_镇冢秘术_逐章施工与伏笔回收表.md', '施工表')):
        p = os.path.join(ROOT, 档)
        if not os.path.isfile(p):
            continue
        for i, line in enumerate(open(p, encoding='utf-8'), 1):
            if re.search(r'(?<!\d)%d(?!\d)' % n, line) and ('⛔' in line or '锁定' in line or '限%d' % n in line):
                出.append('%s:%d %s' % (头, i, line.strip()[:180]))
    return 出


def main():
    末 = 末章()
    下 = 末 + 1
    print('════ 下一章 ════')
    print('  已写到：第 %d 章（%s）' % (末, os.path.basename(正文档(末) or '')))
    ok, 语 = 席记全(末)
    print('  末章席记：%s %s' % ('✓' if ok else '⚠', 语))
    print('  ★下一章：**第 %d 章**' % 下)
    print()
    # ★0910·作者令「一定要跑起来」＋「任务流要连贯」：新开一坐，头两件事是问这两句
    print('  【这一坐从哪儿接·先看这两行】')
    try:
        import subprocess as _sp
        _r = _sp.run(['python3', os.path.join(ROOT, '工具', '续跑.py')],
                     capture_output=True, text=True, timeout=30)
        for _l in (_r.stdout or '').strip().split('\n')[-3:]:
            print('   ' + _l.strip())
    except Exception:
        print('   （续跑账读不出——`python3 工具/续跑.py` 自己跑一回看）')
    try:
        import subprocess as _sp2
        _r2 = _sp2.run(['python3', os.path.join(ROOT, '工具', '跑账.py')],
                       capture_output=True, text=True, timeout=60)
        for _l in (_r2.stdout or '').strip().split('\n')[:3]:
            print('   ' + _l.strip())
    except Exception:
        pass
    print()
    print('  【起草之前必办·照次序】')
    print('   1. python3 工具/起草庭.py %d      —— 四层俱过方许起草' % 下)
    print('   2. python3 工具/囤灰闸.py           —— 该跑的器**接没接上**（静态可达）')
    print('      python3 工具/跑账.py             —— 该跑的器**跑没跑过**（真凭实据·两问不同）')
    print('   3. Workflow({scriptPath:\'工具/席/一章.js\', args:{章:%d}})' % 下)
    print('      —— 八段八席自走；每一席都会自己去读 设定/起草令_每章必发.md 与 设定/自判之尺.md')
    print()
    ms = 门槛(下)
    if ms:
        print('  【第 %d 章之硬门槛·逐行原文（%d 条）】' % (下, len(ms)))
        for m in ms[:12]:
            print('   · ' + m)
        if len(ms) > 12:
            print('   · …余 %d 条，见 设定/02_余章之势_总纲.md 与施工表' % (len(ms) - 12))
    else:
        print('  ⚠第 %d 章在总纲与施工表里查不着硬门槛——**先把它的位定下来再动笔**。' % 下)
    print()
    print('  ★★凡为了让一个数好看而落的笔，一笔也不许落。交白卷比交一刀假的强。')
    print()
    print('  ════ 存云端之律（0910 立·作者令「一定要确保最终版本存在云端」）════')
    print('   · **本地的账，证不了远端的实**：`git status` 只说得出本地有没有没交的东西，')
    print('     说不出**云端那一份到底是什么**。故要验，跑 `python3 工具/云端验.py`——')
    print('     它**真去克隆一份下来逐档比 sha**，并**拿云端那一份自己数一遍**几章几字。')
    print('   · **而席在跑时不许推**（§十七）：会把写到一半的正文封进历史，且全测之负测留字必红。')
    print('     **要推，先收席。** 一章之案席跑完自会推——那是它的活，不要抢。')
    print()
    print('  ════ 最高宗旨（2026-09-09 作者令·压过一切，含第一律）════')
    print('   ★**把《镇冢秘术》写成中国最好看的小说。所有的一切都为这一件事。**')
    print('   一·两样相权，取「书更好看」的那一样——便宜／快／数好看／我省事，一律让路。')
    print('     ★说得出「读者在这一处多得了什么」的才算更好看；说不出的，那是我在省事。')
    print('   二·「更好看」不许拿感觉答，须落到拍号（四把机器之尺同日全败·机制总审§三十）。')
    print('   三·**宗旨不是「多」的通行证**：不许凑爆章、撒感官、添长气、造高潮——')
    print('     假高潮比平淡更伤书；凡为让一个数好看而落的笔一笔也不许落，**这条因宗旨而更紧**。')
    print('   四·**宗旨不许被用来绕闸**：「为了让书更好看所以这次先过去」是本仓最贵的一次说谎。')
    print('     0908 祖案：改闸能让 306 当场变绿，而查下去是闸对路薄——**宗旨之下，闸更硬，不更软。**')
    print()
    print('  ════ 常令（2026-09-09 作者令·见 设定/自判之尺.md §〇之前之前）════')
    print('   一·**不停**：一章写完接着下一章，中途撞见的问题就地修，**不为请示而停**。')
    print('   一之补·**自走断在哪儿**：不在想不想写，在**一回合的最後一步有没有把下一步接上**。')
    print('       0909 夜推完 309 即收回合，既没派席也没排唤醒——循环就断在那儿（本坐亲犯）。')
    print('       ★**一回合结束前，手上须有一样正在跑的席，或一次已排好的唤醒；两样都没有就是停了。**')
    print('       ★★序亦写死：**先派席，再上闹钟，两件都办完才许结束回合。**')
    print('   二·遇问题即修，按「让书更好」那一头修；先干活再看闸——')
    print('       活干完闸还红→闸错了，改它并**同日立负测**；活没干就改闸→那是把欠条撕了。')
    print('   三·**没有一件事值得为了问而停**：所有的事一件不剩，自己决断、自己落字、自己往下走。')
    print('       判之尺只有一把：这个决定能不能让这本书朝最好的那一头走。量完就办，不回头请示。')
    print('       「我拿不准」不是停的理由——按自己判的办，把判与其由写进册子，让下一坐能翻案。')
    print('   四·不许拿「怕做错」当停的由：**错判是可回滚的，停是不可回滚的。**')
    print('   五·改动之权及於全书一切（含已封版之正文·圣经·施工表·canon·势纲·诸令·诸闸·诸席）——')
    print('       **不是「随便改」之令，是「不许拿它已经定了当理由」之令**：旧文旧制之权只有一条：')
    print('       **它到今天还让书更好吗？** 答不出「是」，它就该改。')
    print('       改已封版之文，四问缺一不可：①不改读者在哪一段掉下去（指不出段就是手痒）')
    print('       ②它锁在几处（grep -rn 数遍全仓，不同笔改即是把一处崩换成跨档崩·254祖案）')
    print('       ③全书因这一改强在哪一处 ④是不是只为让某个数好看（是则一笔不许落）。')
    print('       ★权再大也不许的一样：**把闸放松以让自己这一章过**（0908 祖案·306）。')
    return 0


def 自测():
    ok, bad = 0, []

    def T(n, c, note=''):
        nonlocal ok
        if c:
            ok += 1
        else:
            bad.append(n + ('（%s）' % note if note else ''))

    T('①汉数转得对 306→三百零六', _汉数(306) == '三百零六', _汉数(306))
    # ★②这一格逐个咬真档名（本书正文档确有这几章），尤其 110＝「一百一十」不是「一百十」
    据 = (('二百七十三', 273), ('三百零五', 305), ('一', 1), ('十', 10), ('二十', 20),
          ('一百一十', 110), ('一百', 100), ('二百', 200))
    错 = [(a, _汉数(b)) for a, b in 据 if _汉数(b) != a]
    T('②汉数逐个咬真章号（含 110＝一百一十）', not 错, str(错))
    T('②之二 千以上返空串而不崩', _汉数(9999) == '' and _汉数(1000) == '')
    T('③正文档()找得着 273 与 1', bool(正文档(273)) and bool(正文档(1)))
    T('④末章 ≥305（活数）', 末章() >= 305, '实为 %d' % 末章())
    T('⑤正文档()对不存在之章返 None', 正文档(9999) is None)
    T('⑥门槛()对 306 取得着（总纲写过它）', len(门槛(306)) > 0, '实取 %d 条' % len(门槛(306)))
    T('⑦门槛()不拿章号当子串（306 不许被 3060 骗）',
      not any('3060' in x and '306' not in x.replace('3060', '') for x in 门槛(306)))
    print('── 负测·下一章 %d/%d %s ──' % (ok, ok + len(bad), '全通' if not bad else '｜未过：' + '；'.join(bad)))
    return not bad


if __name__ == '__main__':
    sys.exit((0 if 自测() else 1) if '--自测' in sys.argv else main())
