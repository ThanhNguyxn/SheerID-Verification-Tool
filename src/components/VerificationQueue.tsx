import React, { useEffect, useState } from 'react';

interface QueueStatus {
  position: number;
  total: number;
  estimatedWait: number;
  status: 'waiting' | 'processing' | 'completed' | 'failed';
}

interface QueueEntry {
  id: string;
  timestamp: number;
  status: 'waiting' | 'processing' | 'completed' | 'failed';
}

export const VerificationQueue: React.FC = () => {
  const [queueId, setQueueId] = useState<string | null>(null);
  const [queueStatus, setQueueStatus] = useState<QueueStatus | null>(null);
  const [loading, setLoading] = useState(false);

  const joinQueue = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/queue', {
        method: 'POST',
      });
      const data = await response.json();
      
      if (data.success && data.entry) {
        setQueueId(data.entry.id);
      }
    } catch (error) {
      console.error('Failed to join queue:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!queueId) return;

    const checkStatus = async () => {
      try {
        const response = await fetch(`/api/queue/status?id=${queueId}`);
        const data = await response.json();
        
        if (data.success && data.status) {
          setQueueStatus(data.status);
        }
      } catch (error) {
        console.error('Failed to get queue status:', error);
      }
    };

    const interval = setInterval(checkStatus, 5000);
    checkStatus(); // Initial check

    return () => clearInterval(interval);
  }, [queueId]);

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold text-center mb-6">SheerID Verifier</h2>
      <div className="space-y-4">
        {queueStatus ? (
          <div className="p-4 bg-gray-50 rounded-md">
            <p className="text-gray-700">Queue Information:</p>
            <ul className="mt-2 space-y-2">
              <li>Position: {queueStatus.position} of {queueStatus.total}</li>
              <li>Estimated Wait: {queueStatus.estimatedWait}s</li>
              <li>Status: {queueStatus.status}</li>
            </ul>
          </div>
        ) : (
          <div className="text-center">
            <button 
              onClick={joinQueue}
              disabled={loading}
              className={`bg-blue-500 text-white px-6 py-2 rounded-md transition-colors ${
                loading ? 'opacity-50 cursor-not-allowed' : 'hover:bg-blue-600'
              }`}
            >
              {loading ? 'Joining Queue...' : 'Start Verification'}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};