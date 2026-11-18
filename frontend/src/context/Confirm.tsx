import { createContext, useCallback, useContext, useRef, useState, type ReactNode } from 'react';
import { Dialog } from '../components/Dialog';

interface Options { title?: string; confirmText?: string; cancelText?: string; danger?: boolean }
type ConfirmFn = (message: string, options?: Options) => Promise<boolean>;

const Ctx = createContext<ConfirmFn>(() => Promise.resolve(false));
export const useConfirm = () => useContext(Ctx);

export function ConfirmProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<{ message: string; options: Options } | null>(null);
  const resolver = useRef<((v: boolean) => void) | null>(null);

  const confirm = useCallback<ConfirmFn>((message, options = {}) => new Promise(resolve => {
    resolver.current = resolve;
    setState({ message, options });
  }), []);

  const close = (value: boolean) => {
    resolver.current?.(value);
    resolver.current = null;
    setState(null);
  };

  return (
    <Ctx.Provider value={confirm}>
      {children}
      <Dialog open={!!state} onClose={() => close(false)} title={state?.options.title ?? 'Are you sure?'} size="sm">
        <p>{state?.message}</p>
        <div className="dialog-actions">
          <button type="button" className="btn" onClick={() => close(false)}>{state?.options.cancelText ?? 'Cancel'}</button>
          <button type="button" autoFocus className={`btn ${state?.options.danger ? 'btn-danger' : 'btn-primary'}`} onClick={() => close(true)}>
            {state?.options.confirmText ?? 'Confirm'}
          </button>
        </div>
      </Dialog>
    </Ctx.Provider>
  );
}
