'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { isAuthenticated, removeToken } from '@/lib/auth';
import { useRouter } from 'next/navigation';

export default function Navbar() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const router = useRouter();

  useEffect(() => {
    setIsLoggedIn(isAuthenticated());
  }, []);

  const handleLogout = () => {
    removeToken();
    setIsLoggedIn(false);
    router.push('/login');
    router.refresh();
  };

  return (
    <nav className="w-full h-16 bg-gray-900 border-b border-gray-800 flex items-center justify-between px-6 fixed top-0 z-50">
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 bg-red-600 rounded-full flex items-center justify-center text-white font-bold">
          M
        </div>
        <Link href="/" className="text-xl font-bold text-white tracking-wider hover:text-red-500 transition">
          MANGA<span className="text-red-600">READER</span>
        </Link>
      </div>

      <div className="flex items-center gap-4">
        {isLoggedIn ? (
          <>
            {/* Кнопка создания (видна всем залогиненным, но сработает только у админа) */}
            <Link 
              href="/admin/create" 
              className="px-4 py-2 text-sm font-medium text-green-400 hover:text-green-300 transition border border-green-800 rounded bg-green-900/20 mr-2"
            >
              + Create
            </Link>
            
            {/* Кнопка выхода */}
            <button 
              onClick={handleLogout}
              className="px-4 py-2 text-sm font-medium text-gray-300 hover:text-white transition"
            >
              Log Out
            </button>
          </>
        ) : (
          <>
            {/* Кнопки для гостей */}
            <Link 
              href="/login" 
              className="px-4 py-2 text-sm font-medium text-gray-300 hover:text-white transition"
            >
              Log In
            </Link>
            <Link 
              href="/register" 
              className="px-4 py-2 text-sm font-medium bg-red-600 text-white rounded hover:bg-red-700 transition"
            >
              Sign Up
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}