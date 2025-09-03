// Handles webcam start/stop and capturing a frame
export async function startWebcam(video) {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
    await video.play();
    return stream;
  } catch (err) {
    console.error("Cannot access webcam:", err);
    return null;
  }
}

export function stopWebcam(video, stream) {
  if (stream) stream.getTracks().forEach(track => track.stop());
  if (video) {
    video.pause();
    video.srcObject = null;
  }
}

export async function captureFrame(video, canvas) {
  await new Promise(resolve => {
    if (video.readyState >= 2) resolve();
    else video.onloadedmetadata = () => resolve();
  });

  const ctx = canvas.getContext("2d");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  return new Promise(resolve => canvas.toBlob(blob => resolve(blob), "image/jpeg"));
}
