// 以假 agent 跑 剧情庭.js 之流：验题之门、式段之裁令、他式裁令与改前逐字同
// 用法（仓根）：node 设定/_草/W60/X11/模.mjs 工具/席/剧情庭.js <改前之剧情庭.js（git show HEAD:工具/席/剧情庭.js）>
// 驳後（W60·X11 二回）：以真题档 势_第401段.md 之首行（带反引号）为一格；验题席之交以其令中之命令真跑 bash 而得
import fs from 'fs'
import cp from 'child_process'
const [,, 新档, 旧档] = process.argv
const AsyncF = (async () => {}).constructor
function 载(p) {
  const src = fs.readFileSync(p, 'utf8').replace('export const meta', 'const meta')
  return new AsyncF('args', 'agent', 'parallel', 'phase', 'log', src)
}
function 假(首) {
  const 令 = []
  const agent = async (prompt, o) => {
    令.push({ label: o && o.label, prompt, phase: o && o.phase })
    if (o && o.label === '验题·首行') return 首 === '真跑' ? 真跑(prompt) : 首
    if (o && o.label && o.label.startsWith('出案')) return { current_judgement: 'x', current_appeal: 7, current_sound: 7, keep: false, proposals: [{ name: 'a', plan: 'p', why_better: 'w', soundness: 's' }, { name: 'b', plan: 'p', why_better: 'w', soundness: 's' }, { name: 'c', plan: 'p', why_better: 'w', soundness: 's' }] }
    if (o && o.label === '刺·并攻') return { attacks: ['小说家1','小说家2','小说家3','剧本师1','剧本师2','剧本师3'].map(id => ({ id, flaw: 'f', level: '轻', better_claim_true: 'y' })) }
    if (o && o.label && o.label.startsWith('刺·')) return { flaw: 'f', level: '轻', better_claim_true: 'y' }
    if (o && o.label && o.label.startsWith('复评')) {
      const ids = ['小说家1','小说家2','小说家3','剧本师1','剧本师2','剧本师3','总编辑1','总编辑2','总编辑3','顶尖读者1','顶尖读者2','顶尖读者3']
      return { scores: ids.map(id => ({ id, appeal: id === '剧本师1' ? 9 : 6, sound: 8, beats_current: id === '剧本师1', reason: 'r' })), current_appeal: 7, first_choice: '剧本师1' }
    }
    return '摘要'
  }
  const parallel = async ts => Promise.all(ts.map(t => t().catch(() => null)))
  const logs = []
  return { agent, parallel, phase: () => {}, log: m => logs.push(m), 令, logs }
}
async function 跑(p, args, 首) {
  const m = 假(首)
  let r, err = null
  try { r = await 载(p)(args, m.agent, m.parallel, m.phase, m.log) } catch (e) { err = String(e.message || e) }
  return { r, err, 令: m.令, logs: m.logs }
}
function 真跑(prompt) {   // 照验题之令真跑其命令（仓根），如一个照令办事之席
  const m = /`(f='[^`]*)`/.exec(prompt)
  const o = cp.execFileSync('bash', ['-c', m[1]], { encoding: 'utf8' })
  if (/^题档不在$/m.test(o)) return { topic_exists: false, first_line: '', liao_path: '', liao_exists: false }
  const 料 = /^料=(.*) (有|无)$/m.exec(o) || [, '', '无']
  return { topic_exists: true, first_line: (/^首行=(.*)$/m.exec(o) || [, ''])[1], liao_path: 料[1], liao_exists: 料[2] === '有' }
}
const 结 = []
const T = (n, v) => { 结.push([n, !!v]); console.log((v ? '  ✓ ' : '  ⛔ ') + n) }
const 题 = '设定/剧情庭题/势_第401段.md'
const 真首 = fs.readFileSync(题, 'utf8').split('\n')[0]
const 好 = { topic_exists: true, first_line: 真首, liao_path: '设定/段案/_料_401-410.md', liao_exists: true }
T('（前提）真题档 势_第401段.md 首行带反引号', 真首.startsWith('料：`设定/段案/_料_401-410.md`'))
let x = await 跑(新档, { 题, 名: '势_第401段', 式: '段' }, 好)
T('式段无 W ⛔开（未派一席）', x.err && /args\.W/.test(x.err) && x.令.length === 0)
x = await 跑(新档, { 题, 名: '势_第401段', 式: '段', W: 'W61' }, { topic_exists: true, first_line: '# 剧情庭题·势·第 401—410 段', liao_path: '', liao_exists: false })
T('首行无段料 ⛔开、印所缺、只派验题一席', x.err && /首行须写「料：设定\/段案\/_料_<起>-<止>\.md」/.test(x.err) && /剧情庭题·势/.test(x.err) && x.令.length === 1 && x.logs.some(l => l.startsWith('⛔式段不开')))
x = await 跑(新档, { 题, 名: '势_第401段', 式: '段', W: 'W61' }, { topic_exists: true, first_line: '料：设定/段案/_料_401-410.md', liao_path: '设定/段案/_料_401-410.md', liao_exists: false })
T('首行所点段料不在 ⛔开', x.err && /段料不在/.test(x.err) && /段料\.py 401 410/.test(x.err))
x = await 跑(新档, { 题, 名: '势_第401段', 式: '段', W: 'W61' }, { topic_exists: false, first_line: '', liao_path: '', liao_exists: false })
T('题档不在 ⛔开', x.err && /题档不在/.test(x.err))
x = await 跑(新档, { 题, 名: '势_第401段', 式: '段', W: 'W61' }, { topic_exists: true, first_line: '料：设定/段案/_料_410-401.md', liao_path: '设定/段案/_料_410-401.md', liao_exists: true })
T('起大於止 ⛔开', x.err && /大於止/.test(x.err))
x = await 跑(新档, { 题, 名: '势_第401段', 式: '段', W: 'W61' }, { ...好, liao_path: '设定/段案/_料_391-400.md' })
T('验题席所报段料之路与首行不合 ⛔开', x.err && /不合/.test(x.err) && x.令.length === 1)
for (const [名, 首行] of [['无反引号', '料：设定/段案/_料_401-410.md'], ['半角冒号', '料: `设定/段案/_料_401-410.md`（注）']]) {
  x = await 跑(新档, { 题, 名: '势_第401段', 式: '段', W: 'W61' }, { ...好, first_line: 首行 })
  T(`首行${名}亦开庭`, !x.err && x.r && x.r.料 === '设定/段案/_料_401-410.md')
}
x = await 跑(新档, { 题, 名: '势_第401段', 式: '段', W: 'W61' }, '真跑')
T('真题档 势_第401段.md：验题之命令真跑於仓根 → 开庭、料＝_料_401-410', !x.err && x.r && x.r.料 === '设定/段案/_料_401-410.md' && x.logs.includes('题档首行点段料 设定/段案/_料_401-410.md ✓'))
x = await 跑(新档, { 题: "设定/剧情庭题/a'b.md", 名: 'X', 式: '段', W: 'W61' }, 好)
T('题档路含单引号 ⛔开（未派一席）', x.err && /单引号/.test(x.err) && x.令.length === 0)
x = await 跑(新档, { 题, 名: '势_第401段', 式: '段', W: 'W61' }, 好)
const 裁令 = (x.令.find(c => c.label === '裁') || {}).prompt || ''
T('真首行（带反引号）即开庭、走完六席＋验题；验题归「独立出案」之 phase', !x.err && x.令.length === 7 && x.令[0].phase === '独立出案' && x.r && x.r.单 === '设定/_草/W61/剧情庭单.json' && x.r.料 === '设定/段案/_料_401-410.md')
T('出案／刺／评之令俱点段料', x.令.filter(c => /^(出案|刺|复评)/.test(c.label)).every(c => c.prompt.includes('★段料（题档首行所点）：`设定/段案/_料_401-410.md`')))
T('式段裁令：只写裁档与单、单之式、⛔亲改、⛔立改单、自验 --施单', 裁令.includes('`设定/_草/W61/剧情庭单.json`') && 裁令.includes('{"档","原","新","由"}') && 裁令.includes('恰一见') && 裁令.includes('⛔跨行')
  && 裁令.includes('⛔改行数') && 裁令.includes('⛔亲改圣经') && 裁令.includes('⛔`python3 工具/改单.py --立`') && 裁令.includes('python3 工具/改单.py --施单 设定/_草/W61/剧情庭单.json'))
T('式段裁令无「当场以 改单.py --立 立改单」「当场改」之令', !裁令.includes('当场以 `python3 工具/改单.py --立') && !/当场改/.test(裁令) && !裁令.includes('并改题档所指之段案'))
T('式段裁令无底之「须同步更新圣经与三页」旧句，代以「以单代之」', !裁令.includes('须同步更新圣经') && 裁令.includes('★诸册随书更新（式段·以单代之）') && 裁令.includes('⛔亲改。'))
T('式段裁令：无改则单写 []、⛔「⛔出单」与自验相矛、⛔教 grep -c -F', 裁令.includes('单无条则写空列 `[]`') && 裁令.includes('无可动者单写 `[]`') && 裁令.includes('单为 `[]` 亦须跑') && !裁令.includes('⛔出单') && !裁令.includes('grep -c -F'))
T('式段他席（出案／刺／评）之 底 不动（仍含原句）', x.令.filter(c => /^(出案|刺|复评)/.test(c.label)).every(c => c.prompt.includes('须同步更新圣经与根目录总站三页')))
T('式段裁令仍⛔提交', 裁令.includes('⛔不提交、⛔git add（主环提交）'))
T('主环施单之令入 log', x.logs.some(l => l.includes('--施单 设定/_草/W61/剧情庭单.json --落 --号')))
// 他式：与改前逐字同
for (const 式 of ['改', '新']) {
  const a = await 跑(新档, { 题: '设定/剧情庭题/X.md', 名: 'X', 式 }, null)
  const b = await 跑(旧档, { 题: '设定/剧情庭题/X.md', 名: 'X', 式 }, null)
  T(`式${式}：诸席之令与改前逐字同（${a.令.length} 令）、无验题`, !a.err && !b.err && a.令.length === b.令.length && a.令.every((c, i) => c.prompt === b.令[i].prompt && c.label === b.令[i].label) && !a.令.some(c => c.label === '验题·首行') && JSON.stringify(a.r) === JSON.stringify(b.r))
}
{
  const a = await 跑(新档, { 题: 'T.md', 名: 'X', 式: '验', 主案: '设定/剧情庭题/X_主案.md' }, null)
  const b = await 跑(旧档, { 题: 'T.md', 名: 'X', 式: '验', 主案: '设定/剧情庭题/X_主案.md' }, null)
  T(`式验：诸席之令（含裁·验）与改前逐字同（${a.令.length} 令）`, a.令.length > 3 && a.令.length === b.令.length && a.令.every((c, i) => c.prompt === b.令[i].prompt) && (a.err || '') === (b.err || ''))
}
{ // 守原之支（诸席 keep 而无案）
  const 守 = (首) => { const m = 假(首); const g = m.agent; m.agent = async (pr, o) => (o && o.label && o.label.startsWith('出案')) ? { current_judgement: 'x', current_appeal: 9, current_sound: 9, keep: true, proposals: [] } : g(pr, o); return m }
  const run = async (p, args, 首) => { const m = 守(首); let r, err = null; try { r = await 载(p)(args, m.agent, m.parallel, m.phase, m.log) } catch (e) { err = String(e) } return { r, err, 令: m.令 } }
  const a = await run(新档, { 题, 名: '势_第401段', 式: '段', W: 'W61' }, 好)
  const 守令 = (a.令.find(c => c.label === '裁·守原') || {}).prompt || ''
  T('式段守原之裁：只写裁档与空单 []、带段料、返回单与料、⛔旧诸册句', !a.err && 守令.includes('单写空列 `[]`') && 守令.includes('★段料（题档首行所点）：`设定/段案/_料_401-410.md`')
    && !守令.includes('须同步更新圣经') && a.r && a.r.结 === '守原' && a.r.单 === '设定/_草/W61/剧情庭单.json' && a.r.料 === '设定/段案/_料_401-410.md')
  const c = await run(新档, { 题: 'T.md', 名: 'X', 式: '改' }, null), d = await run(旧档, { 题: 'T.md', 名: 'X', 式: '改' }, null)
  T('式改守原之裁与改前逐字同', !c.err && c.令.length === d.令.length && c.令.every((x, i) => x.prompt === d.令[i].prompt))
}
{ const 元 = s => (/export const meta = \{[\s\S]*?\n\}/.exec(fs.readFileSync(s, 'utf8')) || [''])[0]
  T('meta（含 phases）与改前逐字同——⛔另立「验题」之 phase', 元(新档) && 元(新档) === 元(旧档)) }
console.log('模·剧情庭 %d/%d', 结.filter(r => r[1]).length, 结.length)
process.exit(结.every(r => r[1]) ? 0 : 1)
