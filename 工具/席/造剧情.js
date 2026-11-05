export const meta = {
  name: '造剧情',
  description: '三位设计席（小说家／剧本师／逻辑闭环师）各自独立、带料造一份剧情总案（虫洞之的：省下之力全投造剧情），交总编辑亲合',
  phases: [{ title: '造' }],
}
// 用法：Workflow({scriptPath:'工具/席/造剧情.js', args:{题:'余章总案', 料:'设定/_草/余章/料.md', 出:'设定/_草/余章', 读:['设定/02_余章之势_总纲.md:290-915', '设定/02_全书之约_逐站事数表.md'], 令:'（本题之所须，见下）'}})
// 1008 立（W17）：D3 已证之法——料包零 token、多席独立造→总编辑亲合→预筛→只判所留。本器只办「造」一步。
const A = args || {}
if (!A.题 || !A.料 || !A.出 || !A.令) throw new Error('args 须有 题、料、出、令')
const 读 = (A.读 || []).map(x => `\`${x}\``).join('、')
const 底 = `你在长篇小说仓库 /home/user/the-novel 里。
★★★两大铁律（先读这两条，再读其他）：①中国第一——让本书成为中国第一的小说；②剧情全中国最好看、剧情与逻辑闭环绝对完美（每果有因、每因有果、每伏笔有收、每人前後一致、全书无一处相抵，而且闭得漂亮）。
★★★质量永不妥协：⛔为收工、为省时降标准。
★★★虫洞之的（1008 作者令）：虫洞只为让本书成为中国第一——省下之力全数投到造剧情。**你就是那份力投下去的地方**：本席是造剧情之席，要造出剧情非常非常精彩、逻辑非常非常缜密、读者绝对上瘾的案。
★★★造时即满分（永远的痛之教）：造出来就要挑不出毛病——⛔留「待定」「再议」「後补」；每一拍落到物、落到章、落到谁的手。造出垃圾，後面怎么修都修不好。
★★★叫绝之拍（方法之律⑥）：每站列三至五拍，逐拍与全书最强之拍对标——「斗沿那一圈牙印」「东头『我没应』」「那年我十五。我在你後头出来的。」「档里没写。」——够不上者删了重想，⛔凑数。
★★★唯一不改之事：本书是中国第一的小说，剧情必须是 100 分；此外一切皆可改，一切只服务让它成为中国最好看的小说。
★★★名著是写出来的，不是改出来的：一出手就造到 100 分（⛔指望後面去改）；改之准——致命必改、大进方改、微⛔改。
★★★对标叫绝之拍库：动笔前读 \`设定/叫绝之拍库.md\`（全书最强四十拍与「十条手艺」），你所列每一拍逐拍对着它造。
⛔【律⑮·动盘之禁】你在跑之时，旁边可能还有别的席、别的器正在写盘——一律不许跑动整个工作区的命令：\`git checkout\`（含 \`checkout .\`／\`checkout -- 档\`）／\`git stash\`／\`git reset --hard\`／\`git clean\`／\`git add -A\`。要看改前改後：\`git show HEAD:<路径> > /tmp/旧.md\` 再比。
⭐【律⑳·总编辑之权】⛔不许写「交作者裁」「待作者定」「报作者」而停下——凡须判之事，照「让这本书更好看、更闭环」当场判定并写明其由；⛔此权只朝书更好看一个方向用。
⛔改圣经、⛔改正文、⛔改总纲、⛔git add／commit——本席只造设计稿，改由总编辑合成後一次在源头做。
【读之界（坑之账②③④⑧：token 花在「找」上是笨办法）】先通读料包 \`${A.料}\`；再读 ${读 || '（无）'}（带行号区间者只读其区间，用 \`sed -n\`）。正文只许 \`grep -n\` 定点、每处只读上下各三行（\`sed -n 'a,bp'\`）；⛔通读正文整章、⛔通读圣经（2.9MB，只许 grep）。全程读入以约 25 万 token 为限。
【写之界】设计稿写在 \`${A.出}/<你的席名>.md\`，**一节一落盘**（写完一节即存，断了可续）；全档 ≤30KB——短而准，⛔铺陈。`
const 席们 = [
  { k: 'novelist', n: '小说家', 镜: '好看与上瘾：人物之欲与痛、每一拍的情感之刀、一句话的分量、读者哪一页放不下；文字之下的那一层（不说破之力）。' },
  { k: 'dramatist', n: '剧本师', 镜: '结构与节奏：每站一揭一价一由一安、悬念之分配与读者知之阶、章末之钩、高低起伏、主暗两线之交替与汇合、终局之势如何一步步收紧。' },
  { k: 'logician', n: '逻辑闭环师', 镜: '因果与闭环：每一事之因、每一物之去向、每一人每一站知什么不知什么、日子与数、每一条悬线之收、与已写正文与已裁之定无一处相抵。' },
]
const 式 = { type: 'object', properties: {   // ⚠ schema 之键须 ASCII（1008 首跑三席皆 400 而死）
  file: { type: 'string' },
  spine: { type: 'string' },
  beats: { type: 'array', items: { type: 'object', properties: { station: { type: 'string' }, chapter: { type: 'string' }, beat: { type: 'string' } }, required: ['station', 'chapter', 'beat'] } },
  threads: { type: 'object', properties: { rows: { type: 'number' }, pinned: { type: 'number' }, nofill: { type: 'number' }, unpinned: { type: 'number' } }, required: ['rows', 'pinned', 'nofill', 'unpinned'] },
  appeal: { type: 'number' },
  weakest: { type: 'array', items: { type: 'string' } },
}, required: ['file', 'spine', 'beats', 'threads', 'appeal', 'weakest'] }

phase('造')
const 报 = await parallel(席们.map(s => () => agent(`${底}

你是【造剧情·${s.n}席】，题：${A.题}。你的镜头：${s.镜}（镜头只定你看得最深的那一面；案须全，三席各自独立造整案，⛔只交一面。）
${A.令}
返回：file（你的设计稿路径）、spine（你这一案的一句话之骨）、beats（全部叫绝之拍：station 站、chapter 章、beat 拍一句）、threads（rows 悬线行数、pinned 已钉、nofill ⛔不补、unpinned 未钉余）、appeal（自评好看 0—10，照全书最强之拍对标，⛔虚高）、weakest（你自攻出的最弱三处与其治，各一句）。`, { label: `造·${s.n}`, phase: '造', schema: 式, effort: 'max' })))

const 有 = 报.filter(Boolean)
if (有.length < 席们.length) log(`⚠ ${席们.length - 有.length} 席无报——须补跑，⛔当作已造`)
return 有.map((r, i) => ({ 席: 席们[报.indexOf(r)].n, ...r }))
