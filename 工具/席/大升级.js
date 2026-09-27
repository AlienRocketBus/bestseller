export const meta = {
  name: '大升级',
  description: '全书大升级：式「总」定全书升级总案；式「节」十章一小节——五席独立诊并各出三方、挑刺、复评、过门，三大师重写，行家合稿，验而落（大升级之律·0927）',
  phases: [{ title: '通读' }, { title: '诊与方' }, { title: '挑刺' }, { title: '复评' }, { title: '裁' }, { title: '执' }, { title: '验与落' }],
}
// args: { 式: '总' } 或 { 式: '节', 起: 1, 止: 10 }
const 式 = (args && args.式) || '节'
const 起 = args && args.起, 止 = args && args.止
const 并 = !!(args && args.并行)   // 0927 作者令「全部章节同时进行」：并行之节只出稿，不动正文、不提交；合龙由 式「合」统一办
if (式 === '节' && !(起 && 止)) throw new Error('式节须传 起、止')
const 名 = 式 === '总' ? '总案' : `节_${起}_${止}`

const 底 = `你在长篇小说仓库 /home/user/the-novel 里。正文在 \`正文/\`（文件名含「第某章」之汉字章号），各章之档在 \`版本/第N章/\`。
先读：\`设定/大升级之律.md\`、\`设定/选剧情之律.md\`、\`设定/立得住之律.md\`、\`设定/反面教材.md\`、\`设定/大师画像.md\`（唯一之的、共同之底）、圣经 \`设定/00_镇冢秘术_唯一总圣经.md\` 与总纲 \`设定/02_余章之势_总纲.md\` 之相关段${式 === '节' ? '、`设定/大升级_总案.md`（全书升级总案；若尚未出，则依大升级之律与圣经自定，并於裁档写明所依）' : '、诸大审册 `设定/大审_至第*章.md`、`设定/立得住普查_0927.md`、`设定/二稿账.md`'}。
⛔不考虑书名。⛔一切皆可改、可删、可增；唯一之尺：整本书更好看、立得住。⛔尽全力，完美主义，第一次就想到最好——过得去的不许交（反面教材：老头「守秘密熬老」）。
⛔【律⑮·动盘之禁】旁边可能有别的席在写盘——不许跑 \`git checkout\`／\`git stash\`／\`git reset --hard\`／\`git clean\`／\`git add -A\`；要看改前：\`git show HEAD:<路径>\`。
⭐【律⑳·总编辑之权】不许写「交作者裁」而停下；须裁之事照「书更好看」当场裁并写其由；此权不许用来凑字、造高潮、放宽闸。`

const 读令 = 式 === '总'
  ? '通读全书之纲（圣经、总纲、诸大审册、普查、二稿账）；下附三十八位读者逐字通读全书之逐章诊；你再**亲自逐字读**你所拟改动之处与每一站之头、腰、尾，⛔凭印象判者无效。'
  : `**逐字读完第 ${起}—${止} 章全部正文**（⛔不许扫读），再读第 ${起 - 1 > 0 ? 起 - 1 : 1} 章（已升级者读升级後之文）与第 ${止 + 1} 章之头，知其接缝。`
const 方令 = 式 === '总'
  ? '交**三个全书升级总案**（真不同），每案含：①全书压、删、增、并之处，逐段列章号与压到几章（拖拉、绕圈者重点）；②每站之揭晓与不可回之代价放在哪；③三十八个小节（每十章）各自之升级之的一两句；④新章号之法与何时复写新章（380 起）。每案说明为何比现书更好看、如何立得住、改文之价。'
  : `先诊：逐章逐拍列出写得不好、只是过关、有 bug（逻辑、前後、数目、人物走样）、拖沓之处，引原句（章:行）。再交**三个本节升级方案**（真不同）：可删章、并章、增章、重写某拍、改走向；每案逐章写清改什么、改成什么样，对照现文逐点说读者在哪一刻比原来更放不下、为何立得住、改文之价。`

