'use client';

import { useEffect, useState } from 'react';
import api from '@/lib/api';
import MangaCard from '@/components/MangaCard';

// Тип данных, который приходит с бэкенда
interface Manga {
  id: string;
  title: string;
  slug: string;
  cover_image: string;
}

export default function Home() {
  const [mangas, setMangas] = useState<Manga[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/manga/')
      .then((res) => {
        setMangas(res.data);
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-[50vh]">
        <div className="text-red-500 animate-pulse text-xl">Loading library...</div>
      </div>
    );
  }

  return (
    <main className="p-8 max-w-7xl mx-auto">
      <h2 className="text-2xl font-bold mb-6 text-gray-200 border-l-4 border-red-600 pl-4">
        Latest Updates
      </h2>

      {/* Сетка карточек */}
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-6">
        {mangas.map((manga) => (
          <MangaCard 
            key={manga.id}
            slug={manga.slug}
            title={manga.title}
            cover_image={manga.cover_image}
          />
        ))}
      </div>
      
      {mangas.length === 0 && (
        <p className="text-gray-500 text-center mt-10">No manga found.</p>
      )}
    </main>
  );
}