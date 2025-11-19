import EventRow from "./EventRow.jsx";

function EventList({ events, onSelectEvent }) {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-x-auto">
      <table className="min-w-full border-collapse">
        <thead>
          <tr className="bg-gray-100 text-gray-700 text-sm uppercase">
            <th className="px-6 py-3 text-left">ID Evento</th>
            <th className="px-6 py-3 text-left">Tipo Clasificado</th>
            <th className="px-6 py-3 text-left">Tipo Real</th>
            <th className="px-6 py-3 text-left">Confianza (%)</th>
            <th className="px-6 py-3 text-left">Hora Clasificado</th>
            <th className="px-6 py-3 text-left">Hora Sincronizado</th>
            <th className="px-6 py-3 text-left">Duración (s)</th>
          </tr>
        </thead>
        <tbody>
          {events.map((event) => (
            <EventRow
              key={event.id}
              event={event}
              onClick={() => onSelectEvent(event)}
            />
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default EventList;
