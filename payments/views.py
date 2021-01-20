from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class AddPaymentMethodView(TemplateView):
    template_name = 'payments/add_payment_method.html'
