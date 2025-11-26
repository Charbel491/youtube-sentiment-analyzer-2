const API_URL = 'http://localhost:7860/predict_batch'; // ou localhost:8000

document.getElementById('analyze').onclick = async () => {
  const [tab] = await chrome.tabs.query({active:true,currentWindow:true});
  const resp = await chrome.tabs.sendMessage(tab.id, {action:'getComments'});
  const comments = resp.comments;
  if (!comments.length) return alert('Aucun commentaire visible.');
  const res = await fetch(API_URL, {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({comments})
  }).then(r=>r.json());
  display(res);
};

function display(data){
  const stats = data.stats;
  document.getElementById('stats').innerHTML =
    `Total : ${stats.total} &nbsp;|&nbsp; Pos : ${stats.positive} &nbsp;|&nbsp; Neu : ${stats.neutral} &nbsp;|&nbsp; Neg : ${stats.negative} &nbsp;|&nbsp; ${stats.inference_time_ms} ms`;
  renderList(data.predictions);
}

document.querySelectorAll('#filters input').forEach(el=>{
  el.addEventListener('change', ()=> renderList(lastPredictions));
});

let lastPredictions;
function renderList(predictions){
  lastPredictions = predictions;
  const checked = Array.from(document.querySelectorAll('#filters input:checked')).map(c=>c.value);
  const html = predictions
    .filter(p => checked.includes(String(p.label)))
    .map(p => `<div class="comment ${p.label===1?'pos':p.label===-1?'neg':'neu'}">${p.comment} <b>${p.confidence.toFixed(2)}</b></div>`)
    .join('');
  document.getElementById('results').innerHTML = html;
}

document.getElementById('copy').onclick = () => {
  const text = lastPredictions.map(p=>`${p.label},${p.confidence},${p.comment}`).join('\n');
  navigator.clipboard.writeText(text);
};

document.getElementById('export').onclick = () => {
  const csv = 'label,confidence,comment\n' + lastPredictions.map(p=>`${p.label},${p.confidence},"${p.comment}"`).join('\n');
  const blob = new Blob([csv], {type:'text/csv'});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a'); a.href=url; a.download='sentiments.csv'; a.click();
};