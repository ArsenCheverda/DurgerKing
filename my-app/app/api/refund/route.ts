import { NextRequest, NextResponse } from "next/server";

export async function POST(req:NextRequest) {
    // поміняти на реальну датабазу
    return NextResponse.json({
        success: false,
        message: 'In this demo webapp, refunds must be handled through the Telegram Bot',
        details: 'For a production app, you would implement direct refund functionality using real transaction IDs stored in database'
    }, {status: 400})
}