import { useEffect, useState } from "react";
import { getEvents } from "../../../services/eventsService.js";
import EventList from "../../components/review/EventList.jsx";
import EventModal from "../../components/review/EventModal.jsx";
import Header from "../../components/layout/Header.jsx";
import Footer from "../../components/layout/Footer.jsx";
import AdminMenu from "../../components/ui/AdminMenu.jsx";
import PaginationControls from "../../components/ui/PaginationControls.jsx";

function ReviewPage() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const pageSize = 10; // Máx 2 eventos por página

  useEffect(() => {
    const fetchEvents = async () => {
      setLoading(true);
      try {
        const data = await getEvents(currentPage, pageSize);

        // Caso 1: el backend devuelve { events, total }
        if (data.events && data.total) {
          setEvents(data.events);
          setTotalPages(Math.ceil(data.total / pageSize));
        }
        // Caso 2: el backend solo devuelve la lista
        else {
          setEvents(data);
          setTotalPages(Math.ceil(data.length / pageSize));
        }
      } catch (err) {
        setError("Error al obtener los datos del servidor");
      } finally {
        setLoading(false);
      }
    };

    fetchEvents();
  }, [currentPage]);

  return (
    <div className="flex flex-col min-h-screen relative bg-gray-100">
      <Header />

      <main className="grow relative pb-24">
        <div className="relative h-32 md:h-36 bg-[#3B82F6] w-full rounded-b-3xl shadow-md flex flex-col justify-center items-center">
          <AdminMenu />
        </div>

        <div className="relative -mt-24 md:-mt-32 z-50">
          <div className="container mx-auto px-4">
            <div className="bg-white rounded-3xl shadow-lg p-8 mt-12 md:mt-16">
              <h1 className="text-2xl font-semibold mb-6 text-gray-800 text-center">
                Revisión de Clasificaciones
              </h1>

              {loading ? (
                <p className="text-center mt-10 text-gray-500">Cargando datos...</p>
              ) : error ? (
                <p className="text-center mt-10 text-red-500">{error}</p>
              ) : (
                <>
                  <EventList events={events} onSelectEvent={setSelectedEvent} />
                  <PaginationControls
                    currentPage={currentPage}
                    totalPages={totalPages}
                    onPageChange={setCurrentPage}
                  />
                </>
              )}
            </div>
          </div>
        </div>

        {selectedEvent && (
          <EventModal event={selectedEvent} onClose={() => setSelectedEvent(null)} />
        )}
      </main>

      <Footer />
    </div>
  );
}

export default ReviewPage;
