// frontend/src/App.jsx
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/login';
import Register from './pages/register';
import Dashboard from './pages/dashboard';
import MyCard from './pages/mycard';
import Wallet from './pages/wallet';
import JourneyHistory from './pages/journeyhistory';
import ReportIssue from './pages/reportissue';
import AdminDashboard from './pages/admindashboard'; // <-- Import

function App() {
  const isAuthenticated = !!localStorage.getItem('token');

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        
        {/* Passenger Routes */}
        <Route path="/dashboard" element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />} />
        <Route path="/card" element={isAuthenticated ? <MyCard /> : <Navigate to="/login" />} />
        <Route path="/wallet" element={isAuthenticated ? <Wallet /> : <Navigate to="/login" />} />
        <Route path="/history" element={isAuthenticated ? <JourneyHistory /> : <Navigate to="/login" />} />
        <Route path="/report" element={isAuthenticated ? <ReportIssue /> : <Navigate to="/login" />} />
        
        {/* Admin Route */}
        <Route path="/admin" element={isAuthenticated ? <AdminDashboard /> : <Navigate to="/login" />} />
        
        <Route path="*" element={<Navigate to={isAuthenticated ? "/dashboard" : "/login"} />} />
      </Routes>
    </Router>
  );
}

export default App;