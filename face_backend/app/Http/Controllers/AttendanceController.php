<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Attendance;
use App\Models\User;
use Carbon\Carbon;

class AttendanceController extends Controller
{
   public function store(Request $request)
{
    $request->validate([
        'name' => 'required|string',
        'id' => 'required|exists:users,id', 
    ]);

    $user = User::find($request->id);

    $attendance = Attendance::create([
        'name' => $request->name,
        'user_id' => $user->id,
        'attendance_time' => Carbon::now(),
        'status' => $request->status ?? 'in', 
    ]);

    return response()->json(['success' => true, 'data' => $attendance]);
}

    public function latestStatus($user_id)
    {
        $record = Attendance::where('user_id', $user_id)->orderByDesc('attendance_time')->first();
        if ($record) {
            return response()->json(['status' => $record->status]);
        }
        return response()->json(['status' => null]);
    }
}