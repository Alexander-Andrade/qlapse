// Get Stripe publishable key
fetch("/stripe_payments/config/")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey);

  document.querySelector("#press_stripe_payment").addEventListener("click", () => {
    // Get Checkout Session ID
    fetch("/stripe_payments/create-checkout-session/")
    .then((result) => { return result.json(); })
    .then((data) => {
      // Redirect to Stripe Checkout
      return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    .then((res) => {
      console.log(res);
    });
  });
});