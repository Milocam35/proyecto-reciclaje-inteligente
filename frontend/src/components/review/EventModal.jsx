import { useState } from "react";

function EventModal({ event, onClose }) {
  const [tipoReal, setTipoReal] = useState("");
  const isButtonDisabled = tipoReal === "";

  return (
    <div
      className="fixed inset-0 bg-white/30 backdrop-blur-sm flex justify-center items-center z-50 p-6"
      onClick={onClose}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        className="bg-white rounded-xl shadow-2xl p-6 w-[90%] md:w-[700px] relative border border-gray-200"
      >
        {/* Botón de cierre */}
        <button
          onClick={onClose}
          className="absolute top-3 right-3 text-gray-500 hover:text-gray-800 text-xl"
        >
          ✕
        </button>

        {/* Título */}
        <h2 className="text-xl font-semibold text-gray-800 mb-6 text-center">
          Detalles del Evento #{event.id}
        </h2>

        {/* Imagen */}
        <img
          src={event.rutaImagen}
          alt="Imagen del evento"
          className="w-full max-h-[350px] object-contain rounded-md mb-6 shadow-sm"
        />

        {/* Contenido dividido en dos columnas */}
        <div className="flex flex-col md:flex-row justify-between gap-6">
          {/* IZQUIERDA */}
          <div className="flex-1 text-sm text-gray-700">
            <div className="grid grid-cols-[150px_auto] gap-y-1">
              <p className="font-bold">Hora Clasificado:</p>
              <p>{event.horaClasificado}</p>

              <p className="font-bold">Hora Sincronizado:</p>
              <p>{event.horaSincronizado}</p>

              <p className="font-bold">Duración:</p>
              <p>{event.duracion}s</p>

              <p className="font-bold">Confianza:</p>
              <p>{event.confianza}%</p>
            </div>
          </div>

          {/* DERECHA */}
          <div className="flex-1 space-y-1 text-sm text-gray-700">
            {/* Tipo Clasificado */}
            <div className="grid grid-cols-[150px_auto] gap-y-2">
              <p className="font-bold">Tipo Clasificado:</p>
              <span
                className={`font-medium ${
                  event.tipoClasificado === "noRevisado"
                    ? "text-yellow-600"
                    : event.tipoClasificado === "reciclable"
                    ? "text-green-600"
                    : event.tipoClasificado === "organico"
                    ? "text-amber-700"
                    : "text-red-600"
                }`}
              >
                {event.tipoClasificado}
              </span>
            </div>

            {/* Tipo Real */}
            <div className="grid grid-cols-[150px_auto] gap-y-2">
              <p className="font-bold">Tipo Real:</p>
              <select
                value={tipoReal}
                onChange={(e) => setTipoReal(e.target.value)}
                className="border border-gray-300 rounded-md px-3 py-1.5 text-gray-700 focus:ring-2 focus:ring-blue-400 focus:outline-none text-sm"
              >
                <option value="">Seleccione...</option>
                <option value="reciclable">Reciclable</option>
                <option value="noReciclable">No Reciclable</option>
                <option value="organico">Orgánico</option>
              </select>
            </div>

            {/* Botón de enviar */}
            <button
              disabled={isButtonDisabled}
              className={`w-full mt-3 py-2 rounded-md font-medium transition-colors ${
                isButtonDisabled
                  ? "bg-gray-300 text-gray-500 cursor-not-allowed"
                  : "bg-[#3B82F6] text-white hover:bg-[#2563EB]"
              }`}
              onClick={() => alert(`Reporte enviado con tipo: ${tipoReal}`)}
            >
              Enviar Reporte
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default EventModal;
