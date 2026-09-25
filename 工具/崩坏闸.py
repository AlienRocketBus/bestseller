# -*- coding: utf-8 -*-
"""崩坏闸——**剧情前後不许崩：死了的人不许活过来，没立过的能不许凭空出现。**

【其立之由（2026-09-25·作者令，逐字之意）】
  「千万不要出现剧情崩坏——之前一个角色已经死了，後面某一章突然复活；某个角色之前是普通人，
   没有暗示就突然使用超能力；之前从没出现过的设定突然冒出来。这会直接毁掉一本小说。
   我们要写六百多章，不注意的话几百章就白写了。必须设成一个非常强力、非常严格的机制，优先级很高。」
  ★本仓原有 canon 事实库（195 卡·430 条禁式）只拦「某一句具体的话」，**从来没有一本「谁死了、谁能什么、谁知道什么」的状态账**。

【三层】
  一·**状态账**：`设定/人物状态册.json`——逐人记 生死／亡於章／能／不能／知／不知；世界之禁。**每章封版须同步此账**（封版席之令）。
  二·**本器（机器判得死的）**：亡者（亡於章 < N）之名或别称出现在第 N 章白文里，而该句无「追忆之记」
      （想起／记得／当年／那时／梦／坟／牌位／遗／生前／活着的时候／死前 …）→ **红**：亡者在场。
      另：状态账里「不能」一栏之词（如「不会秘术」者）若与本章之能之词同句 → 黄，交审席判。
  三·**逻辑审席**（`工具/席/一章.js`）：起草合稿之後、封版之前，另派一席只拿状态账、世界之禁与前五章白文，
      逐条查 死而复生／能无来由／知不当知／设定新冒／时序自破；**硬崩即回写，二回不净不许封版**。

用法：python3 工具/崩坏闸.py N ｜ --全书 ｜ --自测
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账
except Exception:
    pass
import os, re, sys, json, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
账档 = os.path.join(ROOT, '设定', '人物状态册.json')
追忆 = re.compile(r'想起|想到|记得|记着|当年|那时|那年|从前|早先|梦|坟|牌位|灵位|遗|生前|活着的时候|死前|死後|死了|走了以後|在世|故去|葬|埋|照片|相片|留下的|说过的|教过|讲过|提过')


def _章号(名):
    _cn = {'零': 0, '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9}
    m = re.search(r'第([零〇一二三四五六七八九十百千]+)章', 名)
    if not m:
        return 0
    tot = cur = 0
    for ch in m.group(1):
        if ch in _cn:
            cur = _cn[ch]
        elif ch in '十百千':
            tot += (cur or 1) * {'十': 10, '百': 100, '千': 1000}[ch]; cur = 0
    return tot + cur


def 诸章():
    return {_章号(f): f for f in glob.glob(os.path.join(ROOT, '正文', '镇冢秘术_第*章*.md')) if _章号(f)}


def 读账(p=None):
    try:
        return json.load(open(p or 账档, encoding='utf-8'))
    except Exception:
        return None


def 句们(文):
    文 = 文.split('【本章亮点】')[0]
    return [s for s in re.split(r'(?<=[。！？!?])|\n', 文) if s.strip()]


def 查文(N, 文, 账):
    红, 黄 = [], []
    for 人 in 账.get('人物', []):
        if 人.get('生死') != '亡' or not 人.get('亡於章') or 人['亡於章'] >= N:
            continue
        名们 = [人['名']] + [x for x in 人.get('别称', []) if len(x) >= 2]
        for s in 句们(文):
            if any(n in s for n in 名们) and not 追忆.search(s):
                红.append('亡者在场：%s（亡於第%d章）——「%s」' % (人['名'], 人['亡於章'], s.strip()[:50]))
    return 红, 黄


def 查(N, 印=True):
    账 = 读账()
    if not 账:
        if 印:
            print('⛔崩坏闸：状态账 设定/人物状态册.json 不在或读不得——⛔无账即无防'); 
        return False, ['无账']
    章 = 诸章()
    if N not in 章:
        if 印:
            print('⛔崩坏闸：第%d章之档不在' % N)
        return False, ['无章']
    红, 黄 = 查文(N, open(章[N], encoding='utf-8').read(), 账)
    if 印:
        print('════ 崩坏闸 ════ 第%d章（状态账 %d 人·亡者 %d）' % (
            N, len(账.get('人物', [])), sum(1 for x in 账.get('人物', []) if x.get('生死') == '亡')))
        for x in 红:
            print('  ⛔ ' + x)
        for x in 黄:
            print('  ⚠ ' + x)
        if not 红:
            print('  ✓ 崩坏闸：无亡者在场。（能／知／设定之崩由逻辑审席判）')
    return not 红, 红


def 自测():
    账 = {'人物': [{'名': '张三', '别称': ['老张'], '生死': '亡', '亡於章': 10},
                   {'名': '李四', '生死': '存', '亡於章': None}]}
    r = [
        ('①亡者开口即红', bool(查文(20, '张三推门进来，说：走吧。', 账)[0])),
        ('②别称亦逮', bool(查文(20, '老张蹲在门口抽烟。', 账)[0])),
        ('③追忆不算', not 查文(20, '她想起张三那年说过的话。', 账)[0]),
        ('④坟前不算', not 查文(20, '张三的坟上长了草。', 账)[0]),
        ('⑤亡前之章不判', not 查文(9, '张三推门进来。', 账)[0]),
        ('⑥存者不判', not 查文(20, '李四推门进来。', 账)[0]),
        ('⑦亮点段不算正文', not 查文(20, '正文。\n【本章亮点】张三推门进来。', 账)[0]),
    ]
    for n, v in r:
        print(('  ✓ ' if v else '  ⛔ ') + n)
    print('负测·崩坏闸 %d/%d' % (sum(v for _, v in r), len(r)))
    return all(v for _, v in r)


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--自测' in a:
        sys.exit(0 if 自测() else 1)
    if '--全书' in a:
        账 = 读账(); 坏 = 0
        for n, f in sorted(诸章().items()):
            红, _ = 查文(n, open(f, encoding='utf-8').read(), 账 or {})
            for x in 红:
                print('  ⛔ 第%d章 %s' % (n, x)); 坏 += 1
        print('全书亡者在场 %d 处' % 坏)
        sys.exit(1 if 坏 else 0)
    sys.exit(0 if 查(int(a[0]))[0] else 1)
