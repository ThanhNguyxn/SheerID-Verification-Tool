const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { verifySheerID } = require('./verifier');

const app = express();
const PORT = 3000;

app.use(cors());
app.use(bodyParser.json());
app.use(express.static('public'));

app.post('/api/verify', async (req, res) => {
    const { url, type } = req.body;

    if (!url) {
        return res.status(400).json({ success: false, error: 'URL is required' });
    }

    console.log(`🚀 Received verification request for: ${url} [Type: ${type || 'student'}]`);

    // Start verification asynchronously
    const result = await verifySheerID(url, type);

    res.json(result);
});

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
