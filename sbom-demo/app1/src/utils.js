/**
 * Utility functions for the Customer Portal API
 * Heavy use of lodash for data manipulation
 */

const _ = require('lodash');

/**
 * Format customer data for API response
 * Uses lodash _.pick to select safe fields (avoid exposing internal fields)
 */
function formatCustomerData(customer) {
    return {
        ..._.pick(customer, ['id', 'name', 'status']),
        balance_formatted: `$${customer.balance.toLocaleString()}`,
        account_age_days: Math.floor(Math.random() * 365) + 30
    };
}

/**
 * Filter to only active accounts
 * Uses lodash _.filter
 */
function filterActiveAccounts(customers) {
    return _.filter(customers, (c) => c.status === 'active');
}

/**
 * Deep merge configuration objects
 * Uses lodash _.merge — NOTE: lodash.merge is the function affected by
 * prototype pollution vulnerabilities in older lodash versions
 */
function mergeConfig(defaultConfig, userConfig) {
    return _.merge({}, defaultConfig, userConfig);
}

/**
 * Chunk an array for batch processing
 */
function chunkForBatch(items, batchSize = 50) {
    return _.chunk(items, batchSize);
}

module.exports = {
    formatCustomerData,
    filterActiveAccounts,
    mergeConfig,
    chunkForBatch
};
