export const meta = {
  name: '剧情庭',
  description: '剧情庭：小说家、总编辑、顶尖读者、剧本师、挑刺王独立各出三案，默认守原，唯确更好看方改（选剧情之律·0927）',
  phases: [{ title: '独立出案' }, { title: '挑刺' }, { title: '独立复评' }, { title: '裁' }],
}
// args: { 题: 题档路径, 名: 输出名, 式: '改'（审既定剧情，默认守原）|'新'（想下一步走向） }
const 题 = args && args.题
const 名 = (args && args.名) || 'untitled'
const 式 = (args && args.式) || '改'
if (!题) throw new Error('须传 args.题')

const 底 = `你在长篇小说仓库 /home/user/the-novel 里。先读：
- 设定/选剧情之律.md（⛔唯一之尺：哪一个让整本书更好看；已写之文不是否决之由，只记改文之价）
- 设定/立得住之律.md（立不住的不用）
- 设定/大师画像.md「唯一之的」
- 题档 ${题}；并按题档所指读圣经 设定/00_镇冢秘术_唯一总圣经.md 相关段、相关章正文（版本/第N章/），⛔凭印象判者无效
⛔不考虑书名。
⛔尽全力：绞尽脑汁把这一处想到最好——不是交差，是要放进中国第一的小说里。`

const 守原 = 式 === '改'
  ? `【⛔守原之律】既定剧情默认不改。你若认为「现文」已是最好，直说「守原」并说明为何。你若要改，每一案都须给出**详细之逻辑与方案**：改在哪、改後怎么走、为何比现文更好看（对照现文逐点说：读者在哪一刻比原来更放不下、更震、更信），以及立得住之据与改文之价。⛔说不出比现文更好在哪的案，不许交。⛔不为改而改。`
  : `【出新之律】这是要新想的剧情。你须独立想出**三个**最好的走向，各自写成可照着写的方案（起、转、落、人物之所为与其由、给读者的那一下），并说明为何好看、如何立得住。三案须真不同，不许一案三变。`

const 席 = [
  { k: '小说家', 身: '全中国最顶尖的小说家', 看: '能写出多好看的场面、人物能不能因此立起来、有没有落俗套' },
  { k: '总编辑', 身: '一本中国第一的小说之总编辑', 看: '全书之势、揭晓之序与分量、每站之代价、前後之接、改文之价值不值' },
  { k: '顶尖读者', 身: '读过最多好小说、最挑的读者', 看: '会不会放不下、会不会拍桌、会不会觉得被糊弄' },
  { k: '剧本师', 身: '全中国最顶尖的剧本师（结构与戏剧性之大师）', 看: '戏剧冲突够不够、人物目标与阻力、每一场之转折与代价、高潮是否由前面一步步逼出' },
]

const 案式 = { type: 'object', properties: {
  判现文: { type: 'string' }, 现文好看: { type: 'number' }, 现文立得住: { type: 'number' },
  守原: { type: 'boolean' }, 守原之由: { type: 'string' },
  案: { type: 'array', items: { type: 'object', properties: {
    名: { type: 'string' }, 方案: { type: 'string' }, 为何比现文更好: { type: 'string' },
    立得住之据: { type: 'string' }, 改文之价: { type: 'string' } },
    required: ['名', '方案', '为何比现文更好', '立得住之据'] } } },
  required: ['判现文', '现文好看', '现文立得住', '守原', '案'] }

phase('独立出案')
const 一 = await parallel(席.map(s => () => agent(`${底}

你是【${s.身}】（剧情庭·${s.k}席）。⛔独立：你看不到也不许揣测他席。你看：${s.看}。
先判「现文」（题档所列之现行剧情；若是新想之题，则判题档所列之既定方向）：好看、立得住各 0—10，长短。
${守原}
${式 === '改' ? '若要改，最多三案，每案都须过上面之律。' : ''}`, { label: `出案·${s.k}`, phase: '独立出案', schema: 案式, effort: 'max' })))
const 池 = []
一.forEach((r, i) => { if (r) (r.案 || []).forEach((a, j) => 池.push({ id: `${席[i].k}${j + 1}`, 出: 席[i].k, ...a })) })
const 守原数 = 一.filter(r => r && r.守原).length
log(`出案 ${池.length} 个；守原 ${守原数} 席`)

if (!池.length) {
  const 裁 = await agent(`${底}\n四席皆守原：${JSON.stringify(一)}\n写 \`设定/剧情庭_${名}.md\`：裁「守原」，列四席之判与由。git add 该档并 commit（末两行：\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_016Hgfc2SSNvGktFmk2LX825），⛔不推。返回一句摘要。`, { label: '裁·守原', phase: '裁' })
  return { 题, 结: '守原', 裁 }
}

