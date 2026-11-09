// frontend/src/pages/AdminDashboard.jsx
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Users, CreditCard, Bus, Map, AlertTriangle, LogOut, TrendingUp, CheckCircle } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import api from '../services/api';

export default function AdminDashboard() {
    const [stats, setStats] = useState(null);
    const [hourlyData, setHourlyData] = useState([]);
    const [reports, setReports] = useState([]);
    const [recommendation, setRecommendation] = useState(null);
    const navigate = useNavigate();

    const fetchAdminData = async () => {
        try {
            const statsRes = await api.get('/admin/overview');
            setStats(statsRes.data);

            const hourlyRes = await api.get('/analytics/hourly-demand');
            setHourlyData(hourlyRes.data.map(item => ({ time: `${item.hour}:00`, passengers: item.passenger_count })));

            try {
                const recRes = await api.get('/recommendations/bus-allocation/1');
                setRecommendation(recRes.data);
            } catch (e) { console.log("No recommendation available"); }

            const reportsRes = await api.get('/safety/reports');
            setReports(reportsRes.data);

        } catch (error) {
            console.error("Failed to load admin data", error);
            if (error.response?.status === 403 || error.response?.status === 401) {
                alert("Access Denied: Admin privileges required.");
                navigate('/login');
            }
        }
    };

    useEffect(() => { fetchAdminData(); }, [navigate]);

    // NEW: Function to approve the bus move
    const handleApproveReallocation = async (busId, highRouteId) => {
        if (!window.confirm("Are you sure you want to reallocate this bus? This will affect passengers on the current route.")) return;
        
        try {
            // Calls the assignment endpoint from Day 6
            await api.post(`/buses/${busId}/assign/${highRouteId}`);
            alert("Success! Bus has been reallocated.");
            fetchAdminData(); // Refresh dashboard
        } catch (error) {
            alert("Failed to reallocate bus: " + (error.response?.data?.detail || "Unknown error"));
        }
    };

    const handleStatusChange = async (reportId, newStatus) => {
        try {
            await api.put(`/safety/reports/${reportId}/status`, { status: newStatus });
            fetchAdminData();
        } catch (error) {
            alert("Failed to update status");
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/login');
    };

    if (!stats) return <div className="min-h-screen flex items-center justify-center bg-bmtc-cream text-bmtc-dark font-bold text-xl">Loading Admin Panel...</div>;

    return (
        <div className="min-h-screen bg-bmtc-cream pb-10">
            <div className="bg-bmtc-dark text-bmtc-cream p-4 flex justify-between items-center shadow-md sticky top-0 z-50">
                <h1 className="text-xl font-bold tracking-wider">BMTC ADMIN CONTROL PANEL</h1>
                <button onClick={handleLogout} className="flex items-center gap-2 bg-bmtc-blue px-3 py-1.5 rounded-lg hover:bg-bmtc-navy transition">
                    <LogOut size={16} /> <span className="text-sm font-bold">Logout</span>
                </button>
            </div>

            <div className="p-4 md:p-6 max-w-7xl mx-auto space-y-6">
                
                {/* Overview Section */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="bg-bmtc-tan p-4 rounded-xl shadow-sm border border-bmtc-blue/20">
                        <div className="flex items-center gap-2 text-bmtc-blue mb-2"><Users size={20}/><span className="text-sm font-bold">Passengers</span></div>
                        <p className="text-3xl font-bold text-bmtc-dark">{stats.total_passengers}</p>
                    </div>
                    <div className="bg-bmtc-tan p-4 rounded-xl shadow-sm border border-bmtc-blue/20">
                        <div className="flex items-center gap-2 text-bmtc-sage mb-2"><CreditCard size={20}/><span className="text-sm font-bold">Active Cards</span></div>
                        <p className="text-3xl font-bold text-bmtc-dark">{stats.active_cards}</p>
                    </div>
                    <div className="bg-bmtc-tan p-4 rounded-xl shadow-sm border border-bmtc-blue/20">
                        <div className="flex items-center gap-2 text-bmtc-navy mb-2"><Bus size={20}/><span className="text-sm font-bold">Total Buses</span></div>
                        <p className="text-3xl font-bold text-bmtc-dark">{stats.total_buses}</p>
                    </div>
                    <div className="bg-bmtc-tan p-4 rounded-xl shadow-sm border border-bmtc-blue/20">
                        <div className="flex items-center gap-2 text-bmtc-blue mb-2"><Map size={20}/><span className="text-sm font-bold">Today's Journeys</span></div>
                        <p className="text-3xl font-bold text-bmtc-dark">{stats.todays_journeys}</p>
                    </div>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div className="lg:col-span-2 bg-white p-6 rounded-xl shadow-sm border border-bmtc-blue/20">
                        <h3 className="text-lg font-bold text-bmtc-dark mb-4 flex items-center gap-2"><TrendingUp size={20} className="text-bmtc-blue" /> Hourly Demand</h3>
                        <div className="h-72 w-full">
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={hourlyData}>
                                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#D4C4A8" />
                                    <XAxis dataKey="time" tick={{fill: '#415A77', fontSize: 12}} axisLine={false} tickLine={false} />
                                    <YAxis tick={{fill: '#415A77', fontSize: 12}} axisLine={false} tickLine={false} />
                                    <Tooltip cursor={{fill: '#F4F1DE'}} contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'}} />
                                    <Bar dataKey="passengers" fill="#415A77" radius={[4, 4, 0, 0]} />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </div>
                    
                    {/* AI Card */}
                    <div className="bg-bmtc-dark text-bmtc-cream p-6 rounded-xl shadow-md border border-bmtc-blue/30 flex flex-col justify-between">
                        <div>
                            <h3 className="text-sm font-bold text-bmtc-tan uppercase tracking-wider mb-2">AI Demand Alert</h3>
                            <h2 className="text-2xl font-bold mb-1">Route {recommendation?.high_demand_route || "Loading..."}</h2>
                            
                            <span className={`inline-block text-white text-xs font-bold px-2 py-1 rounded mb-4 ${
                                (recommendation?.high_route_occupancy || 0) > 90 ? 'bg-red-600' : 'bg-green-600'
                            }`}>
                                {(recommendation?.high_route_occupancy || 0) > 90 ? 'VERY HIGH CROWD' : 'OPTIMAL'}
                            </span>
                            
                            <p className="text-sm mb-4">Predicted occupancy: <strong>{recommendation?.high_route_occupancy || 0}%</strong></p>
                            
                            {recommendation && (
                                <div className="bg-bmtc-blue/30 p-3 rounded-lg text-sm border border-bmtc-blue/50 mb-4">
                                    <p className="font-bold mb-1">AI Suggestion:</p>
                                    <p className="text-bmtc-cream/90">{recommendation.action_required}</p>
                                </div>
                            )}
                        </div>

                        {/* Show button ONLY if there is a bus to reallocate */}
                        {recommendation && recommendation.suggested_bus_id && (
                            <button 
                                onClick={() => handleApproveReallocation(recommendation.suggested_bus_id, recommendation.high_route_id)}
                                className="w-full bg-green-500 hover:bg-green-400 text-white font-bold py-3 px-4 rounded-lg flex items-center justify-center gap-2 transition-colors mt-4"
                            >
                                <CheckCircle size={20} />
                                Approve Bus Reallocation
                            </button>
                        )}
                    </div>
                </div>

                {/* 5. Safety Monitoring */}
                <div className="bg-white p-6 rounded-xl shadow-sm border border-bmtc-blue/20">
                    <h3 className="text-lg font-bold text-bmtc-dark mb-4 flex items-center gap-2">
                        <AlertTriangle size={20} className="text-red-600" /> Safety & Incident Reports
                    </h3>
                    <div className="overflow-x-auto">
                        <table className="w-full text-left border-collapse">
                            <thead>
                                <tr className="bg-bmtc-cream text-bmtc-dark text-sm border-b border-bmtc-blue/20">
                                    <th className="p-3 font-bold">Date</th>
                                    <th className="p-3 font-bold">Type</th>
                                    <th className="p-3 font-bold">Description</th>
                                    <th className="p-3 font-bold">Status</th>
                                    <th className="p-3 font-bold">Update Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                {reports.length === 0 ? (
                                    <tr><td colSpan="5" className="p-4 text-center text-bmtc-navy">No reports found.</td></tr>
                                ) : (
                                    reports.map(report => (
                                        <tr key={report.id} className="border-b border-bmtc-blue/10 text-sm hover:bg-gray-50">
                                            <td className="p-3 text-bmtc-navy">{new Date(report.created_at).toLocaleDateString()}</td>
                                            <td className="p-3 font-bold text-red-700">{report.report_type.replace('_', ' ')}</td>
                                            <td className="p-3 text-bmtc-dark">{report.description}</td>
                                            <td className="p-3">
                                                <span className={`px-2 py-1 rounded text-xs font-bold ${
                                                    report.status === 'OPEN' ? 'bg-red-100 text-red-700' :
                                                    report.status === 'INVESTIGATING' ? 'bg-orange-100 text-orange-700' : 
                                                    'bg-green-100 text-green-700'
                                                }`}>
                                                    {report.status}
                                                </span>
                                            </td>
                                            <td className="p-3">
                                                <select 
                                                    className="border border-gray-300 rounded p-1 text-xs bg-white text-gray-800"
                                                    value={report.status}
                                                    onChange={(e) => handleStatusChange(report.id, e.target.value)}
                                                >
                                                    <option value="OPEN">Open</option>
                                                    <option value="INVESTIGATING">Investigating</option>
                                                    <option value="RESOLVED">Resolved</option>
                                                </select>
                                            </td>
                                        </tr>
                                    ))
                                )}
                            </tbody>
                        </table>
                    </div>
                </div>

            </div>
        </div>
    );
}