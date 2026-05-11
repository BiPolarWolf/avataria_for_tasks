// composables/useSound.js (опционально, для повторного использования)
export const playSuccessSound = () => {
  const audio = new Audio('/audio/reward.mp3');
  audio.play().catch(error => {
    console.error("Ошибка воспроизведения звука:", error);
  });
};