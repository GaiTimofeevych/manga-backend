import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/Navbar"; // <--- Импорт (или ../components/Navbar)

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Manga Reader",
  description: "Best manga platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Navbar /> {/* <--- Вставляем меню сюда */}
        
        {/* Добавляем отступ сверху, чтобы контент не заезжал под Navbar */}
        <div className="pt-16 min-h-screen bg-gray-950 text-white">
          {children}
        </div>
      </body>
    </html>
  );
}