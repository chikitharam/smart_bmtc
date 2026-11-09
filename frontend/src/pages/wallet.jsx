import { useEffect, useState } from 'react';
import api from '../services/api';
import Layout from '../components/layout';
import { ArrowUpRight, ArrowDownLeft } from 'lucide-react';

export default function Wallet() {
    const [balance, setBalance] = useState(0);
    const [transactions, setTransactions] = useState([]);
    const [amount, setAmount] = useState('');

    const loadData = () => {
        api.get('/wallet/balance').then(res => setBalance(res.data.balance));
        api.get('/wallet/transactions').then(res => setTransactions(res.data));
    };

    useEffect(() => { loadData(); }, []);

    const handleRecharge = async (e) => {
        e.preventDefault();
        try {
            await api.post('/wallet/recharge', { amount: parseFloat(amount) });
            setAmount('');
            loadData();
            alert("Recharge successful!");
        } catch (error) { alert("Recharge failed"); }
    };

    return (
        <Layout>
            <div className="bg-bmtc-dark text-bmtc-cream p-6 rounded-2xl shadow-xl mb-6 text-center border border-bmtc-blue/30">
                <p className="text-bmtc-tan text-sm mb-1 tracking-widest font-semibold">TOTAL BALANCE</p>
                <h2 className="text-4xl font-bold">₹{balance}</h2>
            </div>

            <form onSubmit={handleRecharge} className="flex gap-2 mb-8">
                <input type="number" placeholder="Amount (₹)" value={amount} onChange={e => setAmount(e.target.value)} className="flex-1 p-3 bg-bmtc-tan border border-bmtc-blue/30 rounded-lg text-bmtc-dark placeholder-bmtc-navy/50 focus:outline-none focus:border-bmtc-blue" required />
                <button type="submit" className="bg-bmtc-sage text-bmtc-cream px-6 py-3 rounded-lg font-bold hover:bg-bmtc-dark transition-colors">Add</button>
            </form>

            <h3 className="font-bold text-bmtc-dark mb-3">Recent Transactions</h3>
            <div className="space-y-3">
                {transactions.map(tx => (
                    <div key={tx.id} className="bg-bmtc-tan p-4 rounded-xl shadow-sm border border-bmtc-blue/10 flex justify-between items-center">
                        <div className="flex items-center gap-3">
                            <div className={`p-2 rounded-full ${tx.type === 'topup' ? 'bg-bmtc-sage/20' : 'bg-red-900/20'}`}>
                                {tx.type === 'topup' ? <ArrowDownLeft className="text-bmtc-sage" size={20}/> : <ArrowUpRight className="text-red-800" size={20}/>}
                            </div>
                            <div>
                                <p className="font-bold text-bmtc-dark capitalize">{tx.type}</p>
                                <p className="text-xs text-bmtc-navy">{new Date(tx.created_at).toLocaleString()}</p>
                            </div>
                        </div>
                        <p className={`font-bold ${tx.type === 'topup' ? 'text-bmtc-sage' : 'text-red-800'}`}>
                            {tx.type === 'topup' ? '+' : '-'}₹{tx.amount}
                        </p>
                    </div>
                ))}
            </div>
        </Layout>
    );
}