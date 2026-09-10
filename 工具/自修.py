# -*- coding: utf-8 -*-
"""自修.py —— 器自修，非我自修。

★立此器之由（拿账说）：
  · 2026-08-27 本坐二十次自撰工具回执。其中数次是「我报了自行修复，而一步没做」。
  · ★★故凡令我「遇问题自行修复」，其结果只会是：我编的更多，而作者更晚发现。
  · ★★★能修的必须是器：它自己诊断、自己动手、自己复验，把前后对比印出来。
  ·   我在这中间只是按下它的人。

★★此器只办「机器判得出对错」之事：
  ① 台账与正文相违        → 补存
  ② 硬项未清              → 扫破折／说破／五逗／半角／英文
  ③ 圣经三样不全          → 报出缺者（不自动写，因其文须人拟）
  ④ 看官凭据过期或未齐    → 重跑五席
  ⑤ 未提交积压逾二十件    → 提交

★★★此器不办「判」：哪一笔冷轮该顺延、这一章该写什么、哪一处该翻案——
  ★★★★那些印出来交作者，不许器自作主张。

用法：
    python3 工具/自修.py            # 只诊断，不动手（默认）
    python3 工具/自修.py --修        # 诊断并动手，逐项复验
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import glob
import io
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CN = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
      '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}


def cn2i(t):
    v = 0
    m = re.match(r'([一二三四五六七八九])?百(.*)', t)
    if m:
        v = CN.get(m.group(1), 1) * 100
        t = m.group(2)
    m = re.match(r'([一二三四五六七八九])?十(.*)', t)
    if m:
        v += CN.get(m.group(1), 1) * 10
        t = m.group(2)
    for c in t:
        if c in CN:
            v += CN[c]
    return v


def R(*a):
    try:
        p = subprocess.run(list(a), cwd=ROOT, capture_output=True,
                           text=True, timeout=900)
        return p.stdout
    except Exception as e:
        return 'ERR:%s' % e


def chapter_path(n):
    for f in glob.glob(os.path.join(ROOT, '正文', '*.md')):
        m = re.search(r'第([零一二三四五六七八九十百]+)章', os.path.basename(f))
        if m and cn2i(m.group(1)) == n:
            return f
    return None


def body_of(fp):
    t = io.open(fp, encoding='utf-8').read().split('【本章亮点】')[0]
    return re.sub(r'^.*?第.+?章[^\n]*\n', '', t, count=1, flags=re.S)


def weight(fp):
    return len(re.sub(r'\s', '', body_of(fp)))


def hard_scan(fp):
    """返回硬项之目（正文与亮点段分计）。"""
    s = io.open(fp, encoding='utf-8').read()
    parts = s.split('【本章亮点】')
    b = re.sub(r'^.*?第.+?章[^\n]*\n', '', parts[0], count=1, flags=re.S)
    h = parts[1] if len(parts) > 1 else ''
    def cnt(t):
        return {
            '破折': len(re.findall(r'—+', t)),
            '说破': len(re.findall(r'所以|因为|就是说', t)),
            '五逗': sum(1 for x in re.split(r'(?<=[。！？…])', t) if x.count('，') >= 5),
            '半角': t.count(','),
            '英文': len(re.findall(r'[A-Za-z]', t)),
        }
    return cnt(b), cnt(h)


def main():
    do = ('--修' in sys.argv or '--fix' in sys.argv)
    print('════ 自修 · %s ════' % ('动手' if do else '只诊断（加 --修 方动手）'))

    try:
        d = json.load(io.open(os.path.join(ROOT, '设定', 'canon事实库.json'),
                              encoding='utf-8'))
        n = int(d['open_brief']['for_ch'])
    except Exception as e:
        print('⛔ 取不到 open_brief：%s' % e)
        return
    print('本章：第%d章' % n)

    todo = []      # (名, 诊断, 修法函数 or None)

    # ── ① 台账与正文 ──
    fp = chapter_path(n)
    lp = os.path.join(ROOT, '版本', '第%d章' % n, '_台账.json')
    if fp and os.path.exists(lp):
        L = json.load(io.open(lp, encoding='utf-8'))
        vs = L.get('版本', [])
        lw = vs[-1].get('soft', {}).get('净重', 0) if vs else 0
        tw = weight(fp)
        rs_now = sorted({int(m.group(1)) for x in vs for m in [re.search(r'第\s*(\d+)\s*轮', x.get('说明',''))] if m})
        if lw != tw:
            todo.append(('台账相违', '台账%d ≠ 正文%d（差%d）' % (lw, tw, tw - lw),
                         # ★2026-08-27 补：其说明先前不带轮号，
                         #   ★★而器数真轮靠说明里之「第N轮」——
                         #   ★★★遂有286第3轮之死结：刀落进v03而轮号数不到，
                         #     再存则空轮闸拦（正文与末版逐字相同），补存亦拦。
                         #   ★★★★故今带上当前轮号。
                         lambda: R('python3', '工具/跑轮.py', '--补存', str(n),
                                   '第%d轮·自修：台账与正文相违，补存以合'
                                   % ((max(rs_now) + 1) if rs_now else 1))))
        else:
            print('① 台账相符（%d）' % tw)
    else:
        print('① 台账或正文不在，跳过')

    # ── ② 硬项 ──
    if fp:
        hb, hh = hard_scan(fp)
        bad = {k: v for k, v in hb.items() if v}
        badh = {k: v for k, v in hh.items() if v and k != '英文'}
        if bad or badh:
            todo.append(('硬项未清', '正文%s｜亮点段%s' % (bad or '净', badh or '净'), None))
        else:
            print('② 硬项全清')

    # ── ③ 圣经三样 ──
    try:
        C = io.open(os.path.join(ROOT, '设定', '00_镇冢秘术_唯一总圣经.md'),
                    encoding='utf-8').read().split('\n')
        rounds = []
        if os.path.exists(lp):
            L = json.load(io.open(lp, encoding='utf-8'))
            rounds = sorted({int(m.group(1)) for x in L.get('版本', [])
                             for m in [re.search(r'第\s*(\d+)\s*轮', x.get('说明', ''))] if m})
        base = n if len(rounds) >= 13 else n - 1
        e = sum(1 for l in C if l.startswith('### 第 %d 章' % base))
        a = sum(1 for l in C if l.startswith('第 %d 章必须从' % (base + 1)))
        p = sum(1 for l in C if '已写 1—%d 章' % base in l)
        if e and a and p:
            print('③ 圣经三样齐（第%d章之条／第%d章之锚／进位%d）' % (base, base + 1, base))
        else:
            todo.append(('圣经三样不全',
                         '条%d 锚%d 进位%d（其文须人拟，器不代写）' % (e, a, p), None))
    except Exception as ex:
        print('③ 圣经查不成：%s' % str(ex)[:50])

    # ── ④ 看官凭据 ──
    try:
        import importlib.util as u
        sp = u.spec_from_file_location('_k', os.path.join(ROOT, '工具', '看官.py'))
        k = u.module_from_spec(sp)
        sp.loader.exec_module(k)
        ok, lack, old = k.验凭(n)
        if ok:
            print('④ 看官五席齐且对版')
        else:
            def refix():
                o = []
                for c in ('--生客', '--挑刺', '--小说家', '--评论'):
                    o.append(R('python3', '工具/看官.py', c, str(n))[-60:])
                o.append(R('python3', '工具/看官.py', '--连读',
                           str(max(1, n - 3)), str(n))[-60:])
                return '五席已重跑'
            todo.append(('看官未齐', '缺%s 过期%s' % (lack or '无', old or '无'), refix))
    except Exception as ex:
        print('④ 凭据查不成：%s' % str(ex)[:50])

    # ── ⑤ 未提交 ──
    st = [x for x in R('git', 'status', '--short').split('\n') if x.strip()]
    if len(st) >= 20:
        todo.append(('未提交积压', '%d 件' % len(st),
                     lambda: (R('git', 'add', '-A'),
                              R('git', 'commit', '-q', '-m',
                                'auto-repair: commit pending work'))[1]))
    else:
        print('⑤ 未提交 %d 件（未逾二十）' % len(st))

    # ── 动手 ──
    print('')
    if not todo:
        print('════ 无待修 ════')
        return
    print('════ 待修 %d 处 ════' % len(todo))
    for name, diag, fn in todo:
        print('  · %s：%s%s' % (name, diag, '' if fn else '　【器修不了，须人办】'))

    if not do:
        print('')
        print('（只诊断。要动手，跑 python3 工具/自修.py --修）')
        return

    print('')
    print('════ 动手 ════')
    for name, diag, fn in todo:
        if fn is None:
            print('  · %s：器修不了，留给人。' % name)
            continue
        print('  · %s：动手中……' % name)
        fn()

    # ── 复验（器自己验，不由人报）──
    print('')
    print('════ 复验 ════')
    if fp and os.path.exists(lp):
        L = json.load(io.open(lp, encoding='utf-8'))
        vs = L.get('版本', [])
        lw = vs[-1].get('soft', {}).get('净重', 0) if vs else 0
        print('  台账%d ｜ 正文%d ｜ %s'
              % (lw, weight(fp), '相符' if lw == weight(fp) else '★仍相违'))
    try:
        import importlib.util as u
        sp = u.spec_from_file_location('_k2', os.path.join(ROOT, '工具', '看官.py'))
        k = u.module_from_spec(sp)
        sp.loader.exec_module(k)
        ok, lack, old = k.验凭(n)
        print('  看官五席%s（缺%s 过期%s）' % ('齐' if ok else '未齐', lack or '无', old or '无'))
    except Exception:
        pass
    st2 = [x for x in R('git', 'status', '--short').split('\n') if x.strip()]
    print('  未提交 %d 件｜末笔 %s' % (len(st2), R('git', 'log', '--oneline', '-1').strip()[:40]))


if __name__ == '__main__':
    main()
