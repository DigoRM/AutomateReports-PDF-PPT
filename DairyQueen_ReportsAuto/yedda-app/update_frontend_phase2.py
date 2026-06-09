import re
import json

def apply_html_updates():
    with open('c:/Users/rodri/Desktop/DairyQueen_ReportsAuto/yedda-app/templates/dashboard.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Add custom purple KBP color
    html = html.replace("--cashier:#D4A017;", "--cashier:#D4A017;--kbp-purple:#8B5CF6;")

    # 1. Resumen Tab
    # Remove "Indicadores de Servicio" card
    ind_card = r'<div class="card">\s*<div class="card-title">Indicadores de Servicio.*?</div>\s*</div>\s*</div>'
    html = re.sub(ind_card, '', html, flags=re.DOTALL)

    # Wrap KBPDist in g2 and add AreaDist
    kbp_dist = r'<div class="card">\s*<div class="card-title">Distribución por KBP <span class="card-badge">visual</span></div>\s*<div style="position:relative;height:210px"><canvas id="cKBPDist"></canvas></div>\s*</div>'
    kbp_area_dist = r'''<div class="g2">
    <div class="card">
      <div class="card-title">Distribución por KBP <span class="card-badge">visual</span></div>
      <div style="position:relative;height:210px"><canvas id="cKBPDist"></canvas></div>
    </div>
    <div class="card">
      <div class="card-title">Distribución por Área <span class="card-badge">visual</span></div>
      <div style="position:relative;height:210px"><canvas id="cAreaDist"></canvas></div>
    </div>
  </div>'''
    html = re.sub(kbp_dist, kbp_area_dist, html, count=1, flags=re.DOTALL)

    # Replace Mejor/Peor Tienda and Ordering Time
    old_tiendas = r'<div class="g2" style="margin-bottom:16px">\s*<div class="card" style="grid-column:1/-1">.*?</div>\s*<div class="card">\s*<div class="card-title">Ranking Tiendas.*?</div>\s*</div>\s*</div>'
    # Actually, the original structure might differ slightly. I will target everything from the start of `<div class="g2" style="margin-bottom:16px">` to the end of the `</div>` before `<div class="g21">` (Top Alerta/Top Loja)
    
    new_tiendas = r'''<div class="g2" style="margin-bottom:16px">
    <div class="card">
      <div class="card-title">Desempeño de Tiendas (Alertas Totales)</div>
      <div class="sp-hdr" style="color:var(--green)">🌟 MEJOR (MENOS ALERTAS)</div>
      <div class="rr"><span class="rr-name" id="bestStoreName"></span><span style="font-family:'DM Mono',monospace;font-size:11px;font-weight:700;color:var(--green)" id="bestStoreAlerts"></span></div>
      <div class="sp-hdr" style="color:var(--danger);margin-top:10px">🐌 PEOR (MÁS ALERTAS)</div>
      <div class="rr"><span class="rr-name" id="worstStoreName"></span><span style="font-family:'DM Mono',monospace;font-size:11px;font-weight:700;color:var(--danger)" id="worstStoreAlerts"></span></div>
    </div>
    <div class="card">
      <div class="card-title">Tiempos Rápidos y Lentos</div>
      <div class="sp-hdr" style="color:var(--rc)">SERVICE TIME (MÁS RÁPIDO / MÁS LENTO)</div>
      <div class="rr"><span class="rr-name" id="bestSvcName"></span><span style="font-family:'DM Mono',monospace;font-size:11px;font-weight:700;color:var(--rc)" id="bestSvcTime"></span></div>
      <div class="rr"><span class="rr-name" id="worstSvcName"></span><span style="font-family:'DM Mono',monospace;font-size:11px;font-weight:700;color:var(--rc)" id="worstSvcTime"></span></div>
      <div class="sp-hdr" style="color:var(--delivery);margin-top:10px">DELIVERY TIME (MÁS RÁPIDO / MÁS LENTO)</div>
      <div class="rr"><span class="rr-name" id="bestDelName"></span><span style="font-family:'DM Mono',monospace;font-size:11px;font-weight:700;color:var(--delivery)" id="bestDelTime"></span></div>
      <div class="rr"><span class="rr-name" id="worstDelName"></span><span style="font-family:'DM Mono',monospace;font-size:11px;font-weight:700;color:var(--delivery)" id="worstDelTime"></span></div>
    </div>
  </div>'''
    html = re.sub(r'<div class="g2" style="margin-bottom:16px">\s*<div class="card" style="grid-column:1/-1">.*?</div>\s*<div class="card">.*?</div>\s*</div>', new_tiendas, html, flags=re.DOTALL)

    # Change Top 5 -> Top 10 texts
    html = html.replace('Top 5 Alertas Globales', 'Top 10 Alertas Globales')
    html = html.replace('Top 5 Lojas', 'Top 10 Lojas')

    # Fix Area Badges hardcoded numbers
    # We will replace them with dynamic IDs
    html = html.replace('<div class="area-badge" style="background:var(--cashier)">1,251<small>61.8%</small></div>', '<div class="area-badge" style="background:var(--cashier)" id="bdgCashier">0<small>0.0%</small></div>')
    html = html.replace('<div class="area-badge" style="background:var(--allstore)">534<small>26.4%</small></div>', '<div class="area-badge" style="background:var(--allstore)" id="bdgAllStore">0<small>0.0%</small></div>')
    html = html.replace('<div class="area-badge" style="background:var(--delivery)">174<small>8.6%</small></div>', '<div class="area-badge" style="background:var(--delivery)" id="bdgDelivery">0<small>0.0%</small></div>')
    html = html.replace('<div class="area-badge" style="background:var(--drivethru)">0<small>0.0%</small></div>', '<div class="area-badge" style="background:var(--drivethru)" id="bdgDriveThru">0<small>0.0%</small></div>')
    # Add CamCheck badge ID
    html = html.replace('<div class="area-badge" style="background:var(--cam)">66<small>3.3%</small></div>', '<div class="area-badge" style="background:var(--cam)" id="bdgCam">0<small>0.0%</small></div>')

    # Update Velocidad Layout
    # Change "grid-template-columns: repeat(5, 1fr);" to "grid-template-columns: 1fr;"
    html = html.replace('<div class="g12" style="grid-template-columns: repeat(5, 1fr);" id="speedCards"></div>', '<div class="g12" style="grid-template-columns: 1fr;" id="speedCards"></div>')

    # KBP Tabs
    html = html.replace('height:200px', 'height:350px')  # Make the Top 10 bars taller

    # Delivery Ranking
    html = html.replace('<div class="cam-hdr" style="grid-template-columns:2fr 1fr 1fr 1fr 1.5fr;"><span>Loja</span><span class="ctr">Delivery Time</span><span class="ctr">Service Time</span><span class="ctr">Total Alertas (Loja)</span><span class="ctr">% Alertas Delivery</span></div>', '<div class="cam-hdr" style="grid-template-columns:2fr 1fr 1fr 1fr;"><span>Loja</span><span class="ctr">Delivery Time</span><span class="ctr">Total Alertas Delivery</span><span class="ctr">% Alertas Delivery</span></div>')

    # Drive Thru Ranking
    html = html.replace('<div class="cam-hdr" style="grid-template-columns:2fr 1fr 1fr 1fr;"><span>Loja</span><span class="ctr">Total Alertas DT</span><span class="ctr">% do Total da Loja</span><span class="ctr">Ranking Geral</span></div>', '<div class="cam-hdr" style="grid-template-columns:2fr 1fr 1fr 1fr;"><span>Loja</span><span class="ctr">Total Alertas DT</span><span class="ctr">Alertas da Loja</span><span class="ctr">% DT</span></div>')


    # ------------------ JAVASCRIPT MODIFICATIONS ------------------
    # Resumen JS
    res_js_old = r"document\.getElementById\('kpiMain'\)\.innerHTML = \[\s*\{l:'Total KBP'.*?\]\.map\(.*?join\(''\);"
    res_js_new = r"""document.getElementById('kpiMain').innerHTML = [
      {l:'Total KBP',v:fmt(D.kbp),s:'alertas · {{ period }}',c:'var(--kbp-purple)'},
      {l:'Customer Exp.',v:fmt(D.ce),s:D.ce_pct+'% del KBP',c:'var(--ce)'},
      {l:'Reduce Costs',v:fmt(D.rc),s:D.rc_pct+'% del KBP',c:'var(--rc)'},
      {l:'Culture/Ops',v:fmt(D.co),s:D.co_pct+'% del KBP',c:'var(--co)'},
    ].map(k=>`<div class="kpi" style="--kc:${k.c}"><div class="kpi-label">${k.l}</div><div class="kpi-val" style="color:${k.c}">${k.v}</div><div class="kpi-sub">${k.s}</div></div>`).join('');

    kill('cAreaDist');
    CH['cAreaDist'] = new Chart(document.getElementById('cAreaDist'),{
      type:'doughnut',
      data:{labels:['Cashier','All Store','Delivery','Drive Thru','Cam Check'],
            datasets:[{data:[D.cash_total,D.allstore_total,D.delivery_total,D.dt_total,D.cam_total],
            backgroundColor:['#D4A017','#C05621','#7B52AB','#2C7DA0','#E8A838'],borderWidth:0}]},
      options:{...coNoScales, cutout:'70%', plugins:{legend:{position:'right',labels:{color:'#4A6080',font:{size:11,family:"'DM Mono',monospace"},boxWidth:12}},
               tooltip:{callbacks:{label:i=>`${i.label}: ${fmt(i.raw)} (${(i.raw/(D.all_alerts||1)*100).toFixed(1)}%)`}}}}
    });

    if(document.getElementById('bestStoreName')) {
        document.getElementById('bestStoreName').textContent = sn(D.kbp_best[0]);
        document.getElementById('bestStoreAlerts').textContent = D.kbp_best[1] + " alertas";
        document.getElementById('worstStoreName').textContent = sn(D.kbp_worst[0]);
        document.getElementById('worstStoreAlerts').textContent = D.kbp_worst[1] + " alertas";
        
        document.getElementById('bestSvcName').textContent = sn(D.svc_fast[0][0]);
        document.getElementById('bestSvcTime').textContent = D.svc_fast[0][1];
        document.getElementById('worstSvcName').textContent = sn(D.svc_slow[0][0]);
        document.getElementById('worstSvcTime').textContent = D.svc_slow[0][1];
        
        document.getElementById('bestDelName').textContent = sn(D.del_fast[0][0]);
        document.getElementById('bestDelTime').textContent = D.del_fast[0][1];
        document.getElementById('worstDelName').textContent = sn(D.del_slow[0][0]);
        document.getElementById('worstDelTime').textContent = D.del_slow[0][1];
    }
"""
    html = re.sub(res_js_old, res_js_new, html, flags=re.DOTALL)

    # Replace old variables for top10 arrays
    html = html.replace("D.top5_alert_types.map", "D.top10_alert_types.map")
    html = html.replace("D.kbp_top5.map", "D.all_top10.map")

    # Stacked KBP -> indexAxis y, sorted descending
    html = html.replace("const stores = D.store_kbp_stacks.map(s => sn(s[0]));", "const sortedKBP = [...D.store_kbp_stacks].sort((a,b)=>(b[1]+b[2]+b[3])-(a[1]+a[2]+a[3]));\n  const stores = sortedKBP.map(s => sn(s[0]));")
    html = html.replace("const ceData = D.store_kbp_stacks.map(s => s[1]);", "const ceData = sortedKBP.map(s => s[1]);")
    html = html.replace("const rcData = D.store_kbp_stacks.map(s => s[2]);", "const rcData = sortedKBP.map(s => s[2]);")
    html = html.replace("const coData = D.store_kbp_stacks.map(s => s[3]);", "const coData = sortedKBP.map(s => s[3]);")
    
    kbp_options = r"options: {...co, scales:{x:{stacked:true, grid:{color:'#1E2D45'}, ticks:{color:'#4A6080',font:{size:9},maxRotation:90,minRotation:90}}, y:{stacked:true, grid:{color:'#1E2D45'}}}}"
    new_kbp_options = r"options: {...co, indexAxis:'y', scales:{x:{stacked:true, grid:{color:'#1E2D45'}}, y:{stacked:true, grid:{color:'#1E2D45'}, ticks:{color:'#C8D8EC',font:{size:9}}}}, plugins:{...co.plugins, datalabels:{display:true, color:'#C8D8EC', font:{size:10}, align:'right', anchor:'end', formatter: (val, ctx) => { let sum = 0; let dataArr = ctx.chart.data.datasets; dataArr.map(d => sum += d.data[ctx.dataIndex]); return ctx.datasetIndex === dataArr.length - 1 ? sum : '';}}}}"
    html = html.replace(kbp_options, new_kbp_options)

    # Areas
    html = html.replace("const aStores = D.store_area_stacks.map(s => sn(s[0]));", "const sortedArea = [...D.store_area_stacks].sort((a,b)=>(b[1]+b[2]+b[3]+b[4]+b[5])-(a[1]+a[2]+a[3]+a[4]+a[5]));\n  const aStores = sortedArea.map(s => sn(s[0]));")
    html = html.replace("data:D.store_area_stacks.map", "data:sortedArea.map")

    # Add dynamic badges assignment in drawAreas
    badges_js = r"""
  const totA = D.all_alerts || 1;
  const updBdg = (id, val) => {
      let el = document.getElementById(id);
      if(el) el.innerHTML = `${fmt(val)}<small>${(val/totA*100).toFixed(1)}%</small>`;
  };
  updBdg('bdgCashier', D.cash_total);
  updBdg('bdgAllStore', D.allstore_total);
  updBdg('bdgDelivery', D.delivery_total);
  updBdg('bdgDriveThru', D.dt_total);
  updBdg('bdgCam', D.cam_total);
"""
    html = html.replace("document.getElementById('tbCashier').innerHTML = tblRows([", badges_js + "\n  document.getElementById('tbCashier').innerHTML = tblRows([")

    # Sort tblRows inputs descending
    # the inputs are arrays of arrays. We can sort them before tblRows.
    html = html.replace("],'var(--cashier)',D.cash_total);", "].sort((a,b)=>b[1]-a[1]),'var(--cashier)',D.cash_total);")
    html = html.replace("],'var(--allstore)',D.allstore_total);", "].sort((a,b)=>b[1]-a[1]),'var(--allstore)',D.allstore_total);")
    html = html.replace("],'var(--delivery)',D.delivery_total);", "].sort((a,b)=>b[1]-a[1]),'var(--delivery)',D.delivery_total);")
    html = html.replace("],'var(--drivethru)',1);", "].sort((a,b)=>b[1]-a[1]),'var(--drivethru)',D.dt_total);")


    # Velocidad vertical layout
    vel_cards = r"""document.getElementById('speedCards').innerHTML = metrics.map(m=>`
    <div class="card">
      <div class="card-title" style="color:${m.c}">${m.label} <span class="card-badge">${m.avg} avg</span></div>
      <div style="font-family:'DM Mono',monospace;font-size:34px;font-weight:700;color:${m.c};margin-bottom:14px;line-height:1;text-align:center">${m.avg}</div>
      <div style="position:relative;height:120px;margin-bottom:14px"><canvas id="cDist_${m.id}"></canvas></div>
      <div class="sp-hdr" style="color:var(--green)">⚡ MÁS RÁPIDAS</div>
      ${m.fast.map((r,i)=>`<div class="rr"><div class="rr-badge" style="background:var(--green);font-size:9px">${i+1}</div><span class="rr-name">${sn(r[0])}</span><span style="font-family:'DM Mono',monospace;font-size:11px;font-weight:700;color:var(--green)">${r[1]}</span></div>`).join('')}
      <div class="sp-hdr" style="color:var(--danger);margin-top:10px">🐌 MÁS LENTAS</div>
      ${m.slow.map((r,i)=>`<div class="rr"><div class="rr-badge" style="background:var(--danger);font-size:9px">${i+1}</div><span class="rr-name">${sn(r[0])}</span><span style="font-family:'DM Mono',monospace;font-size:11px;font-weight:700;color:var(--danger)">${r[1]}</span></div>`).join('')}
    </div>`).join('');"""

    new_vel_cards = r"""document.getElementById('speedCards').innerHTML = metrics.map(m=>`
    <div class="card" style="display:grid;grid-template-columns:200px 1fr 1fr 1fr;gap:20px;align-items:center;">
      <div>
          <div class="card-title" style="color:${m.c};margin-bottom:8px">${m.label}</div>
          <div style="font-family:'DM Mono',monospace;font-size:42px;font-weight:700;color:${m.c};line-height:1">${m.avg}</div>
          <div style="font-size:12px;color:var(--muted);margin-top:4px">Promedio</div>
      </div>
      <div style="position:relative;height:160px;display:flex;align-items:center;justify-content:center">
          <canvas id="cDist_${m.id}"></canvas>
      </div>
      <div>
          <div class="sp-hdr" style="color:var(--green);margin-bottom:8px">⚡ MÁS RÁPIDAS</div>
          ${m.fast.map((r,i)=>`<div class="rr" style="padding:6px;background:rgba(16,185,129,0.05);margin-bottom:4px"><div class="rr-badge" style="background:var(--green);font-size:9px">${i+1}</div><span class="rr-name">${sn(r[0])}</span><span style="font-family:'DM Mono',monospace;font-size:13px;font-weight:700;color:var(--green)">${r[1]}</span></div>`).join('')}
      </div>
      <div>
          <div class="sp-hdr" style="color:var(--danger);margin-bottom:8px">🐌 MÁS LENTAS</div>
          ${m.slow.map((r,i)=>`<div class="rr" style="padding:6px;background:rgba(239,68,68,0.05);margin-bottom:4px"><div class="rr-badge" style="background:var(--danger);font-size:9px">${i+1}</div><span class="rr-name">${sn(r[0])}</span><span style="font-family:'DM Mono',monospace;font-size:13px;font-weight:700;color:var(--danger)">${r[1]}</span></div>`).join('')}
      </div>
    </div>`).join('');"""
    html = html.replace(vel_cards, new_vel_cards)
    
    # Legend position for doughnuts
    html = html.replace("legend:{display:false}", "legend:{display:true, position:'right', labels:{color:'#C8D8EC', font:{size:10}}}")


    # drawKBP
    # Simplify the stacked bar to a simple bar chart sorted descending
    kbp_js_old = r"""  kill(cidStacked);
  CH[cidStacked] = new Chart(document.getElementById(cidStacked),{
    type:'bar',
    data:{
      labels: dataStack.map(s => sn(s[0])),
      datasets: [
        {label:'Cashier', data:dataStack.map(s=>s[1]), backgroundColor:'#D4A01799', borderColor:'#D4A017', borderWidth:1},
        {label:'All Store', data:dataStack.map(s=>s[2]), backgroundColor:'#C0562199', borderColor:'#C05621', borderWidth:1},
        {label:'Delivery', data:dataStack.map(s=>s[3]), backgroundColor:'#7B52AB99', borderColor:'#7B52AB', borderWidth:1},
        {label:'Drive Thru', data:dataStack.map(s=>s[4]), backgroundColor:'#2C7DA099', borderColor:'#2C7DA0', borderWidth:1},
        {label:'Cam Check', data:dataStack.map(s=>s[5]), backgroundColor:'#E8A83899', borderColor:'#E8A838', borderWidth:1}
      ]
    },
    options: {...co, scales:{x:{stacked:true, grid:{color:'#1E2D45'}, ticks:{color:'#4A6080',font:{size:9},maxRotation:45,minRotation:45}}, y:{stacked:true, grid:{color:'#1E2D45'}}}}
  });"""

    kbp_js_new = r"""  kill(cidStacked);
  const sortedStack = [...dataStack].sort((a,b) => (b[1]+b[2]+b[3]+b[4]+b[5]) - (a[1]+a[2]+a[3]+a[4]+a[5]));
  const sumArr = sortedStack.map(s => s[1]+s[2]+s[3]+s[4]+s[5]);
  CH[cidStacked] = new Chart(document.getElementById(cidStacked),{
    type:'bar',
    data:{
      labels: sortedStack.map(s => sn(s[0])),
      datasets: [{label:'Alertas', data:sumArr, backgroundColor:C.hex+'99', borderColor:C.col, borderWidth:1, borderRadius:4}]
    },
    options: {...co, indexAxis:'y', scales:{x:{grid:{color:'#1E2D45'}}, y:{grid:{color:'#1E2D45'}, ticks:{color:'#C8D8EC',font:{size:9}}}}, plugins:{...co.plugins, legend:{display:false}, datalabels:{display:true, color:'#C8D8EC', font:{size:10}, align:'right', anchor:'end'}}}
  });"""
    html = html.replace(kbp_js_old, kbp_js_new)

    # Delivery Ranking modifications
    # old row: 2fr 1fr 1fr 1fr 1.5fr
    del_row_old = r"""        return `<div class="cam-row" style="grid-template-columns:2fr 1fr 1fr 1fr 1.5fr;${bg};position:relative">
          <span class="cam-c">${sn(r[0])}</span>
          <span class="cam-c hi" style="color:var(--delivery)">${r[1]}</span>
          <span class="cam-c ctr">${r[2]}</span>
          <span class="cam-c ctr">${r[3]}</span>
          <span class="cam-c ctr" style="font-weight:700;color:#fff;overflow:hidden;border-radius:4px;display:flex;align-items:center;justify-content:center;height:24px"><div style="background:var(--delivery);width:${r[4]}%;height:100%;position:absolute;opacity:0.25;left:0;top:0;"></div><span style="position:relative">${r[4]}%</span></span>
        </div>`;"""
    # r[2] is service time, we remove it. And r[3] is tot alerts, wait, r[4] is %. The user wants: Loja, Delivery Time, Delivery Alerts, %.
    # We must change what r[2] and r[3] mean from parser.py? No, we can just grab the correct data or re-map it in JS if parser provides it.
    # We know delivery alerts is D.store_area_stacks or we can calculate it from D.delivery_stores_ranking: r[3] is all_alerts, r[4] is pct. So delivery_alerts = r[3] * r[4]/100.
    
    del_row_new = r"""        let delAlerts = Math.round(r[3] * (r[4]/100));
        return `<div class="cam-row" style="grid-template-columns:2fr 1fr 1fr 1fr;${bg};position:relative">
          <span class="cam-c">${sn(r[0])}</span>
          <span class="cam-c hi" style="color:var(--delivery)">${r[1]}</span>
          <span class="cam-c ctr">${delAlerts}</span>
          <span class="cam-c ctr" style="font-weight:700;color:#fff;overflow:hidden;border-radius:4px;display:flex;align-items:center;justify-content:center;height:24px"><div style="background:var(--delivery);width:${r[4]}%;height:100%;position:absolute;opacity:0.25;left:0;top:0;"></div><span style="position:relative">${r[4]}%</span></span>
        </div>`;"""
    html = html.replace(del_row_old, del_row_new)


    # DT Ranking modifications
    # old row: 2fr 1fr 1fr 1fr
    dt_row_old = r"""        <div class="cam-row" style="grid-template-columns:2fr 1fr 1fr 1fr;">
          <span class="cam-c">${sn(r[0])}</span>
          <span class="cam-c hi" style="color:var(--drivethru)">${r[1]}</span>
          <span class="cam-c ctr">${r[2]}%</span>
          <span class="cam-c ctr">#${r[3]}</span>
        </div>"""
    # r[1] is dt alerts, r[2] is pct. total alerts of store is r[1] / (r[2]/100).
    dt_row_new = r"""        
        <div class="cam-row" style="grid-template-columns:2fr 1fr 1fr 1fr;">
          <span class="cam-c">${sn(r[0])}</span>
          <span class="cam-c hi" style="color:var(--drivethru)">${r[1]}</span>
          <span class="cam-c ctr">${r[2] > 0 ? Math.round(r[1] / (r[2]/100)) : 0}</span>
          <span class="cam-c ctr" style="font-weight:700;color:#fff"><span style="color:var(--drivethru)">${r[2]}%</span></span>
        </div>"""
    html = html.replace(dt_row_old, dt_row_new)


    with open('c:/Users/rodri/Desktop/DairyQueen_ReportsAuto/yedda-app/templates/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    apply_html_updates()
