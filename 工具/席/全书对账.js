export const meta = {
  name: '全书对账',
  description: '一份剧情主案对全书正文逐物逐人逐日对账：分组各席 grep 正文全数、逐处核与主案相抵否，交相抵清单（永远的痛之教：完备之查代替撞运气之挑刺）',
  phases: [{ title: '对账' }, { title: '汇' }],
}
// 用法：Workflow({scriptPath:'工具/席/全书对账.js', args:{案:'设定/剧情庭题/X_主案.md', 题:'X', 出:'设定/_草/X_对账', 组:[{k:'a', n:'组名', 管:'R1、W2……与其物之词'}]}})
const A = args || {}
if (!A.案 || !A.组 || !A.组.length || !A.出) throw new Error('args 须有 案、组、出')
const 底 = `你在长篇小说仓库 /home/user/the-novel 里。
★★★两大铁律（先读这两条，再读其他）：①中国第一——让本书成为中国第一的小说；②剧情全中国最好看、剧情与逻辑闭环绝对完美（每果有因、每因有果、每伏笔有收、每人前後一致、全书无一处相抵，而且闭得漂亮）。
★★★质量永不妥协（1008 作者令）：无论做什么事都⛔牺牲本书质量；⛔为收工、为省时降标准；一个方法不行就换一个，总有好方法，⛔固步自封。
★★★虫洞之律（开发方法之第一法则；一切机制随时进化，⛔一成不变）：先找直通之法——效果更好、花费更少，两样都满足才用；⛔笨办法（堆人、堆轮、反复通读、开放式挑刺）。
★★★改之准（1008 作者令）：逼近 100 靠造不靠改——目的一气呵成，第一稿就用全力写出最好的；改只为让书明显更好看：致命（因果断、前後相抵、读者必见之漏）必改｜大进（改後某一拍读者读得出明显更好，须并排引改前改後、说出好在哪）方改｜小瑕末了集中修一回｜微（撑死多 0.1 分）与改後可能更差者⛔改（资源内耗）。
★★★永远的痛（D6 将近四十小时无果）：挑刺式之审撞运气、永不收敛。本席是**完备之查**：不凭印象找毛病，而是把该管之物在正文里**全数**查出来，一行一行核，一行不漏。
⛔【律⑮·动盘之禁】你在跑之时，旁边可能还有别的席、别的器正在写盘——一律不许跑动整个工作区的命令：\`git checkout\`（含 \`checkout .\`／\`checkout -- 档\`）／\`git stash\`／\`git reset --hard\`／\`git clean\`／\`git add -A\`。要看改前改後：\`git show HEAD:<路径> > /tmp/旧.md\` 再比。
⭐【律⑳·总编辑之权】⛔不许写「交作者裁」「待作者定」「报作者」而停下——凡须判之事，照「让这本书更好看、更闭环」当场判定并写明其由；⛔此权只朝书更好看一个方向用。
⛔改主案、⛔改正文、⛔git add／commit——本席只查只报，改由总编辑一次在源头做。中间稿写在仓库内 \`${A.出}/\`，一节一落盘，⛔写沙盒暂存目录。`
const 式 = { type: 'object', properties: {
  file: { type: 'string' },
  words: { type: 'array', items: { type: 'string' } },
  hits: { type: 'number' },
  conflicts: { type: 'array', items: { type: 'object', properties: {
    where: { type: 'string' }, quote: { type: 'string' }, key: { type: 'string' },
    level: { type: 'string', enum: ['致命', '可治', '轻'] }, fix: { type: 'string' } },
    required: ['where', 'quote', 'key', 'level', 'fix'] } },
  unhandled: { type: 'number' },
}, required: ['file', 'words', 'hits', 'conflicts', 'unhandled'] }

phase('对账')
const 报 = await parallel(A.组.map(g => () => agent(`${底}

你是【全书对账·${g.n}】。主案：\`${A.案}\`（${A.题 || ''}）。你管：${g.管}。
做法（逐步，⛔跳）：
1. 读主案之定案表（人、物、日、数、约）与 G 号改处、⛔动之句，把你所管各键之定逐条抄下。
2. 列出你所管诸物、诸人、诸日在正文里可能出现之一切说法（本名、别称、代称、数目之写法；宁多勿漏），逐词 \`grep -n\` \`正文/\` 全书，记每词命中数。
3. 命中之行逐行核（每行亲印原句；必要时读其上下文以定主语与日子）：此行照主案执笔後，与主案之定相抵否？——若主案之 G 号要改此行，核其新文与他键相抵否；若主案未提此行而与之相抵，记为「未处之行」。
4. 写入 \`${A.出}/对账_${g.k}.md\`：一、所管之键与其定；二、词与命中数；三、相抵清单（章:行、原句、所抵之键、级、治法——治法须写到「删」或「改作某句」，⛔写「须斟酌」）；四、核过无抵之行数。
返回 file、words、hits（总命中行数）、conflicts（全部相抵，级：致命＝照执则全书某处塌、读者必见；可治；轻）、unhandled（未处之行数）。`, { label: `对账·${g.n}`, phase: '对账', schema: 式 })))

phase('汇')
const 有 = 报.filter(Boolean)
const 汇 = {
  组: 有.map((r, i) => ({ 组: A.组[i] && A.组[i].n, file: r.file, hits: r.hits, 抵: r.conflicts.length, 致命: r.conflicts.filter(c => c.level === '致命').length, unhandled: r.unhandled })),
  诸抵: 有.flatMap(r => r.conflicts),
}
if (有.length < A.组.length) log(`⚠ ${A.组.length - 有.length} 组无报（席失）——须补跑，⛔当作已核`)
return 汇
