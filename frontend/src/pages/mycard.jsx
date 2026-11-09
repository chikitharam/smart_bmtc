// frontend/src/pages/MyCard.jsx
import { useEffect, useState } from 'react';
import api from '../services/api';
import Layout from '../components/layout';
import { QrCode, PlusCircle } from 'lucide-react';

export default function MyCard() {
    const [card, setCard] = useState(null);

    const fetchCard = () => {
        api.get('/cards/my-card').then(res => setCard(res.data)).catch(() => setCard(null));
    };

    useEffect(() => { fetchCard(); }, []);

    const handleCreateCard = async () => {
        try {
            await api.post('/cards/create');
            fetchCard();
        } catch (error) {
            alert("Error creating card: " + (error.response?.data?.detail || "Unknown error"));
        }
    };

    return (
        <Layout>
            <h2 className="text-xl font-bold mb-4 text-bmtc-dark">My Smart Card</h2>
            {card ? (
                <div className="bg-bmtc-tan p-6 rounded-2xl shadow-xl border border-bmtc-blue/20 text-center">
                    <div className="bg-bmtc-cream p-8 rounded-full w-24 h-24 mx-auto mb-4 flex items-center justify-center border border-bmtc-blue/20">
                        <QrCode size={48} className="text-bmtc-dark" />
                    </div>
                    <h3 className="text-2xl font-bold text-bmtc-dark tracking-wider mb-2">{card.card_number}</h3>
                    <p className={`inline-block px-4 py-1 rounded-full text-xs font-bold mb-6 ${card.status === 'active' ? 'bg-bmtc-sage text-bmtc-cream' : 'bg-red-800 text-bmtc-cream'}`}>
                        {card.status.toUpperCase()}
                    </p>
                    <div className="bg-bmtc-cream p-4 rounded-xl border border-bmtc-blue/20">
                        <p className="text-sm text-bmtc-navy font-semibold">Available Balance</p>
                        <p className="text-3xl font-bold text-bmtc-dark">₹{card.wallet_balance}</p>
                    </div>
                </div>
            ) : (
                <div className="bg-bmtc-tan p-8 rounded-2xl shadow-md border border-bmtc-blue/20 text-center mt-10">
                    <PlusCircle size={64} className="mx-auto text-bmtc-blue mb-4" />
                    <h3 className="text-xl font-bold text-bmtc-dark mb-2">No Active Card</h3>
                    <p className="text-sm text-bmtc-navy mb-6">You don't have a virtual bus card yet.</p>
                    <button onClick={handleCreateCard} className="bg-bmtc-blue text-bmtc-cream px-6 py-3 rounded-lg font-bold hover:bg-bmtc-dark transition-colors w-full">
                        Generate My Card
                    </button>
                </div>
            )}
        </Layout>
    );
}