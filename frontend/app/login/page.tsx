'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';
import { setToken } from '@/lib/auth';
import Link from 'next/link';

export default function LoginPage() {
  const router = useRouter(); // Чтобы перекинуть юзера на главную после входа
  
  const [formData, setFormData] = useState({
    username: '', // FastAPI требует поле username (сюда можно писать email)
    password: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // ВАЖНО: FastAPI OAuth2 ждет form-data, а не JSON!
      const params = new URLSearchParams();
      params.append('username', formData.username);
      params.append('password', formData.password);

      const response = await api.post('/auth/login', params, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });

      // Сохраняем токен
      setToken(response.data.access_token);
      
      // Перенаправляем на главную
      // window.location.href перезагрузит страницу и обновит Navbar
      window.location.href = '/'; 
      
    } catch (err: any) {
      console.error(err);
      setError('Invalid email or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-950 px-4">
      <div className="max-w-md w-full bg-gray-900 border border-gray-800 rounded-xl p-8 shadow-2xl">
        <h2 className="text-3xl font-bold text-white mb-6 text-center">Welcome Back</h2>
        
        {error && (
          <div className="bg-red-900/30 border border-red-800 text-red-400 p-3 rounded mb-4 text-sm text-center">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-1">
              Email or Username
            </label>
            <input
              type="text"
              required
              className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-red-600 transition"
              placeholder="Enter your email"
              value={formData.username}
              onChange={(e) => setFormData({...formData, username: e.target.value})}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-400 mb-1">
              Password
            </label>
            <input
              type="password"
              required
              className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-red-600 transition"
              placeholder="••••••••"
              value={formData.password}
              onChange={(e) => setFormData({...formData, password: e.target.value})}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className={`w-full bg-red-600 hover:bg-red-700 text-white font-bold py-3 rounded-lg transition duration-200 ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <p className="mt-6 text-center text-gray-500 text-sm">
          Don't have an account?{' '}
          <Link href="/register" className="text-red-500 hover:underline">
            Sign up
          </Link>
        </p>
      </div>
    </div>
  );
}