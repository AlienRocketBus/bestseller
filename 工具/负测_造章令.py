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
  ⑦★1024 省 token 之审（records②③／seats①②／failures①②）——N≥411 之新行，N≤410 一字不变：
    ①之二：398—410 诸令之 sha256（改前之造章.js·c2659cdc 之版所渲，轻中重×净病择四局、401 起另带须厚）逐一同；
    通式：411 诸席（连回写、查席）传同一 schema（键 ASCII、各子式之 required 同 410 之旧式、顶层 minProperties:1）、令末「只填『X』一键」；
    交空对象即补派（执笔先查後补、选、合、盲、逻辑审·1、记席）；查收盘稿即⛔补；逻辑审·1 二回空即停；布尔严判（misread 交「否」⛔作读误，410 照旧）；
    回写之令实一字不动（411 去交之一句＝410 之令换号）；记令四刀（{done,left}、式取记料【一】、--前 --红 复跑）；
    窄审：第1回只读误者逻辑审·2 带窄审之门（稿差.py）、第1回之令记「据 正文＝vNN」、soft 并入第1回；有硬崩者照旧全审；承能拆键（承.py 之必填表＝通式之 required）。
    合流（B、C 二组之令）：411 执笔之【量】带「硬项只照 --量 所印之处」；记令带 记落.py 之末步、‹器:键› 诸占位、②之锚独立、主环之职栏⛔治；410 二者俱⛔带。
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
import os, sys, re, json, hashlib, subprocess, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JS = os.path.join(ROOT, '工具', '席', '造章.js')

