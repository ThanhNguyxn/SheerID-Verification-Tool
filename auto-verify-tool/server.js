const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const EventEmitter = require('events');
const { verifySheerID } = require('./verifier');

const app = express();
const PORT = process.env.PORT || 3000;

// Global log emitter for SSE - now session-based
const logEmitter = new EventEmitter();
logEmitter.setMaxListeners(100); // Allow many concurrent connections

// Export for use in verifier
global.logEmitter = logEmitter;

// Helper to emit logs - now with session ID
global.emitLog = (message, type = 'info', sessionId = null) => {
    const logData = { time: new Date().toISOString(), message, type, sessionId };
    console.log(`[${sessionId || 'GLOBAL'}] [${type.toUpperCase()}] ${message}`);
    logEmitter.emit('log', logData);
};

// Store current session ID for each verification
global.currentSessionId = null;

app.use(cors());
app.use(bodyParser.json());

// Health check / root route
app.get('/', (req, res) => {
    res.json({ status: 'ok', message: 'SheerID Verification API is running' });
});

// SSE endpoint for real-time logs - now with session filtering
app.get('/api/logs', (req, res) => {
    const sessionId = req.query.sessionId;

    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    res.setHeader('Access-Control-Allow-Origin', '*');

    const sendLog = (data) => {
        // Only send logs for this session or global logs
        if (!sessionId || !data.sessionId || data.sessionId === sessionId) {
            res.write(`data: ${JSON.stringify(data)}\n\n`);
        }
    };

    logEmitter.on('log', sendLog);

    req.on('close', () => {
        logEmitter.off('log', sendLog);
    });
});

// Original verify endpoint - now with session ID
app.post('/api/verify', async (req, res) => {
    const { url, type, sessionId } = req.body;

    if (!url) {
        return res.status(400).json({ success: false, error: 'URL is required' });
    }

    // Store session ID for this verification
    const sid = sessionId || `session_${Date.now()}`;

    // Create a session-scoped emitLog function
    const originalEmitLog = global.emitLog;
    global.emitLog = (message, logType = 'info') => {
        originalEmitLog(message, logType, sid);
    };

    global.emitLog(`🚀 Received verification request [Type: ${type || 'student'}]`, 'info');

    try {
        const result = await verifySheerID(url, type);
        res.json({ ...result, sessionId: sid });
    } catch (error) {
        global.emitLog(`❌ Error: ${error.message}`, 'error');
        res.json({ success: false, error: error.message, sessionId: sid });
    } finally {
        // Restore original emitLog
        global.emitLog = originalEmitLog;
    }
});

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
