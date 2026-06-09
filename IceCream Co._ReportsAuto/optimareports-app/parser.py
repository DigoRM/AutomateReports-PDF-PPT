import zipfile, xml.etree.ElementTree as ET, re

def read_xlsx(path):
    """Lê xlsx sem openpyxl — retorna lista de listas"""
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        ss = []
        if 'xl/sharedStrings.xml' in names:
            tree = ET.parse(z.open('xl/sharedStrings.xml'))
            root = tree.getroot()
            ns = root.tag.split('}')[0]+'}' if '}' in root.tag else ''
            for si in root.findall(f'{ns}si'):
                ss.append(''.join(t.text or '' for t in si.iter(f'{ns}t')))
        rows = []
        for sf in sorted(n for n in names
                         if n.startswith('xl/worksheets/sheet')
                         and n.endswith('.xml')):
            tree = ET.parse(z.open(sf))
            root = tree.getroot()
            ns2 = root.tag.split('}')[0]+'}' if '}' in root.tag else ''
            for row in root.findall(f'.//{ns2}row'):
                rd = []
                for c in row.findall(f'{ns2}c'):
                    t = c.get('t', ''); v = c.find(f'{ns2}v'); val = ''
                    if v is not None and v.text:
                        val = ss[int(v.text)] if t == 's' else v.text
                    rd.append(val)
                rows.append(rd)
    return rows

def si(v):
    try: return int(float(v)) if v and str(v).strip() else 0
    except: return 0

def sf(v):
    try: return float(str(v).replace('%','')) if v and str(v).strip() else None
    except: return None

def ts(t):
    if not t or not str(t).strip(): return None
    p = str(t).strip().split(':')
    try:
        if len(p) == 2: return int(p[0])*60 + int(p[1])
        if len(p) == 3: return int(p[0])*3600 + int(p[1])*60 + int(p[2])
    except: return None

def mmss(s):
    if s is None: return '--:--'
    return f"{int(s)//60}:{int(s)%60:02d}"

def sn(s):
    """Remove sufixos [z],[g],[d] dos nomes de loja"""
    return re.sub(r'\s*\[.\]$', '', str(s)).strip()

ROW = {
    'CE':7, 'CO':8, 'RC':9, 'KBP':10, 'all_alerts':12,
    'svc_time':14, 'pct_lt3':15, 'pct_3to5':16, 'pct_gt5':17,
    'ordering':18, 'queue':22, 'receiving':26,
    'ord_lt1': 19, 'ord_1to2': 20, 'ord_gt2': 21,
    'queue_lt1': 23, 'queue_1to2': 24, 'queue_gt2': 25,
    'recv_lt1': 27, 'recv_1to2': 28, 'recv_gt2': 29,
    'cash_total':30, 'cash_drawer':32, 'not_attended':33,
    'queue_3':36, 'receipt_given':39, 'receipt_print':40,
    'receive_3min':41, 'outside':42, 'mobile':44, 'pin_cashier':45,
    'cam_total':48, 'cam_blurry':50, 'cam_lagging':51,
    'cam_connect':52, 'cam_lost':53, 'cam_obstructed':54,
    'allstore_total':60, 'complaining':61, 'dirty_floor':62,
    'incomplete_fridge':63, 'lost_customer':64, 'inactive':65,
    'playing':66, 'no_cap':68, 'no_uniform':69,
    'close_sooner':70, 'open_late':71,
    'del_time':73, 'del_lt2':74, 'del_2to3':75, 'del_gt3':76,
    'delivery_total':77, 'check_packaging':78,
    'delivery_wait':79,  # KBP CO — NÃO RC!
    'del_clothes':80, 'pkg_closed':81,
    'dt_total':83, 'dt_cash':85, 'dt_receipt':88,
    'dt_outside':91, 'dt_mobile':94, 'dt_pin':95,
}

KBP1_CE = [
    ('Recepción de orden >3min',       'receive_3min'),
    ('+3 personas en fila',            'queue_3'),
    ('Cliente sin atender >1min',      'not_attended'),
    ('Cliente perdido',                'lost_customer'),
    ('Piso sucio >3min',               'dirty_floor'),
    ('Cliente con queja',              'complaining'),
]
KBP3_CO = [
    ('Personal sin gorra',                  'no_cap'),
    ('Personal sin uniforme',               'no_uniform'),
    ('Repartidor esperando >1min',          'delivery_wait'),  # CO!
    ('Repartidor con producto en ropa',     'del_clothes'),
    ('Empaque cerrado',                     'pkg_closed'),
    ('Refrigeradores incompletos',          'incomplete_fridge'),
]
KBP2_RC_ALL = [
    ('Cajón de dinero abierto',         'cash_drawer'),
    ('Personal fuera de caja >1min',    'outside'),
    ('Personal móvil',                  'mobile'),
    ('Uso incorrecto de PIN pad',       'pin_cashier'),
    ('Cierre anticipado de tienda',     'close_sooner'),
    ('Apertura tardía de tienda',       'open_late'),
    ('Personal inactivo >5min',         'inactive'),
    ('Jugando/peleando',                'playing'),
    ('Verificar empaque',               'check_packaging'),
    ('Recibo no entregado',             'receipt_given'),
    ('Recibo no impreso',               'receipt_print'),
    ('[D] Cajón de dinero',             'dt_cash'),
    ('[D] Recibo no entregado',         'dt_receipt'),
    ('[D] Personal fuera de caja',      'dt_outside'),
    ('[D] Personal móvil',              'dt_mobile'),
    ('[D] PIN pad',                     'dt_pin'),
]

