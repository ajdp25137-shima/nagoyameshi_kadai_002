document.addEventListener('DOMContentLoaded', function () {
    const stripeKey = document.getElementById('stripe-key').dataset.key;
    const stripe = Stripe(stripeKey);
    const elements = stripe.elements();

    const cardElement = elements.create('card', {
        style: {
            base: {
                fontSize: '16px',
                color: '#333',
                '::placeholder': { color: '#aab7c4' },
            },
        },
    });
    cardElement.mount('#card-element');

    // エラー表示
    cardElement.on('change', function (event) {
        const errorEl = document.getElementById('card-errors');
        errorEl.textContent = event.error ? event.error.message : '';
    });

    // フォーム送信
    const form = document.getElementById('payment-form');
    const submitBtn = document.getElementById('submit-btn');

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        submitBtn.disabled = true;
        submitBtn.textContent = '処理中...';

        // SetupIntentを取得
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const response = await fetch('/subscription/setup-intent/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
        });
        const { client_secret } = await response.json();

        // カード情報を確認
        const { setupIntent, error } = await stripe.confirmCardSetup(client_secret, {
            payment_method: { card: cardElement },
        });

        if (error) {
            document.getElementById('card-errors').textContent = error.message;
            submitBtn.disabled = false;
            submitBtn.textContent = '登録する';
            return;
        }

        // payment_method_idをhiddenフィールドにセットして送信
        document.getElementById('payment-method-id').value = setupIntent.payment_method;
        form.submit();
    });
});

