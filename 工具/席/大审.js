export const meta = {
  name: 'da-shen',
  description: '大审瘦式（X51·裁_1021_省律 九）：零 token 先行之包（大审.py --包）＋四席同包（连读客、小说家、逻辑闭环、人物）＋裁一席（只读四报与上册逾限之笔）；录册归器（大审.py --录 runId）',
  phases: [{ title: '大审' }, { title: '裁' }],
}
// ★1023 瘦式（X51／X25／X27）：所废——二十余席各读十章（W50 约 $75）、人物之审六席、驳席、认声盲测（去名之器 X25 随之去：瘦式无去名之路）、录册一席抄档（$21）。
//   旧席之问并入四席，⛔丢问（席表见 工具/大审.py）。旧版在 git（cf9e112:工具/席/大审.js）。
const 参 = (typeof args === 'object' && args) ? args : {}
const 缺 = v => v === undefined || v === null || v === ''
const A0 = 参.起 ?? 参.from, B0 = 参.止 ?? 参.to
if (缺(A0) || 缺(B0)) throw new Error(`大审缺参：须传 {起, 止}（今 起=${A0} 止=${B0}）——⛔默认`)
const A = Number(A0), B = Number(B0)
if (!(Number.isInteger(A) && Number.isInteger(B) && A >= 1 && B >= A)) throw new Error(`大审之界不成：起 ${A0} 止 ${B0}`)
const N = B - A + 1
if (参.孤钩 === undefined || 参.孤钩 === null) throw new Error('大审缺参：args.孤钩 须明传（每笔 {id, 注}；无钩则传 []）——⛔默认')
if (!Array.isArray(参.孤钩)) throw new Error('args.孤钩 须为数组')
const 孤钩 = 参.孤钩.map((x, i) => {
  const id = String((Array.isArray(x) ? x[0] : x && x.id) ?? '').trim(), 注 = String((Array.isArray(x) ? x[1] : x && (x.注 ?? x.note)) ?? '').trim()
  if (!id) throw new Error(`args.孤钩 第 ${i + 1} 笔无 id`)
  return { id, 注 }
})
const 包 = `设定/_草/大审${B}/包.md`, 旧笔 = `设定/_草/大审${B}/旧笔.md`

// ★虹吸：四席之令首逐字同（包之读法同、律同），席之职在末——缓存只建一回
const 令头 = `【最高宗旨】把《镇冢秘术》写成中国最好看的小说。本庭是每十章一回之大审（第 ${A}—${B} 章，共 ${N} 章），站在普通读者、顶尖小说家、评委、编辑、类型读者之位，从头到尾看这十章有没有到最高一等。
【工作目录】/home/user/the-novel。
【第一步·唯一之料】用 Read 一次读完 \`${包}\`（allow_large；它含：甲·零 token 诸器之红——机械之病器已逮，⛔你再找；乙·十章白文，每行前为原行号；各章已付之盲读与逻辑审之末判——⛔你重做其已判者）。⛔再逐章开正文、⛔重读全书记忆整档；要核前文某一句，只许 \`grep -n\` 或 \`awk 'NR==L'\` 取那一行。
【三律·缺一其判不算】甲·你说得出你这一席独见之物；乙·不强制出负，强制留痕——无致命即写「本席无致命之判」并写明读了什么；丙·每一笔判落到「章:行」并逐字引原句（照包中行号；⛔凭印象）。
【判之等】fatal＝读者可见之致命（因果断、前後相抵、读错、读者必在此合书）；leap＝改後读者读得出明显更好（大进）；minor＝小瑕。⛔凑数：「微」（撑死多 0.1 分）⛔交。每席至多十二笔，择最要紧者。
【⛔动盘】只读；⛔写任何档、⛔git。
【⛔】凡引一句先亲印核；数目亲手数；据不够就不判。`

