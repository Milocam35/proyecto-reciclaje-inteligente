import { FaGithubAlt } from "react-icons/fa";
import { FaRecycle } from "react-icons/fa6";
import { IoMailOpenOutline } from "react-icons/io5";

function Footer() {
  return (
    <footer className="bg-[#19363a] text-gray-300 py-6 fixed bottom-0 w-full z-20">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row items-stretch">
          <div className="flex-1 py-4 text-left">
            <h3 className="text-white font-semibold">Acerca de nosotros</h3>
            <p className="text-sm text-gray-300 mt-2">
              Estudiantes de Ciencias de la Computación e inteligencia Artificial de la Universidad Sergio Arboleda
            </p>
          </div>

          <div className="flex-1 py-4 text-left md:px-6">
            <h3 className="text-white font-semibold">Acerca del proyecto</h3>
            <p className="text-sm text-gray-300 mt-2">
              Sistema inteligente de clasificación de residuos que combina visión por computador, sensores y servicios en la nube para identificar materiales reciclables en tiempo real, registrar datos y generar métricas operativas desde una plataforma web.
            </p>

            {/* Icono no clicable + enlace de Git al lado (alineados a la izquierda) */}
            <div className="mt-2 flex items-center text-gray-300 space-x-2 justify-start">
              <FaGithubAlt className="text-xl" aria-hidden="true" />
              <a
                href="https://github.com/Milocam35/proyecto-reciclaje-inteligente.git"
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm hover:text-white transition-colors"
              >
                proyecto-reciclaje-inteligente
              </a>
            </div>
          </div>

          <div className="flex-1 py-4 text-left md:px-6">
            <h3 className="text-white font-semibold flex items-center space-x-2">
              <IoMailOpenOutline className="text-xl text-gray-300" aria-hidden="true" />
              <span>Contacto</span>
            </h3>

            {/* Lista añadida debajo del título */}
            <ul className="mt-2 text-sm text-gray-300 space-y-1">
              <li>valentina.andrade01@usa.edu.co</li>
              <li>catalina.gutierrez01@usa.edu.co</li>
              <li>camilo.millan01@usa.edu.co</li>
              <li>mateo.patiño02@usa.edu.co</li>
            </ul>
          </div>

          {/* Columna EcoVision con ancho reducido para dejar más espacio a las otras secciones */}
          <div className="flex-none w-20 md:w-28 py-4 text-left md:px-6 flex flex-col items-center justify-center">
            <FaRecycle className="text-3xl md:text-4xl text-gray-200" aria-hidden="true" />
            <p className="text-white font-semibold mt-2">EcoVision</p>

            <button className="mt-4 bg-white text-gray-800 px-4 py-3 rounded-lg shadow-sm font-medium hover:bg-gray-100 cursor-pointer hover:text-black transition">
              Admin
            </button>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer;