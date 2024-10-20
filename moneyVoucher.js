import { createAuthenticatedClient } from "@interledger/open-payments";
import crypto from 'crypto';
import fs from 'fs/promises';
import '@interledger/open-payments';

export class MoneyVoucher {
  constructor(sender, recipient, amount, message) {
    this.sender = sender;
    this.recipient = recipient;
    this.amount = amount;
    this.message = message;
    this.voucherCode = this.generateVoucherCode();
    this.issueDate = new Date().toLocaleDateString();
    this.redeemed = false;
    this.client = null;
    this.incomingPayment = null;
  }

  generateVoucherCode() {
    return crypto.randomBytes(4).toString('hex').toUpperCase();
  }

  printVoucher() {
    return `
    ================================
    MONEY VOUCHER
    ================================
    From: ${this.sender}
    To: ${this.recipient}
    Amount: $${this.amount}
    Message: ${this.message}
    --------------------------------
    Voucher Code: ${this.voucherCode}
    Issue Date: ${this.issueDate}
    Redeemed: ${this.redeemed ? 'Yes' : 'No'}
    ================================
    `;
  }

  async initializeClient(walletAddressUrl, privateKeyPath, keyId) {
    try {
      const privateKey = await fs.readFile(privateKeyPath, 'utf8');
      this.client = await createAuthenticatedClient({
        walletAddressUrl,
        privateKey,
        keyId,
      });
    } catch (error) {
      console.error("Error initializing client:", error.message);
      throw error;
    }
  }

  async createPayment(senderWalletUrl, receiverWalletUrl) {
    if (!this.client) {
      throw new Error("Client not initialized. Call initializeClient first.");
    }
    try {
      const senderWalletAddress = await this.client.walletAddress.get({ url: senderWalletUrl });
      const receiverWalletAddress = await this.client.walletAddress.get({ url: receiverWalletUrl });
      
      // Create incoming payment
      const incomingPaymentGrant = await this.client.grant.request(
        { url: receiverWalletAddress.authServer },
        {
          access_token: {
            access: [{ type: "incoming-payment", actions: ["read", "create"] }],
          },
        }
      );
      
      this.incomingPayment = await this.client.incomingPayment.create(
        {
          url: receiverWalletAddress.resourceServer,
          accessToken: incomingPaymentGrant.access_token.value,
        },
        {
          walletAddress: receiverWalletAddress.id,
          incomingAmount: {
            value: this.amount.toString(),
            assetCode: receiverWalletAddress.assetCode,
            assetScale: receiverWalletAddress.assetScale,
          },
        }
      );
      
      console.log("Incoming payment created:", this.incomingPayment);
      return this.incomingPayment;
    } catch (error) {
      console.error("Error creating payment:", error.message);
      throw error;
    }
  }

  async redeemVoucher(redeemerName, redeemerWalletUrl) {
    if (this.redeemed) {
      throw new Error("This voucher has already been redeemed.");
    }

    if (redeemerName.toLowerCase() !== this.recipient.toLowerCase()) {
      throw new Error("This voucher can only be redeemed by the intended recipient.");
    }

    if (!this.incomingPayment) {
      throw new Error("Payment has not been created for this voucher.");
    }

    try {
      // In a real-world scenario, you would implement the actual transfer of funds here.
      // For this example, we'll simulate the process.

      // 1. Verify the redeemer's wallet
      const redeemerWalletAddress = await this.client.walletAddress.get({ url: redeemerWalletUrl });

      // 2. Complete the payment (this is a simplified version)
      const completedPayment = await this.client.incomingPayment.complete(
        { url: this.incomingPayment.id },
        { receivedAmount: this.incomingPayment.incomingAmount }
      );

      // 3. Mark the voucher as redeemed
      this.redeemed = true;

      console.log("Voucher redeemed successfully.");
      return completedPayment;
    } catch (error) {
      console.error("Error redeeming voucher:", error.message);
      throw error;
    }
  }
}

export async function runExample() {
  const voucher = new MoneyVoucher("Alice", "Bob", 150, "Happy Birthday!");
  console.log(voucher.printVoucher());

  try {
    await voucher.initializeClient(
      "https://ilp.interledger-test.dev/cedeee60",
      "private.key",
      "4dde07f1-02fb-4a49-a464-d7a7db121e83"
    );

    await voucher.createPayment(
      "https://ilp.interledger-test.dev/cedeee60",
      "https://ilp.interledger-test.dev/bob"
    );

    // Attempt to redeem the voucher
    await voucher.redeemVoucher("Bob", "https://ilp.interledger-test.dev/bob");
    console.log(voucher.printVoucher()); // Should show as redeemed

    // Attempt to redeem again (should fail)
    await voucher.redeemVoucher("Bob", "https://ilp.interledger-test.dev/bob");
  } catch (error) {
    console.error("Error in example:", error.message);
  }
}

runExample();