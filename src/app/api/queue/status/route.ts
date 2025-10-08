import { QueueService } from '@/lib/queueService';
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  try {
    const { searchParams } = new URL(request.url);
    const id = searchParams.get('id');

    if (!id) {
      return NextResponse.json(
        { success: false, error: 'Queue ID is required' },
        { status: 400 }
      );
    }

    const queueService = QueueService.getInstance();
    const status = queueService.getQueueStatus(id);

    if (!status) {
      return NextResponse.json(
        { success: false, error: 'Queue entry not found' },
        { status: 404 }
      );
    }

    return NextResponse.json({ success: true, status });
  } catch (error) {
    return NextResponse.json(
      { success: false, error: 'Failed to get queue status' },
      { status: 500 }
    );
  }
}