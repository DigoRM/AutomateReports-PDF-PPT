# Yedda AI — Script Completo para Agente de Vibe Coding
## DQ México · Report Automation App
**Versão:** 3.0 · Maio 2026 · Refinado com Claude (Anthropic)

---

## COMO USAR ESTE DOCUMENTO

Este script deve ser colado diretamente no agente de vibe coding (Cursor, Windsurf,
Claude Code, etc.) junto com os seguintes arquivos de referência:

| Arquivo | Papel |
|---------|-------|
| `Yedda_Vibecoding_Script.md` | Este documento — arquitetura, parser, regras |
| `DQ_Zamabrands_Abril2026_Dashboard.html` | **TEMPLATE BASE** — copiar e adaptar para Jinja2 |
| `DQ_Variables_Dinamicas.html` | Referência visual de todas as variáveis com exemplos reais |
| Planilhas `.xlsx` | Dados reais para testar o parser |

**Leia os 3 documentos completamente antes de escrever qualquer linha de código.**

---

## 1. VISÃO GERAL DO APP

O app recebe um arquivo Excel por franquia (exportado pelo Yedda AI) e gera
um relatório HTML interativo com 10 tabs e gráficos Chart.js.

**Fluxo:**
```
Upload Excel (.xlsx) + seleção de franquia + mês
        ↓
Parser Python → dict de variáveis (const D)
        ↓
Jinja2 injeta no dashboard.html (substitui const D = {...})
        ↓
HTML final entregue ao usuário com botão PDF
        ↓
Download PDF via window.print() — já implementado no template
```

**Stack:**
- Backend: Python 3 + Flask
- Parse Excel: `zipfile` stdlib (sem openpyxl, sem dependências externas)
- Template: Jinja2 — adaptar `DQ_Zamabrands_Abril2026_Dashboard.html`
- Frontend: HTML/CSS/JS puro + Chart.js 4.4.1 (cdnjs) — já no template
- PDF: `window.print()` — já implementado no template

**Estrutura de pastas:**
```
yedda-app/
├── app.py
├── parser.py
├── requirements.txt          (flask — único requisito)
├── templates/
│   ├── index.html            (tela de upload — criar do zero)
│   └── dashboard.html        (copiar DQ_Zamabrands_Abril2026_Dashboard.html e adaptar)
└── uploads/                  (temporário)
```

---

## 2. ADAPTAÇÃO DO TEMPLATE HTML

O arquivo `DQ_Zamabrands_Abril2026_Dashboard.html` já tem todo o CSS, JS,
Chart.js e estrutura das 10 tabs funcionando. A única mudança necessária é
substituir o bloco de dados hardcoded pelo placeholder Jinja2.

**Localizar no arquivo:**
```javascript
const D = {"franchise":"Zamabrands", ... };
```

**Substituir por:**
```javascript
const D = {{ DATA_JSON | safe }};
```

Também substituir no topbar os valores hardcoded:
```html
<!-- ANTES -->
<div class="top-meta">Dairy Queen México · Zamabrands · 62 Tiendas · Abril 2026</div>

<!-- DEPOIS -->
<div class="top-meta">Dairy Queen México · {{ franchise }} · {{ n_stores }} Tiendas · {{ period }}</div>
```

**Para o tab Drive Thru — já existe no template, adicionar lógica condicional:**
```javascript
function drawDT() {
  if (!D.has_drive_thru) {
    document.getElementById('dtPanels').innerHTML = `
      <div style="grid-column:1/-1;text-align:center;padding:60px;color:var(--muted)">
        <div style="font-size:40px;margin-bottom:16px">🚗</div>
        <div style="font-size:15px;font-weight:600;color:var(--bright)">
          Sin alertas Drive Thru en este período
        </div>
        <div style="font-size:12px;margin-top:8px;font-style:italic">
          Esta franquicia no registró incidencias en estaciones Drive Thru.
        </div>
      </div>`;
    return;
  }
  // resto da função já existente no template...
}
```

---

## 3. AS 4 FRANQUIAS — CONFIGURAÇÃO E DIFERENÇAS

O app DEVE suportar seleção de franquia na tela de upload.
Cada franquia tem características distintas que afetam a renderização:

