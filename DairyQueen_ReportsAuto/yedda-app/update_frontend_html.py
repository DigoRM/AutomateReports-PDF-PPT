import re

def main():
    with open('c:/Users/rodri/Desktop/DairyQueen_ReportsAuto/yedda-app/templates/dashboard.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Drive Thru Tab
    dt_old = r'<div class="card">\s*<div class="card-title">Conclusiones Drive Thru[^<]*<span class="card-badge">\{\{ period \}\}</span.*?</div\s*>\s*</div\s*>\s*</div\s*>'
    dt_new = r'''<div class="card" style="padding:0;overflow:hidden">
    <div style="background:var(--drivethru);padding:10px 15px">
      <div style="font-family:'DM Mono',monospace;font-size:10px;text-transform:uppercase;letter-spacing:1.5px;color:#fff;font-weight:700">Ranking Lojas com Alertas Drive Thru</div>
    </div>
    <div class="cam-hdr" style="grid-template-columns:2fr 1fr 1fr 1fr;"><span>Loja</span><span class="ctr">Total Alertas DT</span><span class="ctr">% do Total da Loja</span><span class="ctr">Ranking Geral</span></div>
    <div id="dtRows"></div>
  </div>'''
    # Using re.sub with DOTALL for multiline
    content = re.sub(r'<div class="card">\s*<div class="card-title">Conclusiones Drive Thru.*?</div>\s*</div>', dt_new, content, flags=re.DOTALL)

    # 2. Rankings KBP Tab
    rkbp_old = r'<div class="g12">\s*<div class="card">\s*<div class="card-title">KBP por pilar — distribución visual.*?</div>\s*</div>\s*</div>'
    rkbp_new = r'''<div class="g12" style="grid-template-columns: 1fr;">
    <div class="card">
      <div class="card-title">Ranking Geral Stacked por KBP (CE, RC, CO) <span class="card-badge">{{ period }}</span></div>
      <div style="position:relative;height:350px"><canvas id="cKBPStacked"></canvas></div>
    </div>
  </div>'''
    content = re.sub(rkbp_old, rkbp_new, content, flags=re.DOTALL)

    # 3. Areas Tab
    area_old = r'<div class="g2">\s*<div class="card">\s*<div class="card-title">Distribución por área.*?</div>\s*</div>\s*</div>'
    area_new = r'''<div class="g12" style="grid-template-columns: 1fr;">
    <div class="card">
      <div class="card-title">Ranking Geral Stacked por Área <span class="card-badge">{{ period }}</span></div>
      <div style="position:relative;height:350px"><canvas id="cAreaStacked"></canvas></div>
    </div>
  </div>'''
    content = re.sub(area_old, area_new, content, flags=re.DOTALL)

    # 4. Velocidad Tab
    vel_old = r'<div class="g12" style="margin-bottom:16px">\s*<div class="card">\s*<div class="card-title">Distribución Service Time.*?</div>\s*</div>\s*<div class="g4" id="speedCards"></div>'
    vel_new = r'<div class="g12" style="grid-template-columns: repeat(5, 1fr);" id="speedCards"></div>'
    content = re.sub(r'<div class="g12" style="margin-bottom:16px">.*?<div class="g4" id="speedCards"></div>', vel_new, content, flags=re.DOTALL)

    # 5. KBP Desglose Tabs
    content = content.replace('<canvas id="cCE"></canvas>', '<canvas id="cCEStacked"></canvas>')
    content = content.replace('<canvas id="cRC"></canvas>', '<canvas id="cRCStacked"></canvas>')
    content = content.replace('<canvas id="cCO"></canvas>', '<canvas id="cCOStacked"></canvas>')
    content = re.sub(r'<div class="card-title">CE por tipo.*?</div>', r'<div class="card-title">Top 10 Lojas Stacked por Área</div>', content)
    content = re.sub(r'<div class="card-title">RC por tipo.*?</div>', r'<div class="card-title">Top 10 Lojas Stacked por Área</div>', content)
    content = re.sub(r'<div class="card-title">CO por tipo.*?</div>', r'<div class="card-title">Top 10 Lojas Stacked por Área</div>', content)

    # 6. Delivery Tab
    del_old = r'<div class="g21">.*?</div>\s*</div>\s*<!-- ═══════════ TAB DRIVE THRU'
    del_new = r'''<div class="g2" style="margin-bottom:14px">
    <div class="card">
      <div class="card-title">Delivery Wait Avg <span class="card-badge">alertas de espera</span></div>
      <div style="display:flex;align-items:flex-end;gap:16px;margin-bottom:16px">
        <div style="font-family:'DM Mono',monospace;font-size:56px;font-weight:700;color:var(--delivery);line-height:1" id="delAvgLabel"></div>
        <div style="padding-bottom:6px"><div style="font-size:12px;color:var(--muted)">min · promedio del grupo</div></div>
      </div>
      <table class="tbl">
        <thead><tr><th>Alerta</th><th class="r">N</th><th class="r">%</th></tr></thead>
        <tbody>
          <tr><td>Delivery guy waiting &gt;1min</td><td class="r" style="color:var(--delivery)" id="delWaitLabel"></td><td class="r" id="delWaitPctLabel"></td></tr>
          <tr><td>Check packaging</td><td class="r" style="color:var(--delivery)" id="delPkgLabel"></td><td class="r" id="delPkgPctLabel"></td></tr>
        </tbody>
      </table>
    </div>
    <div class="card">
      <div class="card-title">Distribución Delivery <span class="card-badge">visual</span></div>
      <div style="position:relative;height:210px"><canvas id="cDelDist"></canvas></div>
    </div>
  </div>
  <div class="card" style="padding:0;overflow:hidden">
    <div style="background:var(--delivery);padding:10px 15px">
      <div style="font-family:'DM Mono',monospace;font-size:10px;text-transform:uppercase;letter-spacing:1.5px;color:#fff;font-weight:700">Ranking Lojas - Delivery Time</div>
    </div>
    <div class="cam-hdr" style="grid-template-columns:2fr 1fr 1fr 1fr 1.5fr;"><span>Loja</span><span class="ctr">Delivery Time</span><span class="ctr">Service Time</span><span class="ctr">Total Alertas (Loja)</span><span class="ctr">% Alertas Delivery</span></div>
    <div id="delRows"></div>
  </div>
</div>
<!-- ═══════════ TAB DRIVE THRU'''
    content = re.sub(r'<div class="g21">.*?</div>\s*</div>\s*<!-- ═══════════ TAB DRIVE THRU', del_new, content, flags=re.DOTALL)

    # 7. Cam Check Tab
    content = content.replace('>66<', ' id="camTotalLabel">0<')
    content = content.replace('>43 tiendas afectadas de 62<', ' id="camStoresLabel">0 tiendas afectadas<')
    content = re.sub(r'<div class="br" style="border-bottom:1px solid rgba\(30,45,69,\.5\)">.*?</div>\s*</div>\s*<div class="card">', r'<div id="camBars"></div></div>\n      <div class="card">', content, flags=re.DOTALL)

    with open('c:/Users/rodri/Desktop/DairyQueen_ReportsAuto/yedda-app/templates/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    main()