const 席 = [
  { k: 'novelist', n: '小说家', 身: '全中国最顶尖的小说家', 看: '白描、人物、潜台词、每一拍写得好不好、有没有落俗套' },
  { k: 'editor', n: '总编辑', 身: '一本中国第一的小说之总编辑', 看: '全书之势、揭晓与代价之布局、前後之接、拖沓与绕圈' },
  { k: 'reader', n: '顶尖读者', 身: '读过最多好小说、最挑的读者', 看: '哪里想跳、哪里想合上书、哪里被糊弄、哪里拍桌' },
  { k: 'dramatist', n: '剧本师', 身: '全中国最顶尖的剧本师', 看: '冲突、目标与阻力、转折与代价、高潮是否一步步逼出' },
]
const 方式 = { type: 'object', properties: {
  diagnosis: { type: 'string' },
  current_appeal: { type: 'number' }, current_sound: { type: 'number' },
  plans: { type: 'array', minItems: 3, items: { type: 'object', properties: {
    name: { type: 'string' }, plan: { type: 'string' }, why_better: { type: 'string' },
    soundness: { type: 'string' }, rewrite_cost: { type: 'string' } },
    required: ['name', 'plan', 'why_better', 'soundness'] } } },
  required: ['diagnosis', 'current_appeal', 'current_sound', 'plans'] }

// ★总式：先通读全书——三十八位读者各自逐字读十章，交逐章之诊，供五席定总案（0927 作者令「尽全力、绝对完美」）
let 通读 = []
if (式 === '总') {
  phase('通读')
  const 段 = []
  for (let a = 1; a <= 379; a += 10) 段.push([a, Math.min(a + 9, 379)])
  const 读式 = { type: 'object', properties: {
    block_summary: { type: 'string' },
    chapters: { type: 'array', items: { type: 'object', properties: {
      n: { type: 'number' }, what_happens: { type: 'string' }, strong: { type: 'string' },
      weak: { type: 'string' }, drag: { type: 'string' }, bugs: { type: 'string' },
      verdict: { type: 'string', enum: ['保', '修', '压', '并', '删', '重写'] } },
      required: ['n', 'what_happens', 'weak', 'drag', 'bugs', 'verdict'] } },
    reader_holds: { type: 'string' }, missing: { type: 'string' } },
    required: ['block_summary', 'chapters', 'reader_holds', 'missing'] }
  // 0927 作者令：每十章不许让普通人读——三位顶尖之人各自独立、尽全力逐字读完
  const 读者 = [
    { k: '小说家', 身: '全中国最顶尖的小说家', 看: '手艺：白描、人物、潜台词、每一拍写得好不好、哪句是虚的、哪里落俗套' },
    { k: '评委', 身: '全中国最严的文学评委（评过无数获奖之作）', 看: '全书之势与这十章之位：结构、揭晓与代价、前後是否一丝不乱、有无 bug 与立不住之因、够不够中国第一之标准' },
    { k: '老读者', 身: '实战经验最多的顶尖读者（读过上千部好看的长篇，知道读者在哪一页弃书）', 看: '哪里想跳、哪里想合上书、哪里被糊弄、哪里拍桌、哪里放不下' },
  ]
  const 读 = await parallel(段.flatMap(([a, b]) => 读者.map(r => () => agent(`${底}

你是【${r.身}】（全书大升级·通读·第 ${a}—${b} 章·${r.k}席）。⛔独立：你不知道也不许揣测另两位读者。你看：${r.看}。
⛔**尽全力，逐字读完这 ${b - a + 1} 章全部正文**，不许扫读、不许凭摘要；读的时候就在心里问「这一处配不配放进中国第一的小说里」。
逐章交：发生了什么（两三句）、最好之处（引原句）、写得不好或只是过关之处（引原句）、拖沓与绕圈（同一意思隔章重出者指出）、bug（前後矛盾、数目、人物走样、因立不住——引章:行）、判（保／修／压／并／删／重写）。
再交：读完这十章读者手里握着什么大问（reader_holds）；这十章缺了什么（揭晓、代价、前迹、真拦主角之力）（missing）。
⛔另把你的全部所交（逐章一节、引文照录）写入 \`设定/大升级通读/第${a}-${b}章_${r.k}.md\`（目录不在则建；⛔只写此一档，不 git add）。`, { label: `通读·${a}-${b}·${r.k}`, phase: '通读', schema: 读式, effort: 'max' }).then(x => x && ({ 段: `${a}-${b}`, 席: r.k, ...x })))))
  通读 = 读
  const 失 = 通读.map((r, i) => r ? '' : `${段[Math.floor(i / 3)][0]}-${段[Math.floor(i / 3)][1]}·${读者[i % 3].k}`).filter(Boolean)
  if (失.length) throw new Error('通读有失：' + 失.join('、') + '——⛔不许缺读而定总案')
}
const 通读文 = 式 === '总' ? `\n【全书通读】每十章已由三位顶尖之人（小说家、评委、老读者）各自逐字读毕，逐章之诊在 \`设定/大升级通读/\`（共 ${通读.length} 份，档名 第a-b章_席.md）。⛔**你须把这一百一十四份逐份读完**，再亲自逐字读你所拟改动之处的原文，然後下判。各段一句之要：${JSON.stringify(通读.map(r => ({ 段: r.段, 席: r.席, 要: r.block_summary, 缺: r.missing })))}` : ''

