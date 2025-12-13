const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const EventEmitter = require('events');
const { verifySheerID } = require('./verifier');

const app = express();
const PORT = process.env.PORT || 3000;

// Global log emitter for SSE
const logEmitter = new EventEmitter();

// Export for use in verifier
global.logEmitter = logEmitter;

// Helper to emit logs
global.emitLog = (message, type = 'info') => {
    const logData = { time: new Date().toISOString(), message, type };
    console.log(`[${type.toUpperCase()}] ${message}`);
    logEmitter.emit('log', logData);
};

app.use(cors());
app.use(bodyParser.json());

// Health check / root route
app.get('/', (req, res) => {
    res.json({ status: 'ok', message: 'SheerID Verification API is running' });
});

// SSE endpoint for real-time logs
app.get('/api/logs', (req, res) => {
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    res.setHeader('Access-Control-Allow-Origin', '*');

    const sendLog = (data) => {
        res.write(`data: ${JSON.stringify(data)}\n\n`);
    };

    logEmitter.on('log', sendLog);

    req.on('close', () => {
        logEmitter.off('log', sendLog);
    });
});

// Original verify endpoint
app.post('/api/verify', async (req, res) => {
    const { url, type } = req.body;

    if (!url) {
        return res.status(400).json({ success: false, error: 'URL is required' });
    }

    global.emitLog(`🚀 Received verification request [Type: ${type || 'student'}]`, 'info');

    const result = await verifySheerID(url, type);

    res.json(result);
});

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
