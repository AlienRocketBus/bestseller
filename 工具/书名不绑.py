#!/usr/bin/env python3
"""书名不绑（0927·作者令立·永久）：⛔不许以书名之字为尺去量正文，不许以「书名之许诺」立账挂限。

其由见 设定/裁_0927_书名不绑正文.md：书名将来会改；书名只是定向，硬把书名元素塞进正文会毁掉这本书。

查三处，见以书名为尺之语即红：
  ①诸席令（工具/席/*.js）与诸器（工具/*.py，本器与其负测除外）；
  ②到期账.json 里未清之账；
  ③大审册（设定/大审_至第*章.md）裁定表里未作废之行。
所认之语：「书名之许诺」「书名的许诺」「冲着书名」「书名之字」「扣题」「冢／墓／术」一类以书名字计数者。

用法：python3 工具/书名不绑.py   ｜  python3 工具/书名不绑.py --自测
"""
import os, re, sys, json, glob, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
语 = re.compile(r'书名[之的]?许诺|冲着书名|书名之字|扣题|冢／墓／术|冢墓术|书名.{0,6}缺席|只带书名|读书名|切题|对题')
免 = ('书名不绑.py', '负测_书名不绑.py')


def 查(root=ROOT):
    红 = []
    for p in glob.glob(os.path.join(root, '工具', '席', '*.js')) + glob.glob(os.path.join(root, '工具', '*.py')):
        if os.path.basename(p) in 免:
            continue
        for i, l in enumerate(open(p, encoding='utf-8', errors='replace'), 1):
            if 语.search(l) and '裁_0927' not in l and '不以书名' not in l and '不看书名' not in l:
                红.append('%s:%d' % (os.path.relpath(p, root), i))
    zp = os.path.join(root, '设定', '到期账.json')
    if os.path.exists(zp):
        try:
            d = json.load(open(zp, encoding='utf-8'))
            for x in d.get('items', []):
                if x.get('状态') in ('清', 'closed', '作废'):
                    continue
                if 语.search(json.dumps(x, ensure_ascii=False)):
                    红.append('到期账:%s' % x.get('id'))
        except Exception:
            红.append('到期账.json 读不得')
    for p in glob.glob(os.path.join(root, '设定', '大审_至第*章.md')):
        for i, l in enumerate(open(p, encoding='utf-8', errors='replace'), 1):
            if (l.startswith('|') and 语.search(l) and re.search(r'已挂|限\d', l)
                    and not re.search(r'作废|已治|清', l)):
                红.append('%s:%d' % (os.path.relpath(p, root), i))
    return 红


def 自测():
    ok = 共 = 0
    t = tempfile.mkdtemp()
    try:
        os.makedirs(os.path.join(t, '工具', '席')); os.makedirs(os.path.join(t, '设定'))
        共 += 1; ok += (查(t) == [])
        open(os.path.join(t, '设定', '大审_至第400章.md'), 'w').write('| 5 | 冢／墓／术十章零 | 已挂·限410 |\n| 类型读者 | 冲着书名与类型来 | 第1章 |\n')
        共 += 1; ok += (len(查(t)) == 1)   # 未作废之挂账红；旧册里只述席位之行不红
        open(os.path.join(t, '设定', '大审_至第400章.md'), 'w').write('| 5 | 冢／墓／术十章零 | **作废** |\n')
        共 += 1; ok += (查(t) == [])
        open(os.path.join(t, '工具', '席', 'x.js'), 'w').write("问: '冲着书名来的人'\n")
        共 += 1; ok += (len(查(t)) == 1)
        open(os.path.join(t, '工具', '席', 'x.js'), 'w').write("问: '冲着这类故事来的人'\n")
        json.dump({'items': [{'id': 'A', '状态': 'open', '事': '书名之许诺缺席'}]},
                  open(os.path.join(t, '设定', '到期账.json'), 'w'), ensure_ascii=False)
        共 += 1; ok += (查(t) == ['到期账:A'])
    finally:
        shutil.rmtree(t)
    print('书名不绑·自测 %d/%d' % (ok, 共))
    return ok == 共


if __name__ == '__main__':
    if sys.argv[1:] == ['--自测']:
        sys.exit(0 if 自测() else 1)
    红 = 查()
    if 红:
        print('⛔ 书名不绑：以书名为尺之语 %d 处（裁_0927_书名不绑正文）：%s' % (len(红), '｜'.join(红[:12])))
        sys.exit(1)
    print('✓ 书名不绑：诸席令、到期账、大审册皆不以书名为尺')
