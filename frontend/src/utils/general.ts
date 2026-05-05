export const formatShortDate = (isoString: string): string => {
  const date = new Date(isoString);
  if (isNaN(date.getTime())) return '—';

  const pad = (num: number) => num.toString().padStart(2, '0');

  const d = pad(date.getDate());
  const m = pad(date.getMonth() + 1);
  const y = date.getFullYear();
  const h = pad(date.getHours());
  const min = pad(date.getMinutes());

  return `${d}.${m}.${y} ${h}:${min}`;
};