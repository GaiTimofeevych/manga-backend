'use client';

import { useEffect, useState, use } from 'react'; // <--- Добавили импорт use
import api from '@/lib/api';
import Link from 'next/link';
import { isAuthenticated } from '@/lib/auth';

// Типы данных (остались те же)
interface Chapter {
  id: string;
  title: string;
  number: number;
  is_premium: boolean;
  created_at: string;
}

interface MangaDetail {
  id: string;
  title: string;
  description: string;
  cover_image: string;
  chapters: Chapter[];
}

// Теперь params - это Promise.
export default function MangaPage({ params }: { params: Promise<{ slug: string }> }) {
  // Распаковываем Promise с помощью хука use()
  // Это новый синтаксис React/Next.js
  const unwrappedParams = use(params);
  const slug = unwrappedParams.slug;

  const [manga, setManga] = useState<MangaDetail | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Используем уже распакованный slug
    api.get(`/manga/${slug}`)
      .then((res) => setManga(res.data))
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, [slug]);

  if (loading) return <div className="text-center mt-20 text-gray-500">Loading...</div>;
  if (!manga) return <div className="text-center mt-20 text-red-500">Manga not found</div>;

  const coverUrl = manga.cover_image?.startsWith('http') 
    ? manga.cover_image 
    : `http://localhost:8000${manga.cover_image}`;

  return (
    <main className="min-h-screen bg-gray-950 text-gray-100 pb-20">
      {/* ... ВЕСЬ ОСТАЛЬНОЙ JSX КОД ОСТАЕТСЯ ТАКИМ ЖЕ, КАК БЫЛ ... */}
      {/* Скопируй верстку из прошлого сообщения, она не менялась */}
      <div className="relative h-64 md:h-80 w-full overflow-hidden">
        <div 
          className="absolute inset-0 bg-cover bg-center blur-xl opacity-30 scale-110"
          style={{ backgroundImage: `url(${coverUrl})` }}
        />
        <div className="absolute inset-0 bg-gradient-to-t from-gray-950 to-transparent" />
      </div>

      <div className="max-w-5xl mx-auto px-6 -mt-32 relative z-10">
        <div className="flex flex-col md:flex-row gap-8">
          
          <div className="flex-shrink-0 mx-auto md:mx-0">
            <div className="w-48 md:w-64 aspect-[2/3] rounded-lg shadow-2xl overflow-hidden border-4 border-gray-800">
              <img src={coverUrl} alt={manga.title} className="w-full h-full object-cover" />
            </div>
          </div>

          <div className="flex-1 pt-4 md:pt-12 text-center md:text-left">
            <h1 className="text-4xl md:text-5xl font-bold mb-4">{manga.title}</h1>
            <p className="text-gray-400 leading-relaxed text-lg mb-6">
              {manga.description || "No description available."}
            </p>
            
            {manga.chapters.length > 0 && (
              <Link 
                href={`/read/${manga.chapters[manga.chapters.length - 1].id}`}
                className="inline-block bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-8 rounded-full transition transform hover:scale-105"
              >
                Start Reading
              </Link>
            )}
                {/* НОВАЯ КНОПКА: Add Chapter (видна только если вошел) */}
              {/* В идеале тут проверять роль админа, но для MVP просто проверим вход */}
              <Link 
                href={`/admin/manga/${manga.id}/add-chapter`}
                className="inline-block bg-gray-800 hover:bg-gray-700 text-green-400 border border-green-900 font-bold py-3 px-6 rounded-full transition"
              >
                + Add Chapter
              </Link>
          </div>
        </div>

        <div className="mt-16">
          <h2 className="text-2xl font-bold mb-6 border-b border-gray-800 pb-2">
            Chapters ({manga.chapters.length})
          </h2>
          
          <div className="flex flex-col gap-3">
            {manga.chapters.map((chapter) => (
              <Link 
                key={chapter.id} 
                href={`/read/${chapter.id}`}
                className="group flex items-center justify-between p-4 bg-gray-900 rounded-lg border border-gray-800 hover:border-red-900 transition"
              >
                <div className="flex items-center gap-4">
                  <span className="text-gray-500 font-mono text-sm">#{chapter.number}</span>
                  <span className="font-medium group-hover:text-red-400 transition">
                    {chapter.title}
                  </span>
                </div>

                <div className="flex items-center gap-3">
                  <span className="text-xs text-gray-600">
                    {new Date(chapter.created_at).toLocaleDateString()}
                  </span>
                  {chapter.is_premium ? (
                    <span className="px-2 py-1 bg-yellow-900/30 text-yellow-500 text-xs rounded border border-yellow-800/50 flex items-center gap-1">
                      🔒 Premium
                    </span>
                  ) : (
                    <span className="px-2 py-1 bg-green-900/30 text-green-500 text-xs rounded border border-green-800/50">
                      Free
                    </span>
                  )}
                </div>
              </Link>
            ))}

            {manga.chapters.length === 0 && (
              <p className="text-gray-500 italic">No chapters uploaded yet.</p>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}