const 席 = [
  { k: '连读客', 职: `你是**连读客**（并冷起手之生客、半路进来之生客、评委、类型读者、弃卷席之问）。连读十章，答：①同一个意思在这 ${N} 章里说了几遍——逐处给章:行，判「日课原样」（该留）或真重复（该删）；②逐章一句：到这一章末尾你合上书吗？「合」者给那一拍与其由，「不合」者说是哪一样拽住你；③只读 ${B} 一章的冷读者，读到第几行知道谁在干什么；从 ${Math.max(A, B - 2)} 空降读三章的人，拼得出这三章发生了什么吗；④评委读 ${A} 与 ${B} 之首二十拍，读到哪一行决定放下（给行与原句，并说只改一处能留住他，改哪一处）；⑤冲着这类故事来的人（⛔以书名为尺），这十章给了他什么、欠了他什么。` },
  { k: '小说家', 职: `你是**小说家**（白描、繁复、结构、编辑四路合一）。答：①「意思已尽而字还在」者——逐拍给章:行与原句，并说删掉断什么（断不了才算真该删）；②「看着克制，其实是没东西」者——分清留白（读者补得出）与空（没得补）；③这 ${N} 章哪一章是多的、哪两章可并，并了丢什么；④读者最可能在哪一拍弃书，一拍之内要读者同时记住几样东西——负担最重那三拍；⑤全十章最强的三拍（章:行），够不够得上全书叫绝之拍（\`设定/叫绝之拍库.md\` 只 grep 其目）。` },
  { k: '逻辑闭环', 职: `你是**逻辑闭环席**（立得住、主线、悬念账、复述合一）。可 grep 查：\`设定/canon事实库.json\`、\`设定/01_*\`（圣经·锁定行）、\`设定/到期账.json\`、\`设定/02_余章之势_总纲.md\`、\`设定/全书记忆/第N章.md\`（只 grep 不通读）。答：①逐条列这 ${N} 章里每一个「因为……所以……」之果（人之行止、物之来去、人恰好在场），判其因出自书中既立之律／常理／凑的——凑的、量级不配、前文无迹、人不会这样做的，逐条落章:行并给立得住之改法（改法须是造：入下一段之段案，或已写章之一句器施）；②对 canon 与前文：前後相抵者（日子、数、物之所在、谁知什么）逐条给两处之章:行；③只凭这十章说出书中人在找什么、守什么——说不出即判「线丢」并指最该让线露面之拍；同一意思隔章重出而无新变量者列为绕圈；这一站已用几章、总纲许几章；④悬念账：这十章开了几个、结了几个、悬着几个，读者还记得住否（包甲之悬念哨红者一并判其补法与补於何章）；⑤合上包凭记忆每章复述一句，再对其章之「本章之一事」（全书记忆 grep），差最远者三章给其由。${孤钩.length ? `\n⑥孤钩 ${孤钩.length} 笔：${孤钩.map(x => x.注 ? `${x.id}「${x.注}」` : x.id).join('；')}——逐笔只许兑（给所兑之章 > ${B} 与兑之形）或删（给源头章:行与删法），⛔再冷挂；交入 hooks。` : '\n（本回无孤钩；hooks 交空数组。）'}` },
  { k: '人物', 职: `你是**人物席**（诸人合一席）。先 \`ls 设定/全书记忆/人物链/\`，对这十章出场之人，各 \`grep -F -e '- 〔${A}·' … 〕\` 取其链在本界之条及其前三十条（全程而薄，⛔通读整链），再对包中白文。答：①谁前後不一（言、行、知、口吻）——给两处之章:行；②谁的智在这十章降了（为让情节走而变蠢）——给章:行与其应有之行；③关系之线有断、有跳者；④谁这十章没有一件只属於他的事（成了道具）；⑤人物最强之一拍与最弱之一拍各一。每人至多三笔。` },
]
const 席SCHEMA = { type: 'object', additionalProperties: false, properties: {
  read: { type: 'string' },
  findings: { type: 'array', items: { type: 'object', additionalProperties: false, properties: {
    ch: { type: 'integer' }, beat: { type: 'string' }, quote: { type: 'string' }, issue: { type: 'string' },
    severity: { type: 'string', enum: ['fatal', 'leap', 'minor'] }, fix: { type: 'string' } },
    required: ['ch', 'beat', 'quote', 'issue', 'severity', 'fix'] } },
  hooks: { type: 'array', items: { type: 'object', additionalProperties: false, properties: {
    id: { type: 'string' }, verdict: { type: 'string', enum: ['redeem', 'cut'] }, chapter: { type: 'integer' }, form: { type: 'string' } },
    required: ['id', 'verdict', 'form'] } },
  no_fatal_note: { type: 'string' }, summary: { type: 'string' } },
  required: ['read', 'findings', 'no_fatal_note', 'summary'] }

