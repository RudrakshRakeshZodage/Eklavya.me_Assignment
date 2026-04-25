import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const body = await request.json();

    // We are forcing Port 8001 here!
    console.log('Bridge: Connecting to LOCALHOST Port 8001...');

    const response = await fetch('http://127.0.0.1:8001/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Bridge: Backend Error:', errorText);
      return NextResponse.json({ error: errorText }, { status: response.status });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error: any) {
    console.error('Bridge Connection Error:', error);
    return NextResponse.json({ error: 'Backend is offline. Run "python main.py" in backend folder.' }, { status: 500 });
  }
}
