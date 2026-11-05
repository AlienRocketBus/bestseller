export const meta = {
  name: 'D6升级·续：剧本师与合成',
  description: 'D6 续跑：补剧本师独立设计→两席对抗审→合成席读三案六审、对照总站，写定六审主案（前两案已在盘，不重做）',
  phases: [{ title: '设计' }, { title: '对抗审' }, { title: '合成' }],
}
const 底 = `你在长篇小说仓库 /home/user/the-novel 里。题：剧情庭 D6「床上那人」——暗线闲屋里床上那个人是谁、为何在那里、与全书之因果。
⛔【律⑮·动盘之禁】旁边可能有别的席在写盘——一律不许跑 git checkout／git stash／git reset --hard／git clean／git add -A；要看旧版用 git show HEAD:<路径>。
⭐【律⑳·总编辑之权】凡须裁之事当场照「让这本书更好看」裁定并写明其由，⛔停下等人。
★最高宗旨：中国第一——让这本书成为全中国剧情最好看的小说；做出的每一拍都要配得上这四个字。
★力气花在「造」上：拍案叫绝的点子只能在创造时想出来，审是审不出来的；主力用於从 0 到 1 造出最好的剧情。
★改之铁律：只改好车、垃圾车拆了重造；已写得极好之处原样守住；改就改到瞬间升华。
★写小说三要：剧情完美精彩；逻辑闭环完美且闭得漂亮、令人惊叹；全书连贯。
★一切皆可改：圣经、总纲只是工具，挡路就提议改（写明改哪条、为何更好、逻辑如何连上）；无明令禁止之事（唯「鼎心」一词不用）；设定合本书背景即可（盗墓、风水、古阵、死地之律一路）。
★前车之鉴：二审至六审九轮不过门，病在修补时现编新由。所以凡立一由，先列「同物同时对照表」——该物该时在 正文/ 所有出现处（章:行＋亲印原句），核过无一处相抵才落笔；旧句挡住更好的设计就明写「此句改为……」。
须读：设定/剧情庭_D6_床上那人.md（诸审之裁与诸刺——旧车瑕疵清单）、设定/剧情庭题/D6_床上那人.md、设定/剧情庭题/D6_床上那人_六审主案.md、设定/大升级_总案.md 之 D6 相关条与新事实表、设定/全书记忆/（人物、悬线、逐章详记）、D1/D3/D4/D10 裁档、设定/立得住之律.md、设定/反面教材.md、设定/剧情不合理区.md（只作参考），以及根目录 镇冢秘术_总站.html、人物册_总纲_九站.html、动机图_活路账.html 之设定与剧情背景（与圣经同为工具，好的拿来用）。
⚠防丢：一节写完立即写入仓库内之档，⛔攒到最後、⛔写沙盒暂存目录。`
const 设计式 = { type: 'object', properties: { file: { type: 'string' }, core: { type: 'string' }, why_better: { type: 'string' }, closure_tables: { type: 'number' }, source_edits: { type: 'number' }, bible_edits: { type: 'string' } }, required: ['file', 'core', 'why_better', 'closure_tables', 'source_edits', 'bible_edits'] }
const 审式 = { type: 'object', properties: { fatal: { type: 'array', items: { type: 'string' } }, fixable: { type: 'array', items: { type: 'string' } }, best_parts: { type: 'array', items: { type: 'string' } }, appeal: { type: 'number' }, sound: { type: 'number' } }, required: ['fatal', 'fixable', 'best_parts', 'appeal', 'sound'] }