| Franquia   | Lojas (Abril) | Sufixo loja | Drive Thru real?                     | Março? |
|------------|---------------|-------------|--------------------------------------|--------|
| Peninsula  | 9             | numérico    | ❌ 1 alerta apenas — tratar como sem | ✅     |
| Ganfer     | 20            | `[g]`       | ✅ 9 lojas · 10 alertas DT           | ❌     |
| Leva       | 17            | numérico    | ✅ 10 lojas · **154 alertas DT**     | ✅     |
| Zamabrands | 62–63         | `[z]`       | ❌ zero alertas DT                   | ✅     |

**Dados reais Drive Thru — Leva Abril 2026 (para teste):**
```
dt_total:    154   dt_pin: 64   dt_outside: 50   dt_mobile: 15
dt_cash:      13   dt_receipt: 12
Top lojas: 51 Concordia (35), 58 La puerta (28), 52 Contry (27)
```

**Config Python:**
```python
# parser.py
FRANCHISES = {
    'Peninsula':  {'expected_stores': 9,  'has_drive_thru': False},
    'Ganfer':     {'expected_stores': 20, 'has_drive_thru': True},
    'Leva':       {'expected_stores': 17, 'has_drive_thru': True},
    'Zamabrands': {'expected_stores': 63, 'has_drive_thru': False},
}

AVAILABLE_MONTHS = {
    'Peninsula':  ['Marzo 2026', 'Abril 2026'],
    'Ganfer':     ['Abril 2026'],   # sem dados em Março
    'Leva':       ['Marzo 2026', 'Abril 2026'],
    'Zamabrands': ['Marzo 2026', 'Abril 2026'],
}
```

**Nota:** `has_drive_thru` no dict final é calculado dos dados reais:
```python
data['has_drive_thru'] = data['dt_total'] > 0
# Não depende da config acima — depende do que vier no Excel
```

---

## 4. MAPEAMENTO COMPLETO: KBP → ROW → ALERTA

Row indices FIXOS para todos os arquivos Yedda com este template.
- **Col 1** = total da rede (usar para totais e médias)
- **Col 2..N** = lojas individuais (N varia por franquia)
- **Row 5** = header com nomes das lojas nas colunas 2..N

### KBP CE — Customer Experience
**Fórmula oficial:** `m135125 + m139967 + m135122 + m139966 + m139963 + m135143 + m139962`

| Row | ID Yedda | Alerta | Área |
|-----|----------|--------|------|
| 33 | m135125 | Client not attended for over 1 minute | Cashier |
| 34 | m139967 | Counter dirty for over 3 min (cashier) | Cashier |
| 36 | m135122 | More than 3 people in line (1 register) | Cashier |
| 41 | m139966 | Receive order for over 3 minutes | Cashier |
| 61 | m139963 | Complaining customer | All Store |
| 62 | m135143 | Dirty floor for over 3 minutes | All Store |
| 64 | m139962 | Lost customer | All Store |

### KBP CO — Operational Compliance
**Fórmula oficial:** `m135152 + m135146 + m135155 + m135156 + m139965 + m142009`

| Row | ID Yedda | Alerta | Área |
|-----|----------|--------|------|
| 68 | m135152 | Staff without caps | All Store |
| 69 | m135146 | Staff without uniform | All Store |
| **79** | **m135155** | **Delivery guy waiting more than 1 minute** | **Delivery ← CO, NÃO RC!** |
| 80 | m135156 | Delivery man putting product in clothes | Delivery |
| 81 | m139965 | Package closed | Delivery |
| 63 | m142009 | Incomplete refrigerators (novelties) | All Store |

### KBP RC — Reduce Costs (31 alertas — exibir top 8 dinâmico)
**Inclui todos os alertas [D] Drive Thru**

