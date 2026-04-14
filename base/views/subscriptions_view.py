import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse
from base.models.users_model import User
from django.contrib.auth import update_session_auth_hash

stripe.api_key = settings.STRIPE_SECRET_KEY


class SubscriptionCreateView(LoginRequiredMixin, View):
    """サブスクリプション登録ページ"""

    # 1. これが足りなかったため、ページが表示されませんでした
    def get(self, request):
        print("DEBUG: SubscriptionCreateView.get が呼ばれました！")
        return render(request, 'subscription/create.html', {
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        })

    # 2. postメソッド（インデントを SubscriptionCreateView の中に合わせてください）
    def post(self, request):
        # request.user ではなく DB から最新のインスタンスを取得
        user = User.objects.get(pk=request.user.pk)
        payment_method_id = request.POST.get('payment_method_id')

        try:
            # Stripe顧客を作成（既存のロジック）
            if not user.stripe_customer_id:
                customer = stripe.Customer.create(
                    email=user.email,
                    metadata={'name': user.name},
                    payment_method=payment_method_id,
                    invoice_settings={'default_payment_method': payment_method_id},
                )
                user.stripe_customer_id = customer.id
            else:
                # 既存顧客に支払い方法を追加
                stripe.PaymentMethod.attach(payment_method_id, customer=user.stripe_customer_id)
                stripe.Customer.modify(
                    user.stripe_customer_id,
                    invoice_settings={'default_payment_method': payment_method_id},
                )

            # サブスクリプション作成
            subscription = stripe.Subscription.create(
                customer=user.stripe_customer_id,
                items=[{'price': settings.STRIPE_PRICE_ID}],
            )

            # --- ユーザー情報の更新 ---
            user.stripe_subscription_id = subscription.id
            user.user_class = User.UserClass.PREMIUM
            user.save()

            return redirect('subscription_complete')

        except Exception as e:
            print(f"DEBUG: Stripe Error: {e}")
            return render(request, 'subscription/create.html', {
                'error': '決済処理中にエラーが発生しました。',
                'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
            })

class SubscriptionCompleteView(LoginRequiredMixin, View):
    """登録完了ページ"""

    def get(self, request):
        return render(request, 'subscription/complete.html')


class SubscriptionCancelView(LoginRequiredMixin, View):
    """サブスクリプション解約"""

    def get(self, request):
        return render(request, 'subscription/cancel.html')

    def post(self, request):
        user = User.objects.get(pk=request.user.pk)

        if user.stripe_subscription_id:
            stripe.Subscription.delete(user.stripe_subscription_id)
            user.stripe_subscription_id = None
            user.user_class = User.UserClass.FREE
            user.save()

            # 【重要】ログイン中のセッション情報を最新の user (FREE) で上書きする
            update_session_auth_hash(request, user)

        return redirect('subscription_cancel_complete')


class SubscriptionCancelCompleteView(LoginRequiredMixin, View):
    """解約完了ページ"""

    def get(self, request):
        return render(request, 'subscription/cancel_complete.html')


class PaymentMethodUpdateView(LoginRequiredMixin, View):
    """クレジットカード情報の変更"""

    def get(self, request):
        return render(request, 'subscription/payment_update.html', {
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        })

    def post(self, request):
        user = request.user
        payment_method_id = request.POST.get('payment_method_id')

        if user.stripe_customer_id:
            # 新しい支払い方法を追加
            stripe.PaymentMethod.attach(payment_method_id, customer=user.stripe_customer_id)
            # デフォルトに設定
            stripe.Customer.modify(
                user.stripe_customer_id,
                invoice_settings={'default_payment_method': payment_method_id},
            )

        return redirect('payment_update_complete')


class PaymentUpdateCompleteView(LoginRequiredMixin, View):
    """カード変更完了ページ"""

    def get(self, request):
        return render(request, 'subscription/payment_update_complete.html')


class CreatePaymentIntentView(LoginRequiredMixin, View):
    """Stripe SetupIntent作成（AJAX用）"""

    def post(self, request):
        user = request.user

        # 顧客がなければ作成
        if not user.stripe_customer_id:
            customer = stripe.Customer.create(
                email=user.email,
                name=user.name,
            )
            user.stripe_customer_id = customer.id
            user.save()

        # SetupIntent作成
        setup_intent = stripe.SetupIntent.create(
            customer=user.stripe_customer_id,
        )

        return JsonResponse({
            'client_secret': setup_intent.client_secret,
        })

