# -*- coding: utf-8 -*-
"""负测 · 造章令（1020 W53·治席 G3 立·瑕疵总账 X13／X14／X26）

★造章.js 之令逐字渲染而验（node 跑其全流，诸席之交以假交代之，只收令、schema、effort）——四件：
  ①续跑之缓存（1017 作者铁律③）：N≤397 之诸令（连 schema、effort），390—397 八章×三重（轻中重）×二路（净／回写）渲染之 sha256，
    与改前之造章.js（git c299dc4c 之版，sha256 84810dae…）之基逐一同——**⛔一字之改、⛔键之换序**
    （指以原序 JSON 算：schema 之键换序即令请求之字节变、缓存即破；旧以 sort_keys 算，换序验不出——W53 验席逮）；
    390 守 N<391 之枝（无「此法之缺」），391—397 守诸枝之界。新令只许以 N≥398 之条件加。
  ②X26：N≥398 之执笔令「首回即落」——**首条消息**同发 Read 料（allow_large）与一条 Bash「cat > 构思」建档
    （392—397 三十四席读料俱用 Read，⛔以 Bash cat 读料：料逾四万字，回显只留首 2KB——W53 验席逮上回之令「读料之命令末接 cat >」之假前提）；
    想定一样以 cat >> 追记一样、全章之排在档上排（满分之问先落，拍表随第一拍落）；回数之限 28；旧「构思可先落一回」⛔再见。
  ③X14：N≥398 之盲读分二类报——schema 带 prior；①只算本章之卡、①之二前情之指⛔计入读不懂；逻辑审并入回述实证；记席录之。
  ④X13：N≥398 之记令於立卡後跑「第零轮开镜庭.py --静 N+1」，十四格（卡之自牵）红即改卡。
  ⑥X40（1020 立·裁_1020_推闸二红_399封版後）：args.须厚（自走.py 之派令以 分量闸.须厚 现判）且 N≥401 → 诸执笔令带「【硬项·须厚】本章之事须担得起 2,900 净重」、
    选令带「须厚之章，净重 <2,900 之稿作底须写其由」；N≤400 传 须厚 亦⛔认（400 之诸令与不传者原序之指同）、401 不传者⛔带。
  回灌：②③④之判拿 397 之令（旧病）去判，须一一红；上回之假前提（读料之 Bash 末接 cat > 构思）、「思考里只想眼下这一拍」之牵灌回须红；
    ①之指换键序须变——证其判咬得住，⛔一律判过。
⛔限：渲染证得了「令里写了」，证不了「席守了」——守没守归 `工具/费审.py` 之「构思」「构思隔」两列（首落逾五分、诸写最长隔逾十分即⛔）。
用法：python3 工具/负测_造章令.py
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import os, sys, json, hashlib, subprocess, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JS = os.path.join(ROOT, '工具', '席', '造章.js')

# 假交：label 定其交；逻辑审·1 於「病」路交硬崩与读误，令回写、盲读·2、逻辑审·2 俱跑
_器 = r"""
const fs = require('fs')
const [, , 档, n, 重, 病, 厚] = process.argv
const src = fs.readFileSync(档, 'utf8').replace(/^export const meta/m, 'const meta')
const N = Number(n)
const 收 = []
const 交 = (label) => {
  if (label.startsWith('执笔')) return { file: '版本/第' + N + '章/起草_稿一.md', beats: 5, words: 2800, soul: '魂', best: '最好', weak: '最弱', plan: '写法' }
  if (label.startsWith('选')) return { ranking: ['稿一', '稿二'], why: '由', fatal: [{ id: '致命1', draft: '稿一', quote: '句', against: '1:1', fix: '治' }], leap: [{ id: '大进1', win_quote: '甲', better_quote: '乙', gain: '得' }], common_fatal: '', beat_scores: '拍分', peaks: '叫绝' }
  if (label.startsWith('合稿')) return { file: '正文/x.md', beats: 5, words: 2800, base: '稿一', fatal_done: '治毕', leap_done: '嫁', peaks: '叫绝', gates: '器', gates_green: true, reds: '', ledger: '账', recap: '前情' }
  if (label.startsWith('盲读')) return { understood: false, confused: '卡' + label, misread: '错', want_next: true, why_next: '想', happened: '事', remember: '记', prior: '前情之指' }
  if (label === '逻辑审·1') return 病 === '病' ? { hard: [{ kind: '因果断', where: '1:1', what: '断', proof: '据' }], soft: '软', gate: '闸', misread: true, misread_where: '处', misread_fix: '治' } : { hard: [], soft: '软', gate: '闸', misread: false }
  if (label.startsWith('逻辑审')) return { hard: [], soft: '软2', gate: '闸2', misread: false }
  if (label.startsWith('记席')) return { receipt: '回执', lock_row: '行', memory: '忆', next_card: '卡', open_brief: '推' }
  return '办毕'
}
const agent = async (prompt, o) => { 收.push({ label: o.label, prompt, schema: o.schema || null, effort: o.effort || null }); return 交(o.label) }
const parallel = async (fs_) => Promise.all(fs_.map(f => f()))
const AF = Object.getPrototypeOf(async function () {}).constructor
new AF('args', 'agent', 'parallel', 'phase', 'log', src)(厚 === '厚' ? { 章: N, 重, 须厚: true } : { 章: N, 重 }, agent, parallel, () => {}, () => {})
  .then(r => process.stdout.write(JSON.stringify({ 收, 果: r })))
  .catch(e => { process.stderr.write(String(e && e.stack || e)); process.exit(3) })
