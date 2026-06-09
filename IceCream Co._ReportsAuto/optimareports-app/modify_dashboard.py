import re

with open('c:/Users/rodri/Desktop/IceCream Co._ReportsAuto/optimareports-app/templates/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace top-meta
content = re.sub(
    r'<div class="top-meta">IceCream Co. México · AlphaFranchise · 62 Tiendas · Abril 2026</div>',
    r'<div class="top-meta">IceCream Co. México · {{ franchise }} · {{ n_stores }} Tiendas · {{ period }}</div>',
    content
)

# Replace const D
content = re.sub(
    r'const D = \{.*?\};',
    r'const D = {{ DATA_JSON | safe }};',
    content
)

# Replace drawDT
dt_orig = """function drawDT() {
  const items = [
    {lbl:'[D] Staff usando PIN pad',col:'var(--delivery)',top:D.dt_pin_top5,total:D.dt_pin},
    {lbl:'[D] Staff fuera caja >1min',col:'var(--rc)',top:D.dt_outside_top5,total:D.dt_outside},
    {lbl:'[D] Cash drawer open',col:'var(--amber)',top:D.dt_cash_top5,total:D.dt_cash},
    {lbl:'[D] Staff móvil/calc',col:'var(--co)',top:D.dt_mobile_top5,total:D.dt_mobile},
  ];
  document.getElementById('dtPanels').innerHTML = items.map(it=>`
    <div class="card">
      <div class="card-title" style="color:${it.col}">${it.lbl} <span class="card-badge">${it.total} alertas</span></div>
      ${it.top.length ? it.top.map((r,i)=>rankRow(i,r[0],r[2].toFixed(1)+'%',it.col)).join('') :
        '<div style="font-size:12px;color:var(--muted);text-align:center;padding:20px 0">Sin alertas en este período</div>'}
    </div>`).join('');
}"""

dt_new = """function drawDT() {
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
  const items = [
    {lbl:'[D] Staff usando PIN pad',col:'var(--delivery)',top:D.dt_pin_top5,total:D.dt_pin},
    {lbl:'[D] Staff fuera caja >1min',col:'var(--rc)',top:D.dt_outside_top5,total:D.dt_outside},
    {lbl:'[D] Cash drawer open',col:'var(--amber)',top:D.dt_cash_top5,total:D.dt_cash},
    {lbl:'[D] Staff móvil/calc',col:'var(--co)',top:D.dt_mobile_top5,total:D.dt_mobile},
  ];
  document.getElementById('dtPanels').innerHTML = items.map(it=>`
    <div class="card">
      <div class="card-title" style="color:${it.col}">${it.lbl} <span class="card-badge">${it.total} alertas</span></div>
      ${it.top.length ? it.top.map((r,i)=>rankRow(i,r[0],r[2].toFixed(1)+'%',it.col)).join('') :
        '<div style="font-size:12px;color:var(--muted);text-align:center;padding:20px 0">Sin alertas en este período</div>'}
    </div>`).join('');
}"""

content = content.replace(dt_orig, dt_new)

with open('c:/Users/rodri/Desktop/IceCream Co._ReportsAuto/optimareports-app/templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
