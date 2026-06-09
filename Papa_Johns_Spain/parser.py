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
    return re.sub(r'\s*\[.\]$', '', str(s)).strip()ROW = {
    # KBPs and Totals
    'CE': 7,
    'CO': 8,
    'RC': 9,
    'KBP': 10,
    'all_alerts': 12,
    
    # Times (Service metrics)
    'svc_time': 36,    # Time to receive food
    'pct_lt3': 37,     # Less than 5'
    'pct_3to5': 38,    # 5 to 10'
    'pct_gt5': 40,     # More than 15'
    'ordering': 41,    # Ordering Time
    'queue': 45,       # Queue Wait Time
    'receiving': 51,   # Total Experience Time (mapped to receiving in DQ dashboard)
    
    # Ordering Time ranges
    'ord_lt1': 42,
    'ord_1to2': 43,
    'ord_gt2': 44,
    
    # Queue Time ranges
    'queue_lt1': 46,
    'queue_1to2': 47,
    'queue_gt2': 49,   # More than 3'
    
    # Receiving Time ranges (mapped to Total Experience Time ranges in PJ)
    'recv_lt1': 32,    # Less than 5'
    'recv_1to2': 33,   # 5 to 10'
    'recv_gt2': 35,    # More than 15'
    
    # Caja (Cashier) Area - Rows 23-29
    'cash_total': 23,
    'money_register': 24,
    'cash_drawer': 25,
    'cash_fraud': 26,
    'delivered_no_payment': 27,
    'receipt_not_printed': 28,
    'safe_no_manager': 29,
    
    # Service Area - Rows 52-60
    'service_total': 52,
    'no_thermal_bag': 53,
    'lost_customer': 54,
    'queue_3': 55,
    'order_uncollected': 56,
    'driver_5min': 57,
    'no_security_seal': 58,
    'prep_food_15': 59,
    'not_attended': 60,
    
    # Kitchen Area - Rows 67-69
    'kitchen_total': 67,
    'discarded_kitchen': 68,
    'dough_rack': 69,
    
    # All Areas - Rows 72-78
    'allstore_total': 72,   # mapped to allstore_total for Areas tab compatibility
    'abnormal_behavior': 73,
    'discarded_product': 74,
    'removing_product': 75,
    'consuming_product': 76,
    'hiding_product': 77,
    'unproductive_staff': 78,
    
    # Delivery and Drive Thru (Drive thru is not present, so we map to 0/None or empty)
    'del_time': 62,         # Average duration before delivery of Papa John's riders
    'del_lt2': 63,          # 1 - 3 minutes
    'del_2to3': 64,         # 4 - 7 minutes
    'del_gt3': 66,          # More than 10 minutes
    'delivery_total': 52,   # Mapped to service_total since delivery is under Service in PJ
    'dt_total': 0,          # Set to 0 to dynamically disable Drive Thru
    
    # Fallback/Unused
    'receipt_given': 0,
    'receipt_print': 28,
    'no_cap': 76,
    'no_uniform': 0,
    'open_late': 0,
    'playing': 77,
    'dirty_floor': 74,
    'complaining': 0,
    'close_sooner': 0,
    'incomplete_fridge': 0,
    'delivery_wait': 53,
    'check_packaging': 0,
    'del_clothes': 0,
    'pkg_closed': 0,
    'dt_pin': 0,
    'dt_outside': 0,
    'dt_cash': 0,
    'dt_mobile': 0,
    'dt_receipt': 0,
    'cam_total': 14,
    'cam_lost': 17,
    'cam_blurry': 16,
    'cam_connect': 20,
    'cam_obstructed': 18,
    'cam_lagging': 19,
}

KBP1_CE = [
    ('Cliente perdido (deserción en fila)',                'lost_customer'),
    ('Más de 3 personas en fila en el mostrador/caja',     'queue_3'),
    ('Preparación de comida superior a 15 minutos',        'prep_food_15'),
    ('Cliente desatendido por más de 3 minutos',           'not_attended'),
    ('Entregador PJ permanece en tienda >5 minutos',       'driver_5min'),
]

KBP2_RC_ALL = [
    ('Posible fraude de caja',                             'cash_fraud'),
    ('Dinero alrededor de la caja',                        'money_register'),
    ('Cajón de dinero abierto y desatendido >20 seg',      'cash_drawer'),
    ('Recibo no impreso',                                  'receipt_not_printed'),
    ('Personal abre caja fuerte sin gerente',              'safe_no_manager'),
    ('Producto entregado sin pago',                        'delivered_no_payment'),
    ('Personal improductivo por dos minutos',              'unproductive_staff'),
    ('Personal ocultando producto',                        'hiding_product'),
    ('Personal consumiendo producto',                      'consuming_product'),
    ('Personal retirando producto',                        'removing_product'),
    ('Producto descartado',                                'discarded_product'),
]

