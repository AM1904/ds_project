import { useEffect, useId, useRef, type ReactNode } from 'react';
import { X } from 'lucide-react';

interface Props {
  open: boolean;
  onClose: () => void;
  title: string;
  children: ReactNode;
  size?: 'sm' | 'md' | 'lg';
}

/** Native <dialog>: focus trap, Escape, aria-modal and focus restore come from the platform. */
export function Dialog({ open, onClose, title, children, size = 'md' }: Props) {
  const ref = useRef<HTMLDialogElement>(null);
  const titleId = useId();

  useEffect(() => {
    const d = ref.current;
    if (!d) return;
    if (open && !d.open) {
      d.showModal();
      const first = d.querySelector<HTMLElement>('[autofocus], input:not([type=hidden]), select, textarea');
      first?.focus();
    }
    if (!open && d.open) d.close();
  }, [open]);

  return (
    <dialog
      ref={ref}
      className={`dialog dialog-${size}`}
      aria-labelledby={titleId}
      onCancel={e => { e.preventDefault(); onClose(); }}
      onMouseDown={e => { if (e.target === ref.current) onClose(); }}
    >
      {open && (
        <div className="dialog-inner">
          <header className="dialog-head">
            <h3 id={titleId}>{title}</h3>
            <button type="button" className="btn btn-icon btn-ghost" aria-label="Close dialog" onClick={onClose}>
              <X className="ico" aria-hidden="true" />
            </button>
          </header>
          {children}
        </div>
      )}
    </dialog>
  );
}