phase('挑刺')
const 刺 = await parallel(池.map(a => () => agent(`${底}

你是【挑刺王】，专挑逻辑与剧情之刺，⛔不给情面。攻这一案：
${JSON.stringify(a, null, 1)}
找出它最致命的刺（因果立不立得住、人会不会这样做、读者会问的「他为什么不……」、与书中之律相抵、它说的「比现文更好」是不是真的）。⛔与已写正文相抵不算刺，只记改文之价。判：致命／可治／轻；可治者给治法。`, { label: `刺·${a.id}`, phase: '挑刺', effort: 'max',
  schema: { type: 'object', properties: { 刺: { type: 'string' }, 级: { type: 'string', enum: ['致命', '可治', '轻'] }, 治法: { type: 'string' }, 更好之说真否: { type: 'string' } }, required: ['刺', '级', '更好之说真否'] } })
  .then(t => ({ ...a, 刺: t }))))
const 池刺 = 刺.filter(Boolean)

phase('独立复评')
const 评式 = { type: 'object', properties: {
  分: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, 好看: { type: 'number' }, 立得住: { type: 'number' }, 胜现文否: { type: 'boolean' }, 由: { type: 'string' } }, required: ['id', '好看', '立得住', '胜现文否', '由'] } },
  现文好看: { type: 'number' }, 首选: { type: 'string' } }, required: ['分', '现文好看', '首选'] }
const 二 = await parallel([...席, { k: '挑刺王', 身: '挑刺王' }].map(s => () => agent(`${底}

你是【${s.身}】（剧情庭·${s.k}席·独立复评）。⛔不许看作者姓名、不许依谁出的案而偏；只凭案本身。
池中诸案（含挑刺王之刺）：
${JSON.stringify(池刺, null, 1)}
逐案打分：好看、立得住（0—10；有致命之刺未治者立得住 ≤4）；判它胜不胜现文（须真比现文更好看且立得住，才判胜）。再给现文好看之分，与你的首选（案 id，或「现文」）。`, { label: `复评·${s.k}`, phase: '独立复评', schema: 评式, effort: 'max' })))

// 机械之选：守原为默认。一案须 立得住均≥7、好看均高於现文均≥1、过半席判胜现文，方得入裁
const 评 = 二.filter(Boolean)
const 现均 = 评.reduce((x, r) => x + r.现文好看, 0) / Math.max(1, 评.length)
const 计 = 池刺.map(a => {
  const ss = 评.map(r => r.分.find(f => f.id === a.id)).filter(Boolean)
  const 均 = k => ss.reduce((x, f) => x + f[k], 0) / Math.max(1, ss.length)
  return { id: a.id, 好看: 均('好看'), 立得住: 均('立得住'), 胜票: ss.filter(f => f.胜现文否).length, 席数: ss.length }
})
const 可 = 计.filter(c => c.立得住 >= 7 && c.好看 - 现均 >= 1 && c.胜票 * 2 > c.席数).sort((a, b) => b.好看 - a.好看)
log(`现文好看均 ${现均.toFixed(1)}；过门之案 ${可.map(c => c.id).join('、') || '无'}`)

phase('裁')
const 裁 = await agent(`${底}

你是剧情庭之裁席。材料：
【诸席独立出案】${JSON.stringify(一, null, 1)}
【池与刺】${JSON.stringify(池刺, null, 1)}
【独立复评】${JSON.stringify(评, null, 1)}
【机械之计】现文好看均 ${现均.toFixed(2)}；诸案 ${JSON.stringify(计)}；过门者（立得住均≥7、好看均高现文≥1、过半判胜）：${JSON.stringify(可.map(c => c.id))}
⛔过门者无，则裁「守原」（可吸收诸案里不改剧情走向之小长处，须逐条说明）。过门者有，只能在过门者中择一（可嫁接他案之长，但不得带进未治之刺）。
写 \`设定/剧情庭_${名}.md\`：一、裁定（守原，或所择之案写到能照着改圣经与正文的细）；二、为何它比现文与落选诸案更好看（逐一对照）；三、挑刺王之刺如何治；四、改文之价（改哪几章何处）；五、分数表与各席首选。
git add 该档（明路径）并 commit（末两行：
Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_016Hgfc2SSNvGktFmk2LX825），⛔不推。返回摘要一段。`, { label: '裁', phase: '裁', effort: 'max' })
return { 题, 过门: 可, 现均, 裁 }
