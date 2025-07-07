<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
use League\Csv\Reader;

class CourseCsvSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $csvPath = database_path('seeders/csv_data/course-data.csv');
        $csv = fopen($csvPath, 'r');
        $header = fgetcsv($csv);

        while (($row = fgetcsv($csv)) !== false) {
            $data = array_combine($header, $row);

            DB::table('courses')->insert([
                'name' => $data['name'],
                'url' => $data['url'],
                'description' => $data['description'],
                'site' => $data['site'],
                'price' => $data['price'],
                'teacher' => $data['teacher'],
            ]);
        }

        fclose($csv);
    }
}
