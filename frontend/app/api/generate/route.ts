// DEPLOYMENT VERSION: 2.1 (PORT 8000)
import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    
    console.log('Bridge: Sending request to EC2 Port 8000...');
    
    // Use Port 8000 to bypass any Port 80 conflicts on EC2
    const response = await fetch('http://13.217.105.1:8000/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(body),
      cache: 'no-store'
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Bridge: Backend Error Response:', errorText);
      return NextResponse.json({ error: 'Backend error' }, { status: response.status });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error: any) {
    console.error('Bridge Error:', error);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