const 报们 = await parallel(席.map(s => () => agent(`${令头}\n\n【你这一席】${s.职}`,
  { effort: 'high', label: `大审·${s.k}`, phase: '大审', schema: 席SCHEMA })))
const 解 = r => { if (typeof r !== 'string') return r; try { return JSON.parse(r) } catch (e) { return null } }
const 报 = 席.map((s, i) => ({ 席: s.k, r: 解(报们[i]) }))
const 缺席 = 报.filter(x => !x.r).map(x => x.席)
if (缺席.length) log(`⛔未交之席：${缺席.join('、')}——裁席照实记「未交」`)

const 裁SCHEMA = { type: 'object', additionalProperties: false, properties: {
  read: { type: 'string' }, to: { type: 'integer' },
  rows: { type: 'array', items: { type: 'object', additionalProperties: false, properties: {
    judgment: { type: 'string' }, evidence: { type: 'string' },
    ruling: { type: 'string', enum: ['判驳', '判不治', '已挂', '留痕·不裁', '还账'] },
    limit: { type: 'integer' }, to_segment: { type: 'string' }, repay: { type: 'boolean' }, reason: { type: 'string' } },
    required: ['judgment', 'evidence', 'ruling', 'reason'] } },
  carried: { type: 'array', items: { type: 'object', additionalProperties: false, properties: {
    old_no: { type: 'string' }, ruling: { type: 'string' }, limit: { type: 'integer' }, reason: { type: 'string' } },
    required: ['old_no', 'ruling', 'reason'] } },
  verdict_line: { type: 'string' }, to_next_segment: { type: 'array', items: { type: 'string' } } },
  required: ['read', 'to', 'rows', 'carried', 'verdict_line', 'to_next_segment'] }

const 裁 = await agent(`你是大审（第 ${A}—${B} 章）之**裁席**——总编辑之手。⛔重读十章；只读下附四席之报，与 \`${旧笔}\`（上册「已挂」到期之笔）。要核一句只许 \`awk 'NR==L' 正文/<档>\`（档名 \`ls 正文/ | grep -F '_第…章_'\`）。⛔写档、⛔git。
【裁之准·作者令】改只为让书明显更好看：fatal 必治；leap 改；minor 末了集中一回或判不治；「微」⛔改。**出口归造**：凡治法属下一段（409 起）可造者，ruling「已挂」、limit 填 410（或所兑之章）、to_segment 写入段案之一句（「409 段案：……」）；已写章之读者可见致命，ruling「还账」、repay=true、limit 408（器施一单）；四席所判同一事者并为一行；你判其不成者「判驳」带由；无可裁之留痕「留痕·不裁」。
【上册逾限之笔】${旧笔} 逐笔当面裁入 carried（old_no 照其号）：其多挂「W11 之某节（器上）」——W11 未始。照「旧章之改并入 W11 同回、单以器施；⛔为一字开封」之律：仍归 W11 者改限须写新限与其由（W11 起时之章号未定者，限 417 并写「W11 未始·下回大审再面」）；已不值者判不治；所指之器、令已随瘦式废者（如人审令之读列）判不治并写所废。⛔静静顺延。
【verdict_line】一句：这十章合起来，是「慢而深」还是「原地打转」，凭什么。
【to_next_segment】入 409—418 段之剧情庭题与段案之条（每条一句、可照做）。

四席之报（JSON）：
${JSON.stringify(报.map(x => ({ 席: x.席, 报: x.r || '未交' })))}`,
  { effort: 'high', label: '裁', phase: '裁', schema: 裁SCHEMA })
const 裁r = 解(裁)
return { 起: A, 止: B, 席: 报.map(x => ({ 席: x.席, 笔: x.r ? (x.r.findings || []).length : '未交', 致命: x.r ? (x.r.findings || []).filter(f => f.severity === 'fatal').length : 0 })),
  裁: 裁r ? { 行: (裁r.rows || []).length, 还账: (裁r.rows || []).filter(r => r.ruling === '还账').length, 旧笔: (裁r.carried || []).length, 得: 裁r.verdict_line } : '未交',
  录: '跑 python3 工具/大审.py --录 <本 runId> 成册' }
