export function showNotification(message, type = "info") {
  const notification = document.createElement("div");
  notification.className = `notification ${type}`;
  notification.innerText = message;
  document.body.appendChild(notification);
  setTimeout(() => notification.classList.add("show"), 100);
  setTimeout(() => {
    notification.classList.remove("show");
    setTimeout(() => notification.remove(), 300);
  }, 3000);
}

export function renderChart(chartCanvas, attendance) {
  if (!chartCanvas) return;
  if (window.chartInstance) window.chartInstance.destroy();

  const totalDays = 45;
  const attended = attendance.length > totalDays ? totalDays : attendance.length;
  const absent = totalDays - attended;

  window.chartInstance = new Chart(chartCanvas, {
    type: "pie",
    data: {
      labels: ["Attended", "Absent"],
      datasets: [{ data: [attended, absent], backgroundColor: ["#22c55e", "#ef4444"] }]
    },
    options: { responsive: false }
  });
}

export function downloadCSV(data) {
  if (!data || data.length === 0) return showNotification("No attendance data available", "error");
  const rows = [["Date"], ...data.slice(0, 45).map(d => [d])];
  const csvContent = "data:text/csv;charset=utf-8," + rows.map(e => e.join(",")).join("\n");
  const encodedUri = encodeURI(csvContent);
  const link = document.createElement("a");
  link.setAttribute("href", encodedUri);
  link.setAttribute("download", "attendance_last_45_days.csv");
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
