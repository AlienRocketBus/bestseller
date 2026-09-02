# -*- coding: utf-8 -*-
"""负测·数句闸（2026-09-02·第291章第12轮·极限轮所立）

★所测者一句话：**一个数与另一个数比着，两边都没被数过。**
★★291断言「他今天说了六句」，而正文里数得出来的是「他说」十一处；
   ★★★第3轮·逐数对表判其过——其判据是「此数有没有对头」，不是「此数自己对不对」；
   ★★★★於是这一格年年绿（七造§六：一道闸的判据里若少了它本该认的那一样东西，
        它不报错，而在别处稳稳地绿）。
★★★★★而一份在旧式下也全过的测就是陪跑（令§六③）——**故其要害在④：以改前之291回灌，须报红。**
"""
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SJ_TIME = r'今天|昨天|前天|第[一二三四五六七八九十百零]+天|这一回|那一回|这一路|到这会儿|这五天|这三天'


def _scan(t):
    """★与 工具/小说检察官.py 数句闸同式（一处改，二处须同改）。"""
    out = []
    body = t.split('【本章亮点')[0]
    for m in re.finditer(r'([四五六七八九十])句', body):
        q = m.group(1)
        pre = t[max(0, m.start() - 28):m.start()]
        if not re.search(SJ_TIME, pre):
            continue
        if not re.search(r'说|答|问|报|开口', pre):
            continue
        if re.search(r'统共|加起来|一共', t[max(0, m.start() - 28):m.end() + 60]):
            continue
        w = t[max(0, m.start() - 400):m.end() + 400]
        if re.search(q + r'句.{0,15}[：:]', w):
            continue
        if re.search(q + r'句(里头|里|，句句)', w):
            continue
        if len(re.findall(r'第[一二三四五六七八九十]句', w)) >= 2:
            continue
        out.append((q, m.start()))
    return out


def _inscope(t):
    n = 0
    body = t.split('【本章亮点')[0]
    for m in re.finditer(r'([四五六七八九十])句', body):
        pre = t[max(0, m.start() - 28):m.start()]
        if re.search(SJ_TIME, pre) and re.search(r'说|答|问|报|开口', pre):
            n += 1
    return n


def run():
    R = []
    src = io.open(os.path.join(ROOT, '工具', '小说检察官.py'), encoding='utf-8').read()
    files = sorted(glob.glob(os.path.join(ROOT, '正文', '*.md')))
    scope = 0
    reds = []
    for f in files:
        t = io.open(f, encoding='utf-8').read()
        scope += _inscope(t)
        if _scan(t):
            reds.append(os.path.basename(f))

    # ①闸在册（检察官与本测同式，不许只改一处）
    R.append(('①闸在检察官册内（第二十条机械铁律·数句闸）', '数句无明细' in src and 'ＳＪ' not in src))

    # ②其群非孤（令§六②：孤例在档，群在闸）
    R.append(('②其群非孤·全书入闸者%d处（≥5方许立闸）' % scope, scope >= 5))

    # ③正测·今日全书报红归零
    R.append(('③正测·全书数句闸零红（今余 %s）' % (reds or '无'), reds == []))

    # ④真红·以改前之291回灌，须报红二处（故此闸非陪跑）
    bak = os.path.join(ROOT, '版本', '第291章', '_回灌_291改前.txt')
    old = io.open(bak, encoding='utf-8').read() if os.path.exists(bak) else ''
    R.append(('④真红·改前之291报红%d处（须2）' % len(_scan(old)), len(_scan(old)) == 2))

    # ⑤不误伤·泛论不入闸（第194章「一个人说了十句，压着一句」）
    fan = '排完我心里过了一下：说得多跟说得全，是两样。一个人说了十句，压着一句，别人会以为他全说了。'
    R.append(('⑤不误伤·泛论「一个人说了十句」不入闸', _scan(fan) == [] and _inscope(fan) == 0))

    # ⑥认明细·第230章之式「九句，句句是办事：」须放行
    ok230 = '第六十六天他说了九句，句句是办事：两囊、东头呢、谁看着、拉杆就看不着。'
    R.append(('⑥认明细·「N句，句句是…：」放行', _scan(ok230) == [] and _inscope(ok230) == 1))

    # ⑦认编号·第221章之式「第一句…第五句」须放行
    ok221 = '今天她说了五句。第一句她想了三个月。第二句她说得慢。第三句是那一问。'
    R.append(('⑦认编号·「第一句…第N句」二处以上放行', _scan(ok221) == []))

    # ⑧明细在前亦认（291「三个字对六句」在明细之後，须不报）
    R.append(('⑧窗口双向·明细在前之复述不报（今291第二处六句）',
              '400):m.end()+400' in src.replace(' ', '') or 'm.start()-400' in src))

    # ⑨未挖空·真无明细者必报
    bad = '记的时候我数了一下：他今天说了六句。昨天他说了三个字。三个字对六句。'
    R.append(('⑨未挖空·无明细之「六句」必报', len(_scan(bad)) >= 1))

    # ⑩立闸之日之自陈（七造§六④：它认哪几样，本书同类共几样）——不许把它的绿读成「凡数皆可数」
    R.append(('⑩自陈在册·检察官注明三样它认不着（单独成拍之数／跨章累计／N个字）',
              '它认不着的' in src and '跨章累计' in src and '单独成拍之数' in src))

    bad_items = [x for x, o in R if not o]
    for x, o in R:
        print('   %s %s' % ('✓' if o else '✗', x))
    print('  负测·数句闸 %d/%d %s' % (len(R) - len(bad_items), len(R), '全通' if not bad_items else '⛔未通'))
    return 0 if not bad_items else 1


if __name__ == '__main__':
    sys.exit(run())
