import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainPage from '../pages/home/MainPage.jsx';
import AdminPage from '../pages/admin/AdminPage.jsx';
import LoginPage from '../pages/admin/LoginPage.jsx';

function AppRoutes() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainPage />} />
        <Route path="/admin" element={<AdminPage />} />
        <Route path="/login" element={<LoginPage />} />
      </Routes>
    </Router>
  )
}

export default AppRoutes;