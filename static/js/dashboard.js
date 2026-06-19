document.addEventListener('DOMContentLoaded', async () => {
  const charts = ['uploadsChart','divisionChart','reportChart'].map(id => document.getElementById(id));
  if (!charts.some(Boolean)) return;
  const res = await fetch('/api/dashboard/charts');
  const data = await res.json();
  if (charts[0]) new Chart(charts[0], {type:'line', data:{labels:data.uploads_per_month.labels, datasets:[{label:'Uploads', data:data.uploads_per_month.data, borderColor:'#4f46e5'}]}});
  if (charts[1]) new Chart(charts[1], {type:'bar', data:{labels:data.documents_by_division.labels, datasets:[{label:'Documents', data:data.documents_by_division.data, backgroundColor:'#0ea5e9'}]}});
  if (charts[2]) new Chart(charts[2], {type:'doughnut', data:{labels:data.report_distribution.labels, datasets:[{data:data.report_distribution.data, backgroundColor:['#4f46e5','#22c55e','#f59e0b','#ef4444']}]}});
});
