import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import MainPage from "../pages/home/MainPage.jsx";
import AdminPage from "../pages/admin/AdminPage.jsx";
import LoginPage from "../pages/admin/LoginPage.jsx";
import ReviewPage from "../pages/admin/ReviewPage.jsx";
import MiPerfil from "../pages/admin/MiPerfil.jsx";

import PrivateRoute from "./PrivateRoute.jsx";

function AppRoutes() {
  return (
    <Router>
      <Routes>
        {/* PÚBLICA */}
        <Route path="/" element={<MainPage />} />

        {/* LOGIN */}
        <Route path="/login" element={<LoginPage />} />

        {/* TODAS LAS RUTAS PROTEGIDAS */}
        <Route
          path="/admin"
          element={
            <PrivateRoute>
              <AdminPage />
            </PrivateRoute>
          }
        />

        <Route
          path="/admin/revision"
          element={
            <PrivateRoute>
              <ReviewPage />
            </PrivateRoute>
          }
        />

        <Route
          path="/admin/miperfil"
          element={
            <PrivateRoute>
              <MiPerfil />
            </PrivateRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default AppRoutes;
