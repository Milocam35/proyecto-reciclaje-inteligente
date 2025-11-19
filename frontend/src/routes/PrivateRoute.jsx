import { Navigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth.js";

export default function PrivateRoute({ children }) {
  const { user } = useAuth();

  // user === undefined → aún cargando sesión
  if (user === undefined) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        Verificando sesión...
      </div>
    );
  }

  // user === null → no autenticado
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  // Usuario autenticado → renderizar contenido
  return children;
}
