import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../services/api';

export default function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const formData = new URLSearchParams();
            formData.append('username', email); 
            formData.append('password', password);

            const response = await api.post('/auth/login', formData, {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            });
            
            localStorage.setItem('token', response.data.access_token);
            navigate('/dashboard');
        } catch (error) {
            alert("Login failed: " + (error.response?.data?.detail || "Check credentials"));
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-bmtc-cream p-4">
            <form onSubmit={handleLogin} className="bg-bmtc-tan p-8 rounded-2xl shadow-xl w-full max-w-sm border border-bmtc-blue/20">
                <h2 className="text-2xl font-bold mb-6 text-center text-bmtc-dark tracking-wide">SMART BMTC Login</h2>
                <input type="email" placeholder="Email" className="w-full p-3 mb-4 bg-bmtc-cream border border-bmtc-blue/30 rounded-lg text-bmtc-dark placeholder-bmtc-blue/50 focus:outline-none focus:border-bmtc-blue" value={email} onChange={e => setEmail(e.target.value)} required />
                <input type="password" placeholder="Password" className="w-full p-3 mb-6 bg-bmtc-cream border border-bmtc-blue/30 rounded-lg text-bmtc-dark placeholder-bmtc-blue/50 focus:outline-none focus:border-bmtc-blue" value={password} onChange={e => setPassword(e.target.value)} required />
                <button type="submit" className="w-full bg-bmtc-blue text-bmtc-cream py-3 rounded-lg font-bold hover:bg-bmtc-dark transition-colors">Login</button>
                <p className="mt-4 text-center text-sm text-bmtc-navy">Don't have an account? <Link to="/register" className="text-bmtc-dark font-bold hover:underline">Register</Link></p>
            </form>
        </div>
    );
}