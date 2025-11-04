import Header from '../../components/layout/Header.jsx'
import Footer from '../../components/layout/Footer.jsx'

import DashboardLayout from '../../components/MainComponents/DashboardLayout.jsx'
import ChartCard from '../../components/MainComponents/ChartCard.jsx'

import CustomBarChart from '../../components/MainComponents/charts/BarChart.jsx'
import CustomPieChart from '../../components/MainComponents/charts/PieChart.jsx'

function MainPage() {
  return (
    <div className="flex flex-col min-h-screen relative bg-gray-100">
      <Header />

      {/* Contenido principal: ocupa todo el alto restante */}
      <main className="grow relative pb-24">
        <div className="h-20 bg-[#76e0c9] w-full rounded-b-3xl shadow-md"></div>

        <DashboardLayout
          topCharts={
            <>
              <ChartCard title="Revenue Overview">
                <CustomBarChart />
              </ChartCard>

              <ChartCard title="Sales Distribution">
                <CustomPieChart />
              </ChartCard>

              <ChartCard title="Daily Performance">
                <p className="text-gray-400 text-sm">[Gráfica aquí]</p>
              </ChartCard>
            </>
          }
          bottomCharts={
            <>
              <ChartCard title="Summary Progress">
                <p className="text-gray-400 text-sm">[Gráfica aquí]</p>
              </ChartCard>

              <ChartCard title="Orders Analysis">
                <p className="text-gray-400 text-sm">[Gráfica aquí]</p>
              </ChartCard>
            </>
          }
        />
      </main>

      {/* Footer fijo */}
      <Footer />
    </div>
  )
}

export default MainPage
