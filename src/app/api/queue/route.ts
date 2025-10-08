import { QueueService } from '@/lib/queueService';
import { NextResponse } from 'next/server';

export async function POST() {
  try {
    const queueService = QueueService.getInstance();
    const entry = queueService.addToQueue();
    
    return NextResponse.json({ success: true, entry });
  } catch (error) {
    return NextResponse.json(
      { success: false, error: 'Failed to join queue' },
      { status: 500 }
    );
  }
}