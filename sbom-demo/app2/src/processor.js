/**
 * Report Data Processor
 * Uses lodash 4.17.21 — patched version, NOT vulnerable to CVE-2021-23337
 */

const _ = require('lodash');
const moment = require('moment');

const QUARTERLY_DATA = {
    'Q1-2024': { revenue: 4250000, expenses: 3100000, accounts: 847 },
    'Q2-2024': { revenue: 4800000, expenses: 3400000, accounts: 912 },
    'Q3-2024': { revenue: 5100000, expenses: 3600000, accounts: 978 },
    'Q4-2024': { revenue: 5500000, expenses: 3900000, accounts: 1043 },
};

function processReportData(reportType, period) {
    const data = QUARTERLY_DATA[period] || QUARTERLY_DATA['Q1-2024'];

    const base = {
        report_type: reportType,
        period: period,
        generated_at: moment().toISOString(),
        tool_version: '1.1.0',
        lodash_version: _.VERSION
    };

    if (reportType === 'detailed') {
        return _.merge(base, {
            financials: {
                revenue: data.revenue,
                expenses: data.expenses,
                profit: data.revenue - data.expenses,
                margin: (((data.revenue - data.expenses) / data.revenue) * 100).toFixed(2) + '%'
            },
            accounts: { total: data.accounts },
            breakdown: _.map(_.range(1, 4), (month) => ({
                month: moment().quarter(parseInt(period[1])).month(month - 1).format('MMMM'),
                estimated_revenue: Math.floor(data.revenue / 3)
            }))
        });
    }

    return _.merge(base, {
        summary: {
            revenue:  data.revenue,
            expenses: data.expenses,
            profit:   data.revenue - data.expenses
        }
    });
}

module.exports = { processReportData };
