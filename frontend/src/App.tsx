import { Link, Navigate, Route, Routes } from 'react-router-dom';
import ChatPage from './pages/ChatPage';
import RedeemPage from './pages/RedeemPage';
import SkillPage from './pages/SkillPage';
import AdminLoginPage from './pages/AdminLoginPage';
import AdminPage from './pages/AdminPage';

export default function App() {
  return (
    <div>
      <nav className="topbar">
        <Link to="/skill">安装 Skill</Link>
        <Link to="/redeem">兑换 token</Link>
        <Link to="/chat">API 使用说明</Link>
        <Link to="/admin">管理员</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Navigate to="/skill" replace />} />
        <Route path="/skill" element={<SkillPage />} />
        <Route path="/redeem" element={<RedeemPage />} />
        <Route path="/chat" element={<ChatPage />} />
        <Route path="/admin/login" element={<AdminLoginPage />} />
        <Route path="/admin" element={<AdminPage />} />
      </Routes>
    </div>
  );
}
