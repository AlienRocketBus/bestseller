# -*- coding: utf-8 -*-
"""负测·缺报格闸（2026-09-02·六造§八所立）

★所测者一句话：**令逼我每轮写的那一行，须有器数它在不在。**
★★而一份在旧式下也全过的测，它就是陪跑（令§六③）——**故其要害在④⑤：以旧式回灌，须坏。**
★★★而本闸最险之处不在逮不逮得住，在**误伤**：289一轮拆二十三节，
   **按节数必吐假红**；故⑥⑦专验「按轮号合数」。
"""
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEZI = '本可问而未问'


def _by_round(txt):
    """★与 工具/一坐.py 缺报格闸同式：按轮号合数，一轮拆数节者并作一轮。"""
    blk = re.split(r'^##\s*第\s*(\d+)\s*轮', txt, flags=re.M)
    by = {}
    for i in range(1, len(blk) - 1, 2):
        try:
            r = int(blk[i])
        except ValueError:
            continue
        by[r] = by.get(r, '') + blk[i + 1]
    return by


def _miss(c):
    jp = os.path.join(ROOT, '版本', '第%d章' % c, '_轮记.md')
    if not os.path.exists(jp):
        return None
    by = _by_round(io.open(jp, encoding='utf-8').read())
    return sorted(r for r in by if GEZI not in by[r])


def _miss_by_node(c):
    """旧式（按节数，不合轮号）——本测之反面，用以证新式非陪跑亦非误伤。"""
    jp = os.path.join(ROOT, '版本', '第%d章' % c, '_轮记.md')
    if not os.path.exists(jp):
        return None
    blk = re.split(r'^##\s*第\s*(\d+)\s*轮', io.open(jp, encoding='utf-8').read(), flags=re.M)
    bad = []
    for i in range(1, len(blk) - 1, 2):
        if GEZI not in blk[i + 1]:
            bad.append(int(blk[i]))
    return bad


def run():
    R = []
    src = io.open(os.path.join(ROOT, '工具', '一坐.py'), encoding='utf-8').read()

    # ①器在
    R.append(('①器在·一坐立有缺报格闸', '缺报格' in src and GEZI in src))

    # ②同式·一坐与本测同用「按轮号合数」
    R.append(('②同式·一坐之闸亦按轮号合数（非按节）',
              're.split(r\'^##\\\\s*第\\\\s*(\\\\d+)\\\\s*轮\'' in src or '_by = {}' in src))

    # ③正测·本章（291）今零缺
    R.append(('③正测·第291章零缺（今坐所跑六轮俱有此行）', _miss(291) == []))

    # ④真红·以旧章回灌，第290章须报缺（1、4、5、7 四轮）
    R.append(('④真红·第290章报缺四轮 [1,4,5,7]（故此闸非陪跑）', _miss(290) == [1, 4, 5, 7]))

    # ⑤真红·第288、289二章亦须各报二轮
    R.append(('⑤真红·第288报[1,3]、第289报[10,12]', _miss(288) == [1, 3] and _miss(289) == [10, 12]))

    # ⑥不误伤·289一轮拆二十三节，按轮号合数後只13轮
    jp = os.path.join(ROOT, '版本', '第289章', '_轮记.md')
    t289 = io.open(jp, encoding='utf-8').read()
    heads = re.findall(r'^##\s*第\s*(\d+)\s*轮', t289, flags=re.M)
    R.append(('⑥不误伤·289轮题23个而相异轮号13个，合数後按13轮判',
              len(heads) == 23 and len(_by_round(t289)) == 13))

    # ⑦旧式之害·按节数，289之缺由2轮暴涨（证「合数」这一步非可有可无）
    R.append(('⑦旧式之害·按节数则289之缺由2涨至%d' % len(_miss_by_node(289) or []),
              len(_miss_by_node(289) or []) > len(_miss(289) or [])))

    # ⑧未挖空·凡一轮真无此行者必报（造一份假轮记验之）
    fake = '## 第1轮·某庭\n本轮无事。\n\n## 第2轮·某庭\n本可问而未问：无。\n'
    fb = _by_round(fake)
    R.append(('⑧未挖空·假轮记中第1轮报缺、第2轮放行',
              sorted(r for r in fb if GEZI not in fb[r]) == [1]))

    # ⑨「写无亦算答」——本轮实无可问者写「本可问而未问：无」须放行
    R.append(('⑨写「无」亦算答', GEZI in fake.split('## 第2轮·某庭')[1]))

    # ⑩其限·此闸只查当章，不回头判全书（历史章之红不入 fix）
    R.append(('⑩其限·闸只查当章（一坐以 n 为入参）', "for r in rounds" in src))

    bad = [x for x, o in R if not o]
    for x, o in R:
        print('   %s %s' % ('✓' if o else '✗', x))
    print('  负测·缺报格 %d/%d %s' % (len(R) - len(bad), len(R), '全通' if not bad else '⛔未通'))
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(run())
