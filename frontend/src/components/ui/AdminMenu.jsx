import { Link } from "react-router-dom";

function AdminMenu() {
  return (
    <div className="absolute top-6 md:top-2 left-1/2 transform -translate-x-1/2 z-50">
      <div className="bg-white shadow-lg rounded-full px-8 py-2 flex space-x-6 md:space-x-8 border border-gray-200">
        <Link 
          to="/admin/miperfil"
          className="text-gray-700 font-semibold hover:text-[#2b7a78] transition-colors">
          Mi Perfil
        </Link>
        <Link
          to="/admin"
          className="text-gray-700 font-semibold hover:text-[#2b7a78] transition-colors">
          Menú Principal
        </Link>
        <button className="text-gray-700 font-semibold hover:text-[#2b7a78] transition-colors">
          Notificaciones
        </button>

        {/* Enlace hacia la página de revisión */}
        <Link
          to="/admin/revision"
          className="text-gray-700 font-semibold hover:text-[#2b7a78] transition-colors"
        >
          Revisión
        </Link>
      </div>
    </div>
  );
}

export default AdminMenu;