phase('诊与方')
const 一 = await parallel(席.map(s => () => agent(`${底}

你是【${s.身}】（大升级·${s.n}席·${名}）。⛔独立：看不到他席。你看：${s.看}。
${读令}${通读文}
${方令}
给现文打分：好看、立得住（0—10，10＝世界名著之水准）。`, { label: `诊·${s.n}`, phase: '诊与方', schema: 方式, effort: 'max' })))
if (一.some(r => !r)) throw new Error('诊方之席有失——⛔不许以缺席作守原')
const 池 = []
一.forEach((r, i) => r.plans.forEach((p, j) => 池.push({ id: `${席[i].k}${j + 1}`, by: 席[i].n, ...p })))

phase('挑刺')
const 刺 = await parallel(池.map(p => () => agent(`${底}

你是【挑刺王】，⛔不给情面。攻此案（${名}）：
${JSON.stringify(p, null, 1)}
读其所涉之原文与圣经，找它最致命之刺（因果立不立得住、人会不会这样做、与书中之律相抵、前後接缝、它说的「更好」真不真、会不会伤到别的小节）。与已写正文相抵只记改文之价。判级并给治法。`, { label: `刺·${p.id}`, phase: '挑刺', effort: 'max',
  schema: { type: 'object', properties: { flaw: { type: 'string' }, level: { type: 'string', enum: ['致命', '可治', '轻'] }, remedy: { type: 'string' }, better_claim_true: { type: 'string' } }, required: ['flaw', 'level', 'better_claim_true'] } })
  .then(t => ({ ...p, flaw: t }))))
if (刺.some(t => !t)) throw new Error('挑刺之席有失')

phase('复评')
const 评式 = { type: 'object', properties: {
  scores: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, appeal: { type: 'number' }, sound: { type: 'number' }, beats_current: { type: 'boolean' }, reason: { type: 'string' } }, required: ['id', 'appeal', 'sound', 'beats_current', 'reason'] } },
  current_appeal: { type: 'number' }, first_choice: { type: 'string' } }, required: ['scores', 'current_appeal', 'first_choice'] }
