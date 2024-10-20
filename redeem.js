import { MoneyVoucher } from './moneyVoucher.js';
import readline from 'readline';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

async function promptUser(question) {
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      resolve(answer);
    });
  });
}

async function redeemVoucher() {
  try {
    const voucherCode = await promptUser("Enter your voucher code: ");
    const redeemerName = await promptUser("Enter your name: ");
    const redeemerWalletUrl = await promptUser("Enter your wallet URL: ");

    // In a real-world scenario, you would fetch the voucher details from a database
    // using the voucherCode. For this example, we'll create a dummy voucher.
    const dummyVoucher = new MoneyVoucher("Alice", redeemerName, 150, "Happy Birthday!");
    dummyVoucher.voucherCode = voucherCode;

    // Initialize the client
    // Note: In a production environment, you'd need to securely manage these credentials
    await dummyVoucher.initializeClient(
      "https://ilp.interledger-test.dev",
      "./private.key",
      "4dde07f1-02fb-4a49-a464-d7a7db121e83"
    );

    // Create a payment (in a real scenario, this would have been done when the voucher was created)
    await dummyVoucher.createPayment(
      "https://ilp.interledger-test.dev/alice",
      redeemerWalletUrl
    );

    // Attempt to redeem the voucher
    const result = await dummyVoucher.redeemVoucher(redeemerName, redeemerWalletUrl);
    
    console.log("\nVoucher redeemed successfully!");
    console.log("Payment details:", result);
    console.log("\nUpdated voucher information:");
    console.log(dummyVoucher.printVoucher());

  } catch (error) {
    console.error("Error redeeming voucher:", error.message);
  } finally {
    rl.close();
  }
}

redeemVoucher();