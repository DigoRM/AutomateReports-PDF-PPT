import re

def update_parser():
    with open('c:/Users/rodri/Desktop/IceCream Co._ReportsAuto/optimareports-app/parser.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update ROW dictionary
    old_row = r"'ordering':18, 'queue':22, 'receiving':26,"
    new_row = r"'ordering':18, 'queue':22, 'receiving':26," + "\n    'ord_lt1': 19, 'ord_1to2': 20, 'ord_gt2': 21,\n    'queue_lt1': 23, 'queue_1to2': 24, 'queue_gt2': 25,\n    'recv_lt1': 27, 'recv_1to2': 28, 'recv_gt2': 29,"
    content = content.replace(old_row, new_row)

    # 2. Add new variables inside parse_franchise
    # We will inject code right before the `return {`
    injection = r"""
    # NOVO: store_kbp_stacks -> [store, ce, rc, co, rank]
    store_kbp_stacks = []
    for s, tot_alerts in all_ranked:
        i = stores.index(s)
        s_ce = si(gs('CE', i))
        s_rc = si(gs('RC', i))
        s_co = si(gs('CO', i))
        store_kbp_stacks.append([s, s_ce, s_rc, s_co, rank_map.get(s, 0)])

    # NOVO: store_area_stacks -> [store, cashier, allstore, delivery, drivethru, cam, rank]
    store_area_stacks = []
    for s, tot_alerts in all_ranked:
        i = stores.index(s)
        s_cash = si(gs('cash_total', i))
        s_all = si(gs('allstore_total', i))
        s_del = si(gs('delivery_total', i))
        s_dt = si(gs('dt_total', i))
        s_cam = si(gs('cam_total', i))
        store_area_stacks.append([s, s_cash, s_all, s_del, s_dt, s_cam, rank_map.get(s, 0)])

    # NOVO: dt_stores_ranking -> [store, store_dt, store_dt_pct, rank]
    dt_ranked = store_int_rank('dt_total')
    dt_stores_ranking = []
    for s, val in dt_ranked:
        if val > 0:
            i = stores.index(s)
            tot_alerts = si(gs('all_alerts', i))
            pct = round(val / tot_alerts * 100, 1) if tot_alerts > 0 else 0.0
            dt_stores_ranking.append([s, val, pct, rank_map.get(s, 0)])

    # NOVO: delivery_stores_ranking -> [store, del_time_str, svc_time_str, tot_alerts, del_alerts_pct, seconds]
    # Sorted by delivery time (fastest first)
    del_stores = store_time_rank('del_time')
    delivery_stores_ranking = []
    for s, t_secs in del_stores:
        i = stores.index(s)
        s_svc = mmss(ts(gs('svc_time', i)))
        s_tot_al = si(gs('all_alerts', i))
        s_del_al = si(gs('delivery_total', i))
        pct = round(s_del_al / s_tot_al * 100, 1) if s_tot_al > 0 else 0.0
        delivery_stores_ranking.append([s, mmss(t_secs), s_svc, s_tot_al, pct, t_secs])

    # NOVO: top 10 store rankings for CE, RC, CO stacked by Area
    def top10_area_stack(kbp_name):
        res = []
        top10 = store_int_rank(kbp_name)[:10]
        for s, _ in top10:
            i = stores.index(s)
            s_cash = si(gs('cash_total', i))
            s_all = si(gs('allstore_total', i))
            s_del = si(gs('delivery_total', i))
            s_dt = si(gs('dt_total', i))
            s_cam = si(gs('cam_total', i))
            res.append([s, s_cash, s_all, s_del, s_dt, s_cam, rank_map.get(s, 0)])
        return res

"""
    content = content.replace("    return {\n", injection + "    return {\n")

    # 3. Add to the return dict
    return_inj = r"""
        'ord_lt1': sfr('ord_lt1') or 0, 'ord_1to2': sfr('ord_1to2') or 0, 'ord_gt2': sfr('ord_gt2') or 0,
        'queue_lt1': sfr('queue_lt1') or 0, 'queue_1to2': sfr('queue_1to2') or 0, 'queue_gt2': sfr('queue_gt2') or 0,
        'recv_lt1': sfr('recv_lt1') or 0, 'recv_1to2': sfr('recv_1to2') or 0, 'recv_gt2': sfr('recv_gt2') or 0,
        'store_kbp_stacks': store_kbp_stacks,
        'store_area_stacks': store_area_stacks,
        'dt_stores_ranking': dt_stores_ranking,
        'delivery_stores_ranking': delivery_stores_ranking,
        'ce_top10_stack': top10_area_stack('CE'),
        'rc_top10_stack': top10_area_stack('RC'),
        'co_top10_stack': top10_area_stack('CO'),
"""
    content = content.replace("        'franchise':    franchise_name,\n", "        'franchise':    franchise_name,\n" + return_inj)

    with open('c:/Users/rodri/Desktop/IceCream Co._ReportsAuto/optimareports-app/parser.py', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    update_parser()
