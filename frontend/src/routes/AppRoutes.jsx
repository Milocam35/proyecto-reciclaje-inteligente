import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainPage from '../pages/home/MainPage.jsx';

function AppRoutes() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainPage />} />
      </Routes>
    </Router>
  )
}

export default AppRoutes;