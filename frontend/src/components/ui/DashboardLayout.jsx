const DashboardLayout = ({ topCharts, bottomCharts }) => {
  return (
    <div className="relative w-full px-6 -mt-16 space-y-8">
      {/* Fila superior con 3 gráficas */}
      <div className="grid grid-cols-1 sm:grid-cols-3 lg:grid-cols-3 gap-6">
        {topCharts}
      </div>

      {/* Fila inferior con 2 gráficas */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
        {bottomCharts}
      </div>
    </div>
  );
};

export default DashboardLayout;