| Row | ID Yedda | Alerta | Área |
|-----|----------|--------|------|
| 32 | m135120 | Cash drawer open and unattended | Cashier |
| 42 | m139970 | Staff outside cash register >1min | Cashier |
| 44 | m135128 | Staff using calculator/mobile phone | Cashier |
| 45 | m139969 | Staff using customer PIN pad | Cashier |
| 70 | m135153 | Store close sooner | All Store |
| 71 | m135150 | Store open late | All Store |
| 65 | m135147 | More than 2 staff inactive >5min | All Store |
| 66 | m135144 | Personal playing or fighting | All Store |
| 78 | m139964 | Check packaging | Delivery |
| 39 | m135131 | Receipt not given Counter | Cashier |
| 40 | m135126 | Receipt not printed Counter | Cashier |
| 85 | m139981 | [D] Cash drawer open and unattended | Drive Thru |
| 88 | m139974 | [D] Receipt not delivered | Drive Thru |
| 91 | m139978 | [D] Staff outside cash register >1min | Drive Thru |
| 94 | m139976 | [D] Staff using calculator/mobile phone | Drive Thru |
| 95 | m139977 | [D] Staff using customer PIN pad | Drive Thru |

### Totais e Tempos

| Row | Variável | Tipo | Nota |
|-----|----------|------|------|
| 7  | CE | int | KBP Customer Experience total |
| 8  | CO | int | KBP Operational Compliance total |
| 9  | RC | int | KBP Reduce Costs total |
| 10 | KBP | int | CE + RC + CO |
| 12 | all_alerts | int | ∑ todas as áreas |
| 14 | svc_time | MM:SS | Service Time avg |
| 15 | pct_lt3 | float% | % transações < 3min |
| 16 | pct_3to5 | float% | % transações 3–5min |
| 17 | pct_gt5 | float% | % transações > 5min |
| 18 | ordering | MM:SS | Ordering Time avg |
| 22 | queue | MM:SS | Queue Time avg |
| 26 | receiving | MM:SS | Receiving Time avg |
| 30 | cash_total | int | Total Cashier Area |
| 48 | cam_total | int | Total Cam Check |
| 50 | cam_blurry | int | Blurry Image |
| 51 | cam_lagging | int | Camera lagging |
| 52 | cam_connect | int | Can't connect |
| 53 | cam_lost | int | Lost Connection |
| 54 | cam_obstructed | int | Obstructed |
| 60 | allstore_total | int | Total All Store |
| 73 | del_time | MM:SS | Delivery waiting time avg |
| 74 | del_lt2 | float% | Delivery < 2min % |
| 75 | del_2to3 | float% | Delivery 2–3min % |
| 76 | del_gt3 | float% | Delivery > 3min % |
| 77 | delivery_total | int | Total Delivery alerts |
| 83 | dt_total | int | Total Drive Thru alerts |

---

## 5. PARSER PYTHON COMPLETO

Copiar integralmente para `parser.py`:

