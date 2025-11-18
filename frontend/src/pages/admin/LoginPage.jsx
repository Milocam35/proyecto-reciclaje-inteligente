import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { FaUserCircle } from "react-icons/fa";

/**
 * Login básico con credenciales quemadas:
 *   usuario: admin
 *   contraseña: admin123
 *
 * No incluye Header ni Footer (como pediste).
 */

export default function LoginPage() {
  const navigate = useNavigate();

  const [usuario, setUsuario] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  // Credenciales "quemadas"
  const ADMIN_USER = "admin";
  const ADMIN_PASS = "admin123";

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");

    // Validación simple
    if (!usuario || !password) {
      setError("Por favor ingresa usuario y contraseña.");
      return;
    }

    // Comparar con las credenciales quemadas
    if (usuario === ADMIN_USER && password === ADMIN_PASS) {
      // Guardar flag simple (opcional) y redirigir
      localStorage.setItem("isAdminLogged", "true");
      navigate("/admin");
    } else {
      setError("Credenciales inválidas. Intenta de nuevo.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-blue-500">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-lg p-6">
        {/* Icono insertado en la parte superior del cuadro de credenciales */}
        <div className="flex justify-center mb-4">
          <FaUserCircle className="text-6xl text-[#19363a]" aria-hidden="true" />
        </div>

        <h1 className="text-2xl font-bold text-gray-800 mb-2 text-center">Iniciar sesión</h1>
        <p className="text-sm text-gray-500 mb-6 text-center">
          Ingresa las credenciales de administrador.
        </p>

        <form onSubmit={handleSubmit} className="space-y-4">
          <label className="block">
            <span className="text-sm font-medium text-gray-700">Usuario</span>
            <input
              type="text"
              value={usuario}
              onChange={(e) => setUsuario(e.target.value)}
              className="mt-1 block w-full rounded-lg border-gray-200 shadow-sm focus:ring-2 focus:ring-[#3B82F6] focus:outline-none hover:border-[#3B82F6] px-3 py-2 transition-colors"
              placeholder="admin"
              aria-label="Usuario"
              autoComplete="username"
            />
          </label>

          <label className="block relative">
            <span className="text-sm font-medium text-gray-700">Contraseña</span>
            <input
              type={showPassword ? "text" : "password"}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 block w-full rounded-lg border-gray-200 shadow-sm focus:ring-2 focus:ring-[#3B82F6] focus:outline-none hover:border-[#3B82F6] px-3 py-2 pr-10 transition-colors"
              placeholder="••••••••"
              aria-label="Contraseña"
              autoComplete="current-password"
            />
            <button
              type="button"
              onClick={() => setShowPassword((s) => !s)}
              className="absolute right-2 top-9 text-sm text-gray-500 hover:text-gray-700"
              aria-label={showPassword ? "Ocultar contraseña" : "Mostrar contraseña"}
            >
              {showPassword ? "Ocultar" : "Mostrar"}
            </button>
          </label>

          {error && (
            <div className="text-sm text-red-600 bg-red-50 p-2 rounded">{error}</div>
          )}

          <button
            type="submit"
            className="w-full bg-[#19363a] text-white py-2 rounded-lg font-medium hover:opacity-95 transition"
          >
            Ingresar
          </button>
        </form>
      </div>
    </div>
  );
}
