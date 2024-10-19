const IlpConnector = require('ilp-connector');
const IlpPlugin = require('ilp-plugin'); // or another ILP plugin

async function sendPayment() {
    // Create an instance of the connector by calling it as a function
    const connector = IlpConnector({
        // Replace with your connector configuration
        // This could include your account details, secret, etc.
        port: 3000,
        // other configuration options
    });

    // Connect to the plugin
    const plugin = IlpPlugin({
        // Replace with your plugin configuration
        // This could include your account details, secret, etc.
    });

    await plugin.connect();

    const destination = 'ilp.interledger-test.dev/cedeee60';
    const amount = '100'; // Amount in euros, but needs to be in cents (smallest unit)

    try {
        const result = await connector.sendPayment({
            destination,
            amount, // Ensure this is in the
const IlpConnector = require('ilp-connector');
const IlpPlugin = require('ilp-plugin'); // or another ILP plugin

async function sendPayment() {
    // Create an instance of the connector by calling it as a function
    const connector = IlpConnector({
        // Replace with your connector configuration
        // This could include your account details, secret, etc.
                                                                [ Read 106 lines ]
