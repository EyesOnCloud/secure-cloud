/**
 * API Routes — Customer Portal
 * Uses lodash for data transformation and filtering
 */

const express = require('express');
const router = express.Router();
const _ = require('lodash');
const moment = require('moment');
const { formatCustomerData, filterActiveAccounts } = require('./utils');

// Sample customer data (in real app this comes from database)
const customers = [
    { id: 1, name: 'Acme Corp',    status: 'active',   balance: 150000, lastLogin: '2024-01-15' },
    { id: 2, name: 'Beta LLC',     status: 'inactive', balance: 25000,  lastLogin: '2023-11-20' },
    { id: 3, name: 'Gamma Inc',    status: 'active',   balance: 380000, lastLogin: '2024-01-18' },
    { id: 4, name: 'Delta Co',     status: 'active',   balance: 92000,  lastLogin: '2024-01-10' },
    { id: 5, name: 'Epsilon Ltd',  status: 'suspended', balance: 5000,  lastLogin: '2023-09-01' },
];

// GET /api/customers — list all customers
router.get('/customers', (req, res) => {
    const active = filterActiveAccounts(customers);
    const sorted = _.sortBy(active, ['name']);
    res.json({ count: sorted.length, data: sorted });
});

// GET /api/customers/:id — get single customer
router.get('/customers/:id', (req, res) => {
    const customer = _.find(customers, { id: parseInt(req.params.id) });
    if (!customer) {
        return res.status(404).json({ error: 'Customer not found' });
    }
    res.json(formatCustomerData(customer));
});

// GET /api/summary — aggregate summary
router.get('/summary', (req, res) => {
    const grouped = _.groupBy(customers, 'status');
    const totalBalance = _.sumBy(customers, 'balance');
    const summary = _.mapValues(grouped, (group) => ({
        count: group.length,
        totalBalance: _.sumBy(group, 'balance')
    }));
    res.json({
        total_customers: customers.length,
        total_balance: totalBalance,
        by_status: summary,
        generated_at: moment().toISOString()
    });
});

module.exports = router;
