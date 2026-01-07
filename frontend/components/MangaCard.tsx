import Link from 'next/link';

// Описываем, какие данные нужны карточке (TypeScript интерфейс)
interface MangaProps {
  slug: string;
  title: string;
  cover_image: string | null;
}

export default function MangaCard({ slug, title, cover_image }: MangaProps) {
  // Заглушка, если картинки нет
  const imageSrc = cover_image 
    ? `http://localhost:8000${cover_image}` // Если это локальный файл
    : "https://via.placeholder.com/300x450?text=No+Cover"; // Заглушка

  // Если ссылка внешняя (начинается на http), используем её как есть
  const finalImage = cover_image?.startsWith('http') ? cover_image : imageSrc;

  return (
    <Link href={`/manga/${slug}`} className="group block">
      <div className="relative overflow-hidden rounded-lg aspect-[2/3] bg-gray-800">
        {/* Картинка */}
        <img 
          src={finalImage} 
          alt={title}
          className="object-cover w-full h-full group-hover:scale-105 transition duration-300 ease-in-out opacity-90 group-hover:opacity-100"
        />
        
        {/* Градиент снизу для читаемости текста */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-60 group-hover:opacity-80 transition" />
        
        {/* Текст */}
        <div className="absolute bottom-0 left-0 p-4 w-full">
          <h3 className="text-white font-bold text-lg leading-tight truncate">
            {title}
          </h3>
        </div>
      </div>
    </Link>
  );
}