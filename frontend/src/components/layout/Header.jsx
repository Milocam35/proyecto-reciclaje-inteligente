import { FaRecycle } from "react-icons/fa6";

function Header() {
  return (
    <header className="w-full flex items-center justify-between bg-[#3B82F6] px-8 py-8">
      {/* Título y breadcrumb */}
      
      <div className="flex items-center gap-4">
        <FaRecycle size={70} color="white"/>
        <h1 className="text-3xl font-bold text-white">Ecovision</h1>
      </div>

      <h1 className="text-3xl font-bold text-white">DashBoard</h1>

      {/* Botón principal */}
      <button className="bg-white text-gray-800 px-4 py-3 rounded-lg shadow-sm font-medium hover:bg-gray-100 cursor-pointer hover:text-black transition">
        Create Report
      </button>
    </header>
  );
}

export default Header