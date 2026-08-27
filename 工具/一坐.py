# -*- coding: utf-8 -*-
"""一坐.py —— 起手唯一之令。

★立此器之由（拿账说，不拿主意说）：
  · 2026-08-27 本坐十八次自撰工具回执，全发生在一份很详细的提示词之下。
  · 提示词里明写「一坐只发四五个调用」「存版后另发独立调用复核」——照样违反。
  · ★★故：提示词管不住我。管得住的只有一样——把「报告」从我手上拿走。

★★此器之职：查完实况，印出「现在该干什么」与「哪里坏了、怎么修」。
  ★★★我只负责干活，与把它的输出原样贴出来；它没印的数，我不许说。

用法：
    python3 工具/一坐.py          # 自动取 open_brief 之章
    python3 工具/一坐.py 286      # 指定章
"""
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
    """跑一个命令，返回其 stdout（失败则返回空串）。"""
    try:
        p = subprocess.run(list(a), cwd=ROOT, capture_output=True,
                           text=True, timeout=600)
        return p.stdout
    except Exception:
        return ''


def body(n):
    """取第n章白文（去章题与亮点段）。"""
    for f in glob.glob(os.path.join(ROOT, '正文', '*.md')):
        m = re.search(r'第([零一二三四五六七八九十百]+)章', os.path.basename(f))
        if not m or cn2i(m.group(1)) != n:
            continue
        t = io.open(f, encoding='utf-8').read().split('【本章亮点】')[0]
        return re.sub(r'^.*?第.+?章[^\n]*\n', '', t, count=1, flags=re.S)
    return None


