const fs = require('fs');
const html = fs.readFileSync('templates/dashboard.html', 'utf8');
const scriptMatch = html.match(/<script>(.*?)<\/script>/s);
// wait, the html has multiple script tags now because of window.onerror
// let's grab the actual main script
const scripts = html.match(/<script>([\s\S]*?)<\/script>/g);
let script = scripts[scripts.length - 1]; // usually the last one
script = script.replace('<script>', '').replace('</script>', '');

const dataStr = fs.readFileSync('debug_pj_spain.json', 'utf8');
const D = JSON.parse(dataStr);
script = script.replace('const D = {{ DATA_JSON | safe }};', 'const D = ' + dataStr + ';');
const domMock = {
    innerHTML: '',
    textContent: '',
    style: {},
    parentElement: { style: {} },
    appendChild: () => {},
    classList: { add: ()=>{}, remove: ()=>{} }
};
const els = {};

global.document = {
    getElementById: (id) => {
        if (html.includes('id=\"'+id+'\"') || html.includes('id=\''+id+'\'') || html.includes('id='+id)) {
            if(!els[id]) els[id] = Object.assign({}, domMock);
            return els[id];
        }
        return null;
    },
    querySelectorAll: () => [{classList: {remove: ()=>{}}}]
};
global.Chart = class {
    constructor() { this.destroy = () => {}; }
    static register() {}
    static defaults = { set: () => {} };
};
global.ChartDataLabels = {};
global.window = { innerWidth: 1024, onerror: () => {} };
global.getComputedStyle = () => ({
    getPropertyValue: (name) => {
        if (name === '--ce') return '#52B788';
        if (name === '--rc') return '#E63B7A';
        if (name === '--co') return '#4BBFBF';
        if (name === '--cashier') return '#D4A017';
        if (name === '--allstore') return '#C05621';
        if (name === '--delivery') return '#7B52AB';
        if (name === '--drivethru') return '#2C7DA0';
        if (name === '--cam') return '#E8A838';
        if (name === '--green') return '#10B981';
        if (name === '--amber') return '#F59E0B';
        if (name === '--danger') return '#EF4444';
        return '#ffffff';
    }
});

try {
    eval(script);
    console.log('Script loaded successfully.');
    drawResumen(); console.log('drawResumen passed');
    drawRankings(); console.log('drawRankings passed');
    drawAreas(); console.log('drawAreas passed');
    drawVelocidad(); console.log('drawVelocidad passed');
    drawKBP('kbp1'); console.log('drawKBP kbp1 passed');
    drawKBP('kbp2'); console.log('drawKBP kbp2 passed');
    drawKBP('kbp3'); console.log('drawKBP kbp3 passed');
    drawDelivery(); console.log('drawDelivery passed');
    drawCam(); console.log('drawCam passed');
} catch (e) {
    console.error('ERROR:', e.stack);
}
