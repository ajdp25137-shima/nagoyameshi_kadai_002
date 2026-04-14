from django.views.generic import DetailView
from base.models import CompanyInformation
from django.shortcuts import render

class CompanyInformationDetailView(DetailView):
    model = CompanyInformation
    template_name = 'company/info_detail.html'
    context_object_name = 'company_info'

    def get_object(self, queryset=None):
        # 常に最新（最後）に登録・更新された1件を返すように設定
        return CompanyInformation.objects.last()
    
def info_detail(request):
    """会社概要ページ"""
    # DBから1件取得する場合の例（モデルがある場合）
    # company_info = CompanyInformation.objects.first()
    # return render(request, 'info_detail.html', {'company_info': company_info})
    
    # まだDBがない場合は、とりあえずテンプレートだけ表示
    return render(request, 'info_detail.html')

def terms_of_use(request):
    """利用規約ページ"""
    return render(request, 'pages/terms_of_use.html')