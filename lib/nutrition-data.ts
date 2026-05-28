// Nutrition calculation functions based on age and gender

export interface NutrientResult {
  name: string;
  value: number;
  unit: string;
  category: 'carbohydrate' | 'protein' | 'lipid';
  description: string;
}

export interface SimulationResult {
  age: number;
  gender: 'male' | 'female';
  carbohydrates: NutrientResult[];
  proteins: NutrientResult[];
  lipids: NutrientResult[];
  insights: string[];
}

// Age groups for nutritional requirements
type AgeGroup = 'infant' | 'child' | 'teen' | 'adult' | 'elderly';

function getAgeGroup(age: number): AgeGroup {
  if (age < 3) return 'infant';
  if (age < 13) return 'child';
  if (age < 20) return 'teen';
  if (age < 60) return 'adult';
  return 'elderly';
}

// Carbohydrate calculations
function calculateCarbohydrates(age: number, gender: 'male' | 'female'): NutrientResult[] {
  const ageGroup = getAgeGroup(age);
  
  // Base values that vary by age group
  const baseValues: Record<AgeGroup, { glucose: number; fiber: number; totalCarbs: number }> = {
    infant: { glucose: 60, fiber: 5, totalCarbs: 95 },
    child: { glucose: 100, fiber: 20, totalCarbs: 130 },
    teen: { glucose: 130, fiber: 26, totalCarbs: 175 },
    adult: { glucose: 130, fiber: 30, totalCarbs: 225 },
    elderly: { glucose: 100, fiber: 25, totalCarbs: 200 },
  };

  const genderMultiplier = gender === 'male' ? 1.1 : 1.0;
  const values = baseValues[ageGroup];

  return [
    {
      name: 'Total Karbohidrat',
      value: Math.round(values.totalCarbs * genderMultiplier),
      unit: 'g/hari',
      category: 'carbohydrate',
      description: 'Sumber energi utama tubuh, dipecah menjadi glukosa',
    },
    {
      name: 'Glukosa Minimal',
      value: Math.round(values.glucose * genderMultiplier),
      unit: 'g/hari',
      category: 'carbohydrate',
      description: 'Kebutuhan minimum untuk fungsi otak dan sistem saraf',
    },
    {
      name: 'Serat',
      value: Math.round(values.fiber * genderMultiplier),
      unit: 'g/hari',
      category: 'carbohydrate',
      description: 'Penting untuk kesehatan pencernaan dan mikrobioma usus',
    },
  ];
}

// Protein calculations
function calculateProteins(age: number, gender: 'male' | 'female'): NutrientResult[] {
  const ageGroup = getAgeGroup(age);
  
  const baseValues: Record<AgeGroup, { total: number; essential: number }> = {
    infant: { total: 13, essential: 9 },
    child: { total: 34, essential: 20 },
    teen: { total: 52, essential: 30 },
    adult: { total: 56, essential: 35 },
    elderly: { total: 60, essential: 38 },
  };

  const genderMultiplier = gender === 'male' ? 1.15 : 1.0;
  const values = baseValues[ageGroup];

  return [
    {
      name: 'Total Protein',
      value: Math.round(values.total * genderMultiplier),
      unit: 'g/hari',
      category: 'protein',
      description: 'Diperlukan untuk pertumbuhan dan perbaikan jaringan tubuh',
    },
    {
      name: 'Asam Amino Esensial',
      value: Math.round(values.essential * genderMultiplier),
      unit: 'g/hari',
      category: 'protein',
      description: 'Asam amino yang tidak dapat diproduksi tubuh, harus dari makanan',
    },
    {
      name: 'Protein/kg BB',
      value: ageGroup === 'infant' ? 1.5 : ageGroup === 'child' ? 1.1 : ageGroup === 'teen' ? 1.0 : ageGroup === 'adult' ? 0.8 : 1.0,
      unit: 'g/kg/hari',
      category: 'protein',
      description: 'Kebutuhan protein berdasarkan berat badan ideal',
    },
  ];
}

