# 以 391 段裁席之提交 b5a1b449 反演一份小单：取「行内改」之行，求最小而恰一见之 原／新
import subprocess, difflib, json, sys, os
C = 'b5a1b449'; 仓 = '/home/user/the-novel'
出 = sys.argv[1]
取 = {'设定/剧情庭题/余章总案.md': 5, '设定/00_镇冢秘术_唯一总圣经.md': 3, '设定/段案/390-397.md': 2}
def show(rev, p):
    return subprocess.run(['git', 'show', '%s:%s' % (rev, p)], cwd=仓, capture_output=True).stdout.decode('utf-8')
单, 期 = [], {}
for p, k in 取.items():
    a, b = show(C + '^', p), show(C, p)
    A, B = a.split('\n'), b.split('\n')
    n = 0
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B, autojunk=False).get_opcodes():
        if op != 'replace' or i2 - i1 != j2 - j1:
            continue
        for x, y in zip(A[i1:i2], B[j1:j2]):
            if n >= k: break
            前 = 0
            while 前 < min(len(x), len(y)) and x[前] == y[前]: 前 += 1
            後 = 0
            while 後 < min(len(x), len(y)) - 前 and x[-1 - 後] == y[-1 - 後]: 後 += 1
            for 宽 in range(6, 4000, 6):   # 带上下文至原、新俱恰一见
                s, e = max(0, 前 - 宽), min(len(x), len(x) - 後 + 宽)
                原 = x[s:e]; 新 = y[s:len(y) - (len(x) - e)]
                if a.count(原) == 1 and b.count(新) == 1:
                    break
            else:
                continue
            单.append({'档': p, '原': 原, '新': 新, '由': '据 剧情庭_势_第391段（反演自 %s:%d）' % (p, j1 + 1 + (B[j1:j2].index(y)))})
            期.setdefault(p, []).append(y)
            n += 1
        if n >= k: break
json.dump(单, open(出, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(期, open(出 + '.期', 'w', encoding='utf-8'), ensure_ascii=False)
print('反演 %d 条：%s' % (len(单), '；'.join('%s×%d' % (p, len(v)) for p, v in 期.items())))
for x in 单:
    print('  %s ｜原 %d 字｜新 %d 字' % (x['由'][-40:], len(x['原']), len(x['新'])))
