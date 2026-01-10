'use client';

import { useState } from 'react';
import api from '@/lib/api';
import { useRouter } from 'next/navigation';

export default function CreateMangaPage() {
  const router = useRouter();
  
  const [title, setTitle] = useState('');
  const [slug, setSlug] = useState('');
  const [desc, setDesc] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      alert("Please select a cover image");
      return;
    }
    setLoading(true);

    try {
      // 1. Сначала грузим картинку
      const formData = new FormData();
      formData.append('file', file);
      
      const uploadRes = await api.post('/utils/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      const coverUrl = uploadRes.data.url;

      // 2. Создаем мангу с полученной ссылкой
      await api.post('/manga/', {
        title,
        slug,
        description: desc,
        cover_image: coverUrl
      });

      alert("Manga created!");
      router.push(`/manga/${slug}`);

    } catch (err) {
      console.error(err);
      alert("Failed to create manga");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white p-8 pt-24">
      <div className="max-w-2xl mx-auto bg-gray-900 p-8 rounded-xl border border-gray-800">
        <h1 className="text-3xl font-bold mb-6">Create New Manga</h1>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Title */}
          <div>
            <label className="block mb-2 text-gray-400">Title</label>
            <input 
              type="text" required 
              className="w-full bg-gray-800 border border-gray-700 rounded p-3"
              value={title} onChange={e => setTitle(e.target.value)}
            />
          </div>

          {/* Slug */}
          <div>
            <label className="block mb-2 text-gray-400">Slug (URL)</label>
            <input 
              type="text" required 
              placeholder="e.g. naruto-shippuden"
              className="w-full bg-gray-800 border border-gray-700 rounded p-3"
              value={slug} onChange={e => setSlug(e.target.value)}
            />
          </div>

          {/* Description */}
          <div>
            <label className="block mb-2 text-gray-400">Description</label>
            <textarea 
              className="w-full bg-gray-800 border border-gray-700 rounded p-3 h-32"
              value={desc} onChange={e => setDesc(e.target.value)}
            />
          </div>

          {/* File Upload */}
          <div>
            <label className="block mb-2 text-gray-400">Cover Image</label>
            <input 
              type="file" accept="image/*"
              className="w-full bg-gray-800 border border-gray-700 rounded p-3"
              onChange={e => setFile(e.target.files?.[0] || null)}
            />
          </div>

          <button 
            type="submit" 
            disabled={loading}
            className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 rounded"
          >
            {loading ? 'Uploading...' : 'Create Manga'}
          </button>
        </form>
      </div>
    </div>
  );
}