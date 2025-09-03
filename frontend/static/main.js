import { startWebcam, stopWebcam, captureFrame } from './webcam.js';
import { handleRegisterForm, handleUserInfoForm } from './form.js';
import { showNotification, renderChart, downloadCSV } from './utils.js';

document.addEventListener("DOMContentLoaded", () => {
  const registerForm = document.querySelector("#registerForm");
  const userInfoForm = document.querySelector("#userInfoForm");
  const chartCanvas = document.getElementById("attendanceChart");
  const downloadCsvBtn = document.getElementById("downloadCsvBtn");
  const video = document.getElementById("webcam");
  const canvas = document.getElementById("snapshot");
  const captureButton = document.getElementById("captureBtn");
  let stream = null;
  let currentAttendanceData = [];

  if (registerForm) handleRegisterForm(registerForm);
  if (userInfoForm) handleUserInfoForm(userInfoForm, (data) => {
    currentAttendanceData = data;
    renderChart(chartCanvas, data);
  });

  if (captureButton) {
    captureButton.addEventListener("click", async () => {
      stream = await startWebcam(video);
      const blob = await captureFrame(video, canvas);
      setTimeout(
        () => stopWebcam(stream),
        15000
      )

      if (!blob) return showNotification("No frame captured", "error");

      const formData = new FormData();
      formData.append("frame", blob, "frame.jpg");

      try {
        const res = await fetch("/capture", { method: "POST", body: formData });
        const data = await res.json();
        if (data.status === "success") showNotification(data.message, "success");
        else showNotification(data.message, "error");
      } catch (err) {
        showNotification("Failed: " + err.message, "error");
      }
    });
  }

  if (downloadCsvBtn) downloadCsvBtn.addEventListener("click", () => downloadCSV(currentAttendanceData));

  document.querySelectorAll("nav a").forEach(link => {
    link.addEventListener("click", e => {
      e.preventDefault();
      const targetId = link.getAttribute("href").substring(1);
      const targetSection = document.getElementById(targetId);
      if (targetSection) targetSection.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });
});
