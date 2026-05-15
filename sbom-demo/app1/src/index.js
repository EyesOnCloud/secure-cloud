/**
 * Customer Portal API
 * App1 — Financial Services Platform
 *
 * This application provides REST endpoints for the customer portal.
 * It uses lodash for data manipulation utilities.
 */

const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const routes = require('./routes');

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Mount routes
app.use('/api', routes);

// Health check
app.get('/health', (req, res) => {
    res.json({
        status: 'running',
        app: 'customer-portal-api',
        version: '2.3.1',
        timestamp: new Date().toISOString()
    });
});

// Error handler
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).json({ error: 'Internal server error' });
});

app.listen(PORT, () => {
    console.log(`Customer Portal API running on port ${PORT}`);
});

module.exports = app;
