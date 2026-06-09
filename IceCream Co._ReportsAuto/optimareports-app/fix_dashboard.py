import re

with open('c:/Users/rodri/Desktop/IceCream Co._ReportsAuto/optimareports-app/templates/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Title
content = re.sub(r'<title>IC AlphaFranchise · Abril 2026 · DA07QUMX</title>',
                 r'<title>IC {{ franchise }} · {{ period }} · DA07QUMX</title>', content)

# 2. Hardcoded dates and counts
content = content.replace('Abril 2026', '{{ period }}')
content = content.replace('1,959 alertas', '<span id="kbpTotalLabel"></span> alertas')

# 3. Delivery Insight
del_ins_old = r'<div class="ins"><span style="font-size:18px">📊</span><span><strong>Insight:</strong> Mejor: IC TOWN SQUARE \(0:41\) &nbsp;·&nbsp; Peor: IC SAN ANGEL \(5:07\) &nbsp;·&nbsp; 21.35% supera los 3 minutos de espera</span></div>'
del_ins_new = r'<div class="ins" id="delInsight"></div>'
content = re.sub(del_ins_old, del_ins_new, content)

# 4. Drive Thru hardcoded insight
dt_ins_old = r'<div class="ins"><span>🚗</span><span>AlphaFranchise registró <strong>0 alertas Drive Thru</strong> en \{\{ period \}\}. Las estaciones de Drive Thru operaron sin incidencias detectadas en este período.</span></div>'
content = re.sub(dt_ins_old, r'<div class="ins" id="dtInsight"></div>', content)

# 5. Fix Print CSS
css_old = r'''@media print{
  .topbar,.tabs-bar{display:none!important;}
  .tc{display:block!important;}
  .card{page-break-inside:avoid;border:1px solid #ccc;background:#fff;color:#111;}
  body{background:#fff;color:#111;}
  :root{--bg:#fff;--surface:#f5f5f5;--card:#f0f0f0;--border:#ddd;--text:#222;--muted:#666;--bright:#000;}
}'''
css_new = r'''@media print{
  @page { size: A4 landscape; margin: 10mm; }
  .topbar,.tabs-bar{display:none!important;}
  .tc{display:block!important; page-break-after: always; padding-top: 0 !important;}
  .main{padding: 0 !important;}
  body{-webkit-print-color-adjust: exact; print-color-adjust: exact;}
}'''
content = content.replace(css_old, css_new)

# 6. Add JS to populate the new dynamic elements at the end
js_add = r'''
document.getElementById('kbpTotalLabel').textContent = fmt(D.kbp);
if(D.del_fast.length > 0 && D.del_slow.length > 0) {
    document.getElementById('delInsight').innerHTML = `<span style="font-size:18px">📊</span><span><strong>Insight:</strong> Mejor: ${sn(D.del_fast[0][0])} (${D.del_fast[0][1]}) &nbsp;·&nbsp; Peor: ${sn(D.del_slow[0][0])} (${D.del_slow[0][1]}) &nbsp;·&nbsp; ${D.del_gt3}% supera los 3 minutos de espera</span>`;
} else {
    document.getElementById('delInsight').style.display = 'none';
}
if(D.has_drive_thru) {
    document.getElementById('dtInsight').innerHTML = `<span>🚗</span><span>${D.franchise} registró <strong>${D.dt_total} alertas Drive Thru</strong> en ${D.period}.</span>`;
} else {
    document.getElementById('dtInsight').innerHTML = `<span>🚗</span><span>${D.franchise} registró <strong>0 alertas Drive Thru</strong> en ${D.period}. Las estaciones operaron sin incidencias detectadas.</span>`;
}
'''
content = content.replace("drawn.add('resumen');\ndrawResumen();", "drawn.add('resumen');\ndrawResumen();\n" + js_add)

with open('c:/Users/rodri/Desktop/IceCream Co._ReportsAuto/optimareports-app/templates/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)
