/**
 * Report CLI Tool
 * App2 — Financial Reporting Command Line Interface
 *
 * This tool generates financial reports from CSV data files.
 * It was updated to lodash 4.17.21 during a routine dependency
 * review in Q3 2023.
 */

const { program } = require('commander');
const chalk = require('chalk');
const { processReportData } = require('./processor');

program
    .name('report-cli')
    .description('Financial report generation tool')
    .version('1.1.0');

program
    .command('generate')
    .description('Generate a financial report')
    .option('-t, --type <type>', 'Report type (summary|detailed|audit)', 'summary')
    .option('-p, --period <period>', 'Reporting period', 'Q1-2024')
    .option('-o, --output <file>', 'Output file path', './report-output.json')
    .action((options) => {
        console.log(chalk.blue('Financial Report Generator v1.1.0'));
        console.log(chalk.gray(`Generating ${options.type} report for ${options.period}...`));
        const result = processReportData(options.type, options.period);
        console.log(chalk.green('Report generated successfully'));
        console.log(JSON.stringify(result, null, 2));
    });

program.parse();

// Default action when run without subcommand
if (process.argv.length === 2) {
    console.log(chalk.blue('Report CLI Tool — use --help for options'));
    const result = processReportData('summary', 'Q1-2024');
    console.log(JSON.stringify(result, null, 2));
}
