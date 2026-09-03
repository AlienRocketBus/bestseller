# -*- coding: utf-8 -*-
"""负测·立价查（2026-09-03·296第9轮立）

★立此测之由（★而起手所报者有一处错，同日正之）：
  ★我起手写「此器全书无一条负测」——**错**。`工具/负测_层census.py` 早有三条管它，12/12 全通。
  ★★**而实情比「没有负测」更该记**：那三条问的是「它逮不逮得着292拍10」「它是不是遍地皆红」，
    **一条也没问§六④那一行——它认哪几样，本书同类共几样**；
  ★★★**於是那份负测年年全通，而这道闸对两成一的条件句一眼看不见。**
  ★★★★故本测不重复那三条，只补§六④那一行，并以旧式驱真器回灌。
★★而296第9轮当场见其缺口：**旧式四条（就得／就成了／非…不可／一X就）认不着「只要」**，
  故 立价查 在296之第4、7、9三轮连印「✓全章无立章之句」，
  **而本章之价正写在拍118「而它管用只在一样上：只要它今天这么摆着」**。
★★★本测之头一项断言即§六④那一行：**它认哪几样，本书同类共几样。**
"""
import io, os, re, sys, glob
from importlib.util import spec_from_file_location, module_from_spec

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_sp = spec_from_file_location('_lj', os.path.join(ROOT, '工具', '立价查.py'))
LJ = module_from_spec(_sp); _sp.loader.exec_module(LJ)

# ★旧式（296第9轮之前的四条）——回灌之用
旧式 = LJ.FORMS[:4]

OK = [0, 0]


def chk(name, cond):
    OK[1] += 1
    OK[0] += 1 if cond else 0
    print('  %s %s' % ('✓' if cond else '⛔', name))


def 群():
    """逐样 grep 全书正文（去亮点段），返回 {式: (处, 章)}。"""
    pats = {'就得': r'就得', '就成了': r'就成了', '一X就': r'一(?:回|下|样)就',
            '非…不可': r'非[^。；！？\n]{1,20}不可',
            '只要': r'只要', '除非': r'除非', '只有…才': r'只有[^。；！？\n]{1,20}才'}
    out = {k: [0, 0] for k in pats}
    for f in glob.glob(os.path.join(ROOT, '正文', '*.md')):
        b = io.open(f, encoding='utf-8').read().split('【本章亮点')[0]
        for k, p in pats.items():
            n = len(re.findall(p, b))
            if n:
                out[k][0] += n; out[k][1] += 1
    return out


def 扫(text, forms):
    hits = []
    for nm, rx, g in forms:
        for m in re.finditer(rx, text):
            hits.append((nm, m.group(0)))
    return hits


def main():
    print('███ 负测·立价查 ███')
    g = 群()
    旧认 = sum(g[k][0] for k in ('就得', '就成了', '一X就', '非…不可'))
    新增 = sum(g[k][0] for k in ('只要', '除非', '只有…才'))
    print('  ★§六④·它认哪几样，本书同类共几样：')
    for k in ('就得', '就成了', '一X就', '非…不可', '只要', '除非', '只有…才'):
        print('     %-8s %4d 处 ／ %3d 章' % (k, g[k][0], g[k][1]))
    print('     ★★旧式认 %d 处｜新式另认 %d 处｜合 %d 处（新增占 %.0f%%）'
          % (旧认, 新增, 旧认 + 新增, 100.0 * 新增 / max(1, 旧认 + 新增)))

    # ①判据行本身：新增之三式在本书须成群（各样皆不得为零），否则此改是陪跑
    chk('①新增三式在本书皆非零（只要/除非/只有…才 俱有其章）',
        all(g[k][0] > 0 for k in ('只要', '除非', '只有…才')))
    chk('②新增之量须够得上「群」（≥全集之一成）',
        新增 >= 0.10 * (旧认 + 新增))

    # ③④旧式回灌：拿296真犯过此项之原句，旧式须看不见，新式须逮着
    句 = '而它管用只在一样上：只要它今天这么摆着。'
    chk('③以旧式回灌296那一句：一处也认不着（此即它三轮连绿之由）',
        len(扫(句, 旧式)) == 0)
    chk('④以新式跑同一句：逮得着，且认作「只要」',
        any(nm == '只要' for nm, _ in 扫(句, LJ.FORMS)))

    # ⑤⑥端到端：**不许自撰扫法，须驱真器**（否则测的是我这份重写，不是那道闸）
    #   ★其教出自本坐：初版⑥自撰正则回灌，报「旧式亦逮得着」而真器印「全章无立价之句」
    #     ——**真器另有筛（果之实字、逐拍之界），自撰之扫一样也没有。**
    import contextlib
    def 跑(ch, forms):
        keep = LJ.FORMS
        LJ.FORMS = forms
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                LJ.查(ch)
        finally:
            LJ.FORMS = keep
        return buf.getvalue()
    旧出 = 跑(296, 旧式)
    chk('⑥驱真器·旧式回灌第296章：真器印「✓全章无立价之句」（证此改非陪跑）',
        '全章无立价之句' in 旧出)

    # ★★★★★2026-09-03·296第12轮所逮·同日改：**⑤原钉在第296章之现文上**
    #   （「新式跑296须报得出立价」），★而第12轮翻案把那一拍删了（全章唯一一句判语），
    #   ★★於是我第9轮亲手立的负测，被我第12轮亲手写红——**第二十八犯之族：把断言钉在快照上。**
    #   ★★★故改：⑤不再问「某一章此刻有没有」，改问「全书还有没有」——
    #     **逐章扫，新式认得而旧式认不着者须≥1章**；这一断言不随任何一章之刀而动。
    新逮 = []
    for f in glob.glob(os.path.join(ROOT, '正文', '*.md')):
        n = LJ._num(f)
        if n < 0:
            continue
        bw = io.open(f, encoding='utf-8').read().split('【本章亮点')[0]
        if 扫(bw, LJ.FORMS) and not 扫(bw, 旧式):
            新逮.append(n)
    chk('⑤全书之中「新式认得而旧式认不着」者 ≥1 章（此断言不钉在任何一章之现文上）',
        len(新逮) >= 1)
    print('     ★其章 %d 篇%s' % (len(新逮), ('，如 ' + '、'.join(str(x) for x in sorted(新逮)[:6])) if 新逮 else ''))

    chk('⑦无条件词之白文不得报立价',
        len(扫('她数她自己那五个：一、二、三、四、五。', LJ.FORMS)) == 0)

    print('  ── %d/%d %s ──' % (OK[0], OK[1], '全通' if OK[0]==OK[1] else '有红'))
    return 0 if OK[0] == OK[1] else 1


if __name__ == '__main__':
    sys.exit(main())
