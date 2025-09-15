import { NextRequest, NextResponse } from 'next/server';
import { getItemById } from '@/app/data/items';

export async function POST(req: NextRequest) {
    try {
        const body = await req.json();
        const { userId, itemId } = body;

        if (!userId || !itemId) {
            return NextResponse.json({ error: 'Missing required fields: userId and itemId' }, { status: 400 });
        }

        // Get item details from our data store
        const item = getItemById(itemId);
        if (!item) {
            return NextResponse.json({ error: 'Invalid item ID' }, { status: 400 });
        }

        // Extract item details
        const { name: title, description, price } = item;

        const BOT_TOKEN = process.env.BOT_TOKEN;

        if (!BOT_TOKEN) {
            return NextResponse.json({ error: 'Bot token not configured'}, { status: 500});
        }

        // Create an actual invoice link by calling the Telegram Bot API
        const response = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/createInvoiceLink`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title,
                description,
                payload: itemId,        // In production, use a JSON string with a unique request ID
                provider_token: '',     // Empty for Telegram Stars payments
                currency: 'XTR',        // Telegram Stars currency code
                prices: [{ label: title, amount: price }],
                start_parameter: "start_parameter" // Required for some clients
            })
        });

        const data = await response.json();

        if (!data.ok) {
            console.error('Telegram API error:', data);
            return NextResponse.json({ error: data.description || 'Failed to create invoice' }, { status: 500 });
        }

        const invoiceLink = data.result;

        return NextResponse.json({ invoiceLink });

    } catch (error) {
        console.error('Error creating invoice:', error);
        return NextResponse.json({ error: 'Failed to create invoice' }, { status: 500 });
    }
}
