import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from 'react';
import { api } from '../lib/api';
import { useAuth } from './Auth';

interface BadgeValue {
  /** Admin: number of pending requests. */
  pending: number;
  /** Faculty: requests decided since the teacher last opened their Requests page. */
  newDecisions: number;
  refresh: () => void;
  /** Faculty: call when the Requests page is shown. */
  markDecisionsSeen: () => void;
}
const Ctx = createContext<BadgeValue>({ pending: 0, newDecisions: 0, refresh: () => {}, markDecisionsSeen: () => {} });
export const useBadges = () => useContext(Ctx);

const seenKey = (email: string) => `reqSeen:${email}`;

export function BadgesProvider({ children }: { children: ReactNode }) {
  const { user } = useAuth();
  const [pending, setPending] = useState(0);
  const [newDecisions, setNew] = useState(0);
  const [tick, setTick] = useState(0);

  useEffect(() => {
    if (!user) { setPending(0); setNew(0); return; }
    if (user.role === 'Admin') {
      api.requests({ status: 'pending' }).then(r => setPending(r.length)).catch(() => {});
    } else if (user.role === 'Faculty') {
      const seen = localStorage.getItem(seenKey(user.email)) ?? '';
      api.requests({ faculty_email: user.email })
        .then(r => setNew(r.filter(x => x.resolved_at && x.resolved_at > seen).length)).catch(() => {});
    }
  }, [user, tick]);

  const refresh = useCallback(() => setTick(t => t + 1), []);
  const markDecisionsSeen = useCallback(() => {
    if (!user) return;
    const d = new Date();
    const p = (n: number) => String(n).padStart(2, '0');
    localStorage.setItem(seenKey(user.email), `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}:${p(d.getSeconds())}`);
    setNew(0);
  }, [user]);

  const value = useMemo(() => ({ pending, newDecisions, refresh, markDecisionsSeen }), [pending, newDecisions, refresh, markDecisionsSeen]);
  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}
