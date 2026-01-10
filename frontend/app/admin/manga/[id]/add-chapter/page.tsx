'use client';

import { useState, use } from 'react';
import api from '@/lib/api';
import { useRouter } from 'next/navigation';

export default function AddChapterPage({ params }: { params: Promise<{ id: string }> }) {
  const { id: mangaId } = use(params); // Получаем ID манги из URL
  const router = useRouter();

  const [title, setTitle] = useState('');
  const [number, setNumber] = useState('');
  const [isPremium, setIsPremium] = useState(false);
  const [files, setFiles] = useState<FileList | null>(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!files || files.length === 0) {
      alert("Please select pages (images)");
      return;
    }
    setLoading(true);
    setStatus('Uploading images...');

    try {
      // 1. Загружаем картинки по одной (или параллельно)
      const pageUrls: string[] = [];
      
      // Превращаем FileList в массив и проходим по нему
      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const formData = new FormData();
        formData.append('file', file);

        setStatus(`Uploading page ${i + 1} of ${files.length}...`);
        
        // Отправляем файл на наш бэкенд
        const uploadRes = await api.post('/utils/upload', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        pageUrls.push(uploadRes.data.url);
      }

      setStatus('Creating chapter...');

      // 2. Создаем главу со списком ссылок
      await api.post(`/manga/${mangaId}/chapters`, {
        title,
        number: parseFloat(number),
        is_premium: isPremium,
        pages: pageUrls
      });

      alert("Chapter added successfully!");
      // Возвращаемся назад на страницу манги (нам нужно знать slug, но у нас только id.
      // Для простоты вернемся на главную, или можно сделать history.back())
      router.back(); 

    } catch (err) {
      console.error(err);
      alert("Failed to add chapter");
    } finally {
      setLoading(false);
      setStatus('');
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white p-8 pt-24">
      <div className="max-w-2xl mx-auto bg-gray-900 p-8 rounded-xl border border-gray-800">
        <h1 className="text-3xl font-bold mb-6">Add New Chapter</h1>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Title */}
          <div>
            <label className="block mb-2 text-gray-400">Chapter Title</label>
            <input 
              type="text" required 
              className="w-full bg-gray-800 border border-gray-700 rounded p-3"
              value={title} onChange={e => setTitle(e.target.value)}
            />
          </div>

          {/* Number */}
          <div>
            <label className="block mb-2 text-gray-400">Chapter Number</label>
            <input 
              type="number" step="0.1" required 
              placeholder="e.g. 1 or 10.5"
              className="w-full bg-gray-800 border border-gray-700 rounded p-3"
              value={number} onChange={e => setNumber(e.target.value)}
            />
          </div>

          {/* Premium Checkbox */}
          <div className="flex items-center gap-3 bg-gray-800 p-3 rounded border border-gray-700">
            <input 
              type="checkbox" 
              id="premium"
              className="w-5 h-5 accent-red-600"
              checked={isPremium} onChange={e => setIsPremium(e.target.checked)}
            />
            <label htmlFor="premium" className="text-white cursor-pointer select-none">
              Is this a <b>Premium</b> (Paid) chapter?
            </label>
          </div>

          {/* Files Upload (Multiple) */}
          <div>
            <label className="block mb-2 text-gray-400">Pages (Select multiple images)</label>
            <input 
              type="file" multiple accept="image/*"
              className="w-full bg-gray-800 border border-gray-700 rounded p-3"
              onChange={e => setFiles(e.target.files)}
            />
            <p className="text-xs text-gray-500 mt-1">Images will be uploaded in the order selected.</p>
          </div>

          {/* Status Message */}
          {status && (
            <div className="text-yellow-400 text-sm animate-pulse text-center">
              {status}
            </div>
          )}

          <button 
            type="submit" 
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded"
          >
            {loading ? 'Processing...' : 'Upload Chapter'}
          </button>
        </form>
      </div>
    </div>
  );
}