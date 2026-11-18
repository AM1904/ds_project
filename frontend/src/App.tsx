import { Navigate, Route, Routes } from 'react-router-dom';
import { AppShell } from './components/AppShell';
import { Protected } from './components/Protected';
import Login from './pages/Login';
import Student from './pages/Student';
import Faculty from './pages/Faculty';
import FacultyRequests from './pages/FacultyRequests';
import AdminTimetable from './pages/AdminTimetable';
import AdminNew from './pages/AdminNew';
import AdminRequests from './pages/AdminRequests';


export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<Login />} />
      <Route element={<Protected roles={['Student']}><AppShell /></Protected>}>
        <Route path="/student" element={<Student />} />
      </Route>
      <Route element={<Protected roles={['Faculty']}><AppShell /></Protected>}>
        <Route path="/faculty" element={<Faculty />} />
        <Route path="/faculty/requests" element={<FacultyRequests />} />
      </Route>
      <Route element={<Protected roles={['Admin']}><AppShell /></Protected>}>
        <Route path="/admin" element={<AdminTimetable />} />
        <Route path="/admin/new" element={<AdminNew />} />
        <Route path="/admin/requests" element={<AdminRequests />} />
      </Route>
      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}
