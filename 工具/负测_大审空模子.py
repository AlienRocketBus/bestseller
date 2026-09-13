# -*- coding: utf-8 -*-
"""负测 · 大审之「空模子不算一回大审」（2026-09-13 立）

⛔其局：`大审.py --立 N` 造出来的册若无人填，它照旧叫「大审_至第N章.md」，
   而 `诸册()` 只认档名——**於是一份没开过的庭，在账上与开过的一模一样。**
★其实据：0913 亲数——313 册 42 行、323 册 42 行，通篇 `第%d—%d章`、裁定表一行「⛔待裁」；
   而 324 册 248 行、裁定表逐行有裁。**319—327 九章之卡逐章照抄「大审停在313」，实则停在 324。**

★★本测两路，缺一即假：
   一·**空模子须逮得出**（真局四样：模子记号未换｜裁定表一笔裁也没有｜档读不出｜两样俱缺）；
   二·⛔**而真册不许被误逮**——**一道只会说「不算」的闸，与没有闸是一样的。**
"""
import io, os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib
大审 = importlib.import_module('大审')

_模 = '# 大审 · 至第%d章（第%d—%d章）\n\n## 三·逐笔裁定\n\n| # | 判 | 据 | 裁 | 其由 |\n|---|---|---|---|---|\n| 1 | | | ⛔待裁／已治／判驳／已挂 | |\n'
_真 = ('# 大审 · 至第324章（第314—324章）\n\n## 三·逐笔裁定\n\n'
       '| # | 判（席·题） | 据 | 裁 | 其由 |\n|---|---|---|---|---|\n'
       '| 1 | 结构·323是多的那一章 | 323拍4 | 已挂 限330 | 收站同庭裁 |\n'
       '| 2 | 编辑·十一收拍同一币值 | 320拍9 | 已治 | 改其三 |\n')
_挂而无裁 = ('# 大审 · 至第999章\n\n## 三·逐笔裁定\n\n| # | 判 | 据 | 裁 | 其由 |\n'
             '|---|---|---|---|---|\n| 1 | 某席·某题 | 某拍 | ⛔待裁 | |\n')

def _写(t):
    f = tempfile.NamedTemporaryFile('w', suffix='.md', delete=False, encoding='utf-8')
    f.write(t); f.close(); return f.name

def chk_dashen_kongmuzi():
    out = []
    局 = [
        ('模子记号未换（313／323 之真形）', _模, True),
        ('裁定表一笔裁也没有（只「⛔待裁」）', _挂而无裁, True),
        ('档读不出（宁可判空不可判它开过）', None, True),
        ('真册·裁定表逐行有裁（324 之真形）', _真, False),
    ]
    坏 = 0
    for 名, 文, 期 in 局:
        路 = '/nonexistent/大审_至第1章.md' if 文 is None else _写(文)
        得 = 大审.空模子(路)
        if 文 is not None:
            os.unlink(路)
        if 得 != 期:
            坏 += 1
            out.append('  ⛔[%s] 期 %s 得 %s' % (名, 期, 得))
        else:
            out.append('  ✓[%s] %s' % (名, '判空模子' if 得 else '认作一回大审'))
    # 三·盘上之真局：324 须被认得，313／323 须落选
    册 = dict((n, p) for n, p in 大审.诸册())
    全 = dict((n, p) for n, p in 大审.诸册(含空=True))
    for n, 期 in ((324, True), (313, False), (323, False)):
        if n not in 全:
            out.append('  ⚠盘上无 大审_至第%d章.md，此格跳过' % n)
            continue
        得 = n in 册
        if 得 != 期:
            坏 += 1
            out.append('  ⛔[盘上·%d] 期 %s 得 %s' % (n, 期, 得))
        else:
            out.append('  ✓[盘上·%d] %s' % (n, '认得' if 得 else '落选'))
    头 = '════ 负测·大审空模子 ════ %d/%d %s' % (len(out) - 坏, len(out),
                                              '全通' if 坏 == 0 else '有败')
    return (坏 == 0), '\n'.join([头] + out)

if __name__ == '__main__':
    ok, s = chk_dashen_kongmuzi()
    print(s)
    sys.exit(0 if ok else 1)
