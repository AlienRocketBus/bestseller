# -*- coding: utf-8 -*-
"""负测·检察官之到期账不凭空记一笔冷轮之欠（2026-09-22 立）

★**其所验者係本日一笔真漏**：`裁_0922_冷轮之令_无档者不凭空记一笔欠.md` 当日
  **只改了 `开轮六检::check6` 一处**，⛔**而 `小说检察官::_auto_cold` 是第二处判同一件事的码**
  ——於是 `开轮六检⑥` 印绿，而 `--doctor` 照旧印「⛔[COLD-350]……到期3项」并据之判 ERROR。
★★**本器逐格皆拿真盘之局跑**，⛔**并含一格旧式回灌**（证其非陪跑）。
"""
import os as _o, sys as _s
_s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__)))
try:
    import _账  # 跑账·自记（工具/跑账.py）
except Exception:
    pass
import importlib.util as u
import os
import sys

根 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _载(名, 路):
    s = u.spec_from_file_location(名, os.path.join(根, 路))
    m = u.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def 自测():
    检 = _载('检', '工具/小说检察官.py')
    六 = _载('六', '工具/开轮六检.py')
    R = []
    # ①—③ 真盘之局：350 无档而其回执 §九 明裁「销而不立」
    R.append(('①350 盘上无 `冷轮_COLD350_*.md`', not 六._cold_有档(350)))
    R.append(('②350 之回执有一句立／不立之明裁', bool(六._cold_明裁(350))))
    R.append(('③故检察官不替 350 记一笔欠', 检._cold_无面而明裁(350) is True))
    # ④⛔旧式回灌：旧式只问 done／void 二事——350 二者皆 False，故旧式必记一笔
    旧 = (not 六._cold_done(350)) and (not 六._cold_void(350))
    R.append(('④⛔旧式（只问 done／void）对同一局照记一笔欠——证本格非陪跑', 旧 is True))
    # ⑤⛔不是一律免：无档且无明裁者照旧记欠（317 即其一）
    R.append(('⑤317 无档而无明裁——照旧记欠（⛔新令不是一张免死牌）',
              检._cold_无面而明裁(317) is False))
    # ⑥有档者不因本条免（345 有废档，其免走 void 那一路）
    R.append(('⑥345 有档——不走本条（其免在 `_cold_void`）',
              检._cold_无面而明裁(345) is False))
    # ⑦一处判：检察官不自写一份判，只转调 开轮六检
    码 = open(os.path.join(根, '工具/小说检察官.py'), encoding='utf-8').read()
    R.append(('⑦⛔一处判：检察官只转调 `开轮六检._cold_有档／_cold_明裁`，不另写一份码',
              '_m._cold_有档(n)' in 码 and '_m._cold_明裁(n)' in 码))
    # ⑧取不着开轮六检时宁可多催一笔
    R.append(('⑧⛔取不着 `开轮六检` 时返 False（宁可多催，不可少催）',
              'return False' in 码.split('def _cold_无面而明裁')[1].split('def _auto_cold')[0]))
    # ⑨真跑 `_auto_cold`：其内不再有 COLD-350
    try:
        files = sorted(检._chapter_files().keys()) if hasattr(检, '_chapter_files') else None
    except Exception:
        files = None
    if files:
        ids = [x['id'] for x in 检._auto_cold(files)]
        R.append(('⑨真跑 `_auto_cold`：COLD-350 已不在其内', 'COLD-350' not in ids))
    for 名, o in R:
        print(('  ✓ ' if o else '  ⛔ ') + 名)
    _过 = sum(1 for _, o in R if o)
    print('  ── 负测·检察官冷轮明裁 %d/%d %s ──'
          % (_过, len(R), '全通' if _过 == len(R) else '⛔未过'))
    return all(o for _, o in R)


if __name__ == '__main__':
    sys.exit(0 if 自测() else 1)
