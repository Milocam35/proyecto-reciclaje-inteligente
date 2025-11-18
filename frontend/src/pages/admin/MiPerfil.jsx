import Header from "../../components/layout/Header.jsx";
import Footer from "../../components/layout/Footer.jsx";
import AdminMenu from "../../components/ui/AdminMenu.jsx";
import { FaCircleUser } from "react-icons/fa6";
import { useNavigate } from "react-router-dom";

export default function AdminProfilePage() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    sessionStorage.clear();
    navigate("/login");
  };

  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      <Header />

      <main className="grow relative pb-24">
        {/* Banner superior con menú admin */}
        <div className="relative h-32 md:h-36 bg-blue-500 w-full rounded-b-3xl shadow-md flex justify-center items-center">
          <AdminMenu />
        </div>

        {/* Contenedor superpuesto: se usa negative margin para montarlo sobre el banner */}
        <div className="relative -mt-28 z-50 flex flex-col items-center p-6 w-full">
          <div className="w-full max-w-6xl bg-white shadow-lg rounded-2xl p-8 mt-10">
            <h1 className="text-2xl font-semibold text-center mb-8">Perfil del Administrador</h1>
            
            {/* Contenedor de 3 columnas */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              
              {/* Columna 1: Icono y nombre */}
              <div className="flex flex-col items-center justify-center space-y-4 p-6">
                <FaCircleUser className="text-9xl text-gray-400" aria-hidden="true" />
                <h2 className="text-2xl font-semibold text-center">Admin Demo</h2>
                <p className="text-gray-600 text-center text-lg">Administrador</p>
              </div>

              {/* Columna 2: Información del usuario */}
              <div className="space-y-6 p-6">
                <h2 className="text-xl font-medium mb-6">Información del usuario</h2>
                <div className="space-y-4">
                  <div>
                    <p className="font-semibold text-gray-700 text-lg mb-2">Nombre</p>
                    <p className="text-gray-900 text-lg border border-gray-300 rounded-lg p-3">Admin Demo</p>
                  </div>
                  <div>
                    <p className="font-semibold text-gray-700 text-lg mb-2">Usuario</p>
                    <p className="text-gray-900 text-lg border border-gray-300 rounded-lg p-3">admin</p>
                  </div>
                  <div>
                    <p className="font-semibold text-gray-700 text-lg mb-2">Email</p>
                    <p className="text-gray-900 text-lg border border-gray-300 rounded-lg p-3">admin@example.com</p>
                  </div>
                </div>
              </div>

              {/* Columna 3: Botones de acción */}
              <div className="flex flex-col justify-center space-y-6 p-6">
                <button className="w-full bg-blue-500 text-white py-4 rounded-xl hover:bg-blue-600 transition font-medium text-lg">
                  Editar información
                </button>
                <button 
                  onClick={handleLogout}
                  className="w-full bg-red-500 text-white py-4 rounded-xl hover:bg-red-600 transition font-medium text-lg"
                >
                  Cerrar sesión
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}