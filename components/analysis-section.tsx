'use client';

import { useState } from 'react';
import { ageGroupData, genderComparisonData } from '@/lib/nutrition-data';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  BarChart,
  Bar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
} from 'recharts';

const COLORS = {
  carbs: '#F99C01',
  protein: '#FF006E',
  lipid: '#748C2C',
  male: '#A07ED2',
  female: '#FF470B',
};

export function AnalysisSection() {
  return (
    <div className="space-y-6">
      <Tabs defaultValue="age" className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="age">Berdasarkan Usia</TabsTrigger>
          <TabsTrigger value="gender">Berdasarkan Gender</TabsTrigger>
          <TabsTrigger value="comparison">Perbandingan</TabsTrigger>
        </TabsList>

        <TabsContent value="age" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Kebutuhan Nutrisi Berdasarkan Kelompok Usia</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-[400px]">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={ageGroupData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="ageGroup" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Area
                      type="monotone"
                      dataKey="carbs"
                      name="Karbohidrat (g)"
                      stackId="1"
                      stroke={COLORS.carbs}
                      fill={COLORS.carbs}
                      fillOpacity={0.6}
                    />
                    <Area
                      type="monotone"
                      dataKey="protein"
                      name="Protein (g)"
                      stackId="1"
                      stroke={COLORS.protein}
                      fill={COLORS.protein}
                      fillOpacity={0.6}
                    />
                    <Area
                      type="monotone"
                      dataKey="lipid"
                      name="Lemak (g)"
                      stackId="1"
                      stroke={COLORS.lipid}
                      fill={COLORS.lipid}
                      fillOpacity={0.6}
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
              <div className="mt-4 rounded-lg bg-[#F99C01]/10 p-4">
                <h4 className="font-semibold text-[#F99C01]">Interpretasi:</h4>
                <p className="mt-2 text-sm text-[#F99C01]/80">
                  Kebutuhan nutrisi meningkat dari masa kanak-kanak hingga dewasa,
                  kemudian sedikit menurun pada usia lanjut. Puncak kebutuhan terjadi
                  pada usia 20-59 tahun ketika aktivitas metabolisme paling tinggi.
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="gender" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Perbandingan Kebutuhan Berdasarkan Jenis Kelamin</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-[400px]">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={genderComparisonData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="nutrient" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar
                      dataKey="male"
                      name="Laki-laki"
                      fill={COLORS.male}
                      radius={[8, 8, 0, 0]}
                    />
                    <Bar
                      dataKey="female"
                      name="Perempuan"
                      fill={COLORS.female}
                      radius={[8, 8, 0, 0]}
                    />
                  </BarChart>
                </ResponsiveContainer>
              </div>
              <div className="mt-4 rounded-lg bg-[#FF006E]/10 p-4">
                <h4 className="font-semibold text-[#FF006E]">Interpretasi:</h4>
                <p className="mt-2 text-sm text-[#FF006E]/80">
                  Laki-laki umumnya membutuhkan lebih banyak kalori dan makronutrien
                  karena rata-rata memiliki massa otot lebih besar dan tingkat
                  metabolisme basal yang lebih tinggi.
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="comparison" className="mt-6">
          <Card>
            <CardHeader>
              <CardTitle>Radar Perbandingan Nutrisi</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="h-[400px]">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart data={genderComparisonData}>
                    <PolarGrid />
                    <PolarAngleAxis dataKey="nutrient" />
                    <PolarRadiusAxis />
                    <Radar
                      name="Laki-laki"
                      dataKey="male"
                      stroke={COLORS.male}
                      fill={COLORS.male}
                      fillOpacity={0.5}
                    />
                    <Radar
                      name="Perempuan"
                      dataKey="female"
                      stroke={COLORS.female}
                      fill={COLORS.female}
                      fillOpacity={0.5}
                    />
                    <Legend />
                    <Tooltip />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
              <div className="mt-4 rounded-lg bg-[#A07ED2]/10 p-4">
                <h4 className="font-semibold text-[#A07ED2]">Interpretasi:</h4>
                <p className="mt-2 text-sm text-[#A07ED2]/80">
                  Grafik radar menunjukkan profil nutrisi secara visual.
                  Perbedaan kebutuhan antara laki-laki dan perempuan relatif
                  proporsional di semua makronutrien dengan faktor sekitar 10-15%.
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Info Cards */}
      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        <Card className="border-[#F99C01]/40 bg-gradient-to-br from-[#F99C01]/10 to-[#FF470B]/10">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-[#F99C01]">
              <span className="text-2xl">🍞</span>
              Karbohidrat
            </CardTitle>
          </CardHeader>
          <CardContent className="text-sm text-[#F99C01]/80">
            <p>
              Sumber energi utama tubuh. Dipecah menjadi glukosa yang digunakan
              sel untuk produksi ATP. Otak sangat bergantung pada glukosa.
            </p>
            <ul className="mt-3 list-inside list-disc space-y-1">
              <li>Monosakarida: glukosa, fruktosa</li>
              <li>Disakarida: sukrosa, laktosa</li>
              <li>Polisakarida: pati, glikogen</li>
            </ul>
          </CardContent>
        </Card>

        <Card className="border-[#FF006E]/40 bg-gradient-to-br from-[#FF006E]/10 to-[#A07ED2]/10">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-[#FF006E]">
              <span className="text-2xl">🥩</span>
              Protein
            </CardTitle>
          </CardHeader>
          <CardContent className="text-sm text-[#FF006E]/80">
            <p>
              Blok pembangun tubuh. Tersusun dari asam amino yang membentuk
              enzim, hormon, antibodi, dan struktur sel.
            </p>
            <ul className="mt-3 list-inside list-disc space-y-1">
              <li>9 asam amino esensial</li>
              <li>11 asam amino non-esensial</li>
              <li>Protein lengkap vs tidak lengkap</li>
            </ul>
          </CardContent>
        </Card>

        <Card className="border-[#748C2C]/40 bg-gradient-to-br from-[#D2D641]/10 to-[#748C2C]/10">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-[#748C2C]">
              <span className="text-2xl">🥑</span>
              Lipid
            </CardTitle>
          </CardHeader>
          <CardContent className="text-sm text-[#748C2C]/80">
            <p>
              Cadangan energi dan komponen membran sel. Penting untuk absorpsi
              vitamin larut lemak (A, D, E, K).
            </p>
            <ul className="mt-3 list-inside list-disc space-y-1">
              <li>Lemak jenuh vs tak jenuh</li>
              <li>Omega-3 dan Omega-6 esensial</li>
              <li>Fosfolipid untuk membran sel</li>
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
