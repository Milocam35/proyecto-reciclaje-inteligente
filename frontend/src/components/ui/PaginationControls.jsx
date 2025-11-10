function PaginationControls({ currentPage, totalPages, onPageChange }) {
  if (totalPages <= 1) return null; // No mostrar si solo hay una página

  const pages = Array.from({ length: totalPages }, (_, i) => i + 1);

  return (
    <div className="flex justify-center items-center space-x-3 mt-6">
      {pages.map((page) => (
        <button
          key={page}
          onClick={() => onPageChange(page)}
          className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold transition-all duration-200 ${
            page === currentPage
              ? "bg-[#3B82F6] text-white scale-110 shadow-md"
              : "bg-gray-200 text-gray-700 hover:bg-gray-300"
          }`}
          aria-label={`Ir a la página ${page}`}
        >
          {page}
        </button>
      ))}
    </div>
  );
}

export default PaginationControls;