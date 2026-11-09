import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Home, CreditCard, Wallet, History, AlertTriangle, LogOut } from 'lucide-react';

export default function Layout({ children }) {
    const location = useLocation();
    const navigate = useNavigate();

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/login');
    };

    const navItems = [
        { path: '/dashboard', icon: <Home size={20} />, label: 'Home' },
        { path: '/card', icon: <CreditCard size={20} />, label: 'Card' },
        { path: '/wallet', icon: <Wallet size={20} />, label: 'Wallet' },
        { path: '/history', icon: <History size={20} />, label: 'History' },
        { path: '/report', icon: <AlertTriangle size={20} />, label: 'Report' },
    ];

    return (
        <div className="min-h-screen bg-bmtc-cream pb-20">
            {/* Top Header */}
            <div className="bg-bmtc-dark text-bmtc-cream p-4 flex justify-between items-center shadow-md sticky top-0 z-50">
                <h1 className="text-xl font-bold tracking-wider">SMART BMTC</h1>
                <button onClick={handleLogout} className="p-2 bg-bmtc-blue rounded-full hover:bg-bmtc-navy transition-colors">
                    <LogOut size={18} />
                </button>
            </div>

            {/* Main Content */}
            <div className="p-4 max-w-md mx-auto">
                {children}
            </div>

            {/* Bottom Navigation */}
            <div className="fixed bottom-0 left-0 right-0 bg-bmtc-tan border-t border-bmtc-blue/20 flex justify-around p-2 max-w-md mx-auto rounded-t-xl shadow-lg z-50">
                {navItems.map((item) => (
                    <Link 
                        key={item.path} 
                        to={item.path}
                        className={`flex flex-col items-center p-2 transition-colors ${location.pathname === item.path ? 'text-bmtc-dark font-bold' : 'text-bmtc-blue hover:text-bmtc-dark'}`}
                    >
                        {item.icon}
                        <span className="text-[10px] mt-1 font-semibold">{item.label}</span>
                    </Link>
                ))}
            </div>
        </div>
    );
}