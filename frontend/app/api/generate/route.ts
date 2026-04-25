import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    
    console.log('Bridge: Connecting to Production Render Backend...');
    
    // Connect to the Render HTTPS URL
    const response = await fetch('https://eklavya-me-assignment.onrender.com/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
      cache: 'no-store'
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Backend Error' }));
      console.error('Bridge: Production Backend Error:', errorData);
      return NextResponse.json(errorData, { status: response.status });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error: unknown) {
    console.error('Bridge Connection Error:', error);
    const errorMessage = error instanceof Error ? error.message : 'Unknown production error';
    return NextResponse.json({ error: errorMessage }, { status: 500 });
  }
}
