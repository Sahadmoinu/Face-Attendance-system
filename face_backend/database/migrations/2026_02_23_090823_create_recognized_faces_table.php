<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
       Schema::create('attendance', function (Blueprint $table) {
    $table->id();
    $table->string('user_id');
    $table->string('name');
    $table->time('attendance_time'); // just a time column
    $table->enum('status', ['in', 'out']); // status as enum
    $table->timestamps();
});
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('attendance');
    }
};
