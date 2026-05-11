export const formatShortDate = (isoString: string): string => {
  // Добавляем 'Z' на конец строки, если бэкенд прислал дату без зоны.
  // Это заставит JS понять, что время в UTC, и он сам прибавит часы для локальной зоны.
  const safeIsoString = isoString.endsWith('Z') ? isoString : `${isoString}Z`;
  
  const date = new Date(safeIsoString);
  if (isNaN(date.getTime())) return '—';

  const pad = (num: number) => num.toString().padStart(2, '0');

  const d = pad(date.getDate());
  const m = pad(date.getMonth() + 1);
  const y = date.getFullYear();
  const h = pad(date.getHours());
  const min = pad(date.getMinutes());

  return `${d}.${m}.${y} ${h}:${min}`;
};