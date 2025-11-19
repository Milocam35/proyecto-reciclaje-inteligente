import { useEffect, useRef } from "react";

export default function LogoutPopUp({ setShowLogoutConfirm, handleLogout }) {
  const panelRef = useRef(null);

  // Cerrar con Escape
  useEffect(() => {
    function onKey(e) {
      if (e.key === "Escape") setShowLogoutConfirm(false);
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [setShowLogoutConfirm]);

  // Click fuera del panel
  const onBackdropClick = (e) => {
    if (panelRef.current && !panelRef.current.contains(e.target)) {
      setShowLogoutConfirm(false);
    }
  };

  return (
    <div
      className="fixed inset-0 bg-black/50 flex justify-center items-center z-50"
      onMouseDown={onBackdropClick}
      role="dialog"
      aria-modal="true"
      aria-labelledby="logout-title"
    >
      <div
        ref={panelRef}
        className="bg-white p-6 rounded-2xl shadow-xl max-w-sm w-full text-center"
        onMouseDown={(e) => e.stopPropagation()} // evitar que el click en el panel cierre
      >
        <h2 id="logout-title" className="text-xl font-semibold mb-2">
          ¿Cerrar sesión?
        </h2>

        <p className="text-gray-600 mb-6">
          ¿Estás seguro de que deseas cerrar sesión?
        </p>

        <div className="flex gap-4 justify-center">
          <button
            type="button"
            onClick={() => setShowLogoutConfirm(false)}
            className="px-4 py-2 bg-gray-200 rounded-lg hover:bg-gray-300 transition font-medium cursor-pointer"
          >
            Cancelar
          </button>

          <button
            type="button"
            onClick={handleLogout}
            className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition font-medium cursor-pointer"
          >
            Sí, cerrar sesión
          </button>
        </div>
      </div>
    </div>
  );
}
