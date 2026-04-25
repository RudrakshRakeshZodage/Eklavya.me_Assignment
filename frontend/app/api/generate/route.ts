import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    
    // This code runs on Vercel's server, so it can talk to HTTP IPs without browser blocking
    const response = await fetch('http://13.217.105.1/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    const data = await response.json();
    
    if (!response.ok) {
      return NextResponse.json({ error: 'Backend error' }, { status: response.status });
    }

    return NextResponse.json(data);
  } catch (error: any) {
    console.error('Bridge Error:', error);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
