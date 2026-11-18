// All date maths is on local calendar dates ('YYYY-MM-DD'), never UTC, so week
// navigation behaves the same in every timezone.
const p2 = (n: number) => String(n).padStart(2, '0');

export const toISO = (d: Date) => `${d.getFullYear()}-${p2(d.getMonth() + 1)}-${p2(d.getDate())}`;
export const todayISO = () => toISO(new Date());
export const fromISO = (s: string) => new Date(`${s}T00:00:00`);

export function addDays(s: string, n: number) {
  const d = fromISO(s);
  d.setDate(d.getDate() + n);
  return toISO(d);
}
export function weekStart(s: string) {
  const d = fromISO(s);
  d.setDate(d.getDate() - ((d.getDay() + 6) % 7));
  return toISO(d);
}
export const isWeekend = (s: string) => [0, 6].includes(fromISO(s).getDay());
/** Saturday/Sunday -> the following Monday; weekdays unchanged. */
export function toWeekday(s: string) {
  const dow = fromISO(s).getDay();
  return dow === 6 ? addDays(s, 2) : dow === 0 ? addDays(s, 1) : s;
}
export const isValidISO = (s: string | null | undefined): s is string =>
  !!s && /^\d{4}-\d{2}-\d{2}$/.test(s) && !Number.isNaN(fromISO(s).getTime());

export function formatDay(s: string, opts: Intl.DateTimeFormatOptions = { weekday: 'short', day: 'numeric', month: 'short' }) {
  return fromISO(s).toLocaleDateString('en-IN', opts);
}
export function formatLong(s: string) {
  return formatDay(s, { weekday: 'long', day: 'numeric', month: 'short', year: 'numeric' });
}

/** 'YYYY-MM-DD HH:MM:SS' (server time) -> '18 Nov, 11:55 PM'. Anything else is returned unchanged. */
export function formatStamp(s: string) {
  const m = /^(\d{4}-\d{2}-\d{2})[ T](\d{2}):(\d{2})/.exec(s ?? '');
  if (!m) return s;
  const d = fromISO(m[1]);
  d.setHours(+m[2], +m[3]);
  return `${d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short' })}, ${d.toLocaleTimeString('en-IN', { hour: 'numeric', minute: '2-digit', hour12: true }).toUpperCase()}`;
}

const to24 = (t: string) => {
  const m = /^(\d{1,2}):(\d{2})\s*(AM|PM)$/i.exec(t.trim());
  if (!m) return null;
  return ((+m[1] % 12) + (m[3].toUpperCase() === 'PM' ? 12 : 0)) * 60 + +m[2];
};
/** '09:00 AM - 10:00 AM' -> '9:00–10:00 AM'; '11:15 AM - 12:15 PM' -> '11:15 AM–12:15 PM'. */
export function formatSlot(ts: string) {
  const [a, b] = ts.split(' - ');
  if (!a || !b) return ts;
  const strip = (t: string) => t.replace(/^0/, '');
  const mer = (t: string) => t.trim().slice(-2).toUpperCase();
  return mer(a) === mer(b) ? `${strip(a).replace(/\s*(AM|PM)$/i, '')}–${strip(b)}` : `${strip(a)}–${strip(b)}`;
}
/** True when `now` falls inside the slot on the given date. */
export function isSlotNow(date: string, ts: string, now = new Date()) {
  if (date !== toISO(now)) return false;
  const [a, b] = ts.split(' - ').map(to24);
  if (a == null || b == null) return false;
  const m = now.getHours() * 60 + now.getMinutes();
  return m >= a && m < b;
}

/** Days before today are read-only history. */
export const isPastDay = (s: string) => s < todayISO();