const 二 = await parallel([...席, { k: 'critic', n: '挑刺王', 身: '挑刺王' }].map(s => () => agent(`${底}

你是【${s.身}】（大升级·${s.n}席·独立复评·${名}）。⛔只凭案本身，不依出者而偏。
诸案与其刺：
${JSON.stringify(刺, null, 1)}
逐案打分（scores[{id,appeal,sound,beats_current,reason}]、current_appeal、first_choice）：好看、立得住 0—10；致命之刺未治者立得住 ≤4；须真比现文好看且立得住方判 beats_current。`, { label: `复评·${s.n}`, phase: '复评', schema: 评式, effort: 'max' })))
if (二.some(r => !r)) throw new Error('复评之席有失')
const 现均 = 二.reduce((x, r) => x + r.current_appeal, 0) / 二.length
const 计 = 刺.map(a => {
  const ss = 二.map(r => r.scores.find(f => f.id === a.id)).filter(Boolean)
  const 均 = k => ss.reduce((x, f) => x + f[k], 0) / Math.max(1, ss.length)
  return { id: a.id, appeal: 均('appeal'), sound: 均('sound'), wins: ss.filter(f => f.beats_current).length, n: ss.length }
})
const 可 = 计.filter(c => c.sound >= 7 && c.appeal - 现均 >= 1 && c.wins * 2 > c.n).sort((a, b) => b.appeal - a.appeal)
log(`${名}：现文好看均 ${现均.toFixed(1)}；过门 ${可.map(c => c.id).join('、') || '无（只修 bug，不改走向）'}`)

phase('裁')
const 裁档 = 式 === '总' ? '设定/大升级_总案.md' : `设定/大升级_${名}.md`
const 圣经令 = 并
  ? '⛔并行之节：⛔不改圣经、⛔不 git add／commit；本节所改之设定写在裁档「## 待入圣经」一节，由合龙统一落。'
  : `⛔随裁即改圣经（圣经随裁）：以 \`python3 工具/改单.py --立 …\` 立改单，把${式 === '总' ? '总案之要写进圣经与总纲（总纲之章数图照总案重排）' : '本节所改之设定写进圣经'}，写「据 大升级_${名}」；无设定之变者於档中写「圣经无改」及其由。git add 明路径并 commit（末两行：Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com> ／ Claude-Session: https://claude.ai/code/session_016Hgfc2SSNvGktFmk2LX825），⛔不推。`
const 裁 = await agent(`${底}

你是大升级之裁席（总编辑，兼听挑刺王）。${名}。
【诸席诊与方】${JSON.stringify(一, null, 1)}
【诸案与刺】${JSON.stringify(刺, null, 1)}
【复评】${JSON.stringify(二, null, 1)}
【机械之计】现文好看均 ${现均.toFixed(2)}；${JSON.stringify(计)}；过门者：${JSON.stringify(可.map(c => c.id))}
⛔过门者无：裁「走向守原」，但诸席诊出之 bug、只过关处、拖沓处（逐条落到章:行）仍全数列为必修。过门者有：只能在其中择一（可嫁接他案之长，不带进未治之刺）。
写 \`${裁档}\`：一、裁定之案（${式 === '总' ? '全书压删增并之处逐段、各站揭晓与代价、三十八小节之的、新章号之法、何时复写新章' : '逐章：删／并／增／重写哪几拍、改成什么样，写到三位执笔照着就能写的细'}）；二、为何它最好看（对照现文与落选诸案）；三、刺之治；四、必修之 bug 清单（章:行）；五、分数表。
${圣经令}返回：裁定之要（一段）＋本节要重写之章号列表（JSON 数组，如 [3,5,7]；总式返回 []）。`, { label: '裁', phase: '裁', effort: 'max',
  schema: { type: 'object', properties: { summary: { type: 'string' }, chapters: { type: 'array', items: { type: 'number' } } }, required: ['summary', 'chapters'] } })
if (!裁) throw new Error('裁席有失')
if (式 === '总') return { 名, 过门: 可, 现均, 裁 }

