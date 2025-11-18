function EventRow({ event, onClick }) {

  const confianzaPorcentaje = Math.round((event.confianza || 0) * 100);

  return (
    <tr
      className="border-b hover:bg-gray-200 cursor-pointer transition"
      onClick={onClick}
    >
      <td className="px-6 py-3 font-medium text-blue-600 hover:underline">
        #{event.id}
      </td>
      <td
        className={`px-6 py-3 font-medium ${
          event.tipoClasificado === "reciclable"
            ? "text-green-600"
            : "text-red-600"
        }`}
      >
        {event.tipoClasificado}
      </td>
      <td
        className={`px-6 py-3 font-medium ${
          event.tipoReal === "noRevisado"
            ? "text-yellow-600"
            : event.tipoReal === "reciclable"
            ? "text-green-600"
            : "text-red-600"
        }`}
      >
        {event.tipoReal}
      </td>
      <td className="px-6 py-3">
        <div className="flex items-center">
          <div className="w-24 bg-gray-200 rounded-full h-3 mr-2">
            <div
              className="bg-blue-500 h-3 rounded-full"
              style={{
                width: `${Math.min(confianzaPorcentaje, 100)}%`,
              }}
            ></div>
          </div>
          <span className="text-sm text-gray-700">{confianzaPorcentaje}%</span>
        </div>
      </td>
      <td className="px-6 py-3 text-gray-700">{event.horaClasificado}</td>
      <td className="px-6 py-3 text-gray-700">{event.horaSincronizado}</td>
      <td className="px-6 py-3 text-gray-700">{event.duracion}</td>
    </tr>
  );
}

export default EventRow;
