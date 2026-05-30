import { Link, Navigate, Route, Routes } from 'react-router-dom';
import RedeemPage from './pages/RedeemPage';
import ChatPage from './pages/ChatPage';
import AdminLoginPage from './pages/AdminLoginPage';
import AdminPage from './pages/AdminPage';

export default function App() {
  return (
    <div>
      <nav className="topbar">
        <Link to="/chat">API 使用说明</Link>
        <Link to="/redeem">兑换 token</Link>
        <Link to="/admin">管理员</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Navigate to="/chat" replace />} />
        <Route path="/redeem" element={<RedeemPage />} />
        <Route path="/chat" element={<ChatPage />} />
        <Route path="/admin/login" element={<AdminLoginPage />} />
        <Route path="/admin" element={<AdminPage />} />
      </Routes>
    </div>
  );
}
