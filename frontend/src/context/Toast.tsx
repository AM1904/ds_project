import { createContext, useCallback, useContext, useMemo, useRef, useState, type ReactNode } from 'react';
import { AlertTriangle, CheckCircle2, Info, X } from 'lucide-react';

type Kind = 'success' | 'error' | 'info';
interface ToastAction { label: string; onClick: () => void }
interface ToastItem { id: number; message: string; kind: Kind; action?: ToastAction }
type Push = (message: string, kind?: Kind, action?: ToastAction) => void;

const Ctx = createContext<Push>(() => {});
export const useToast = () => useContext(Ctx);

const ICON = { success: CheckCircle2, error: AlertTriangle, info: Info } as const;

export function ToastProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<ToastItem[]>([]);
  const next = useRef(1);

  const dismiss = useCallback((id: number) => setItems(list => list.filter(t => t.id !== id)), []);
  const push = useCallback<Push>((message, kind = 'info', action) => {
    const id = next.current++;
    setItems(list => [...list.slice(-3), { id, message, kind, action }]);
    window.setTimeout(() => dismiss(id), action ? 8000 : kind === 'error' ? 7000 : 4500);
  }, [dismiss]);
  const value = useMemo(() => push, [push]);

  return (
    <Ctx.Provider value={value}>
      {children}
      <div className="toasts" role="status" aria-live="polite">
        {items.map(t => {
          const Icon = ICON[t.kind];
          return (
            <div key={t.id} className={`toast toast-${t.kind}`}>
              <Icon className="ico" aria-hidden="true" />
              <span>{t.message}</span>
              {t.action && (
                <button type="button" className="toast-action" onClick={() => { t.action!.onClick(); dismiss(t.id); }}>
                  {t.action.label}
                </button>
              )}
              <button type="button" className="toast-x" aria-label="Dismiss" onClick={() => dismiss(t.id)}>
                <X className="ico" aria-hidden="true" />
              </button>
            </div>
          );
        })}
      </div>
    </Ctx.Provider>
  );
}