KBP3_CO = [
    ('Masa en rack de amasado >30 minutos',                'dough_rack'),
    ('Pizza entregada sin sello de seguridad',             'no_security_seal'),
    ('Pedido no retirado por mais de 15 minutos',          'order_uncollected'),
    ('Repartidor sin bolsa térmica',                       'no_thermal_bag'),
]

def parse_franchise(xlsx_path, franchise_name, period, period_long):
    rows = read_xlsx(xlsx_path)
    header = rows[5]
    stores = [h.strip() for h in header[2:] if h.strip()]
    n = len(stores)

    # Dynamic row adjustments to handle row shifts when "Total notifications" row is removed
    R = ROW.copy()
    has_total_notifications = any(len(r) > 0 and 'Total notifications' in str(r[0]) for r in rows[:15])
    if not has_total_notifications:
        # Shift rows from row 10 onwards up by 1
        for k, v in ROW.items():
            if v >= 10:
                R[k] = v - 1
        # Point both KBP and all_alerts to 'Total alerts of all types' (row 11 in shifted layout)
        R['KBP'] = 11
        R['all_alerts'] = 11

    def gt(k):
        ri = R.get(k, 0)
        if ri == 0 or ri >= len(rows) or len(rows[ri]) < 2: return ''
        return rows[ri][1]

    def gs(k, i):
        ri = R.get(k, 0)
        if ri == 0 or ri >= len(rows) or len(rows[ri]) < i+3: return ''
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
                for _, k, _ in alerts if k in R}

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

    # NOVO: store_area_stacks -> [store, cashier, servicio, cocina, allstore, cam, rank]
    store_area_stacks = []
    for s, tot_alerts in all_ranked:
        i = stores.index(s)
        s_cash = si(gs('cash_total', i))
        s_svc = si(gs('delivery_total', i))
        s_kit = si(gs('kitchen_total', i))
        s_all = si(gs('allstore_total', i))
        s_cam = si(gs('cam_total', i))
        store_area_stacks.append([s, s_cash, s_svc, s_kit, s_all, s_cam, rank_map.get(s, 0)])

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
        s_del_al = si(gs('no_thermal_bag', i)) + si(gs('driver_5min', i))
        pct = round(s_del_al / s_tot_al * 100, 1) if s_tot_al > 0 else 0.0
        delivery_stores_ranking.append([s, mmss(t_secs), s_svc, s_tot_al, pct, t_secs])

    # NOVO: top 10 store rankings for CE, RC, CO stacked by Area
    def top10_area_stack(kbp_name):
        res = []
        top10 = store_int_rank(kbp_name)[:10]
        for s, _ in top10:
            i = stores.index(s)
            s_cash = si(gs('cash_total', i))
            s_svc = si(gs('delivery_total', i))
            s_kit = si(gs('kitchen_total', i))
            s_all = si(gs('allstore_total', i))
            s_cam = si(gs('cam_total', i))
            res.append([s, s_cash, s_svc, s_kit, s_all, s_cam, rank_map.get(s, 0)])
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
        'code':         'DA07QUMX',
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
        
        # Cashier Area
        'cash_fraud':          sir('cash_fraud'),
        'money_register':      sir('money_register'),
        'cash_drawer':         sir('cash_drawer'),
        'receipt_not_printed': sir('receipt_not_printed'),
        'safe_no_manager':     sir('safe_no_manager'),
        'delivered_no_payment': sir('delivered_no_payment'),
        
        # Service Area
        'no_thermal_bag':      sir('no_thermal_bag'),
        'lost_customer':       sir('lost_customer'),
        'queue_3':             sir('queue_3'),
        'order_uncollected':   sir('order_uncollected'),
        'driver_5min':         sir('driver_5min'),
        'no_security_seal':    sir('no_security_seal'),
        'prep_food_15':        sir('prep_food_15'),
        'not_attended':        sir('not_attended'),
        
        # Kitchen Area
        'kitchen_total':       sir('kitchen_total'),
        'discarded_kitchen':   sir('discarded_kitchen'),
        'dough_rack':          sir('dough_rack'),
        
        # All Areas
        'abnormal_behavior':   sir('abnormal_behavior'),
        'discarded_product':   sir('discarded_product'),
        'removing_product':    sir('removing_product'),
        'consuming_product':   sir('consuming_product'),
        'hiding_product':      sir('hiding_product'),
        'unproductive_staff':  sir('unproductive_staff'),

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
