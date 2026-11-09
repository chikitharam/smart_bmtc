import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '../services/api';

export default function Register() {
    const [form, setForm] = useState({ name: '', email: '', phone: '', password: '' });
    const navigate = useNavigate();

    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            await api.post('/auth/register', form);
            alert("Registration successful! Please login.");
            navigate('/login');
        } catch (error) {
            alert("Error: " + (error.response?.data?.detail || "Registration failed"));
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-bmtc-cream p-4">
            <form onSubmit={handleRegister} className="bg-bmtc-tan p-8 rounded-2xl shadow-xl w-full max-w-sm border border-bmtc-blue/20">
                <h2 className="text-2xl font-bold mb-6 text-center text-bmtc-dark tracking-wide">Create Account</h2>
                <input type="text" placeholder="Full Name" className="w-full p-3 mb-3 bg-bmtc-cream border border-bmtc-blue/30 rounded-lg text-bmtc-dark focus:outline-none focus:border-bmtc-blue" onChange={e => setForm({...form, name: e.target.value})} required />
                <input type="email" placeholder="Email" className="w-full p-3 mb-3 bg-bmtc-cream border border-bmtc-blue/30 rounded-lg text-bmtc-dark focus:outline-none focus:border-bmtc-blue" onChange={e => setForm({...form, email: e.target.value})} required />
                <input type="text" placeholder="Phone Number" className="w-full p-3 mb-3 bg-bmtc-cream border border-bmtc-blue/30 rounded-lg text-bmtc-dark focus:outline-none focus:border-bmtc-blue" onChange={e => setForm({...form, phone: e.target.value})} required />
                <input type="password" placeholder="Password" className="w-full p-3 mb-6 bg-bmtc-cream border border-bmtc-blue/30 rounded-lg text-bmtc-dark focus:outline-none focus:border-bmtc-blue" onChange={e => setForm({...form, password: e.target.value})} required />
                <button type="submit" className="w-full bg-bmtc-blue text-bmtc-cream py-3 rounded-lg font-bold hover:bg-bmtc-dark transition-colors">Register</button>
                <p className="mt-4 text-center text-sm text-bmtc-navy">Already have an account? <Link to="/login" className="text-bmtc-dark font-bold hover:underline">Login</Link></p>
            </form>
        </div>
    );
}