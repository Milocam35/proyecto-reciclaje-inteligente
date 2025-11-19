import { useState, useEffect } from "react";
import { login, logout, currentUser } from "../../services/authService";

export const useAuth = () => {
  const [user, setUser] = useState(undefined); // undefined = cargando
  const [loading, setLoading] = useState(false);

  // Cargar sesión
  useEffect(() => {
    const loadSession = async () => {
      const session = await currentUser();
      setUser(session); // null si no hay
    };
    loadSession();
  }, []);

  const handleLogin = async (username, password) => {
    setLoading(true);
    const res = await login(username, password);
    setLoading(false);

    if (res.ok) setUser(res.user);
    return res;
  };

  const handleLogout = async () => {
    await logout();
    setUser(null);
  };

  return {
    user,          // null = no logueado / undefined = cargando
    loading,
    handleLogin,
    handleLogout,
  };
};
