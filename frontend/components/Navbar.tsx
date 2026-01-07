import Link from 'next/link';

export default function Navbar() {
  return (
    <nav className="w-full h-16 bg-gray-900 border-b border-gray-800 flex items-center justify-between px-6 fixed top-0 z-50">
      {/* Логотип */}
      <div className="flex items-center gap-2">
        <div className="w-8 h-8 bg-red-600 rounded-full flex items-center justify-center text-white font-bold">
          M
        </div>
        <Link href="/" className="text-xl font-bold text-white tracking-wider hover:text-red-500 transition">
          MANGA<span className="text-red-600">READER</span>
        </Link>
      </div>

      {/* Кнопки справа */}
      <div className="flex items-center gap-4">
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
      </div>
    </nav>
  );
}