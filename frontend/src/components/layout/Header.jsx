import { FaRecycle } from "react-icons/fa6";
import { useLocation } from "react-router-dom";

function Header() {
  const location = useLocation();
  
  // Rutas donde NO debe aparecer el botón
  const hideButtonRoutes = ["/admin/miperfil", "/admin/revision"];
  const shouldShowButton = !hideButtonRoutes.includes(location.pathname);

  return (
    <header className="w-full flex items-center justify-between bg-[#3B82F6] px-8 py-8">
      {/* Logo y nombre */}
      <div className="flex items-center gap-4">
        <FaRecycle size={70} color="white"/>
        <h1 className="text-3xl font-bold text-white">Ecovision</h1>
      </div>

      {/* Título centrado */}
      <h1 className="text-3xl font-bold text-white absolute left-1/2 transform -translate-x-1/2">
        DashBoard
      </h1>

      {/* Botón condicional */}
      {shouldShowButton && (
        <button className="bg-white text-gray-800 px-4 py-3 rounded-lg shadow-sm font-medium hover:bg-gray-100 cursor-pointer hover:text-black transition">
          Create Report
        </button>
      )}
    </header>
  );
}

export default Header;