'use client';

import { type SimulationResult } from '@/lib/nutrition-data';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
  PieChart,
  Pie,
  Legend,
} from 'recharts';

interface SimulationResultsProps {
  result: SimulationResult;
}

const COLORS = {
  carbohydrate: '#F99C01',
  protein: '#FF006E',
  lipid: '#748C2C',
};

export function SimulationResults({ result }: SimulationResultsProps) {
  const allNutrients = [
    ...result.carbohydrates,
    ...result.proteins,
    ...result.lipids,
  ];

  const chartData = [
    {
      name: 'Karbohidrat',
      value: result.carbohydrates[0].value,
      color: COLORS.carbohydrate,
    },
    {
      name: 'Protein',
      value: result.proteins[0].value,
      color: COLORS.protein,
    },
    {
      name: 'Lemak',
      value: result.lipids[0].value,
      color: COLORS.lipid,
    },
  ];

  const pieData = chartData.map((item) => ({
    name: item.name,
    value: item.value,
    fill: item.color,
  }));

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'carbohydrate':
        return 'from-[#F99C01] to-[#FF470B]';
      case 'protein':
        return 'from-[#FF006E] to-[#A07ED2]';
      case 'lipid':
        return 'from-[#748C2C] to-[#D2D641]';
      default:
        return 'from-gray-500 to-gray-600';
    }
  };

  const getCategoryBorder = (category: string) => {
    switch (category) {
      case 'carbohydrate':
        return 'border-[#F99C01]/40';
      case 'protein':
        return 'border-[#FF006E]/40';
      case 'lipid':
        return 'border-[#748C2C]/40';
      default:
        return 'border-gray-200';
    }
  };

  return (
    <div className="space-y-6">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
        {chartData.map((item) => (
          <Card
            key={item.name}
            className={`border-2 ${item.name === 'Karbohidrat' ? 'border-[#F99C01]/40 bg-[#F99C01]/5' : item.name === 'Protein' ? 'border-[#FF006E]/40 bg-[#FF006E]/5' : 'border-[#748C2C]/40 bg-[#748C2C]/5'}`}
          >
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">{item.name}</p>
                  <p className="text-3xl font-bold" style={{ color: item.color }}>
                    {item.value}
                    <span className="text-base font-normal text-muted-foreground"> g/hari</span>
                  </p>
                </div>
                <div
                  className="flex h-12 w-12 items-center justify-center rounded-full"
                  style={{ backgroundColor: item.color + '20' }}
                >
                  <span className="text-2xl">
                    {item.name === 'Karbohidrat' ? '🍞' : item.name === 'Protein' ? '🥩' : '🥑'}
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Distribusi Makronutrien</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip
                    formatter={(value: number) => [`${value} g/hari`, 'Kebutuhan']}
                  />
                  <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                    {chartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Proporsi Kebutuhan</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={5}
                    dataKey="value"
                    label={({ name, percent }) =>
                      `${name} ${(percent * 100).toFixed(0)}%`
                    }
                  />
                  <Tooltip formatter={(value: number) => [`${value} g/hari`]} />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Detailed Table */}
      <Card>
        <CardHeader>
          <CardTitle>Detail Kebutuhan Nutrisi</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b">
                  <th className="p-3 text-left font-semibold">Nutrisi</th>
                  <th className="p-3 text-left font-semibold">Kebutuhan</th>
                  <th className="p-3 text-left font-semibold">Kategori</th>
                  <th className="p-3 text-left font-semibold">Keterangan</th>
                </tr>
              </thead>
              <tbody>
                {allNutrients.map((nutrient, index) => (
                  <tr key={index} className="border-b last:border-0">
                    <td className="p-3 font-medium">{nutrient.name}</td>
                    <td className="p-3">
                      <span
                        className={`inline-flex items-center rounded-full bg-gradient-to-r ${getCategoryColor(nutrient.category)} px-3 py-1 text-sm font-semibold text-white`}
                      >
                        {nutrient.value} {nutrient.unit}
                      </span>
                    </td>
                    <td className="p-3">
                      <span
                        className={`inline-flex rounded-full border-2 ${getCategoryBorder(nutrient.category)} px-3 py-1 text-sm capitalize`}
                      >
                        {nutrient.category === 'carbohydrate'
                          ? 'Karbohidrat'
                          : nutrient.category === 'protein'
                            ? 'Protein'
                            : 'Lipid'}
                      </span>
                    </td>
                    <td className="p-3 text-sm text-muted-foreground">
                      {nutrient.description}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      {/* Insights */}
      <Card className="border-2 border-[#A07ED2]/40 bg-gradient-to-br from-[#A07ED2]/5 to-[#FF006E]/5">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-[#A07ED2]">
            <span className="text-2xl">💡</span>
            Insight Biologis
          </CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="space-y-3">
            {result.insights.map((insight, index) => (
              <li
                key={index}
                className="flex items-start gap-3 rounded-lg bg-white p-3 shadow-sm"
              >
                <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-[#A07ED2] text-sm font-bold text-white">
                  {index + 1}
                </span>
                <span className="text-[#A07ED2]/90">{insight}</span>
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>
    </div>
  );
}