```python
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
    ('Receive order >3min',       'receive_3min'),
    ('+3 personas en fila',       'queue_3'),
    ('Cliente no atendido >1min', 'not_attended'),
    ('Lost customer',             'lost_customer'),
    ('Dirty floor >3min',         'dirty_floor'),
    ('Complaining customer',      'complaining'),
]
KBP3_CO = [
    ('Staff sin gorra',                  'no_cap'),
    ('Staff sin uniforme',               'no_uniform'),
    ('Delivery guy waiting >1min',       'delivery_wait'),  # CO!
    ('Delivery man product in clothes',  'del_clothes'),
    ('Package closed',                   'pkg_closed'),
    ('Incomplete refrigerators',         'incomplete_fridge'),
]
KBP2_RC_ALL = [
    ('Cash drawer open',          'cash_drawer'),
    ('Staff fuera caja >1min',    'outside'),
    ('Staff móvil/calc',          'mobile'),
    ('PIN pad misuse',            'pin_cashier'),
    ('Store close sooner',        'close_sooner'),
    ('Store open late',           'open_late'),
    ('Staff inactivo >5min',      'inactive'),
    ('Playing/fighting',          'playing'),
    ('Check packaging',           'check_packaging'),
    ('Receipt not given',         'receipt_given'),
    ('Receipt not printed',       'receipt_print'),
    ('[D] Cash drawer',           'dt_cash'),
    ('[D] Receipt not delivered', 'dt_receipt'),
    ('[D] Staff fuera caja',      'dt_outside'),
    ('[D] Staff móvil',           'dt_mobile'),
    ('[D] PIN pad',               'dt_pin'),
]

def parse_franchise(xlsx_path, franchise_name, period, period_long):
    rows = read_xlsx(xlsx_path)
    header = rows[5]
    stores = [h.strip() for h in header[2:] if h.strip()]
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
        return {k: [[s, v] for s, v in store_int_rank(k)[:5]]
                for _, k, _ in alerts if k in ROW}

    all_types = kbp_dyn(KBP1_CE + KBP3_CO + KBP2_RC_ALL)
    top5_types = sorted(
        [{'label': l, 'val': v,
          'pct': round(v/kbp_total*100, 1) if kbp_total else 0}
         for l, k, v in all_types if v > 0],
        key=lambda x: -x['val']
    )[:5]

    dt_total = sir('dt_total')

    def dt_top5(k):
        total = sir(k)
        if total == 0: return []
        return [[s, v, round(v/total*100, 1)]
                for s, v in store_int_rank(k)[:5] if v > 0]

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

    return {
        'franchise':    franchise_name,
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
        'kbp_top5':  [[s, v, round(v/kbp_total*100, 1)] for s, v in store_int_rank('KBP')[:5]],
        'kbp_worst': [store_int_rank('KBP')[0][0], round(store_int_rank('KBP')[0][1]/kbp_total*100, 1)],
        'kbp_best':  [all_ranked[-1][0], round(all_ranked[-1][1]/max(sir('all_alerts'),1)*100, 1)],
        'ce_top5':   [[s, v, round(v/max(ce,1)*100, 1)] for s, v in store_int_rank('CE')[:5]],
        'rc_top5':   [[s, v, round(v/max(rc,1)*100, 1)] for s, v in store_int_rank('RC')[:5]],
        'co_top5':   [[s, v, round(v/max(co,1)*100, 1)] for s, v in store_int_rank('CO')[:5]],
        'ord_top5_fast': [[s, mmss(t)] for s, t in store_time_rank('ordering')[:5]],
        'top5_alert_types': top5_types,
        'dt_pin_top5':     dt_top5('dt_pin'),
        'dt_outside_top5': dt_top5('dt_outside'),
        'dt_cash_top5':    dt_top5('dt_cash'),
        'dt_mobile_top5':  dt_top5('dt_mobile'),
        'cam_stores': cam_stores,
    }
```

---

## 6. INTEGRAÇÃO FLASK — app.py COMPLETO

