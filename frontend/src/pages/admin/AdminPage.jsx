import Header from '../../components/layout/Header.jsx';
import Footer from '../../components/layout/Footer.jsx';

import DashboardLayout from '../../components/ui/DashboardLayout.jsx';
import ChartCard from '../../components/ui/ChartCard.jsx';

import CustomBarChart from '../../components/ui/charts/BarChart.jsx';
import CustomPieChart from '../../components/ui/charts/PieChart.jsx';
import AdminMenu from '../../components/ui/AdminMenu.jsx'; // 👈 nuevo import

function AdminPage() {
  return (
    <div className="flex flex-col min-h-screen relative bg-gray-100">
      {/* Header */}
      <Header />

      {/* Contenedor principal */}
      <main className="grow relative pb-24">
        {/* Fondo superior */}
        <div className="relative h-32 md:h-36 bg-[#3B82F6] w-full rounded-b-3xl shadow-md flex flex-col justify-center items-center">

          {/* 👇 Menú elevado ahora importado como componente */}
          <AdminMenu />
        </div>

        {/* Reducir el margen superior */}
        <div className="mt-9">
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
  );
}

export default AdminPage;