def main():
    fix = []          # 坏了的地方与其修法
    out = []

    # ── 本章之号 ──
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        n = int(sys.argv[1])
    else:
        try:
            d = json.load(io.open(os.path.join(ROOT, '设定', 'canon事实库.json'),
                                  encoding='utf-8'))
            n = int(d['open_brief']['for_ch'])
        except Exception:
            print('⛔ 取不到 open_brief.for_ch，请以 python3 工具/一坐.py N 指定章号')
            return
    out.append('════ 一坐 · 第%d章 ════' % n)

    # ── 一·台账与正文 ──
    lp = os.path.join(ROOT, '版本', '第%d章' % n, '_台账.json')
    b = body(n)
    tw = len(re.sub(r'\s', '', b)) if b else 0
    if os.path.exists(lp):
        L = json.load(io.open(lp, encoding='utf-8'))
        vs = L.get('版本', [])
        last = vs[-1] if vs else {}
        lw = last.get('soft', {}).get('净重', 0)
        hard = sum(last.get('hard', {}).values()) if last.get('hard') else 0
        rounds = sorted({int(m.group(1)) for x in vs
                         for m in [re.search(r'第\s*(\d+)\s*轮', x.get('说明', ''))] if m})
        out.append('台账：%d版｜末版 %s｜硬项 %d' % (len(vs), last.get('版', '?'), hard))
        out.append('净重：台账 %d ｜ 正文 %d ｜ %s'
                   % (lw, tw, '相符' if lw == tw else '★相违（差%d）' % (tw - lw)))
        out.append('真轮：%d/13　已跑 %s' % (len(rounds), rounds if rounds else '无'))
        if lw != tw:
            fix.append('台账与正文相违 → 跑 python3 工具/跑轮.py --补存 %d "说明"，'
                       '再以独立调用复核' % n)
        if hard:
            fix.append('硬项 %d 未清 → 扫破折／说破／五逗／半角／英文，清零后补存' % hard)
        nxt = (max(rounds) + 1) if rounds else 1
        if len(rounds) >= 13:
            out.append('▶ 十三轮已满 → 该跑封版之序')
        else:
            out.append('▶ 下一轮：第%d轮' % nxt)
            # ★2026-08-27 补：286第1、2轮连犯两回「未领轮即动手」，闸拦二次且落旗成死结。
            #   ★★故此处焊一行：印下一轮，必连其领轮之命令一并印。
            out.append('   ★动手之前先领轮：python3 工具/跑轮.py --下一轮 %d' % n)
            out.append('   ★★若旗已落（存版被拦），领轮不落基线；须以 --补存 销旗。')
    else:
        out.append('台账：无（本章尚未起轮）')
        out.append('正文：%s（%d字）' % ('在' if b else '不在', tw))
        out.append('▶ 该跑第1轮（起草）')

    # ── 二·闸 ──
    six = R('python3', '工具/开轮六检.py', str(n))
    bad = [l.strip() for l in six.split('\n') if '⛔' in l]
    out.append('── 闸 ──')
    if bad:
        for l in bad[:6]:
            out.append('  ' + re.sub(r'\s+', ' ', l)[:100])
    else:
        out.append('  六检全绿')
    for l in bad:
        if '冷轮之欠' in l:
            fix.append('冷轮未执 → 读其原档第五节全文再落笔，'
                       '不许凭记忆；补执毕於第11轮落回执')
        if '锚' in l and '未备' in l:
            fix.append('下一章之锚未备 → 改圣经三样（本章之条／下一章之锚／进位），'
                       '★每改一样，另发一个只做核查的调用验它')
        if '亮点段' in l:
            fix.append('亮点段缺 → 补毕当场以正文之尺扫一遍（破折／说破／五逗／半角／英文）')

    # ── 三·冷轮（只看近四章）──
    out.append('── 冷轮（近四章）──')
    ck = []
    for f in glob.glob(os.path.join(ROOT, '设定', '冷轮_COLD*.md')):
        m = re.search(r'COLD(\d+)_於(\d+)', os.path.basename(f))
        if not m:
            continue
        src, due = int(m.group(1)), int(m.group(2))
        if abs(due - n) > 3:
            continue
        s = io.open(f, encoding='utf-8').read()
        done = ('已执' in s and '销档' in s)
        ck.append('  COLD-%d 限%d %s' % (src, due, '已执' if done else '★待执'))
        if not done and due <= n:
            fix.append('COLD-%d 限%d 未执 → 於第%d章补执，'
                       '照其档第五节抄，不凭记忆' % (src, due, due))
    out += (ck or ['  无'])

    # ── 四·看官凭据 ──
    out.append('── 看官 ──')
    try:
        import importlib.util as u
        sp = u.spec_from_file_location('_k', os.path.join(ROOT, '工具', '看官.py'))
        k = u.module_from_spec(sp)
        sp.loader.exec_module(k)
        ok, lack, old = k.验凭(n)
        out.append('  五席%s｜缺 %s｜过期 %s'
                   % ('齐' if ok else '未齐', lack or '无', old or '无'))
        if lack or old:
            fix.append('看官未齐或过期 → 跑 --生客/--挑刺/--小说家/--评论 %d 与 --连读 %d %d；'
                       '小说家所交三拍须逐一回话，答不出即删' % (n, n - 3, n))
    except Exception as e:
        out.append('  凭据查不成：%s' % str(e)[:40])

    # ── 五·圣经三样 ──
    out.append('── 圣经 ──')
    try:
        C = io.open(os.path.join(ROOT, '设定', '00_镇冢秘术_唯一总圣经.md'),
                    encoding='utf-8').read().split('\n')
        # ★本章十三轮已满者，其身已成「前章」：查本章之条与下一章之锚。
        #   ★★未满者仍查前章之条与本章之锚。此别2026-08-27立（器初造时漏之）。
        done13 = (os.path.exists(lp) and len(rounds) >= 13) if os.path.exists(lp) else False
        base = n if done13 else (n - 1)
        e_prev = sum(1 for l in C if l.startswith('### 第 %d 章' % base))
        a_cur = sum(1 for l in C if l.startswith('第 %d 章必须从' % (base + 1)))
        pos = sum(1 for l in C if '已写 1—%d 章' % base in l)
        out.append('  第%d章之条 %d｜第%d章之锚 %d｜进位%d %d'
                   % (base, e_prev, base + 1, a_cur, base, pos))
        if not (e_prev and a_cur and pos):
            fix.append('圣经三样不全 → 逐样写，★每写一样另发一个只做核查的调用；'
                       '不许一次写三样')
    except Exception as e:
        out.append('  查不成：%s' % str(e)[:40])

    # ── 六·git ──
    st = R('git', 'status', '--short')
    lg = R('git', 'log', '--oneline', '-1')
    ah = R('git', 'status', '-sb')
    m = re.search(r'ahead (\d+)', ah)
    out.append('── git ──')
    out.append('  未提交 %d 件｜本地领先 %s 笔｜末笔 %s'
               % (len([x for x in st.split('\n') if x.strip()]),
                  m.group(1) if m else '0', lg.strip()[:44]))
    if len([x for x in st.split('\n') if x.strip()]) > 20:
        fix.append('未提交逾二十件 → 先提交，免其失於一处')

    # ── 修法 ──
    out.append('')
    if fix:
        out.append('════ 该修者 %d 处 ════' % len(fix))
        seen = []
        for x in fix:
            if x in seen:
                continue
            seen.append(x)
            out.append('  · ' + x)
    else:
        out.append('════ 无待修 ════')

    # ── 铁则（每回印，不许略）──
    out.append('')
    out.append('════ 三铁则 ════')
    out.append('  ① 一次只干一件事，干完发一个只做核查的调用，把它的输出原样贴出来。')
    out.append('  ② 此器没印的数，不许说。「我以为」「应该已经」一律作未做。')
    out.append('  ③ 修不动的，报出来交作者判；不许自造诊断，不许说「已定」。')

    print('\n'.join(out))


if __name__ == '__main__':
    main()