"""

# ①之基：改前之造章.js（git c299dc4c 之版·sha256 84810dae…）渲染所得、以原序 JSON 算——N≤397 之令⛔动、⛔换序
_基 = {"390轻净": "446235d2ae12bfba", "390轻病": "c3b7b946890cc774", "390中净": "4c039e947b88a4a5", "390中病": "2637239d514be0cc",
      "390重净": "e962618acc460b20", "390重病": "7376f43ef2c8f1b4",
      "391中净": "d81731e5a2dea60b", "391中病": "d8df30474c07d5eb", "391轻净": "2ef492c74b0b1c20", "391轻病": "25202b027ddbd821",
      "391重净": "5a08da748604da17", "391重病": "c8ed175f14e8b3c4", "392中净": "c4a354ffca3e63ee", "392中病": "e8d88c9b7b026432",
      "392轻净": "21148e279fff6a2e", "392轻病": "fa1e4966a4c70230", "392重净": "d3c0a29713e4a2d5", "392重病": "0094443a0ddedfae",
      "393中净": "7306c13984cf3c5e", "393中病": "b98108879d0ec573", "393轻净": "836cab91bef46d4c", "393轻病": "be2746a40f57838b",
      "393重净": "8c55b4f8d50995fa", "393重病": "3dc6098873b8147b", "394中净": "f986b2cbaf38e5ca", "394中病": "3f29cde7a5094979",
      "394轻净": "801ee39fe9f1a7c1", "394轻病": "c58dbe02c4a36d3a", "394重净": "12e5ad7ec936c3a7", "394重病": "fb064f52de193a1e",
      "395中净": "a42aa5140441d7f1", "395中病": "c1ad447e9931274f", "395轻净": "d82459e843fbffeb", "395轻病": "2c0775a51a2be9ae",
      "395重净": "37009624103bce82", "395重病": "fd95b43fa75a8a9b", "396中净": "cbf17443256db523", "396中病": "e4d2a0c73aeada3e",
      "396轻净": "f9c81aae5e0080fa", "396轻病": "d08aab083108656a", "396重净": "68e35a52033e2415", "396重病": "05a98b9f58006d82",
      "397中净": "c582cc7d1b2eb860", "397中病": "2fe8c3db8e3f2603", "397轻净": "d2f7c5b79f2e31e4", "397轻病": "1ca55a9cd69543c6",
      "397重净": "51e00fda90975036", "397重病": "2ee9fe5da8bd43e0"}


def 渲(器, n, 重='中', 病='病', js=JS, 厚='否'):
    o = subprocess.run(['node', 器, js, str(n), 重, 病, 厚], capture_output=True, text=True, cwd=ROOT, timeout=60)
    if o.returncode:
        raise RuntimeError('造章.js 渲染不起（%d %s %s）：%s' % (n, 重, 病, o.stderr.strip()[:300]))
    return json.loads(o.stdout)['收']


def 指(收):
    """原序 JSON 之 sha256（⛔sort_keys：schema 之键换序，请求之字节即变、缓存即破——须验得出）。"""
    return hashlib.sha256(json.dumps(收, ensure_ascii=False).encode()).hexdigest()[:16]


def _令(收, 首):
    return [c for c in 收 if c['label'].startswith(首)]


def 新条(收, n):
    """→ [(条, 合否)]：N≥398 之诸条（X26／X14／X13）。拿 397 之令来判须一一不合（回灌）。"""
    笔 = _令(收, '执笔·甲')
    笔 = 笔[0]['prompt'] if 笔 else ''
    盲 = _令(收, '盲读')
    审 = _令(收, '逻辑审·1')
    记 = _令(收, '记席')
    记 = 记[0]['prompt'] if 记 else ''
    假前提 = ('读料那一条命令', '&& cat > 版本/第%d章/起草_甲_构思.md' % n)   # 上回之令：读料之 Bash 末接 cat > 构思（席读料俱用 Read）
    return [
        ('X26·首条消息 Read 料与 Bash 建构思档同发（⛔以 Bash cat 读料；上回之假前提⛔见）',
         '首回即落】' in 笔 and '**第一条消息**同发两个调用' in 笔 and ('① Read「版本/第%d章/_料.md」（allow_large' % n) in 笔
         and ("② 一条 Bash「cat > 版本/第%d章/起草_甲_构思.md <<'EOF'」建档" % n) in 笔 and '⛔以 Bash cat 读料' in 笔
         and not any(x in 笔 for x in 假前提)),
        ('X26·想定一样即以 cat >> 追记、每定一拍即追记；费审量首落与最长隔',
         '想定一样即以 cat >> 追记一样' in 笔 and '每定一拍即追记一行' in 笔 and '构思首落−席起' in 笔 and '构思诸写之最长隔' in 笔),
        ('X26·全章之排在档上排（满分之问先落、拍表随第一拍落）；⛔「思考里只想眼下这一拍」之牵',
         '全章之排在档上排' in 笔 and '「## 满分之问」（三种写法与其比）先落' in 笔 and '随第一拍同落' in 笔
         and '思考里只想眼下这一拍' not in 笔),
        ('X26·回数之限 28（逐样追记有其回）', '至多 28 回工具' in 笔),
        ('X26·旧「构思可先落一回」⛔再见（彻删於新令）', bool(笔) and '构思可先落一回' not in 笔),
        ('X14·盲读 schema 带 prior 且必交', bool(盲) and all('prior' in (c['schema'] or {}).get('required', []) for c in 盲)),
        ('X14·盲读①只算本章之卡、①之二前情之指⛔计入读不懂',
         bool(盲) and all('只算本章之卡' in c['prompt'] and '①之二 prior' in c['prompt'] and '⛔写进 confused' in c['prompt'] and '六答' in c['prompt'] for c in 盲)),
        ('X14·逻辑审把前情之指并入回述实证', bool(审) and '前情之指「' in 审[0]['prompt'] and '并入下「回述实证」逐条核' in 审[0]['prompt']),
        ('X14·记席录前情之指', '前情之指：' in 记 and '盲读六答' in 记),
        ('X13·记席立卡後跑开镜庭十四格', ('第零轮开镜庭.py --静 %d' % (n + 1)) in 记 and '十四·卡之自牵' in 记),
    ]


硬项须厚 = '【硬项·须厚】本章须厚（分量闸·须厚）：本章之事须担得起 2,900 净重——⛔凑字、⛔撒感官；担不起即换一件更大的事，写进构思之满分之问'
选须厚 = '须厚之章，净重 <2,900 之稿作底须写其由'


def 带须厚(收):
    """→ (诸执笔令俱带其硬项, 有执笔令带其硬项, 选令带其底)。"""
    笔 = [c['prompt'] for c in _令(收, '执笔')]
    选 = [c['prompt'] for c in _令(收, '选')]
    return (bool(笔) and all(硬项须厚 in p for p in 笔), any(硬项须厚 in p for p in 笔),
            bool(选) and all(选须厚 in p for p in 选))


def 须厚之条(器):
    """★1020 X40：→ [(条, 合否)]。⛔动 N≤400——400 传 须厚 与不传者原序之指须同（args.须厚 於 N≤400 一字不认）。"""
    出 = []
    for 重 in ('中', '轻', '重'):
        a = 带须厚(渲(器, 401, 重, '净', 厚='厚'))
        出.append(('401（须厚:true·%s）之诸执笔令俱带「本章须厚」之硬项、选令带「须厚之章之底」' % 重, a[0] and a[2]))
    b = 带须厚(渲(器, 401, '中', '净'))
    出.append(('401 不传 须厚 者⛔带（执笔令、选令俱无）', not b[1] and not b[2]))
    c400 = 渲(器, 400, '中', '病', 厚='厚')
    d = 带须厚(c400)
    出.append(('400（传 须厚:true）之执笔令、选令⛔带——N≤400 之令⛔动', not d[1] and not d[2]))
    出.append(('400 传 须厚 与不传者原序之指同（轻中重×净病俱同）',
              all(指(渲(器, 400, 重, 病, 厚='厚')) == 指(渲(器, 400, 重, 病)) for 重 in ('轻', '中', '重') for 病 in ('净', '病'))))
    # 回灌：把 401 之硬项抹去（假其被删），本条须红
    抹 = [dict(c, prompt=c['prompt'].replace(硬项须厚, '')) for c in 渲(器, 401, '中', '净', 厚='厚')]
    出.append(('回灌·抹去 401 之「本章须厚」硬项 → 本条红', not 带须厚(抹)[0]))
    return 出


def _换笔(收, f):
    return [dict(c, prompt=f(c['prompt'])) if c['label'].startswith('执笔·甲') else c for c in 收]


def 跑():
    R = []
    d = tempfile.mkdtemp(prefix='造章令_')
    try:
        器 = os.path.join(d, '渲.js')
        open(器, 'w', encoding='utf-8').write(_器)
        # ①N≤397 逐字不变（键序亦入）
        坏 = []
        for k, v in sorted(_基.items()):
            if 指(渲(器, int(k[:3]), k[3], k[4])) != v:
                坏.append(k)
        R.append(('①N≤397 之诸令逐字不变、键序不变（%d 局·原序 sha256 同改前之基）%s' % (len(_基), ('｜⛔变：' + '、'.join(坏[:8])) if 坏 else ''), not 坏))
        # ①之回灌：397 之收把一份 schema 之键换序——原序之指须变（旧 sort_keys 之指不变，验不出）
        收397 = 渲(器, 397)
        i = next(j for j, c in enumerate(收397) if c['schema'])
        sc = 收397[i]['schema']
        换 = [dict(c) for c in 收397]
        换[i] = dict(换[i], schema=dict(sc, properties=dict(reversed(list(sc['properties'].items())))))
        旧指 = lambda 收: hashlib.sha256(json.dumps(收, ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:16]
        R.append(('回灌·①schema 之键换序→原序之指即变（旧 sort_keys 之指不变：%s）' % ('验不出' if 旧指(换) == 旧指(收397) else '?'),
                  指(换) != 指(收397) and 旧指(换) == 旧指(收397)))
        # ②③④ N≥398 诸条俱在（中重·回写一路）；轻重二宽亦渲得起
        收 = 渲(器, 398)
        for 条, ok in 新条(收, 398):
            R.append(('398·' + 条, ok))
        for 重 in ('轻', '重'):
            R.append(('398·%s（宽 %d）渲得起、执笔令俱带首回即落' % (重, {'轻': 3, '重': 7}[重]),
                      all('首回即落】' in c['prompt'] for c in _令(渲(器, 398, 重, '净'), '执笔'))))
        # 回灌：397 之令（旧病）照新条判，须一一红
        旧 = 新条(收397, 397)
        R.append(('回灌·397 之令（旧病）照新条判 %d 条俱红（⛔一律判过）' % len(旧), not any(ok for _, ok in 旧)))
        # 回灌之二：把 398 之令里「首回即落」一段抹去（假其被删），X26 首条须红
        R.append(('回灌·抹去 398 之「首回即落」→ X26 首条红', not 新条(_换笔(收, lambda p: p.replace('首回即落】', '')), 398)[0][1]))
        # 回灌之三：上回（W53 治席首版）之假前提——「读料那一条命令之末接 && cat > 构思」（392—397 读料俱用 Read）→ X26 首条红
        假 = "**第一条工具调用**——读料那一条命令——之末即接「&& cat > 版本/第398章/起草_甲_构思.md <<'EOF'」建档；"
        R.append(('回灌·上回之假前提（读料之 Bash 末接 cat > 构思）→ X26 首条红',
                  not 新条(_换笔(收, lambda p: p.replace('你的**第一条消息**', 假 + '你的**第一条消息**')), 398)[0][1]))
        # 回灌之四：上回之牵扯——「思考里只想眼下这一拍」（与构思①全章怎么排、②三种写法相牵）→ 第三条红
        R.append(('回灌·「思考里只想眼下这一拍；⛔在思考里把全章排完」之牵 → X26 第三条红',
                  not 新条(_换笔(收, lambda p: p.replace('思考里一回只想一样', '思考里只想眼下这一拍')), 398)[2][1]))
        # ⑤X33（1020）：N≥399 记令述记料以今之十二节；398 照旧（已封之章之令⛔变）
        记399 = (_令(渲(器, 399), '记席') or [{'prompt': ''}])[0]['prompt']
        记398 = (_令(收, '记席') or [{'prompt': ''}])[0]['prompt']
        R.append(('399·X33 记令述记料十二节（【十二】canon 卡名在）；398 仍旧式（九件事）',
                  '十二节已汇' in 记399 and '【十二】canon' in 记399 and '九件事要翻' not in 记399 and '九件事要翻' in 记398 and '十二节已汇' not in 记398))
        # ⑥★1020 X40：须厚入令——401（须厚:true）之执笔令带其硬项、选令带其底；400 传之亦⛔认；401 不传者⛔带
        for 名, ok in 须厚之条(器):
            R.append(('X40·' + 名, ok))
    except Exception as e:
        R.append(('⛔渲染不起：%s' % e, False))
    finally:
        shutil.rmtree(d, ignore_errors=True)
    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    过 = sum(1 for _, o in R if o)
    print('  ── 负测·造章令 %d/%d %s ──' % (过, len(R), '全通' if 过 == len(R) else '⛔未过'))
    return 过 == len(R)


if __name__ == '__main__':
    sys.exit(0 if 跑() else 1)
