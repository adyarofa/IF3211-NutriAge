'use client';

import { useState } from 'react';
import { calculateNutrition, type SimulationResult } from '@/lib/nutrition-data';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Slider } from '@/components/ui/slider';

interface SimulationFormProps {
  onResult: (result: SimulationResult) => void;
}

export function SimulationForm({ onResult }: SimulationFormProps) {
  const [age, setAge] = useState(25);
  const [gender, setGender] = useState<'male' | 'female'>('male');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const result = calculateNutrition(age, gender);
    onResult(result);
  };

  return (
    <Card className="border-2 border-[#A07ED2]/40 bg-gradient-to-br from-[#A07ED2]/10 to-[#FF006E]/10">
      <CardHeader>
        <CardTitle className="text-[#A07ED2]">Input Data</CardTitle>
        <CardDescription className="text-[#FF006E]/70">
          Masukkan usia dan jenis kelamin untuk simulasi kebutuhan nutrisi
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <Label htmlFor="age" className="text-base font-medium text-[#A07ED2]">
                Usia
              </Label>
              <span className="rounded-lg bg-gradient-to-r from-[#A07ED2] to-[#FF006E] px-4 py-1 text-lg font-bold text-white">
                {age} tahun
              </span>
            </div>
            <Slider
              id="age"
              min={0}
              max={100}
              step={1}
              value={[age]}
              onValueChange={(value) => setAge(value[0])}
              className="[&_[role=slider]]:bg-[#FF006E] [&_[role=slider]]:border-[#A07ED2]"
            />
            <div className="flex justify-between text-sm text-[#A07ED2]/60">
              <span>0</span>
              <span>25</span>
              <span>50</span>
              <span>75</span>
              <span>100</span>
            </div>
          </div>

          <div className="space-y-3">
            <Label className="text-base font-medium text-[#A07ED2]">Jenis Kelamin</Label>
            <RadioGroup
              value={gender}
              onValueChange={(value) => setGender(value as 'male' | 'female')}
              className="flex gap-4"
            >
              <div className="flex-1">
                <RadioGroupItem
                  value="male"
                  id="male"
                  className="peer sr-only"
                />
                <Label
                  htmlFor="male"
                  className="flex cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-[#A07ED2]/30 bg-white p-4 transition-all hover:bg-[#A07ED2]/10 peer-data-[state=checked]:border-[#A07ED2] peer-data-[state=checked]:bg-[#A07ED2]/20"
                >
                  <span className="text-3xl">👨</span>
                  <span className="mt-2 font-medium text-[#A07ED2]">Laki-laki</span>
                </Label>
              </div>
              <div className="flex-1">
                <RadioGroupItem
                  value="female"
                  id="female"
                  className="peer sr-only"
                />
                <Label
                  htmlFor="female"
                  className="flex cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-[#FF006E]/30 bg-white p-4 transition-all hover:bg-[#FF006E]/10 peer-data-[state=checked]:border-[#FF006E] peer-data-[state=checked]:bg-[#FF006E]/20"
                >
                  <span className="text-3xl">👩</span>
                  <span className="mt-2 font-medium text-[#FF006E]">Perempuan</span>
                </Label>
              </div>
            </RadioGroup>
          </div>

          <Button
            type="submit"
            className="w-full bg-gradient-to-r from-[#A07ED2] to-[#FF006E] text-white hover:from-[#8B68BD] hover:to-[#E6005F]"
            size="lg"
          >
            Hitung Kebutuhan Nutrisi
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
