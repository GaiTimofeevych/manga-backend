'use client';

import { useEffect, useState, use } from 'react';
import api from '@/lib/api';
import Link from 'next/link';

interface ChapterPages {
  id: string;
  title: string;
  number: number;
  pages: string[]; // Список URL картинок
}

export default function ReaderPage({ params }: { params: Promise<{ chapterId: string }> }) {
  const { chapterId } = use(params);

  const [chapter, setChapter] = useState<ChapterPages | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    // Запрашиваем главу
    // Благодаря нашему новому api.ts, токен отправится сам!
    api.get(`/manga/chapters/${chapterId}`)
      .then((res) => {
        setChapter(res.data);
      })
      .catch((err) => {
        console.error(err);
        if (err.response?.status === 403) {
          setError("🔒 Premium content. Please subscribe to access.");
        } else if (err.response?.status === 401) {
          setError("🔑 Please log in to read this chapter.");
        } else {
          setError("Failed to load chapter.");
        }
      })
      .finally(() => setLoading(false));
  }, [chapterId]);

  if (loading) return <div className="text-center mt-20 text-gray-500">Loading pages...</div>;

  if (error) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-gray-950 text-white p-4">
        <div className="text-4xl mb-4">🚫</div>
        <h2 className="text-2xl font-bold mb-4 text-center">{error}</h2>
        <div className="flex gap-4">
            <Link href="/login" className="text-red-500 hover:underline">Log In</Link>
            <Link href="/" className="text-gray-400 hover:underline">Go Home</Link>
        </div>
      </div>
    );
  }

  if (!chapter) return null;

  return (
    <div className="min-h-screen bg-gray-900 pb-20">
      {/* Верхняя панель (Навигация) */}
      <div className="sticky top-0 z-50 bg-gray-900/90 backdrop-blur border-b border-gray-800 p-4 flex justify-between items-center text-white">
        <button onClick={() => history.back()} className="text-gray-400 hover:text-white">
          ← Back
        </button>
        <h1 className="font-bold truncate max-w-xs md:max-w-md">
           Ch. {chapter.number} - {chapter.title}
        </h1>
        <div className="w-10"></div> {/* Пустой блок для центровки заголовка */}
      </div>

      {/* Список страниц (Картинки) */}
      <div className="max-w-3xl mx-auto bg-black min-h-screen shadow-2xl">
        {chapter.pages.map((pageUrl, index) => (
          <img 
            key={index}
            src={pageUrl.startsWith('http') ? pageUrl : `http://localhost:8000${pageUrl}`}
            alt={`Page ${index + 1}`}
            className="w-full h-auto block" // block убирает отступы между картинками
            loading="lazy" // Ленивая загрузка для скорости
          />
        ))}
      </div>

      {/* Кнопки внизу */}
      <div className="max-w-3xl mx-auto p-8 text-center">
        <p className="text-gray-500 mb-4">End of Chapter</p>
        <button 
           onClick={() => history.back()}
           className="bg-red-600 hover:bg-red-700 text-white px-6 py-3 rounded-full font-bold transition"
        >
            Back to Manga
        </button>
      </div>
    </div>
  );
}