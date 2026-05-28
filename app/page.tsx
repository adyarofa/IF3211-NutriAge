'use client';

import { useState } from 'react';
import { SimulationForm } from '@/components/simulation-form';
import { SimulationResults } from '@/components/simulation-results';
import { AnalysisSection } from '@/components/analysis-section';
import { type SimulationResult } from '@/lib/nutrition-data';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export default function Page() {
  const [result, setResult] = useState<SimulationResult | null>(null);
  const [activeTab, setActiveTab] = useState('home');

  return (
    <div className="min-h-screen bg-gradient-to-b from-purple-50 via-white to-pink-50">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm">
        <div className="mx-auto max-w-6xl px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-[#A07ED2] to-[#FF006E] text-2xl shadow-lg">
                🧬
              </div>
              <div>
                <h1 className="text-2xl font-bold text-[#A07ED2]">NutriAge</h1>
                <p className="text-sm text-[#FF006E]">Simulasi Kebutuhan Nutrisi</p>
              </div>
            </div>
            <nav className="hidden md:block">
              <ul className="flex gap-6 text-sm font-medium">
                <li>
                  <button
                    onClick={() => setActiveTab('home')}
                    className={`transition-colors ${activeTab === 'home' ? 'text-[#A07ED2]' : 'text-gray-600 hover:text-[#A07ED2]'}`}
                  >
                    Beranda
                  </button>
                </li>
                <li>
                  <button
                    onClick={() => setActiveTab('simulation')}
                    className={`transition-colors ${activeTab === 'simulation' ? 'text-[#FF006E]' : 'text-gray-600 hover:text-[#FF006E]'}`}
                  >
                    Simulasi
                  </button>
                </li>
                <li>
                  <button
                    onClick={() => setActiveTab('analysis')}
                    className={`transition-colors ${activeTab === 'analysis' ? 'text-[#F99C01]' : 'text-gray-600 hover:text-[#F99C01]'}`}
                  >
                    Analisis Data
                  </button>
                </li>
                <li>
                  <button
                    onClick={() => setActiveTab('about')}
                    className={`transition-colors ${activeTab === 'about' ? 'text-[#748C2C]' : 'text-gray-600 hover:text-[#748C2C]'}`}
                  >
                    Tentang
                  </button>
                </li>
              </ul>
            </nav>
          </div>
        </div>
      </header>

      {/* Mobile Navigation */}
      <div className="border-b bg-white md:hidden">
        <div className="mx-auto max-w-6xl px-4">
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="w-full justify-start overflow-x-auto">
              <TabsTrigger value="home">Beranda</TabsTrigger>
              <TabsTrigger value="simulation">Simulasi</TabsTrigger>
              <TabsTrigger value="analysis">Analisis</TabsTrigger>
              <TabsTrigger value="about">Tentang</TabsTrigger>
            </TabsList>
          </Tabs>
        </div>
      </div>

      {/* Main Content */}
      <main className="mx-auto max-w-6xl px-4 py-8">
        {activeTab === 'home' && (
          <div className="space-y-8">
            {/* Hero Section */}
            <section className="rounded-2xl bg-gradient-to-r from-[#A07ED2] via-[#FF006E] to-[#FF470B] p-8 text-white shadow-xl md:p-12">
              <div className="max-w-2xl">
                <h2 className="text-3xl font-bold md:text-4xl">
                  Pelajari Kebutuhan Nutrisi Berdasarkan Usia
                </h2>
                <p className="mt-4 text-lg text-white/90">
                  NutriAge adalah aplikasi simulasi interaktif yang membantu Anda
                  memahami bagaimana kebutuhan karbohidrat, protein, dan lemak
                  berubah seiring usia.
                </p>
                <button
                  onClick={() => setActiveTab('simulation')}
                  className="mt-6 rounded-lg bg-white px-6 py-3 font-semibold text-[#FF006E] shadow-lg transition-transform hover:scale-105"
                >
                  Mulai Simulasi
                </button>
              </div>
            </section>

            {/* Features */}
            <section className="grid gap-6 md:grid-cols-3">
              <Card className="border-2 border-[#A07ED2]/30 bg-gradient-to-br from-[#A07ED2]/5 to-[#A07ED2]/10">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-[#A07ED2]">
                    <span className="text-2xl">📊</span>
                    Simulasi Interaktif
                  </CardTitle>
                </CardHeader>
                <CardContent className="text-muted-foreground">
                  Masukkan usia dan jenis kelamin untuk melihat kebutuhan nutrisi
                  harian yang dipersonalisasi.
                </CardContent>
              </Card>

              <Card className="border-2 border-[#FF006E]/30 bg-gradient-to-br from-[#FF006E]/5 to-[#FF006E]/10">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-[#FF006E]">
                    <span className="text-2xl">📈</span>
                    Visualisasi Data
                  </CardTitle>
                </CardHeader>
                <CardContent className="text-muted-foreground">
                  Lihat grafik perbandingan kebutuhan nutrisi antar kelompok usia
                  dan jenis kelamin.
                </CardContent>
              </Card>

              <Card className="border-2 border-[#748C2C]/30 bg-gradient-to-br from-[#D2D641]/10 to-[#748C2C]/10">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-[#748C2C]">
                    <span className="text-2xl">💡</span>
                    Insight Biologis
                  </CardTitle>
                </CardHeader>
                <CardContent className="text-muted-foreground">
                  Dapatkan penjelasan ilmiah tentang mengapa kebutuhan nutrisi
                  berbeda di setiap fase kehidupan.
                </CardContent>
              </Card>
            </section>

            {/* How to Use */}
            <Card>
              <CardHeader>
                <CardTitle>Cara Menggunakan NutriAge</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid gap-4 md:grid-cols-4">
                  {[
                    { step: 1, title: 'Buka Simulasi', desc: 'Klik menu Simulasi di navigasi', color: '#A07ED2' },
                    { step: 2, title: 'Input Data', desc: 'Masukkan usia dan jenis kelamin', color: '#FF006E' },
                    { step: 3, title: 'Lihat Hasil', desc: 'Periksa kebutuhan nutrisi harian', color: '#F99C01' },
                    { step: 4, title: 'Analisis', desc: 'Eksplorasi data lebih lanjut', color: '#748C2C' },
                  ].map((item) => (
                    <div key={item.step} className="text-center">
                      <div 
                        className="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-full text-xl font-bold text-white"
                        style={{ backgroundColor: item.color }}
                      >
                        {item.step}
                      </div>
                      <h4 className="font-semibold">{item.title}</h4>
                      <p className="mt-1 text-sm text-muted-foreground">{item.desc}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {activeTab === 'simulation' && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-[#FF006E]">Simulasi Kebutuhan Nutrisi</h2>
            <div className="grid gap-6 lg:grid-cols-3">
              <div className="lg:col-span-1">
                <SimulationForm onResult={setResult} />
              </div>
              <div className="lg:col-span-2">
                {result ? (
                  <SimulationResults result={result} />
                ) : (
                  <Card className="flex h-full min-h-[400px] items-center justify-center border-2 border-dashed border-[#A07ED2]/40">
                    <div className="text-center">
                      <div className="text-6xl">📋</div>
                      <p className="mt-4 text-lg text-muted-foreground">
                        Hasil simulasi akan muncul di sini
                      </p>
                      <p className="text-sm text-muted-foreground">
                        Isi form di samping untuk memulai
                      </p>
                    </div>
                  </Card>
                )}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'analysis' && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-[#F99C01]">Analisis Data Nutrisi</h2>
            <AnalysisSection />
          </div>
        )}

        {activeTab === 'about' && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-[#748C2C]">Tentang NutriAge</h2>
            
            <Card>
              <CardHeader>
                <CardTitle>Apa itu NutriAge?</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4 text-muted-foreground">
                <p>
                  NutriAge adalah aplikasi simulasi edukasi yang dirancang untuk
                  membantu mempelajari kebutuhan makromolekul (karbohidrat, protein,
                  dan lipid) berdasarkan usia dan jenis kelamin.
                </p>
                <p>
                  Aplikasi ini dibuat sebagai bagian dari pembelajaran mata kuliah
                  Biologi dengan fokus pada metabolisme dan gizi.
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Sumber Data</CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 text-muted-foreground">
                  <li className="flex items-start gap-2">
                    <span className="text-[#F99C01]">•</span>
                    Angka Kecukupan Gizi (AKG) Indonesia 2019
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-[#F99C01]">•</span>
                    Dietary Reference Intakes (DRI) - National Academies
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-[#F99C01]">•</span>
                    WHO Nutrient Requirements Guidelines
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-[#F99C01]">•</span>
                    Campbell Biology, 12th Edition
                  </li>
                </ul>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Tim Pengembang</CardTitle>
              </CardHeader>
              <CardContent className="text-muted-foreground">
                <p>
                  Dikembangkan untuk tugas mata kuliah Biologi Sel dan Molekuler.
                </p>
                <p className="mt-2">
                  Menggunakan teknologi: Next.js, React, Tailwind CSS, dan Recharts.
                </p>
              </CardContent>
            </Card>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t bg-white/80 py-6">
        <div className="mx-auto max-w-6xl px-4 text-center text-sm text-muted-foreground">
          <p>NutriAge - Simulasi Kebutuhan Nutrisi Berdasarkan Usia</p>
          <p className="mt-1">Dibuat untuk tujuan edukasi</p>
        </div>
      </footer>
    </div>
  );
}
