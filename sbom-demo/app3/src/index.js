/**
 * ETL Data Pipeline
 * App3 — Financial Transaction Processing
 *
 * This pipeline processes financial transaction data.
 * It does NOT directly use lodash — the development team
 * was not aware that their dependencies (winston, async)
 * pull in lodash as a transitive dependency.
 *
 * This is the critical SBOM teaching moment:
 * you cannot find this vulnerability by reading package.json.
 * You need an SBOM that captures transitive dependencies.
 */

const express = require('express');
const winston = require('winston');
const { v4: uuidv4 } = require('uuid');
const { runPipeline } = require('./pipeline');

// Configure logger using winston (which internally depends on lodash)
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
    ),
    transports: [new winston.transports.Console()]
});

const app = express();
const PORT = process.env.PORT || 3003;

app.use(express.json());

app.get('/health', (req, res) => {
    res.json({
        status: 'running',
        app: 'etl-data-pipeline',
        version: '3.0.2',
        timestamp: new Date().toISOString()
    });
});

app.post('/pipeline/run', (req, res) => {
    const jobId = uuidv4();
    const { source, destination, filters } = req.body;

    logger.info('Pipeline job started', { jobId, source, destination });

    try {
        const result = runPipeline(jobId, source, destination, filters);
        logger.info('Pipeline job completed', { jobId, recordsProcessed: result.records });
        res.json({ jobId, status: 'completed', result });
    } catch (err) {
        logger.error('Pipeline job failed', { jobId, error: err.message });
        res.status(500).json({ jobId, status: 'failed', error: err.message });
    }
});

app.listen(PORT, () => {
    logger.info(`ETL Pipeline running on port ${PORT}`);
});
