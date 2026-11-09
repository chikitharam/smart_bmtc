// frontend/src/pages/Dashboard.jsx
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { MapPin, CreditCard } from 'lucide-react';
import api from '../services/api';
import Layout from '../components/layout';

export default function Dashboard() {
    const [user, setUser] = useState(null);
    const [card, setCard] = useState(null);
    const [prediction, setPrediction] = useState(null);
    const navigate = useNavigate();

    const fetchData = async () => {
        try {
            const userRes = await api.get('/users/me');
            setUser(userRes.data);
            try {
                const cardRes = await api.get('/cards/my-card');
                setCard(cardRes.data);
            } catch (e) { setCard(null); }
            try {
                const predRes = await api.post('/ai/predict-demand', {
                    route_id: 1, hour: 8, day_of_week: 0, previous_demand: 45, capacity: 50
                });
                setPrediction(predRes.data);
            } catch (e) { console.log("No prediction"); }
        } catch (error) {
            if (error.response?.status === 401) { localStorage.removeItem('token'); navigate('/login'); }
        }
    };

    useEffect(() => { fetchData(); }, [navigate]);

    const handleCreateCard = async () => {
        try {
            await api.post('/cards/create');
            fetchData(); // Refresh data to show the new card
        } catch (error) {
            alert("Error creating card: " + (error.response?.data?.detail || "Unknown error"));
        }
    };

    if (!user) return <div className="p-10 text-center text-bmtc-dark font-bold">Loading...</div>;

    return (
        <Layout>
            <h2 className="text-2xl font-bold text-bmtc-dark mb-4">Hello, {user.name.split(' ')[0]}</h2>
            
            {/* Virtual Card Section */}
            {card ? (
                <div className="bg-bmtc-dark text-bmtc-cream p-6 rounded-2xl shadow-xl mb-6 relative overflow-hidden border border-bmtc-blue/30">
                    <p className="text-sm text-bmtc-tan mb-1 tracking-widest">YOUR DIGITAL BUS CARD</p>
                    <h2 className="text-xl font-bold tracking-widest mb-4">{card.card_number}</h2>
                    <div>
                        <p className="text-xs text-bmtc-tan">WALLET BALANCE</p>
                        <p className="text-3xl font-bold text-bmtc-cream">₹{card.wallet_balance}</p>
                    </div>
                </div>
            ) : (
                <div className="bg-bmtc-tan p-8 rounded-2xl shadow-md mb-6 border border-bmtc-blue/20 text-center">
                    <CreditCard size={48} className="mx-auto text-bmtc-blue mb-3" />
                    <h3 className="text-lg font-bold text-bmtc-dark mb-2">No Smart Card Found</h3>
                    <p className="text-sm text-bmtc-navy mb-4">Generate a virtual BMTC card to start traveling.</p>
                    <button onClick={handleCreateCard} className="bg-bmtc-blue text-bmtc-cream px-6 py-3 rounded-lg font-bold hover:bg-bmtc-dark transition-colors w-full">
                        Create My Card
                    </button>
                </div>
            )}

            <h3 className="text-lg font-bold text-bmtc-dark mb-3">Live Bus Information</h3>
            <div className="bg-bmtc-tan p-5 rounded-xl shadow-md mb-6 border-l-4 border-bmtc-blue">
                <div className="flex justify-between items-start mb-2">
                    <div>
                        <h3 className="text-lg font-bold text-bmtc-dark">Route 500D</h3>
                        <p className="text-sm text-bmtc-navy flex items-center gap-1"><MapPin size={14} /> Majestic → Electronic City</p>
                    </div>
                    {prediction && (
                        <span className="px-3 py-1 rounded-full text-xs font-bold bg-bmtc-blue text-bmtc-cream">{prediction.demand_level} CROWD</span>
                    )}
                </div>
                {prediction && (
                    <div className="mt-4 bg-bmtc-cream p-3 rounded-lg border border-bmtc-blue/20">
                        <p className="text-xs text-bmtc-navy mb-1 font-semibold">ESTIMATED OCCUPANCY</p>
                        <div className="w-full bg-bmtc-tan rounded-full h-2.5">
                            <div className="h-2.5 rounded-full bg-bmtc-blue" style={{ width: `${prediction.predicted_occupancy}%` }}></div>
                        </div>
                        <p className="text-right text-xs font-bold mt-1 text-bmtc-dark">{prediction.predicted_occupancy}%</p>
                    </div>
                )}
            </div>
        </Layout>
    );
}