```python
# app.py
from flask import Flask, request, render_template, jsonify
from parser import parse_franchise
import json, os, tempfile

app = Flask(__name__)

FRANCHISES = ['Peninsula', 'Ganfer', 'Leva', 'Zamabrands']

AVAILABLE_MONTHS = {
    'Peninsula':  ['Marzo 2026', 'Abril 2026'],
    'Ganfer':     ['Abril 2026'],
    'Leva':       ['Marzo 2026', 'Abril 2026'],
    'Zamabrands': ['Marzo 2026', 'Abril 2026'],
}

@app.route('/')
def index():
    return render_template('index.html',
                           franchises=FRANCHISES,
                           available_months=AVAILABLE_MONTHS)

@app.route('/generate', methods=['POST'])
def generate():
    # Validações
    if 'excel' not in request.files:
        return 'Arquivo Excel não enviado', 400

    file      = request.files['excel']
    franchise = request.form.get('franchise', '')
    period    = request.form.get('period', '')
    period_long = request.form.get('period_long', f'01 – 30 {period}')

    if franchise not in FRANCHISES:
        return f'Franquia inválida: {franchise}', 400

    if not file.filename.endswith('.xlsx'):
        return 'Apenas arquivos .xlsx são aceitos', 400

    # Verificar disponibilidade do mês
    if period not in AVAILABLE_MONTHS.get(franchise, []):
        # Aviso mas não bloqueia — pode ser um mês novo
        pass

    # Salvar temporariamente e parsear
    tmp = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
    file.save(tmp.name)

    try:
        data = parse_franchise(tmp.name, franchise, period, period_long)
    except Exception as e:
        return f'Erro ao processar o arquivo: {str(e)}', 500
    finally:
        os.unlink(tmp.name)

    return render_template(
        'dashboard.html',
        DATA_JSON=json.dumps(data, ensure_ascii=False),
        franchise=franchise,
        period=period,
        n_stores=data['n_stores'],
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

---

## 7. TELA DE UPLOAD — index.html

Criar com visual dark consistente com o dashboard:

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Yedda AI · Generar Reporte DQ México</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&family=DM+Mono:wght@400&display=swap" rel="stylesheet">
<style>
:root{--bg:#0A0F1A;--surface:#111828;--card:#161F30;--border:#1E2D45;--ce:#52B788;--text:#C8D8EC;--muted:#4A6080;--bright:#EDF4FF;}
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:'DM Sans',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px 20px;}
.logo{font-family:'Syne',sans-serif;font-size:22px;font-weight:800;color:var(--ce);margin-bottom:8px;}
.logo span{color:var(--bright);}
.subtitle{font-size:13px;color:var(--muted);margin-bottom:40px;font-family:'DM Mono',monospace;}
.form-card{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:36px 40px;width:100%;max-width:480px;}
.form-title{font-family:'Syne',sans-serif;font-size:20px;font-weight:700;color:var(--bright);margin-bottom:28px;}
.field{margin-bottom:20px;}
label{display:block;font-family:'DM Mono',monospace;font-size:10px;text-transform:uppercase;letter-spacing:1px;color:var(--muted);margin-bottom:8px;}
select,input[type=text]{width:100%;background:var(--card);border:1px solid var(--border);color:var(--text);border-radius:8px;padding:10px 14px;font-family:'DM Sans',sans-serif;font-size:14px;outline:none;transition:border-color .2s;}
select:focus,input:focus{border-color:var(--ce);}
.file-area{border:2px dashed var(--border);border-radius:8px;padding:28px;text-align:center;cursor:pointer;transition:all .2s;}
.file-area:hover{border-color:var(--ce);background:rgba(82,183,136,.04);}
.file-area input{display:none;}
.file-label{font-size:13px;color:var(--muted);}
.file-label strong{color:var(--ce);}
.file-name{font-family:'DM Mono',monospace;font-size:12px;color:var(--ce);margin-top:8px;}
.btn{width:100%;background:var(--ce);color:#0A0F1A;border:none;border-radius:8px;padding:13px;font-family:'Syne',sans-serif;font-weight:700;font-size:15px;cursor:pointer;margin-top:8px;letter-spacing:.5px;transition:opacity .2s;}
.btn:hover{opacity:.85;}
.btn:disabled{opacity:.4;cursor:not-allowed;}
.loading{display:none;text-align:center;margin-top:16px;font-size:13px;color:var(--muted);}
</style>
</head>
<body>
<div class="logo">Yedda<span>.ai</span></div>
<div class="subtitle">DA07QUMX · Dairy Queen México · Report Generator</div>

<div class="form-card">
  <div class="form-title">Generar Reporte Mensual</div>
  <form action="/generate" method="POST" enctype="multipart/form-data" id="reportForm">

    <div class="field">
      <label>Franquicia</label>
      <select name="franchise" id="franchiseSelect" required>
        <option value="">— Seleccionar —</option>
        {% for f in franchises %}
        <option value="{{ f }}">{{ f }}</option>
        {% endfor %}
      </select>
    </div>

    <div class="field">
      <label>Período</label>
      <input type="text" name="period" placeholder="Abril 2026" required />
    </div>

    <div class="field">
      <label>Período completo</label>
      <input type="text" name="period_long" placeholder="01 – 30 Abril 2026" required />
    </div>

    <div class="field">
      <label>Archivo Excel (.xlsx)</label>
      <div class="file-area" onclick="document.getElementById('fileInput').click()">
        <input type="file" id="fileInput" name="excel" accept=".xlsx" required
               onchange="document.getElementById('fileName').textContent=this.files[0]?.name||''">
        <div class="file-label">Clique para seleccionar o <strong>arrastre</strong> el archivo</div>
        <div class="file-name" id="fileName"></div>
      </div>
    </div>

    <button type="submit" class="btn" id="submitBtn">Generar Reporte →</button>
    <div class="loading" id="loading">⏳ Procesando archivo...</div>
  </form>
</div>

<script>
document.getElementById('reportForm').onsubmit = function() {
  document.getElementById('submitBtn').disabled = true;
  document.getElementById('loading').style.display = 'block';
};
</script>
</body>
</html>
```

