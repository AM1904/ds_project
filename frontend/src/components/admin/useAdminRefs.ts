import { useCallback, useEffect, useState } from 'react';
import { api, ApiError } from '../../lib/api';
import type { Classroom, FacultyUser, Subject } from '../../lib/types';

export interface AdminRefs {
  subjects: Subject[]; faculty: FacultyUser[]; classrooms: Classroom[]; timeslots: string[]; sections: string[];
}

/** Reference lists every admin form needs, loaded once per page. */
export function useAdminRefs() {
  const [refs, setRefs] = useState<AdminRefs | null>(null);
  const [error, setError] = useState('');
  const [tries, setTries] = useState(0);

  useEffect(() => {
    let alive = true;
    setError('');
    Promise.all([api.subjects(), api.facultyUsers(), api.classrooms(), api.timeslots(), api.sections()])
      .then(([subjects, faculty, classrooms, timeslots, sections]) => alive && setRefs({ subjects, faculty, classrooms, timeslots, sections }))
      .catch(e => alive && setError(e instanceof ApiError ? e.message : 'Could not load reference data.'));
    return () => { alive = false; };
  }, [tries]);

  const retry = useCallback(() => setTries(n => n + 1), []);
  return { refs, error, retry };
}