// Lipid calculations
function calculateLipids(age: number, gender: 'male' | 'female'): NutrientResult[] {
  const ageGroup = getAgeGroup(age);
  
  const baseValues: Record<AgeGroup, { total: number; saturated: number; omega3: number }> = {
    infant: { total: 31, saturated: 10, omega3: 0.5 },
    child: { total: 50, saturated: 15, omega3: 0.9 },
    teen: { total: 65, saturated: 18, omega3: 1.2 },
    adult: { total: 70, saturated: 20, omega3: 1.6 },
    elderly: { total: 60, saturated: 15, omega3: 1.6 },
  };

  const genderMultiplier = gender === 'male' ? 1.1 : 1.0;
  const values = baseValues[ageGroup];

  return [
    {
      name: 'Total Lemak',
      value: Math.round(values.total * genderMultiplier),
      unit: 'g/hari',
      category: 'lipid',
      description: 'Sumber energi cadangan dan pelindung organ vital',
    },
    {
      name: 'Lemak Jenuh (maks)',
      value: Math.round(values.saturated * genderMultiplier),
      unit: 'g/hari',
      category: 'lipid',
      description: 'Batas maksimum untuk kesehatan jantung',
    },
    {
      name: 'Omega-3',
      value: values.omega3 * genderMultiplier,
      unit: 'g/hari',
      category: 'lipid',
      description: 'Asam lemak esensial untuk otak dan jantung',
    },
  ];
}

// Generate insights based on age and gender
function generateInsights(age: number, gender: 'male' | 'female'): string[] {
  const ageGroup = getAgeGroup(age);
  const insights: string[] = [];

  switch (ageGroup) {
    case 'infant':
      insights.push('Masa pertumbuhan cepat - kebutuhan nutrisi per kg BB sangat tinggi');
      insights.push('ASI adalah sumber nutrisi terbaik hingga usia 2 tahun');
      insights.push('Pembentukan mikrobioma usus sangat penting di fase ini');
      break;
    case 'child':
      insights.push('Pertumbuhan aktif membutuhkan protein berkualitas tinggi');
      insights.push('Kalsium dan vitamin D penting untuk pembentukan tulang');
      insights.push('Batasi gula tambahan untuk kesehatan gigi dan metabolisme');
      break;
    case 'teen':
      insights.push('Masa pubertas - kebutuhan energi dan protein meningkat signifikan');
      insights.push('Zat besi penting terutama untuk remaja perempuan');
      insights.push('Pola makan mempengaruhi kesehatan jangka panjang');
      break;
    case 'adult':
      insights.push('Fokus pada keseimbangan energi untuk menjaga berat badan ideal');
      insights.push('Serat penting untuk kesehatan pencernaan dan kontrol gula darah');
      insights.push('Batasi lemak jenuh untuk kesehatan kardiovaskular');
      break;
    case 'elderly':
      insights.push('Kebutuhan protein meningkat untuk mencegah sarcopenia (kehilangan massa otot)');
      insights.push('Penyerapan nutrisi menurun - perlu makanan padat nutrisi');
      insights.push('Hidrasi dan serat penting untuk fungsi pencernaan optimal');
      break;
  }

  if (gender === 'female') {
    if (ageGroup === 'teen' || ageGroup === 'adult') {
      insights.push('Kebutuhan zat besi lebih tinggi karena menstruasi');
    }
    if (ageGroup === 'adult') {
      insights.push('Kalsium dan vitamin D penting untuk mencegah osteoporosis');
    }
  }

  if (gender === 'male' && (ageGroup === 'teen' || ageGroup === 'adult')) {
    insights.push('Kebutuhan kalori lebih tinggi karena massa otot lebih besar');
  }

  return insights;
}

export function calculateNutrition(age: number, gender: 'male' | 'female'): SimulationResult {
  return {
    age,
    gender,
    carbohydrates: calculateCarbohydrates(age, gender),
    proteins: calculateProteins(age, gender),
    lipids: calculateLipids(age, gender),
    insights: generateInsights(age, gender),
  };
}

// Data for analysis charts
export const ageGroupData = [
  { ageGroup: '0-2 tahun', carbs: 95, protein: 13, lipid: 31 },
  { ageGroup: '3-12 tahun', carbs: 130, protein: 34, lipid: 50 },
  { ageGroup: '13-19 tahun', carbs: 175, protein: 52, lipid: 65 },
  { ageGroup: '20-59 tahun', carbs: 225, protein: 56, lipid: 70 },
  { ageGroup: '60+ tahun', carbs: 200, protein: 60, lipid: 60 },
];

export const genderComparisonData = [
  { nutrient: 'Karbohidrat', male: 248, female: 225 },
  { nutrient: 'Protein', male: 64, female: 56 },
  { nutrient: 'Lemak', male: 77, female: 70 },
];