---

## 8. REGRAS CRÍTICAS DE RENDERIZAÇÃO

### Barras proporcionais — normalizar pelo MAX da lista
```javascript
// CORRETO — proporcional ao maior valor da lista
const maxVal = Math.max(...list.map(r => r.val));
barWidth = `${(val / maxVal * 100).toFixed(0)}%`;

// ERRADO — não usar o total KBP
barWidth = `${(val / D.kbp * 100).toFixed(0)}%`;
```

### RC — top 8 dinâmico (varia por franquia e mês)
```python
# Leva tem [D] alerts no top8; Zamabrands não tem DT → [D] nunca aparecem
kbp2 = sorted(all_rc_alerts, key=lambda x: -x[2])[:8]
```

### Remover sufixos dos nomes de loja na exibição
```javascript
const sn = s => s.replace(/ \[.\]$/, '');
// "DQ ARAGON [z]" → "DQ ARAGON"
// "DQ Hampton [g]" → "DQ Hampton"
// já implementado no template — não remover esta função
```

### Drive Thru — sempre renderizar tab, conteúdo condicional
```javascript
// has_drive_thru vem do parser — True se dt_total > 0
if (!D.has_drive_thru) { /* mostrar mensagem */ return; }
// senão renderizar painéis normalmente
```

### Filtrar val > 0 antes de renderizar qualquer painel KBP
```python
kbp1 = [(l, k, v) for l, k, v in alerts if v > 0]
# painéis vazios não aparecem — layout dinâmico
```

### Cam stores — max 14 linhas, sorted desc por cam
```python
cam_stores = sorted(cam_list, key=lambda x: -x['cam'])[:14]
```

---

## 9. PALETA DE CORES

```css
--ce:        #52B788;   /* KBP Customer Experience */
--rc:        #E63B7A;   /* KBP Reduce Costs */
--co:        #4BBFBF;   /* KBP Operational Compliance */
--cashier:   #D4A017;   /* Área Cashier */
--allstore:  #C05621;   /* Área All Store */
--delivery:  #7B52AB;   /* Área Delivery */
--drivethru: #2C7DA0;   /* Área Drive Thru */
--green:     #10B981;   /* positivo / mais rápido */
--amber:     #F59E0B;   /* atenção */
--danger:    #EF4444;   /* negativo / mais lento */
--red2:      #C0392B;   /* top5 negativos */
--cam:       #E8A838;   /* cam check */
--bg:        #0A0F1A;
--surface:   #111828;
--card:      #161F30;
--border:    #1E2D45;
--muted:     #4A6080;
--text:      #C8D8EC;
--bright:    #EDF4FF;
```

---

## 10. CHECKLIST FINAL

- [ ] Ler os 3 arquivos de referência ANTES de escrever código
- [ ] `DQ_Zamabrands_Abril2026_Dashboard.html` = template base → adaptar para Jinja2
- [ ] `DQ_Variables_Dinamicas.html` = referência de todas as variáveis com exemplos
- [ ] Parser usa `zipfile` stdlib — sem openpyxl
- [ ] Row 79 (`delivery_wait`) = **KBP CO** — não RC
- [ ] RC exibe apenas top 8 dinâmico
- [ ] `has_drive_thru = dt_total > 0` — calculado dos dados reais
- [ ] Tab Drive Thru SEMPRE aparece — conteúdo é condicional
- [ ] Ganfer sem dados em Março — não bloquear, apenas avisar
- [ ] Filtrar alertas com val > 0 antes de renderizar painéis
- [ ] Barras: normalizar pelo max da lista
- [ ] Sufixos [z],[g] removidos via `sn()` — função já existe no template
- [ ] Cam stores: sorted desc por cam, max 14 linhas
- [ ] `const D = {{ DATA_JSON | safe }}` — injeção via Jinja2
- [ ] Testar com planilha da Leva para validar Drive Thru real
- [ ] PDF via `window.print()` — já implementado no template

---

*Yedda AI · DQ México Report Automation · Script v3.0 · Maio 2026*
