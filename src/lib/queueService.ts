// Queue service for managing verification requests
export interface QueueEntry {
  id: string;
  timestamp: number;
  status: 'waiting' | 'processing' | 'completed' | 'failed';
}

export class QueueService {
  private static instance: QueueService;
  private queue: QueueEntry[] = [];

  private constructor() {}

  public static getInstance(): QueueService {
    if (!QueueService.instance) {
      QueueService.instance = new QueueService();
    }
    return QueueService.instance;
  }

  public addToQueue(): QueueEntry {
    const entry: QueueEntry = {
      id: Math.random().toString(36).substring(7),
      timestamp: Date.now(),
      status: 'waiting',
    };
    this.queue.push(entry);
    return entry;
  }

  public getQueueStatus(id: string) {
    const position = this.queue.findIndex(entry => entry.id === id);
    if (position === -1) return null;

    return {
      position: position + 1,
      total: this.queue.length,
      estimatedWait: position * 30, // Assuming 30 seconds per verification
      status: this.queue[position].status,
    };
  }
}