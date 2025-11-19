import { Link, useLocation, useNavigate } from "react-router-dom";

function AdminToggleButton() {
  const location = useLocation();
  const navigate = useNavigate();
  const isAdminPage = location.pathname.startsWith("/admin");

  const handleLogout = () => {
    localStorage.removeItem("token");
    sessionStorage.clear();
    navigate("/");
  };

  if (isAdminPage) {
    return (
      <button
        onClick={handleLogout}
        className="mt-4 bg-white text-gray-800 px-4 py-3 rounded-lg shadow-sm font-medium hover:bg-gray-100 cursor-pointer hover:text-black transition inline-block"
      >
        Home
      </button>
    );
  }

  return (
    <Link
      to="/login"
      className="mt-4 bg-white text-gray-800 px-4 py-3 rounded-lg shadow-sm font-medium hover:bg-gray-100 cursor-pointer hover:text-black transition inline-block"
    >
      Admin
    </Link>
  );
}

export default AdminToggleButton;
