import re

def rewrite_js():
    with open('c:/Users/rodri/Desktop/IceCream Co._ReportsAuto/optimareports-app/templates/dashboard.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Helpers
    def replace_func(func_name, new_body):
        pattern = r"function " + func_name + r"\([^)]*\)\s*\{.*?(?=\nfunction |// ───|\n</script>)"
        # We need to use DOTALL to match across newlines
        return re.sub(pattern, "function " + func_name + "() {\n" + new_body + "\n}\n", content, flags=re.DOTALL)

    def replace_func_args(func_name, new_body, args=""):
        pattern = r"function " + func_name + r"\([^)]*\)\s*\{.*?(?=\nfunction |// ───|\n</script>)"
        return re.sub(pattern, "function " + func_name + "(" + args + ") {\n" + new_body + "\n}\n", content, flags=re.DOTALL)


    # 1. drawRankings
    rankings_body = r"""  const mkRank = (data,col) => data.map((r,i)=>rankRow(i,r[0],r[2]+'%',col)).join('');
  document.getElementById('rCE').innerHTML = mkRank(D.ce_top5,'var(--ce)');
  document.getElementById('rRC').innerHTML = mkRank(D.rc_top5,'var(--rc)');
  document.getElementById('rCO').innerHTML = mkRank(D.co_top5,'var(--co)');
  document.getElementById('rOrd').innerHTML = D.ord_top5_fast.map((r,i)=>rankRow(i,r[0],r[1],'var(--green)')).join('');

  const stores = D.store_kbp_stacks.map(s => sn(s[0]));
  const ceData = D.store_kbp_stacks.map(s => s[1]);
  const rcData = D.store_kbp_stacks.map(s => s[2]);
  const coData = D.store_kbp_stacks.map(s => s[3]);
  kill('cKBPStacked');
  CH['cKBPStacked'] = new Chart(document.getElementById('cKBPStacked'), {
    type: 'bar',
    data: {
      labels: stores,
      datasets: [
        {label:'CE', data:ceData, backgroundColor:'#52B78899', borderColor:'#52B788', borderWidth:1},
        {label:'RC', data:rcData, backgroundColor:'#E63B7A99', borderColor:'#E63B7A', borderWidth:1},
        {label:'CO', data:coData, backgroundColor:'#4BBFBF99', borderColor:'#4BBFBF', borderWidth:1}
      ]
    },
    options: {...co, scales:{x:{stacked:true, grid:{color:'#1E2D45'}, ticks:{color:'#4A6080',font:{size:9},maxRotation:90,minRotation:90}}, y:{stacked:true, grid:{color:'#1E2D45'}}}}
  });"""
    content = replace_func("drawRankings", rankings_body)

    # 2. drawAreas
    areas_body = r"""  const tblRows = (rows,col,total) => rows.map(([l,v])=>`<tr>
    <td>${l}<div style="height:3px;background:${col};opacity:.35;border-radius:1px;width:${(v/(rows[0][1]||1)*60).toFixed(0)}px;margin-top:3px"></div></td>
    <td class="r" style="color:${col}">${fmt(v)}</td>
    <td class="r">${total?(v/total*100).toFixed(1)+'%':'—'}</td>
  </tr>`).join('');

  document.getElementById('tbCashier').innerHTML = tblRows([
    ['Receive order >3min',D.receive_3min],['+3 personas en fila',D.queue_3],
    ['Staff móvil (caja)',D.mobile],['Staff fuera caja >1min',D.outside],
    ['No atendido >1min',D.not_attended],['Cash drawer open',D.cash_drawer],
    ['PIN pad misuse',D.pin_cashier],
  ],'var(--cashier)',D.cash_total);

  document.getElementById('tbAllStore').innerHTML = tblRows([
    ['Staff sin gorra',D.no_cap],['Lost customer',D.lost_customer],
    ['Store open late',D.open_late],['Staff inactivo >5min',D.inactive],
    ['Playing/fighting',D.playing],['Staff sin uniforme',D.no_uniform],
    ['Dirty floor',D.dirty_floor],
  ],'var(--allstore)',D.allstore_total);

  document.getElementById('tbDelivery').innerHTML = tblRows([
    ['Delivery waiting >1min',D.delivery_wait],['Check packaging',D.check_packaging],
  ],'var(--delivery)',D.delivery_total);

  document.getElementById('tbDT').innerHTML = tblRows([
    ['[D] PIN pad misuse',D.dt_pin],['[D] Staff fuera caja',D.dt_outside],
    ['[D] Cash drawer open',D.dt_cash],['[D] Staff móvil',D.dt_mobile],
    ['[D] Receipt not given',D.dt_receipt],
  ],'var(--drivethru)',1);

  const aStores = D.store_area_stacks.map(s => sn(s[0]));
  kill('cAreaStacked');
  CH['cAreaStacked'] = new Chart(document.getElementById('cAreaStacked'), {
    type: 'bar',
    data: {
      labels: aStores,
      datasets: [
        {label:'Cashier', data:D.store_area_stacks.map(s=>s[1]), backgroundColor:'#D4A01799', borderColor:'#D4A017', borderWidth:1},
        {label:'All Store', data:D.store_area_stacks.map(s=>s[2]), backgroundColor:'#C0562199', borderColor:'#C05621', borderWidth:1},
        {label:'Delivery', data:D.store_area_stacks.map(s=>s[3]), backgroundColor:'#7B52AB99', borderColor:'#7B52AB', borderWidth:1},
        {label:'Drive Thru', data:D.store_area_stacks.map(s=>s[4]), backgroundColor:'#2C7DA099', borderColor:'#2C7DA0', borderWidth:1},
        {label:'Cam Check', data:D.store_area_stacks.map(s=>s[5]), backgroundColor:'#E8A83899', borderColor:'#E8A838', borderWidth:1}
      ]
    },
    options: {...co, scales:{x:{stacked:true, grid:{color:'#1E2D45'}, ticks:{color:'#4A6080',font:{size:9},maxRotation:90,minRotation:90}}, y:{stacked:true, grid:{color:'#1E2D45'}}}}
  });"""
    content = replace_func("drawAreas", areas_body)

    # 3. drawVelocidad
    vel_body = r"""  document.getElementById('kpiTimes').innerHTML = [
    {l:'Service Time',v:D.svc_avg,c:'var(--rc)'},{l:'Ordering Time',v:D.ord_avg,c:'var(--co)'},
    {l:'Queue Time',v:D.queue_avg,c:'var(--green)'},{l:'Receiving Time',v:D.recv_avg,c:'var(--co)'},
    {l:'Delivery Wait',v:D.del_avg,c:'var(--delivery)'},
  ].map(k=>`<div class="kpi" style="--kc:${k.c}"><div class="kpi-label">${k.l}</div><div class="kpi-val t" style="color:${k.c}">${k.v}</div><div class="kpi-sub">promedio grupo</div></div>`).join('');

  const metrics = [
    {id:'svc',label:'Service Time',avg:D.svc_avg,fast:D.svc_fast,slow:D.svc_slow,c:'var(--rc)',hex:'#E63B7A', dist:[D.pct_lt3, D.pct_3to5, D.pct_gt5], lbls:['<3m','3-5m','>5m']},
    {id:'ord',label:'Ordering Time',avg:D.ord_avg,fast:D.ord_fast,slow:D.ord_slow,c:'var(--co)',hex:'#4BBFBF', dist:[D.ord_lt1, D.ord_1to2, D.ord_gt2], lbls:['<1m','1-2m','>2m']},
    {id:'queue',label:'Queue Time',avg:D.queue_avg,fast:D.queue_fast,slow:D.queue_slow,c:'var(--green)',hex:'#10B981', dist:[D.queue_lt1, D.queue_1to2, D.queue_gt2], lbls:['<1m','1-2m','>2m']},
    {id:'recv',label:'Receiving Time',avg:D.recv_avg,fast:D.recv_fast,slow:D.recv_slow,c:'var(--co)',hex:'#4BBFBF', dist:[D.recv_lt1, D.recv_1to2, D.recv_gt2], lbls:['<1m','1-2m','>2m']},
    {id:'del',label:'Delivery Time',avg:D.del_avg,fast:D.del_fast,slow:D.del_slow,c:'var(--delivery)',hex:'#7B52AB', dist:[D.del_lt2, D.del_2to3, D.del_gt3], lbls:['<2m','2-3m','>3m']},
  ];
  document.getElementById('speedCards').innerHTML = metrics.map(m=>`
    <div class="card">
      <div class="card-title" style="color:${m.c}">${m.label} <span class="card-badge">${m.avg} avg</span></div>
      <div style="font-family:'DM Mono',monospace;font-size:34px;font-weight:700;color:${m.c};margin-bottom:14px;line-height:1;text-align:center">${m.avg}</div>
      <div style="position:relative;height:120px;margin-bottom:14px"><canvas id="cDist_${m.id}"></canvas></div>
      <div class="sp-hdr" style="color:var(--green)">⚡ MÁS RÁPIDAS</div>
      ${m.fast.map((r,i)=>`<div class="rr"><div class="rr-badge" style="background:var(--green);font-size:9px">${i+1}</div><span class="rr-name">${sn(r[0])}</span><span style="font-family:'DM Mono',monospace;font-size:11px;font-weight:700;color:var(--green)">${r[1]}</span></div>`).join('')}
      <div class="sp-hdr" style="color:var(--danger);margin-top:10px">🐌 MÁS LENTAS</div>
      ${m.slow.map((r,i)=>`<div class="rr"><div class="rr-badge" style="background:var(--danger);font-size:9px">${i+1}</div><span class="rr-name">${sn(r[0])}</span><span style="font-family:'DM Mono',monospace;font-size:11px;font-weight:700;color:var(--danger)">${r[1]}</span></div>`).join('')}
    </div>`).join('');

  metrics.forEach(m => {
      kill('cDist_'+m.id);
      CH['cDist_'+m.id] = new Chart(document.getElementById('cDist_'+m.id),{
        type:'doughnut',
        data:{labels:m.lbls, datasets:[{data:m.dist, backgroundColor:['#10B98199','#F59E0B99','#EF444499'], borderColor:['#10B981','#F59E0B','#EF4444'], borderWidth:1}]},
        options:{...coNoScales, cutout:'60%', plugins:{legend:{display:false}, tooltip:{callbacks:{label:i=>`${i.label}: ${(i.raw*100).toFixed(1)}%`}}}}
      });
  });"""
    content = replace_func("drawVelocidad", vel_body)

    # 4. drawKBP
    kbp_body = r"""  const C = {
    kbp1:{alerts:D.kbp1_alerts,all:D.kbp1_all,ranks:D.kbp1_store_ranks,total:D.ce,col:'var(--ce)',hex:'#52B788',cid:'cCE'},
    kbp2:{alerts:D.kbp2_alerts,all:D.kbp2_all,ranks:D.kbp2_store_ranks,total:D.rc,col:'var(--rc)',hex:'#E63B7A',cid:'cRC'},
    kbp3:{alerts:D.kbp3_alerts,all:D.kbp3_all,ranks:D.kbp3_store_ranks,total:D.co,col:'var(--co)',hex:'#4BBFBF',cid:'cCO'},
  }[id];

  document.getElementById(id+'Panels').innerHTML = C.alerts.map(a=>kbpPanel(a[0],a[2],pct(a[2],C.total),C.col,C.ranks[a[1]]||[])).join('');
  const maxAll = C.all.length ? C.all[0][1] : 1;
  document.getElementById(id+'Res').innerHTML = C.all.map(a=>barRow(a[0],a[1],maxAll,C.col,pct(a[1],C.total))).join('');

  const cidStacked = C.cid + 'Stacked';
  const dataStack = id === 'kbp1' ? D.ce_top10_stack : (id === 'kbp2' ? D.rc_top10_stack : D.co_top10_stack);
  
  kill(cidStacked);
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
    content = replace_func_args("drawKBP", kbp_body, "id")

    # 5. drawDelivery
    delivery_body = r"""  if (document.getElementById('delAvgLabel')) document.getElementById('delAvgLabel').textContent = D.del_avg;
  if (document.getElementById('delWaitLabel')) {
      document.getElementById('delWaitLabel').textContent = D.delivery_wait;
      document.getElementById('delWaitPctLabel').textContent = (D.delivery_wait / (D.delivery_total||1) * 100).toFixed(1) + '%';
      document.getElementById('delPkgLabel').textContent = D.check_packaging;
      document.getElementById('delPkgPctLabel').textContent = (D.check_packaging / (D.delivery_total||1) * 100).toFixed(1) + '%';
  }

  kill('cDelDist');
  CH['cDelDist'] = new Chart(document.getElementById('cDelDist'),{
    type:'bar',
    data:{labels:['< 2 min','2–3 min','> 3 min'],
          datasets:[{data:[D.del_lt2,D.del_2to3,D.del_gt3],backgroundColor:['#10B98199','#F59E0B99','#EF444499'],borderColor:['#10B981','#F59E0B','#EF4444'],borderWidth:2,borderRadius:6}]},
    options:{...co,plugins:{...co.plugins,tooltip:{...co.plugins.tooltip,callbacks:{label:i=>`${(i.raw*100).toFixed(1)}% de entregas`}}}}
  });

  if (document.getElementById('delRows')) {
      document.getElementById('delRows').innerHTML = D.delivery_stores_ranking.map((r,i) => {
        let bg = '';
        if (i < 3) bg = 'background:rgba(16,185,129,0.1);';
        else if (i >= D.delivery_stores_ranking.length - 3) bg = 'background:rgba(239,68,68,0.1);';
        
        return `<div class="cam-row" style="grid-template-columns:2fr 1fr 1fr 1fr 1.5fr;${bg};position:relative">
          <span class="cam-c">${sn(r[0])}</span>
          <span class="cam-c hi" style="color:var(--delivery)">${r[1]}</span>
          <span class="cam-c ctr">${r[2]}</span>
          <span class="cam-c ctr">${r[3]}</span>
          <span class="cam-c ctr" style="font-weight:700;color:#fff;overflow:hidden;border-radius:4px;display:flex;align-items:center;justify-content:center;height:24px"><div style="background:var(--delivery);width:${r[4]}%;height:100%;position:absolute;opacity:0.25;left:0;top:0;"></div><span style="position:relative">${r[4]}%</span></span>
        </div>`;
      }).join('');
  }"""
    content = replace_func("drawDelivery", delivery_body)

    # 6. drawDT
    dt_body = r"""  if (!D.has_drive_thru) {
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
    if (document.getElementById('dtRows')) document.getElementById('dtRows').innerHTML = '';
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

  if (document.getElementById('dtRows')) {
      document.getElementById('dtRows').innerHTML = D.dt_stores_ranking.map((r,i)=>`
        <div class="cam-row" style="grid-template-columns:2fr 1fr 1fr 1fr;">
          <span class="cam-c">${sn(r[0])}</span>
          <span class="cam-c hi" style="color:var(--drivethru)">${r[1]}</span>
          <span class="cam-c ctr">${r[2]}%</span>
          <span class="cam-c ctr">#${r[3]}</span>
        </div>
      `).join('');
  }"""
    content = replace_func("drawDT", dt_body)

    # 7. drawCam
    cam_body = r"""  if(document.getElementById('camTotalLabel')) document.getElementById('camTotalLabel').textContent = fmt(D.cam_total);
  if(document.getElementById('camStoresLabel')) document.getElementById('camStoresLabel').textContent = `${D.cam_stores_count} tiendas afectadas de ${D.n_stores}`;

  const falloTypes = [
      ['Lost Connection', D.cam_lost],
      ['Blurry Image', D.cam_blurry],
      ['Camera lagging', D.cam_lagging],
      ["Can't connect", D.cam_connect],
      ['Obstructed', D.cam_obstructed]
  ].filter(x => x[1] > 0).sort((a,b) => b[1] - a[1]);

  const maxCam = Math.max(...falloTypes.map(x=>x[1]), 1);

  if(document.getElementById('camBars')) {
      document.getElementById('camBars').innerHTML = falloTypes.map(ft => `
        <div class="br" style="border-bottom:1px solid rgba(30,45,69,.5)">
          <span class="br-label">${ft[0]}</span>
          <div class="br-track"><div class="br-fill" style="width:${(ft[1]/maxCam*100).toFixed(0)}%;background:var(--cam)"></div></div>
          <span class="br-val" style="color:var(--cam)">${ft[1]}</span>
        </div>
      `).join('');
  }

  kill('cCam');
  CH['cCam'] = new Chart(document.getElementById('cCam'),{
    type:'bar',
    data:{labels:falloTypes.map(r=>r[0]),datasets:[{data:falloTypes.map(r=>r[1]),backgroundColor:'#E8A83899',borderColor:'#E8A838',borderWidth:1,borderRadius:6}]},
    options:{...co,plugins:{...co.plugins,tooltip:{...co.plugins.tooltip,callbacks:{label:i=>`${i.raw} alertas`}}}}
  });

  document.getElementById('camRows').innerHTML = D.cam_stores.map(cs=>{
    const top5 = cs.rank<=5;
    const tag = cs.cam>=3 ? '<span class="tag-r">⚠️ Revisar</span>' : '<span class="tag-m">👁️ Monit.</span>';
    return `<div class="cam-row">
      <span class="cam-c">${sn(cs.store)}</span>
      <span class="cam-c hi">${cs.cam}</span>
      <span class="cam-c ctr">${cs.kbp}</span>
      <span class="cam-c ctr">${cs.all_alerts}</span>
      <span class="cam-c ctr ${top5?'bld':''}">#${cs.rank}/${D.n_stores}</span>
      <span class="cam-c ctr">${tag}</span>
    </div>`;
  }).join('');"""
    content = replace_func("drawCam", cam_body)

    with open('c:/Users/rodri/Desktop/IceCream Co._ReportsAuto/optimareports-app/templates/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    rewrite_js()
