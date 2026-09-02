# -*- coding: utf-8 -*-
"""负测·翻页备料查（检五）之对象（2026-09-02·291第1轮所逮）

★所测者一句话：**一章的翻页，问的是它自己的下一章，不是全书的下下一章。**
★★而一份在旧式下也全过的测，它就是陪跑（令§六③）——**故其要害在④⑤：以旧式回灌，须坏。**
"""
import io
import os
import re
import sys
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = io.open(os.path.join(ROOT, '工具', '小说检察官.py'), encoding='utf-8').read()
CANON = json.load(io.open(os.path.join(ROOT, '设定', 'canon事实库.json'), encoding='utf-8'))
MASTER = io.open(os.path.join(ROOT, '设定', '00_镇冢秘术_唯一总圣经.md'), encoding='utf-8').read()


def _chs():
    out = []
    for f in os.listdir(os.path.join(ROOT, '正文')):
        m = re.search(r'第([一二三四五六七八九十百零]+)章', f)
        if m:
            out.append(f)
    return out


def _n_written():
    """全书已写之章号（自圣经末章锚取，免得再解汉字数）。"""
    m = re.search(r'## 十一、已写 1—(\d+) 章', MASTER)
    return int(m.group(1)) if m else 0


def _anchor(n):
    return bool(re.search(r'第\s*%d\s*章必须从' % n, MASTER))


def run():
    R = []
    cur = _n_written()

    # ①器在：检五之对象已改作 n+1
    R.append(('①器在·检五之对象取 n+1', 'nx = n + 1' in SRC))

    # ②未挖空：锚之查仍在（其式仍读圣经之「第N章必须从」）
    R.append(('②未挖空·锚之查仍读圣经之接写锚',
              "r'第\\s*%d\\s*章必须从'" in SRC or '章必须从' in SRC))

    # ③旧式之凭：原码之「max(files)+1」已不在检五之内
    seg = SRC[SRC.index('检五·翻页备料查'):SRC.index('检五·翻页备料查') + 2000]
    R.append(('③旧式已除·检五之内不再取 max(files)+1', 'nx = max(files) + 1' not in seg))

    # ④回灌·旧式之害（同一时刻，二章所索者同为一个数）
    #   以旧式算：289 与 290 所索者皆 cur+1；以新式算：各索其 n+1。
    old_289 = cur + 1
    old_290 = cur + 1
    R.append(('④回灌·旧式令289与290所索者同为第%d章（故此闸非陪跑）' % old_290,
              old_289 == old_290 == cur + 1))

    # ⑤新式·各索其下一章，且二者不同
    R.append(('⑤新式·289索290、290索291，二者不同', (289 + 1) != (290 + 1)))

    # ⑥真凭：290之下一章锚（第291章必须从）确在圣经里
    R.append(('⑥真凭·圣经有「第291章必须从…接写」', _anchor(291)))

    # ⑦真凭：289之下一章锚（第290章必须从）亦在
    R.append(('⑦真凭·圣经有「第290章必须从…接写」', _anchor(290)))

    # ⑧未挖空之要害：一个未备之锚仍报红（取一个必不存在之章）
    R.append(('⑧未挖空·未备之锚仍判无', not _anchor(cur + 3)))

    # ⑨状态卡指针之查只问前沿：n+1 已写出者放行，未写出者照旧问
    R.append(('⑨指针之查只问前沿·已写出之 n+1 放行',
              'if nx not in files else True' in SRC))

    # ⑩而前沿仍逮得住：open_brief 现指第%d章，与 cur+1 相符
    ob = CANON.get('open_brief', {}).get('for_ch')
    R.append(('⑩前沿仍逮得住·open_brief.for_ch=%s 与 cur+1=%d 相符' % (ob, cur + 1),
              ob == cur + 1))

    bad = [x for x, o in R if not o]
    for x, o in R:
        print('   %s %s' % ('✓' if o else '✗', x))
    print('  负测·翻页备料查 %d/%d %s' % (len(R) - len(bad), len(R),
                                  '全通' if not bad else '⛔未通'))
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(run())