phase('执')
const 执果 = []
for (const n of 裁.chapters) {   // ⛔逐章依次：後章须接前章已升级之文
  const 稿 = await parallel(['甲', '乙', '丙'].map(x => () => agent(`${底}

你是执笔·${x}（读 \`设定/大师画像.md\` 之「执笔·${x}」一节，那就是你）。照 \`${裁档}\` 之裁，**重写第 ${n} 章**（若裁为「增章」则新写）。先读：原第 ${n} 章全文、其前一章（已升级者读新文）与後一章、\`设定/大师进化账.md\` 末 30 条。
先写构思 \`版本/第${n}章/大升级_起草_${x}_构思.md\`（含「满分之问」：最重那一拍想过的三条路、为何所取最好）；再写全章于 \`版本/第${n}章/大升级_起草_${x}.md\`。⛔尽全力，代表作之水准；⛔不许为过闸而写。返回稿之路径与一句自评。`, { label: `执·${n}·${x}`, phase: '执', effort: 'max' })))
  const 合 = await agent(`${底}

你是本章之合稿席，兼请两位行家（读 \`设定/大师画像.md\` 之「行家·小说家」「行家·总编辑」）。第 ${n} 章三稿：版本/第${n}章/大升级_起草_{甲,乙,丙}.md（执笔回报：${JSON.stringify(稿)}）。
①以两位行家之眼逐字读三稿，写 \`版本/第${n}章/大升级_行家评.md\`（八项加「立得住」逐稿打分、好坏引原句、改法给改後之句、「反面教材又犯」点名）；②择最好一稿为底，嫁接他稿之长，逐条办行家之改法（写「## 合稿逐条回话」）；${并 ? '③新文写入 \`版本/第${n}章/大升级稿.md\`（⛔并行之节不动 \`正文/\`，由合龙统一替换；章名若改，写在稿首一行「章名：……」）；' : '③把原正文存为 \`版本/第${n}章/大升级前.md\`，新文写回 \`正文/\` 该章之档（章名可改，改则同步改档名并记 \`设定/大升级_章号对照.md\`）；'}④跑 \`python3 工具/硬闸.py\`（本章${并 ? '，对大升级稿' : ''}）并治红（照反面教材，不缝补）。返回：所取之底、嫁接何处、硬闸结果。`, { label: `合·${n}`, phase: '执', effort: 'max' })
  执果.push({ n, 合 })
}

phase('验与落')
if (并) {
  const 验并 = await agent(`${底}

你是本节之验席（并行之节）。第 ${起}—${止} 章已依 \`${裁档}\` 出新稿于 版本/第N章/大升级稿.md（${JSON.stringify(执果)}）。以总编辑之眼逐字读完本节新稿（未重写之章读原文），查前後、数目、人物、立得住、canon；有伤当场改稿（照反面教材，改到最好）。⛔不动 正文/、⛔不 git add／commit。把验之所得与本节首尾两章之接缝要点写进裁档末「## 验与接缝」（供合龙用）。返回所验之伤与所治。`, { label: '验·并行', phase: '验与落', effort: 'max' })
  return { 名, 过门: 可, 现均, 裁: 裁.summary, 重写: 裁.chapters, 验: 验并 }
}
const 验 = await agent(`${底}

你是本节之验与落席。第 ${起}—${止} 章已依 \`${裁档}\` 重写（${JSON.stringify(执果)}）。
①以总编辑之眼逐字读完本节新文与前後接缝：前後、数目、人物、立得住、canon 皆须过；有伤当场治（照反面教材，改到最好）；
②跑 \`python3 工具/同步全本阅读器.py\`、\`python3 工具/全测.py\`，逐红治根（⛔不许放宽闸、⛔不许 ZM_SKIP_HOOK／--no-verify）；
③把本节之改记入改单（\`python3 工具/改单.py --立 "大升级·${名}" "……" 诸档\`，提交後 \`--毕\`）；
④git add 明路径并 commit（末两行同前），然後 \`git push -u origin claude/the-novel-review-4dtuit\`。
返回：所验之伤与所治、全测结果、推没推。`, { label: '验与落', phase: '验与落', effort: 'max' })
return { 名, 过门: 可, 现均, 裁: 裁.summary, 重写: 裁.chapters, 验 }