# 假交：label 定其交；逻辑审·1 於「病」路交硬崩与读误，令回写、盲读·2、逻辑审·2 俱跑
_器 = r"""
const fs = require('fs')
const [, , 档, n, 重, 病, 厚, 空 = ''] = process.argv
const src = fs.readFileSync(档, 'utf8').replace(/^export const meta/m, 'const meta')
const N = Number(n)
const 收 = []
const 交 = (label) => {
  if (label.startsWith('执笔')) return { file: '版本/第' + N + '章/起草_稿一.md', beats: 5, words: 2800, soul: '魂', best: '最好', weak: '最弱', plan: '写法' }
  if (label.startsWith('选')) return { ranking: ['稿一', '稿二'], why: '由', fatal: [{ id: '致命1', draft: '稿一', quote: '句', against: '1:1', fix: '治' }], leap: [{ id: '大进1', win_quote: '甲', better_quote: '乙', gain: '得' }], common_fatal: '', beat_scores: '拍分', peaks: '叫绝' }
  if (label.startsWith('合稿')) return { file: '正文/x.md', beats: 5, words: 2800, base: '稿一', fatal_done: '治毕', leap_done: '嫁', peaks: '叫绝', gates: '器', gates_green: true, reds: '', ledger: '账', recap: '前情' }
  if (label === '逻辑审·1' && 病 === '串') return { hard: [], soft: '软', gate: '闸', misread: '否' }   // 布尔严判之验（旧以真值判）
  if (label.startsWith('盲读')) return { understood: false, confused: '卡' + label, misread: '错', want_next: true, why_next: '想', happened: '事', remember: '记', prior: '前情之指' }
  if (label === '逻辑审·1') return 病 === '病' ? { hard: [{ kind: '因果断', where: '1:1', what: '断', proof: '据' }], soft: '软', gate: '闸', misread: true, misread_where: '处', misread_fix: '治' } : { hard: [], soft: '软', gate: '闸', misread: false }
  if (label.startsWith('逻辑审')) return { hard: [], soft: '软2', gate: '闸2', misread: false }
  if (label.startsWith('记席')) return { receipt: '回执', lock_row: '行', memory: '忆', next_card: '卡', open_brief: '推' }
  return '办毕'
}
// ★1024 通式（N≥411）：交包於其键；空＝逗号相隔之 label（末 * 为前缀）交 {flaws} 之空对象；「查收」令查席交盘稿
const 空们 = 空 ? 空.split(',') : []
const 通键 = l => l.startsWith('执笔') ? 'draft' : l.startsWith('选') ? 'pick' : l.startsWith('合稿') ? 'merge' : l.startsWith('盲读') ? 'blind'
  : l.startsWith('逻辑审') ? 'audit' : l.startsWith('记席') ? 'record' : 'rewrite'
const 交通 = (label, prompt) => {
  if (label.endsWith('·查')) { const m = /--查 \S+ (\S+)/.exec(prompt); return 空们.includes('查收') && m ? { draft: { file: m[1], beats: 3, words: 2600, soul: '魂' }, flaws: '无' } : { flaws: '无稿' } }
  if (空们.some(x => label === x || (x.endsWith('*') && label.startsWith(x.slice(0, -1))))) return { flaws: '无' }
  if (label.startsWith('记席')) return { record: { done: true, left: '无' }, flaws: '无' }
  if (label === '回写') return { rewrite: { done: true, note: '治' } }
  if (label === '逻辑审·1' && 病 === '误') return { audit: { hard: [], soft: '软1', gate: '闸', misread: true, misread_where: '处', misread_fix: '治' }, flaws: '无' }
  return { [通键(label)]: 交(label), flaws: '无' }
}
const agent = async (prompt, o) => { 收.push({ label: o.label, prompt, schema: o.schema || null, effort: o.effort || null }); return N >= 411 ? 交通(o.label, prompt) : 交(o.label) }
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

# ①之二（1024 立）：398—410 之基——改前之造章.js（git c2659cdc 之版）所渲、原序 JSON；N≤410 之令⛔动、⛔换序（通式等新行只走 N≥411）
62
_基二 = {"398轻病": "b043bdd206d3a656", "398中净": "73bdff10966a522d", "398中病": "21a09b28c87b3264", "398重净": "a9f3ff5d7c1f8de3", "399轻病":
      "be3913b136a3eaab", "399中净": "3d9d4176cffcb8ba", "399中病": "550206833592cc37", "399重净": "57259bae95edf249", "400轻病": "cc2722f80b290c66",
      "400中净": "cd63e765854c9528", "400中病": "2f0f9f8a927a7d5a", "400重净": "f8af0f233433f30c", "401轻病": "a099e494702cae64", "401中净":
      "ebe0464da8d040f3", "401中病": "03365259c1a77674", "401中病厚": "fcb4d740715963fe", "401重净": "81cb569f4a2e5401", "402轻病": "a5439713032de288",
      "402中净": "ecab5acee1802de6", "402中病": "ab83ef2897f2a7ad", "402中病厚": "c3271da46a52f90b", "402重净": "895993fb1618ce0c", "403轻病":
      "2fec25541a0392ab", "403中净": "f2b8f2380c4ae413", "403中病": "a888dbbd70378c4a", "403中病厚": "cd5d6088a65cae37", "403重净": "a7201e19aa55903f",
      "404轻病": "84237899e0cdf045", "404中净": "ada8eec59ede6911", "404中病": "44814d2d01a7d195", "404中病厚": "5e42ebb8141dc218", "404重净":
      "1ce08bd9bc4ae209", "405轻病": "b926801932fc47dc", "405中净": "17ef5a438de2c04d", "405中病": "76e0f82f67f0dd76", "405中病厚": "24aae86ef238650d",
      "405重净": "42874012d888b405", "406轻病": "78d18d4668fd5ce4", "406中净": "4b3d76af3158dcdc", "406中病": "081f07a566c62ed8", "406中病厚":
      "2250d46d70347dd7", "406重净": "580eb02f50afc9d5", "407轻病": "3f3630644bad9f77", "407中净": "2a7ba5f66021ff64", "407中病": "939f8277a547eed3",
      "407中病厚": "6d5367ca74b32680", "407重净": "2a7ba5f66021ff64", "408轻病": "7ee6af815adeffa6", "408中净": "5473d397060c645e", "408中病":
      "985c42cb3e4d5370", "408中病厚": "22babd03cb8c00b7", "408重净": "5473d397060c645e", "409轻病": "b24109ae94d2f39e", "409中净": "a8af6bef9a125627",
      "409中病": "6f0bfcaa993725ce", "409中病厚": "55528e6aed0df661", "409重净": "a8af6bef9a125627", "410轻病": "f8db9ae1b43a3f23", "410中净":
      "b3c8a8460bd40311", "410中病": "0053d64e255a2ba5", "410中病厚": "9d9437e0ddeb2db4", "410重净": "b3c8a8460bd40311"}


def 渲(器, n, 重='中', 病='病', js=JS, 厚='否', 空='', 果=False):
    o = subprocess.run(['node', 器, js, str(n), 重, 病, 厚, 空], capture_output=True, text=True, cwd=ROOT, timeout=60)
    if o.returncode:
        raise RuntimeError('造章.js 渲染不起（%d %s %s）：%s' % (n, 重, 病, o.stderr.strip()[:300]))
    d = json.loads(o.stdout)
    return (d['收'], d['果']) if 果 else d['收']


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


def _键之句(k):
    return '【交之键】诸席共一交卷之式：StructuredOutput 只填「%s」一键' % k


通之键 = [('执笔', 'draft'), ('选', 'pick'), ('合稿', 'merge'), ('盲读', 'blind'), ('逻辑审', 'audit'), ('回写', 'rewrite'), ('记席', 'record')]


def 通之条(器):
    """★1024 省 token 之审：→ [(条, 合否)]。N≥411 之通式、补派、严判、记令四刀、窄审；拿 410 之令回灌须红。"""
    出 = []
    收, 果 = 渲(器, 411, 果=True)
    收410 = 渲(器, 410)
    式们 = [c['schema'] for c in 收]
    ASCII = lambda o: all(re.fullmatch(r'[A-Za-z0-9_.-]{1,64}', k) for k in (o.get('properties') or {}))
    通 = 式们[0] or {}
    旧式 = {k: next((c['schema'] for c in 收410 if c['label'].startswith(首) and c['schema']), None) for 首, k in 通之键 if k != 'rewrite'}
    出.append(('通式：411 诸席（%d·连回写）传同一 schema（原序之指同）、键俱 ASCII（坑⑩）、顶层 minProperties:1、带 flaws' % len(收),
              all(式们) and len({指(x) for x in 式们}) == 1 and ASCII(通) and all(ASCII(v) for v in 通.get('properties', {}).values() if isinstance(v, dict))
              and 通.get('minProperties') == 1 and list(通.get('properties', {})) == ['draft', 'pick', 'merge', 'blind', 'audit', 'rewrite', 'record', 'flaws']))
    出.append(('通式：各子式之 required 与 properties 同 410 之旧式（记式另验）；回写之子式 required done',
              all(通['properties'][k].get('required') == (旧式[k] or {}).get('required') and 通['properties'][k].get('properties') == {
                  kk: vv for kk, vv in (旧式[k] or {}).get('properties', {}).items() if kk != 'flaws'} for k in ('draft', 'pick', 'merge', 'blind', 'audit'))
              and 通['properties']['rewrite'].get('required') == ['done']))
    出.append(('令末一句「只填『X』一键」，X 与席相应（%d 席）' % len(收),
              all(_键之句(next(k for 首, k in 通之键 if c['label'].startswith(首))) in c['prompt'].rsplit('\n\n', 1)[-1] for c in 收)))
    出.append(('回灌·410 之令⛔带交之键、诸席之 schema 各异（旧式·N≤410 ⛔动）',
              not any('【交之键】' in c['prompt'] for c in 收410) and len({指(c['schema']) for c in 收410 if c['schema']}) > 1))
    写411 = next(c['prompt'] for c in 收 if c['label'] == '回写')
    写410 = next(c['prompt'] for c in 收410 if c['label'] == '回写')
    出.append(('回写之令实一字不动：411 去交之一句＝410 之令换号', 写411.rsplit('\n\n【交之键】', 1)[0] == 写410.replace('410', '411')))
    # 交空对象即补派
    def 标(空, 病='病'):
        c, r = 渲(器, 411, '中', 病, 空=空, 果=True)
        return [x['label'] for x in c], r
    for 空, 补 in (('选·行家兼两眼', '选·补'), ('合稿', '合稿·补'), ('盲读', '盲读·补'), ('逻辑审·1', '逻辑审·1·补'), ('记席', '记席·补')):
        L, _ = 标(空)
        出.append(('交空对象即补派：%s 交 {flaws} → 派 %s' % (空, 补), 补 in L))
    L, _ = 标('执笔·甲*')
    出.append(('交空对象即补派：执笔·甲交空 → 先派「执笔·甲·查」、查无稿再「执笔·甲·补」（⛔径派整席）', '执笔·甲·查' in L and '执笔·甲·补' in L and L.index('执笔·甲·查') < L.index('执笔·甲·补')))
    L, _ = 标('执笔·甲*,查收')
    查令 = next((c for c in 渲(器, 411, 空='执笔·甲*,查收') if c['label'] == '执笔·甲·查'), {'prompt': '', 'effort': None})
    出.append(('查席收盘稿 → ⛔补；查令只跑 承.py 411 --查 甲 <蒙档>、effort low、首句认章', '执笔·甲·查' in L and '执笔·甲·补' not in L
              and bool(re.search(re.escape('python3 工具/承.py 411 --查 甲 ') + r'\S+/第411章/起草_稿[一二三四五]\.md', 查令['prompt'])) and 查令['effort'] == 'low'   # re.escape：死处方哨认「承\.py」为器名而红
              and 查令['prompt'].startswith('你是第 411 章的**')))
    L, r = 标('逻辑审·1,逻辑审·1·补')
    出.append(('逻辑审·1 二回交空 → 停「逻辑审未交」（旧以 null 作无病照放）', r.get('停') == '逻辑审未交' and '记席' not in L))
    L, r = 标('逻辑审·2,逻辑审·2·补')
    出.append(('逻辑审·2 二回交空 → 停（⛔无复审而记）', r.get('停') == '致命未净' and '逻辑审·2·补' in L and '记席' not in L))
    L, _ = 标('', '串')
    L410 = [c['label'] for c in 渲(器, 410, '中', '串')]
    出.append(('布尔严判：misread 交「否」→ 411 ⛔作读误（无回写）；410 照旧真值判（有回写·旧行⛔动）', '回写' not in L and '回写' in L410))
    # 记令四刀
    记 = next(c for c in 收 if c['label'] == '记席')
    记410 = next(c['prompt'] for c in 收410 if c['label'] == '记席')
    出.append(('记令四刀：式 {done,left}、式取记料【一】⛔另读前章回执、治毕复跑 --前 --红、交 left 含 §十四',
              通['properties']['record'] == {'type': 'object', 'properties': {'done': {'type': 'boolean'}, 'left': {'type': 'string'}}, 'required': ['done', 'left']}
              and '式取记料【一】，⛔另读前章回执' in 记['prompt'] and '式照前章回执（封版.py --前 印其路，读之）' not in 记['prompt']
              and 'python3 工具/封版.py 411 --前 --红' in 记['prompt'] and 'left（未了之事＋回执 §十四 交总编辑诸条' in 记['prompt'] and '交：receipt' not in 记['prompt']))
    出.append(('回灌·410 记令照旧（读前章回执、交 receipt）', '式照前章回执（封版.py --前 印其路，读之）' in 记410 and '交：receipt' in 记410 and '--前 --红' not in 记410))
    # 窄审
    c误, r误 = 渲(器, 411, '中', '误', 果=True)
    审1 = next(c['prompt'] for c in 收 if c['label'] == '逻辑审·1')
    审2误 = next(c['prompt'] for c in c误 if c['label'] == '逻辑审·2')
    审2病 = next(c['prompt'] for c in 收 if c['label'] == '逻辑审·2')
    出.append(('窄审：第1回只读误 → 逻辑审·2 带窄审之门（首跑 稿差.py 411、判全照全审、名词 grep 401—410、节名不变）；第1回之令记「据 正文＝vNN」',
              '【窄审之门' in 审2误 and '首条命令「python3 工具/稿差.py 411」' in 审2误 and '至少第 401 至 410 章' in 审2误 and '盲读·2 未复读' in 审2误
              and '「## 造式·逻辑审·合後·第2回」' in 审2误 and 'python3 工具/稿差.py 411 --据' in 审1 and '稿差' not in 审2误.split('【窄审之门')[0]))
    出.append(('窄审：第1回有硬崩 → 逻辑审·2 照旧全审（⛔窄门）；soft 并入第1回（窄者）', '窄审之门' not in 审2病
              and '〔第1回〕软1' in (r误.get('逻辑审') or {}).get('soft', '') and '〔第1回〕' not in (果.get('逻辑审') or {}).get('soft', '')))
    出.append(('回灌·410 之逻辑审令⛔带窄门、⛔带据句', not any('窄审之门' in c['prompt'] or '稿差' in c['prompt'] for c in 收410)))
    # 承能拆键：承.py 之必填表＝通式之 required；拆之得子
    import 承 as _承
    出.append(('承能拆键：承.通之必＝通式诸子式之 required；{键: 子, flaws} → 子、缺必填 → 未交',
              all(_承.通之必[k] == 通['properties'][k].get('required') for k in 通['properties'] if k != 'flaws')
              and _承.拆({'pick': {k: 1 for k in _承.通之必['pick']}, 'flaws': '无'}, '选') == {k: 1 for k in _承.通之必['pick']}
              and _承.拆({'pick': {'ranking': []}}, '选') is None and _承.拆({'flaws': '无'}, '草') is None))
    # 合流：C 组之硬项之处、B 组之记落入令——只 N≥411
    量们 = [c['prompt'] for c in 收 if '【量·⛔心算】' in c['prompt']]
    出.append(('硬项之处入执笔令：411 诸执笔之【量】俱带「硬项只照 --量 所印之处」；410 ⛔带',
              bool(量们) and all('硬项只照 --量 所印之处（白文／骨记 L行＋原句' in t for t in 量们)
              and not any('硬项只照' in c['prompt'] for c in 收410)))
    记落之句 = ['python3 工具/记落.py 411 --试', '10. **末步·记落**', '跑「python3 工具/记落.py 411」', '‹器:回执之数›', '‹器:日号›', '‹器:终稿›',
             '‹器:大审#号›', 'OPEN_BRIEF_CARD_SCHEMA[412]', '你只立②（第 412 章', '「主环之职（记席⛔治）」一栏', '交：done（1—10 俱毕否）']
    出.append(('记落入记令：411 带末步·记落、‹器:键› 诸占位、②之锚独立、主环之职栏⛔治；410 ⛔带记落、⛔带占位',
              all(k in 记['prompt'] for k in 记落之句) and '记落' not in 记410 and '‹器:' not in 记410))
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
        # ①之二·1024：398—410 逐字不变
        坏2 = [k for k, v in sorted(_基二.items()) if 指(渲(器, int(k[:3]), k[3], k[4], 厚='厚' if k.endswith('厚') else '否')) != v]
        R.append(('①之二 N≤410 之诸令逐字不变、键序不变（%d 局·原序 sha256 同 c2659cdc 之基）%s' % (len(_基二), ('｜⛔变：' + '、'.join(坏2[:8])) if 坏2 else ''), not 坏2))
        for 名, ok in 通之条(器):
            R.append(('1024·' + 名, ok))
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
