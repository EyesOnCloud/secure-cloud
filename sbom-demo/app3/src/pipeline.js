/**
 * Pipeline Processing Logic
 * No direct lodash usage — but transitive dependencies bring it in
 */

const async = require('async');
const Joi = require('joi');
const moment = require('moment');

// Validation schema for pipeline input
const pipelineSchema = Joi.object({
    source:      Joi.string().required(),
    destination: Joi.string().required(),
    filters:     Joi.object().optional()
});

// Sample transaction records to simulate ETL processing
const SAMPLE_TRANSACTIONS = [
    { id: 'TXN001', amount: 15000,  type: 'credit', date: '2024-01-15', account: 'ACC-001' },
    { id: 'TXN002', amount: 8500,   type: 'debit',  date: '2024-01-15', account: 'ACC-002' },
    { id: 'TXN003', amount: 225000, type: 'credit', date: '2024-01-16', account: 'ACC-003' },
    { id: 'TXN004', amount: 3200,   type: 'debit',  date: '2024-01-16', account: 'ACC-001' },
    { id: 'TXN005', amount: 75000,  type: 'credit', date: '2024-01-17', account: 'ACC-004' },
];

function runPipeline(jobId, source, destination, filters) {
    // Validate input
    const { error } = pipelineSchema.validate({ source, destination, filters });
    if (error) {
        throw new Error(`Validation failed: ${error.message}`);
    }

    // Simulate extraction
    let records = [...SAMPLE_TRANSACTIONS];

    // Apply filters if provided
    if (filters && filters.type) {
        records = records.filter(r => r.type === filters.type);
    }
    if (filters && filters.min_amount) {
        records = records.filter(r => r.amount >= filters.min_amount);
    }

    // Simulate transformation
    const transformed = records.map(r => ({
        ...r,
        processed_at: moment().toISOString(),
        job_id: jobId,
        amount_formatted: `$${r.amount.toLocaleString()}`
    }));

    return {
        records: transformed.length,
        source,
        destination,
        processed_at: moment().toISOString(),
        sample: transformed[0] || null
    };
}

module.exports = { runPipeline };
