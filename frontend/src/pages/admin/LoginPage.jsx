import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { FaUserCircle } from "react-icons/fa";
import { useAuth } from "../../hooks/useAuth";

export default function LoginPage() {
  const navigate = useNavigate();
  const { handleLogin, loading, user } = useAuth();

  const [usuario, setUsuario] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  // Redirigir si ya está logueado
  useEffect(() => {
    if (user) {
      navigate("/admin", { replace: true });
    }
  }, [user, navigate]);

  if (user === undefined) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-linear-to-br from-blue-700 to-blue-500 text-white text-lg">
        Verificando sesión...
      </div>
    );
  }

  const onSubmit = async (e) => {
    e.preventDefault();
    setError("");

    const res = await handleLogin(usuario, password);
    if (!res.ok) {
      setError(res.message || "Login incorrecto");
      return;
    }

    navigate("/admin");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-linear-to-br from-blue-700 to-blue-500 p-4">
      <div className="w-full max-w-md bg-white shadow-2xl rounded-3xl p-8 border border-gray-200 animate-fadeIn">
        <div className="flex justify-center mb-4">
          <FaUserCircle className="text-7xl text-blue-600" />
        </div>

        <h1 className="text-3xl font-bold text-gray-800 mb-2 text-center">
          Iniciar sesión
        </h1>

        {error && (
          <div className="text-sm text-red-600 bg-red-50 border border-red-200 p-2 rounded-lg mb-3 text-center">
            {error}
          </div>
        )}

        <form onSubmit={onSubmit} className="space-y-5">
          <label className="block">
            <span className="text-sm font-semibold text-gray-700">Usuario</span>
            <input
              type="text"
              value={usuario}
              onChange={(e) => setUsuario(e.target.value)}
              className="mt-1 w-full rounded-lg bg-gray-50 border border-gray-300 text-gray-800 px-3 py-2 shadow-sm focus:ring-2 focus:ring-blue-500 outline-none transition"
              autoComplete="username"
            />
          </label>

          <label className="block relative">
            <span className="text-sm font-semibold text-gray-700">
              Contraseña
            </span>
            <input
              type={showPassword ? "text" : "password"}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 w-full rounded-lg bg-gray-50 border border-gray-300 text-gray-800 px-3 py-2 pr-12 shadow-sm focus:ring-2 focus:ring-blue-500 outline-none transition"
              autoComplete="current-password"
            />
            <button
              type="button"
              onClick={() => setShowPassword((s) => !s)}
              className="absolute right-3 top-9 text-xs text-blue-600 hover:text-blue-800 transition"
            >
              {showPassword ? "Ocultar" : "Mostrar"}
            </button>
          </label>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-xl font-semibold shadow-lg transition active:scale-95"
          >
            {loading ? "Cargando..." : "Ingresar"}
          </button>
          <Link
            to="/"
            className="block w-full text-center text-blue-600 hover:text-blue-800 font-medium mt-2"
          >
            Regresar a home
          </Link>
        </form>
      </div>
    </div>
  );
}
