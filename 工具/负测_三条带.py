# -*- coding: utf-8 -*-
"""负测·评论员三条带（2026-09-03 立·第298章第13轮·补跑第7轮所立）

★立此测之由：`看官.py::评论员` 之群只一条——**前6章之窗**；
　★★而 `比带.py` 两造之前就立过「一个数报三条带（全书／同镜／同形），
　　三条带若不同判，以同形为先」，其档头自陈「本坐第5、7、8三轮各栽一回，皆因只看同镜那一条」。
★★★298第13轮实逮：本席判「本章之弱在动拍%：本章46，前6章中位54.5，低17%」，
　　**而全书之中位38、同形「做事」之中位38，本章46在两条带之上**——
　　**那个「弱」是六章之窗造出来的**（292—297恰是一段动拍极密之章）。
★★★★故本测之要害两条（令§六③·改闸必同日立负测且以旧式回灌验）：
　★①旧式（只取窗）与新式（另取二带）在此项上须判得不同——同判者，本带即陪跑；
　★★②而新式不许把凡「弱」都洗白：三条带俱在中位之下者，新式仍须报「本章在其下」。
"""
import io, os, sys, statistics as st, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load(name, path):
    sp = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def 跑(n=298):
    kg = _load('_kg', '工具/看官.py')
    bd = _load('_bd', '工具/比带.py')
    坏, 项 = [], 0

    def 量(x):
        bs = kg.拍(x)
        if not bs:
            return None
        L = [len(y) for y in bs]
        动 = sum(1 for y in bs if kg.手.search(y))
        return {'长拍%': round(100 * sum(1 for y in L if y >= 33) / len(L)),
                '动拍%': round(100 * 动 / len(bs))}

    _, t = kg.白文(n)
    if not t:
        print('✗ 负测·三条带：第%d章白文取不着' % n)
        return 1
    本 = 量(t)
    我形 = bd._形(n)
    窗, 全书, 同形 = [], [], []
    for m in range(1, n):
        _, x = kg.白文(m)
        if not x:
            continue
        v = 量(x)
        if not v:
            continue
        全书.append(v)
        if bd._形(m) == 我形:
            同形.append(v)
        if n - 6 <= m < n:
            窗.append(v)

    # ★①回灌验：旧式（窗）判「动拍%」为弱，而新式二带俱在其上——二式须判得不同
    项 += 1
    窗中 = st.median([v['动拍%'] for v in 窗])
    全中 = st.median([v['动拍%'] for v in 全书])
    形中 = st.median([v['动拍%'] for v in 同形])
    if not (本['动拍%'] < 窗中):
        坏.append('★回灌之料不对：旧式（窗）已不判动拍%为弱，此测即成陪跑')
    if not (本['动拍%'] > 全中 and 本['动拍%'] > 形中):
        坏.append('新式失效：动拍%%在全书（中位%s）或同形（中位%s）之带上，'
                  '本章%s——二式竟同判' % (全中, 形中, 本['动拍%']))

    # ★★②不许洗白：长拍%三条带俱在中位之下，新式仍须报「其下」
    项 += 1
    for xs, lab in ((窗, '窗'), (全书, '全书'), (同形, '同形')):
        中 = st.median([v['长拍%'] for v in xs])
        if 本['长拍%'] >= 中:
            坏.append('新式洗白：长拍%%在%s之中位（%s）之上，本章%s'
                      % (lab, 中, 本['长拍%']))

    # ★★★③真器上须有此带，且其群非窗
    项 += 1
    if not hasattr(kg, '_三条带'):
        坏.append('★真器无 _三条带：此测所验者不在器上')
    项 += 1
    src = io.open(os.path.join(ROOT, '工具', '看官.py'), encoding='utf-8').read()
    if '同形' not in src or 'range(1, n)' not in src:
        坏.append('★真器之群仍是窗：它没有取全书与同形')

    # ★★★★④本席之判不许被本带改掉（只添不减）
    项 += 1
    if '弱.sort(reverse=True)' not in src or '⛔本章之弱，在「%s」' not in src:
        坏.append('★本席之强制出负被本带动了——本带只许添，不许减')

    if 坏:
        print('✗ 负测·三条带 %d/%d' % (项 - len(坏), 项))
        for x in 坏:
            print('   ⛔ ' + x)
        return 1
    print('✓ 负测·三条带 %d/%d 全通（旧式判弱而新式二带俱在其上，故非陪跑；'
          '且长拍%%三带俱下，未被洗白）' % (项, 项))
    return 0


if __name__ == '__main__':
    sys.exit(跑())
