from django.views.generic import DetailView
from base.models import CompanyInformation

class CompanyInformationDetailView(DetailView):
    model = CompanyInformation
    template_name = 'company/info_detail.html'
    context_object_name = 'company_info'

    def get_object(self, queryset=None):
        # 常に最新（最後）に登録・更新された1件を返すように設定
        return CompanyInformation.objects.last()