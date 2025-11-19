import { createContext, useContext, useEffect, useState } from "react";
import { currentUser } from "../../services/authService.js";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(undefined); // undefined = loading

  useEffect(() => {
    const load = async () => {
      const u = await currentUser(); // ← 🔥 Esperamos la promesa
      setUser(u);                    // ← guardamos el objeto real
    };
    load();
  }, []);

  return (
    <AuthContext.Provider value={{ user, setUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuthContext() {
  return useContext(AuthContext);
}
