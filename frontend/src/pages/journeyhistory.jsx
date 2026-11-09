import { useEffect, useState } from 'react';
import api from '../services/api';
import Layout from '../components/layout';
import { MapPin } from 'lucide-react';

export default function JourneyHistory() {
    const [tickets, setTickets] = useState([]);

    useEffect(() => {
        api.get('/tickets/').then(res => setTickets(res.data)).catch(console.error);
    }, []);

    return (
        <Layout>
            <h2 className="text-xl font-bold mb-4 text-bmtc-dark">My Journeys</h2>
            {tickets.length === 0 ? <p className="text-bmtc-navy text-center mt-10 font-semibold">No completed journeys yet.</p> : null}
            
            <div className="space-y-4">
                {tickets.map(ticket => (
                    <div key={ticket.journey_id} className="bg-bmtc-tan p-5 rounded-xl shadow-md border-l-4 border-bmtc-blue">
                        <div className="flex justify-between items-start mb-4 border-b border-bmtc-blue/20 pb-3">
                            <div>
                                <p className="font-bold text-bmtc-dark">Route {ticket.route_number}</p>
                                <p className="text-sm text-bmtc-navy">Bus: {ticket.bus_number}</p>
                            </div>
                            <div className="text-right">
                                <p className="text-lg font-bold text-bmtc-dark">₹{ticket.fare}</p>
                                <p className="text-xs text-bmtc-navy">{new Date(ticket.start_time).toLocaleDateString()}</p>
                            </div>
                        </div>
                        <div className="flex items-center gap-2 text-sm text-bmtc-dark">
                            <MapPin size={16} className="text-bmtc-sage"/>
                            <span className="font-semibold">{ticket.from_stop}</span>
                            <span className="text-bmtc-blue">→</span>
                            <MapPin size={16} className="text-red-800"/>
                            <span className="font-semibold">{ticket.to_stop}</span>
                        </div>
                    </div>
                ))}
            </div>
        </Layout>
    );
}