def parse_franchise(xlsx_path, franchise_name, period, period_long):
    rows = read_xlsx(xlsx_path)
    header = rows[5]
    raw_stores = [h.strip() for h in header[2:] if h.strip()]
    stores = [f"Store {i+1:02d}" for i in range(len(raw_stores))]
    n = len(stores)

    def gt(k):
        ri = ROW[k]
        if ri >= len(rows) or len(rows[ri]) < 2: return ''
        return rows[ri][1]

    def gs(k, i):
        ri = ROW[k]
        if ri >= len(rows) or len(rows[ri]) < i+3: return ''
        return rows[ri][i+2]

    def sir(k): return si(gt(k))
    def tsr(k): return ts(gt(k))
    def sfr(k): return sf(gt(k))

    def store_int_rank(k):
        return sorted([(stores[i], si(gs(k,i))) for i in range(n)],
                      key=lambda x: -x[1])

    def store_time_rank(k):
        return sorted([(stores[i], ts(gs(k,i)))
                       for i in range(n) if ts(gs(k,i))],
                      key=lambda x: x[1])

    def kbp_dyn(alert_list):
        return sorted([(l, k, sir(k)) for l, k in alert_list if sir(k) > 0],
                      key=lambda x: -x[2])

    kbp_total = sir('KBP')
    ce = sir('CE'); rc = sir('RC'); co = sir('CO')

    kbp1 = kbp_dyn(KBP1_CE)
    kbp3 = kbp_dyn(KBP3_CO)
    kbp2 = kbp_dyn(KBP2_RC_ALL)[:8]  # top 8 do RC

    def store_ranks(alerts):
        return {k: [[s, v] for s, v in store_int_rank(k)[:10]]
                for _, k, _ in alerts if k in ROW}

    all_types = kbp_dyn(KBP1_CE + KBP3_CO + KBP2_RC_ALL)
    top5_types = sorted(
        [{'label': l, 'val': v,
          'pct': round(v/kbp_total*100, 1) if kbp_total else 0}
         for l, k, v in all_types if v > 0],
        key=lambda x: -x['val']
    )[:15]

    dt_total = sir('dt_total')

    def dt_top5(k):
        total = sir(k)
        if total == 0: return []
        return [[s, v, round(v/total*100, 1)]
                for s, v in store_int_rank(k)[:10] if v > 0]

    all_ranked = store_int_rank('all_alerts')
    rank_map = {s: i+1 for i, (s, _) in enumerate(all_ranked)}

    cam_stores = sorted([
        {'store': stores[i],
         'cam':   si(gs('cam_total', i)),
         'kbp':   si(gs('KBP', i)),
         'all_alerts': si(gs('all_alerts', i)),
         'rank':  rank_map.get(stores[i], 0)}
        for i in range(n) if si(gs('cam_total', i)) > 0
    ], key=lambda x: -x['cam'])[:14]


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

    return {
        'franchise':    franchise_name,

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
        'period':       period,
        'period_long':  period_long,
        'code':         '',
        'n_stores':     n,
        'kbp': kbp_total,
        'ce': ce, 'ce_pct': round(ce/kbp_total*100, 1) if kbp_total else 0,
        'rc': rc, 'rc_pct': round(rc/kbp_total*100, 1) if kbp_total else 0,
        'co': co, 'co_pct': round(co/kbp_total*100, 1) if kbp_total else 0,
        'all_alerts': sir('all_alerts'),
        'svc_avg':   mmss(tsr('svc_time')),
        'ord_avg':   mmss(tsr('ordering')),
        'queue_avg': mmss(tsr('queue')),
        'recv_avg':  mmss(tsr('receiving')),
        'del_avg':   mmss(tsr('del_time')),
        'pct_lt3':  sfr('pct_lt3') or 0,
        'pct_3to5': sfr('pct_3to5') or 0,
        'pct_gt5':  sfr('pct_gt5') or 0,
        'del_lt2':  sfr('del_lt2') or 0,
        'del_2to3': sfr('del_2to3') or 0,
        'del_gt3':  sfr('del_gt3') or 0,
        'cash_total':     sir('cash_total'),
        'allstore_total': sir('allstore_total'),
        'delivery_total': sir('delivery_total'),
        'dt_total':       dt_total,
        'cam_total':      sir('cam_total'),
        'receive_3min':        sir('receive_3min'),
        'queue_3':             sir('queue_3'),
        'mobile':              sir('mobile'),
        'outside':             sir('outside'),
        'not_attended':        sir('not_attended'),
        'cash_drawer':         sir('cash_drawer'),
        'pin_cashier':         sir('pin_cashier'),
        'receipt_not_given':   sir('receipt_given'),
        'receipt_not_printed': sir('receipt_print'),
        'no_cap':            sir('no_cap'),
        'no_uniform':        sir('no_uniform'),
        'lost_customer':     sir('lost_customer'),
        'open_late':         sir('open_late'),
        'inactive':          sir('inactive'),
        'playing':           sir('playing'),
        'dirty_floor':       sir('dirty_floor'),
        'complaining':       sir('complaining'),
        'close_sooner':      sir('close_sooner'),
        'incomplete_fridge': sir('incomplete_fridge'),
        'delivery_wait':    sir('delivery_wait'),
        'check_packaging':  sir('check_packaging'),
        'del_clothes':      sir('del_clothes'),
        'pkg_closed':       sir('pkg_closed'),
        'has_drive_thru': dt_total > 0,
        'dt_pin':     sir('dt_pin'),
        'dt_outside': sir('dt_outside'),
        'dt_cash':    sir('dt_cash'),
        'dt_mobile':  sir('dt_mobile'),
        'dt_receipt': sir('dt_receipt'),
        'cam_lost':       sir('cam_lost'),
        'cam_blurry':     sir('cam_blurry'),
        'cam_connect':    sir('cam_connect'),
        'cam_obstructed': sir('cam_obstructed'),
        'cam_lagging':    sir('cam_lagging'),
        'cam_stores_count': len(cam_stores),
        'kbp1_alerts': [[l, k, v] for l, k, v in kbp1],
        'kbp1_all':    [[l, v] for l, k, v in kbp1],
        'kbp2_alerts': [[l, k, v] for l, k, v in kbp2],
        'kbp2_all':    [[l, v] for l, k, v in kbp2],
        'kbp3_alerts': [[l, k, v] for l, k, v in kbp3],
        'kbp3_all':    [[l, v] for l, k, v in kbp3],
        'kbp1_store_ranks': store_ranks(kbp1),
        'kbp2_store_ranks': store_ranks(kbp2),
        'kbp3_store_ranks': store_ranks(kbp3),
        'svc_fast':   [[s, mmss(t)] for s, t in store_time_rank('svc_time')[:3]],
        'svc_slow':   [[s, mmss(t)] for s, t in store_time_rank('svc_time')[-3:][::-1]],
        'ord_fast':   [[s, mmss(t)] for s, t in store_time_rank('ordering')[:3]],
        'ord_slow':   [[s, mmss(t)] for s, t in store_time_rank('ordering')[-3:][::-1]],
        'queue_fast': [[s, mmss(t)] for s, t in store_time_rank('queue')[:3]],
        'queue_slow': [[s, mmss(t)] for s, t in store_time_rank('queue')[-3:][::-1]],
        'recv_fast':  [[s, mmss(t)] for s, t in store_time_rank('receiving')[:3]],
        'recv_slow':  [[s, mmss(t)] for s, t in store_time_rank('receiving')[-3:][::-1]],
        'del_fast':   [[s, mmss(t)] for s, t in store_time_rank('del_time')[:3]],
        'del_slow':   [[s, mmss(t)] for s, t in store_time_rank('del_time')[-3:][::-1]],
        'kbp_top10':  [[s, v, round(v/kbp_total*100, 1)] for s, v in store_int_rank('KBP')[:10]],

        'all_top10': [[s, v, round(v/max(sir('all_alerts'),1)*100, 1)] for s, v in all_ranked[:10]],
        'kbp_worst': [store_int_rank('KBP')[0][0], round(store_int_rank('KBP')[0][1]/kbp_total*100, 1), store_int_rank('KBP')[0][1]],
        'kbp_best':  [all_ranked[-1][0], round(all_ranked[-1][1]/max(sir('all_alerts'),1)*100, 1), all_ranked[-1][1]],
        'ce_top10':   [[s, v, round(v/max(ce,1)*100, 1)] for s, v in store_int_rank('CE')[:10]],
        'rc_top10':   [[s, v, round(v/max(rc,1)*100, 1)] for s, v in store_int_rank('RC')[:10]],
        'co_top10':   [[s, v, round(v/max(co,1)*100, 1)] for s, v in store_int_rank('CO')[:10]],
        'ord_top5_fast': [[s, mmss(t)] for s, t in store_time_rank('ordering')[:10]],
        'top10_alert_types': top5_types,
        'dt_pin_top10':     dt_top5('dt_pin'),
        'dt_outside_top10': dt_top5('dt_outside'),
        'dt_cash_top10':    dt_top5('dt_cash'),
        'dt_mobile_top10':  dt_top5('dt_mobile'),
        'cam_stores': cam_stores,
    }
