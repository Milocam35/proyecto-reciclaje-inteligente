import Header from '../../components/layout/Header.jsx'
import Footer from '../../components/layout/Footer.jsx'

import DashboardLayout from '../../components/MainComponents/DashboardLayout.jsx'
import ChartCard from '../../components/MainComponents/ChartCard.jsx'

import CustomBarChart from '../../components/MainComponents/charts/BarChart.jsx'
import CustomPieChart from '../../components/MainComponents/charts/PieChart.jsx'

function AdminPage() {
  return (
    <div className="flex flex-col min-h-screen relative bg-gray-100">
      {/* Header */}
      <Header />

      {/* Contenedor principal */}
      <main className="grow relative pb-24">
        {/* Fondo superior (título "Dashboard" eliminado para evitar repetición) */}
        <div className="relative h-32 md:h-36 bg-[#76e0c9] w-full rounded-b-3xl shadow-md flex flex-col justify-center items-center">

          {/* Menú elevado dentro del header (más arriba) */}
          <div className="absolute top-6 md:top-2 left-1/2 transform -translate-x-1/2 z-50">
            <div className="bg-white shadow-lg rounded-full px-8 py-2 flex space-x-6 md:space-x-8 border border-gray-200">
              <button className="text-gray-700 font-semibold hover:text-[#2b7a78] transition-colors">
                Mi Perfil
              </button>
              <button className="text-gray-700 font-semibold hover:text-[#2b7a78] transition-colors">
                Menú Principal
              </button>
              <button className="text-gray-700 font-semibold hover:text-[#2b7a78] transition-colors">
                Notificaciones
              </button>
              <button className="text-gray-700 font-semibold hover:text-[#2b7a78] transition-colors">
                Revisión
              </button>
            </div>
          </div>
        </div>

        {/* Reducir el margen superior para evitar espacio innecesario ahora que el menú subió */}
        <div className="mt-9">
          {/* Layout de gráficas — ahora se superponen sobre el header */}
          <div className="relative">
            <div className="relative -mt-16 md:-mt-24 z-50">
              <DashboardLayout
                topCharts={
                  <>
                    <ChartCard title="Usuarios Registrados">
                      <CustomBarChart />
                    </ChartCard>

                    <ChartCard title="Actividad del Sistema">
                      <CustomPieChart />
                    </ChartCard>

                    <ChartCard title="Estadísticas de Sesiones">
                      <p className="text-gray-400 text-sm">[Gráfica aquí]</p>
                    </ChartCard>
                  </>
                }
                bottomCharts={
                  <>
                    <ChartCard title="Rendimiento de Servicios">
                      <p className="text-gray-400 text-sm">[Gráfica aquí]</p>
                    </ChartCard>

                    <ChartCard title="Logs del Sistema">
                      <p className="text-gray-400 text-sm">[Gráfica aquí]</p>
                    </ChartCard>
                  </>
                }
              />
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <Footer />
    </div>
  )
}

export default AdminPage
