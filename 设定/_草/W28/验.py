"""W28 之验（零 token）：python3 设定/_草/W28/验.py 甲|乙|丙 ——印该组章记残留之原片与骨记残引（W26 新造）；二数俱 0 方交。"""
import sys,json,subprocess,os,re,io; sys.path.insert(0,'工具')
import 章料, 亮点对表 as A
W='设定/_草/W26/'
names=open('/tmp/claude-0/-home-user-the-novel/2f785fc3-f03f-5b56-ad3f-32a68833152c/scratchpad/链.txt').read().split()+[W+x for x in ['单_总2.json','单_随一.json','单_随二.json','单_随三.json','单_随四.json']]
片={}
def old(c):
    return subprocess.run(['git','show','e2f332b3:'+os.path.relpath(章料.章档(c))],capture_output=True,text=True).stdout
for p in names:
    for o in json.load(open(p,encoding='utf-8'))['ops']:
        c=int(o['章'])
        if o['式']=='换' and len(o.get('原',''))>=6: 片.setdefault(c,{})[o['原']]=o.get('新','') or '（删）'
        if o['式']=='清':
            L=old(c).split('\n')
            for k in range(int(o['行']),int(o.get('止') or o['行'])+1):
                for s in re.split(r'[。！？]',L[k-1]):
                    if len(s.strip())>=8: 片.setdefault(c,{})[s.strip()]='（整段已删·G%s）'%o['G'][1:]
拍={261:(161,135),263:(155,118),275:(138,137),283:(145,144),316:(104,102)}
组={'甲':[261,263,265],'乙':[232,235,241,244,247,251,253,255],'丙':[195,199,217,275,283,286,288,292,300,304,308,316,318]}
只 = sys.argv[1] if len(sys.argv) > 1 else None
for g,cs in 组.items():
    if 只 and g != 只: continue

    out=['# W28 之料·%s（全书记忆与骨记随 W26 之白文）'%g,'','> 零 token 所汇。「原片」係 W26 所换／所删之旧白文；「→」後係今之白文（或已删）。章记之档在 设定/全书记忆/第N章.md；骨记在 正文 该章【本章亮点】以下。','']
    for c in cs:
        p='设定/全书记忆/第%d章.md'%c
        m=open(p,encoding='utf-8').read() if os.path.exists(p) else ''
        hit=[(s,n) for s,n in 片.get(c,{}).items() if s in m]
        f=章料.章档(c); now=io.open(f,encoding='utf-8').read()
        残=[x for x in A.旧版残引(c,now) if x not in A.旧版残引(c,old(c))]
        L=now.split('\n'); i=next((k for k,l in enumerate(L) if l.startswith('【本章亮点】')),None)
        骨行=[]
        for q in 残:
            for k in range(i or 0,len(L)):
                if q[:12] in L[k]: 骨行.append(k+1); break
        out.append('## 第%d章（%s）'%(c,os.path.basename(f)))
        out.append('- 章记：`%s`｜残留原片 %d 处'%(p,len(hit)))
        for s,n in hit: out.append('  - 「%s」→ %s'%(s,n))
        out.append('- 骨记残引（W26 新造）%d 处%s'%(len(残),'；骨记起於第 %d 行'%(i+1) if i is not None else ''))
        for q,k in zip(残,骨行+[None]*len(残)): out.append('  - %s行：「%s」'%(('第%d'%k) if k else '？',q))
        if c in 拍: out.append('- 拍数：W26 前 %d 个「＊」→ 今 %d 个（全章拍数减 %d）；骨记、锁定行（施工表）、章记里按拍号所记者，删处以後之号须随减'%(拍[c][0],拍[c][1],拍[c][0]-拍[c][1]))
        out.append('')
    n1=sum(int(re.search(r'残留原片 (\d+)',x).group(1)) for x in out if '残留原片' in x)
    n2=sum(int(re.search(r'骨记残引（W26 新造）(\d+)',x).group(1)) for x in out if '骨记残引' in x)
    print('W28 验·%s：章记残留原片 %d｜骨记残引 %d' % (g, n1, n2))
    for x in out:
        if x.startswith('## ') or x.startswith('  - '): print(x)