phase('设计')
const 剧 = await agent(`${底}

你是【剧本师】——全中国最顶尖的剧本结构师，独立设计（不看另外两份设计稿，以免被带偏）。你最看重：结构与揭晓——伏笔怎么埋、何时何物翻、读者何时比沈鸢先懂；每一拍落在物与人上，而不是纸上之账。
不必承接六审主案；可承其骨，也可另造更好的骨——只看哪样最好看、最闭环。
交一份完整的升级设计，分节写入 \`设定/_草/D6_升级/dramatist.md\`：一、一句话之骨；二、全案（人、物、日、数、约，逐项一处定）；三、读者体验（哪一章哪一拍倒吸一口气、为何比现文与前诸审之案都好看）；四、同物同时对照表（每一由一表，亲印原句）；五、正文改处（章:行、改前→改後）；六、圣经改议（若有）；七、自攻：最可能被打的三根刺与已治之法。⛔git add／commit。
返回 file、core（一段）、why_better、closure_tables、source_edits、bible_edits。`, { label: '设计·剧本师', phase: '设计', schema: 设计式, effort: 'max' })

let 剧审 = []
if (剧) {
  phase('对抗审')
  剧审 = (await parallel(['逻辑闭环', '好看'].map(lens => () => agent(`${底}

你是【对抗审·${lens}】，⛔情面。审剧本师之升级设计：\`${剧.file}\`。
${lens === '逻辑闭环' ? '逐条亲印其所引之原句核对；找每一处因果断链、人物前後不一、日子数目对不上、伏笔无收、与全书他处相抵、像现编之由。' : '以全中国最挑的读者之眼：这一案真比现文与前诸审之案好看吗？哪一拍会让人倒吸一口气，哪一拍平、拖、靠纸上之账、像在补坑。'}
fatal：致命之刺（每条附 章:行 与原句）；fixable：可治之刺附治法；best_parts：此案最该保留之长处；appeal、sound 各 0—10。`, { label: `审·剧本师·${lens}`, phase: '对抗审', schema: 审式, effort: 'max' })))).filter(Boolean)
} else {
  log('剧本师又失——以前两案合成（已记）')
}

phase('合成')
const 合 = await agent(`${底}

你是【合成席】（全中国最顶尖的剧情总设计）。三位设计席各自独立做了升级设计，各经逻辑闭环与好看两席对抗审：
- 小说家案：\`设定/_草/D6_升级/novelist.md\`；逻辑闭环师案：\`设定/_草/D6_升级/logician.md\`；二案之核与四席对抗审全文（fatal／fixable／best_parts／分数）在 \`设定/_草/D6_升级/前两案与诸审.json\`——逐条读。
- 剧本师案：${剧 ? JSON.stringify({ 设计: 剧, 审: 剧审 }, null, 1) : '（本回失，以前两案合成）'}
任务：这不是拼补——是在三案之上**再造**出一份完美的升级剧情：择最强之骨，嫁接诸案之长（best_parts），根治每一条 fatal 与 fixable（⛔带进任何未治之致命刺；治每一刺先列同物同时对照表、亲印原句再落笔），并吸收总站里更好的设定与剧情。目标：比现文与前诸审之案都好看得多，逻辑从头到尾完美闭环，而且闭得漂亮、令人叫绝。
分节写成干净本，覆盖 \`设定/剧情庭题/D6_床上那人_六审主案.md\`（旧本在 git 里）：档首写末审之约（无一席列致命刺、立得住均 ≥6、≥2 席判胜方许七审，否则结案守原）；一、一句话之骨；二、定案表（人、物、日、数、约，每事只写一处）；三、读者体验与为何最好看；四、正文改处；五、圣经改议；六、同物同时对照表（附录）；七、取舍记（取了谁之骨、嫁接了谁之长、各刺如何治、总站里吸收了什么）；八、拍案叫绝之处（三到五拍：何章何物、为何叫绝）；九、因果链全表（逐条「因→果」，确认无断）。
然後 git add 本档与 设定/_草/D6_升级/ 之明路径并 commit（说明末两行：Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com> ／ Claude-Session: https://claude.ai/code/session_016Hgfc2SSNvGktFmk2LX825），⛔推。
返回一段：骨、取舍、诸致命刺如何治、拍案叫绝之处、改处数、commit 号。`, { label: '合成', phase: '合成', effort: 'max' })
return { 剧本师: 剧 ? { core: 剧.core, 审: 剧审.map(x => ({ appeal: x.appeal, sound: x.sound, fatal: x.fatal.length })) } : null, 合 }
