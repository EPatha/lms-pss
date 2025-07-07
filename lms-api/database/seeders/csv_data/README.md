### Step 1: Prepare Your CSV Data
Ensure you have your CSV data ready. For example, let's say you have a CSV file named `courses.csv` with the following structure:

```
id,title,description,created_at,updated_at
1,Introduction to Programming,Learn the basics of programming,2023-01-01,2023-01-01
2,Advanced Python,Deep dive into Python programming,2023-01-02,2023-01-02
```

### Step 2: Create the Seeder File
1. Navigate to the `lms-api/database/seeders/csv_data` directory.
2. Create a new PHP file for your seeder. For example, `CoursesSeeder.php`.

### Step 3: Write the Seeder Code
Open the `CoursesSeeder.php` file and write the following code:

```php
<?php

namespace Database\Seeders\CsvData;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\File;

class CoursesSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        // Path to the CSV file
        $csvFilePath = database_path('seeders/csv_data/courses.csv');

        // Check if the file exists
        if (!File::exists($csvFilePath)) {
            $this->command->error("CSV file not found at: {$csvFilePath}");
            return;
        }

        // Read the CSV file
        $csvData = array_map('str_getcsv', file($csvFilePath));
        $header = array_shift($csvData); // Get the header row

        // Prepare data for insertion
        $dataToInsert = [];
        foreach ($csvData as $row) {
            $dataToInsert[] = array_combine($header, $row);
        }

        // Insert data into the database
        DB::table('courses')->insert($dataToInsert);

        $this->command->info('Courses table seeded successfully!');
    }
}
```

### Step 4: Register the Seeder
Make sure to register your new seeder in the `DatabaseSeeder.php` file located in the `lms-api/database/seeders` directory:

```php
use Database\Seeders\CsvData\CoursesSeeder;

class DatabaseSeeder extends Seeder
{
    public function run()
    {
        $this->call([
            CoursesSeeder::class,
            // Other seeders can be added here
        ]);
    }
}
```

### Step 5: Run the Seeder
Finally, run the seeder using the Artisan command:

```bash
php artisan db:seed
```

This will execute the `CoursesSeeder`, read the data from `courses.csv`, and insert it into the `courses` table in your database.

### Notes
- Ensure that the database table (`courses` in this case) exists and matches the structure of your CSV data.
- Adjust the CSV file path and table name as necessary based on your project structure and requirements.