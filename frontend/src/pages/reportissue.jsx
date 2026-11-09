// frontend/src/pages/ReportIssue.jsx
import { useState, useEffect } from 'react';
import api from '../services/api';
import Layout from '../components/layout';
import { AlertOctagon } from 'lucide-react';

export default function ReportIssue() {
    const [form, setForm] = useState({ report_type: 'OVER_CROWDING', description: '' });
    const [status, setStatus] = useState('');
    const [reports, setReports] = useState([]);

    const fetchReports = () => {
        api.get('/safety/my-reports').then(res => setReports(res.data)).catch(console.error);
    };

    useEffect(() => { fetchReports(); }, []);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await api.post('/safety/report', { ...form, bus_id: 1, route_id: 1 });
            setStatus('Report submitted successfully. BMTC will review this shortly.');
            setForm({ report_type: 'OVER_CROWDING', description: '' });
            fetchReports();
        } catch (error) {
            setStatus('Failed to submit report. Please try again.');
        }
    };

    return (
        <Layout>
            <h2 className="text-xl font-bold mb-4 text-bmtc-dark">Report an Issue</h2>
            
            {/* EMERGENCY DISCLAIMER */}
            <div className="bg-red-100 border-l-4 border-red-600 p-4 mb-6 rounded-r-lg flex gap-3">
                <AlertOctagon className="text-red-600 shrink-0" />
                <div>
                    <p className="font-bold text-red-800 text-sm">NOT AN EMERGENCY SERVICE</p>
                    <p className="text-xs text-red-700 mt-1">If you are in immediate danger, please call 112 or contact local authorities. This prototype is for non-emergency feedback only.</p>
                </div>
            </div>

            {status && <div className="bg-bmtc-sage text-bmtc-cream p-3 rounded-lg mb-4 text-sm font-semibold">{status}</div>}

            <form onSubmit={handleSubmit} className="bg-bmtc-tan p-6 rounded-xl shadow-md border border-bmtc-blue/20 mb-8">
                <label className="block text-sm font-bold text-bmtc-dark mb-2">Issue Type</label>
                <select 
                    className="w-full p-3 border border-bmtc-blue/30 rounded-lg mb-4 bg-bmtc-cream text-bmtc-dark focus:outline-none focus:border-bmtc-blue"
                    value={form.report_type}
                    onChange={e => setForm({...form, report_type: e.target.value})}
                >
                    <option value="OVER_CROWDING">Overcrowding</option>
                    <option value="HARASSMENT">Harassment</option>
                    <option value="UNSAFE_TRAVEL">Unsafe Travel Conditions</option>
                    <option value="BUS_BREAKDOWN">Bus Breakdown</option>
                    <option value="OTHER">Other Complaint</option>
                </select>

                <label className="block text-sm font-bold text-bmtc-dark mb-2">Description</label>
                <textarea 
                    className="w-full p-3 border border-bmtc-blue/30 rounded-lg mb-4 bg-bmtc-cream text-bmtc-dark placeholder-bmtc-navy/50 h-32 focus:outline-none focus:border-bmtc-blue"
                    placeholder="Please provide details (do not include personal info)..."
                    value={form.description}
                    onChange={e => setForm({...form, description: e.target.value})}
                    required
                ></textarea>

                <button type="submit" className="w-full bg-bmtc-blue text-bmtc-cream py-3 rounded-lg font-bold hover:bg-bmtc-dark transition-colors">
                    Submit Report
                </button>
            </form>

            <h3 className="font-bold text-bmtc-dark mb-3">My Past Reports</h3>
            <div className="space-y-3">
                {reports.length === 0 ? <p className="text-sm text-bmtc-navy">No reports submitted yet.</p> : null}
                {reports.map(report => (
                    <div key={report.id} className="bg-bmtc-cream p-4 rounded-xl shadow-sm border border-bmtc-blue/20">
                        <div className="flex justify-between items-start mb-1">
                            <p className="font-bold text-bmtc-dark">{report.report_type.replace('_', ' ')}</p>
                            <span className={`text-xs font-bold px-2 py-1 rounded ${
                                report.status === 'OPEN' ? 'bg-red-100 text-red-700' :
                                report.status === 'INVESTIGATING' ? 'bg-orange-100 text-orange-700' : 
                                'bg-green-100 text-green-700'
                            }`}>{report.status}</span>
                        </div>
                        <p className="text-sm text-bmtc-navy">{report.description}</p>
                        <p className="text-xs text-bmtc-navy mt-2">{new Date(report.created_at).toLocaleDateString()}</p>
                    </div>
                ))}
            </div>
        </Layout>
    );
}