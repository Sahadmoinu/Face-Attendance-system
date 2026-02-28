<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AttendanceController;
Route::get('/', function () {
    return view('welcome');
});

Route::post('/recognized-face', [AttendanceController::class, 'store'])->withoutMiddleware('web');
Route::get('/recognized-face/latest-status/{user_id}', [AttendanceController::class, 'latestStatus'])->withoutMiddleware('web');;