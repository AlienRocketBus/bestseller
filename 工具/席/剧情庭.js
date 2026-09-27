export const meta = {
  name: '剧情庭',
  description: '剧情庭：小说家、总编辑、顶尖读者、挑刺王四席三轮，择最好看而立得住之剧情（选剧情之律·0927）',
  phases: [{ title: '独立评与提案' }, { title: '挑刺与复评' }, { title: '裁' }],
}
// args: { 题: '设定/剧情庭题/xxx.md', 名: 'xxx' }
const 题 = args && args.题
const 名 = (args && args.名) || 'untitled'
if (!题) throw new Error('须传 args.题（题档路径）')

const 底 = `你在长篇小说仓库 /home/user/the-novel 里。先读：
- 设定/选剧情之律.md（⛔唯一之尺：哪一个让整本书更好看；已写之文不是否决之由，只记「改文之价」；过得去不够）
- 设定/立得住之律.md（立不住的不用；而「和已写的对不上」不等於立不住）
- 设定/大师画像.md 之「唯一之的」
- 题档 ${题}（本回要裁之事与诸方案，含「现文」一案）
- 按题档所指，读圣经 设定/00_镇冢秘术_唯一总圣经.md 之相关段与相关章之正文（正文在 版本/第N章/ 或题档所指处），⛔凭印象判者无效
⛔不考虑书名（裁_0927_书名不绑正文）。尽全力：这是要放进中国第一的小说里的剧情。`

const 席 = [
  { k: '小说家', 身: '全中国最顶尖的小说家', 看: '这个剧情能写出多好看的场面；人物能不能因此立起来、有没有让人心口一紧的那一刻；有没有落俗套' },
  { k: '总编辑', 身: '一本中国第一的小说之总编辑', 看: '全书之势：揭晓的次序与分量、每站之代价、前後之接、读者手里握着的问题够不够大；改文之价值不值' },
  { k: '顶尖读者', 身: '读过最多好小说、最挑的读者（⛔不读说明文字以外的作者意图，只凭读者之感）', 看: '我会不会放不下、会不会到那一章拍桌、会不会觉得被糊弄、会不会骂作者' },
  { k: '挑刺王', 身: '专挑逻辑与剧情之刺的挑刺王，⛔不给任何方案情面', 看: '每一个方案最致命的刺：因立不立得住、人会不会这样做、读者会问的「他为什么不……」、与书中之律相抵处（与已写之文相抵只记改文之价，⛔不当致命）' },
]

const 评式 = { type: 'object', properties: {
  诸案: { type: 'array', items: { type: 'object', properties: {
    案: { type: 'string' }, 好看: { type: 'number' }, 立得住: { type: 'number' },
    长: { type: 'string' }, 短: { type: 'string' }, 最致命之刺: { type: 'string' }, 改文之价: { type: 'string' } },
    required: ['案', '好看', '立得住', '长', '短'] } },
  新提: { type: 'array', items: { type: 'object', properties: {
    名: { type: 'string' }, 内容: { type: 'string' }, 为何更好看: { type: 'string' }, 如何立得住: { type: 'string' }, 改文之价: { type: 'string' } },
    required: ['名', '内容', '为何更好看', '如何立得住'] } },
  想过而弃之路: { type: 'string' },
  首选: { type: 'string' }, 由: { type: 'string' } },
  required: ['诸案', '新提', '首选', '由'] }

phase('独立评与提案')
const 一 = (await parallel(席.map(s => () => agent(`${底}

你是【${s.身}】（剧情庭·${s.k}席）。你独立判，⛔不与他席商量。
你看：${s.看}。
①对题档中每一个方案（含「现文」）评：好看 0—10、立得住 0—10（10＝放进中国第一的小说里毫无愧色；拿不准往低打），各写长、短、最致命之刺、改文之价（只作价，不作否决）。
②⛔**必须提案**：绞尽脑汁想出至少一个比诸案都更好看、且立得住的方案（可嫁接诸案之长），写清内容、为何更好看、如何立得住、改文之价。想不出更好的，在「想过而弃之路」里写明想过哪几条、为何不如。
③给出你的首选与由。`, { label: `一·${s.k}`, phase: '独立评与提案', schema: 评式, effort: 'max' })))).filter(Boolean)

const 汇一 = JSON.stringify(一.map((r, i) => ({ 席: 席[i] ? 席[i].k : i, ...r })), null, 1)

phase('挑刺与复评')
const 刺式 = { type: 'object', properties: {
  逐案之刺: { type: 'array', items: { type: 'object', properties: {
    案: { type: 'string' }, 致命之刺: { type: 'string' }, 可治否: { type: 'string' }, 治法: { type: 'string' } },
    required: ['案', '致命之刺', '可治否'] } } }, required: ['逐案之刺'] }
const 刺 = await parallel(['逻辑与因果', '人物与动机', '全书前後与揭晓'].map(角 => () => agent(`${底}

你是【挑刺王】，本回只从「${角}」一角下刀。下面是第一轮四席之评与所有新提之案（JSON）：
${汇一}

把题档原案与所有新提之案合为一池，逐案找出它从「${角}」看最致命的一根刺；并判此刺可治否、治法（治法须让它更好看，不是只圆上）。⛔与已写正文相抵不算刺，只记改文之价。`, { label: `刺·${角}`, phase: '挑刺与复评', schema: 刺式, effort: 'max' })))

const 汇刺 = JSON.stringify(刺.filter(Boolean), null, 1)
const 二 = (await parallel(席.filter(s => s.k !== '挑刺王').map(s => () => agent(`${底}

你是【${s.身}】（剧情庭·${s.k}席·复评）。第一轮诸席之评与新提：
${汇一}
挑刺王三角之刺：
${汇刺}

据刺复评：①池中每案重打好看、立得住；②把你认为最强之一案改良到治好其刺、且更好看——写进「新提」（名以「良·」起头）；③给首选与由。`, { label: `二·${s.k}`, phase: '挑刺与复评', schema: 评式, effort: 'max' })))).filter(Boolean)

phase('裁')
const 裁 = await agent(`${底}

你是剧情庭之裁席（一本中国第一的小说之总编辑，兼听挑刺王）。三份材料：
【第一轮】${汇一}
【挑刺】${汇刺}
【复评】${JSON.stringify(二, null, 1)}

择一个**最好看而立得住**之案（可嫁接诸案之长），⛔不许以「已写之文」为否决之由，改文之价只作掂量；⛔不许取「过得去」之案而舍更好看者。
写 \`设定/剧情庭_${名}.md\`，含：
一、裁定之案（写到能照着改圣经与正文的细）；
二、为何它最好看（对比落选诸案，逐一说输在哪）；
三、挑刺王之刺逐条如何治；
四、改文之价（改哪几章、何处，另列入 设定/二稿账.md 之草）；
五、诸席分数表与分歧。
写毕 git add 该档（明路径）并 commit（说明末两行：
Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_016Hgfc2SSNvGktFmk2LX825），⛔不推。返回裁定一段话之摘要。`, { label: '裁', phase: '裁', effort: 'max' })
return { 题, 裁 }
