from django.shortcuts import render
from django.views.generic import View

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg, CityDict, Teacher
# Create your views here.


class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self, request):
        # 所有的课程机构
        all_orgs = CourseOrg.objects.all()
        org_nums = all_orgs.count()
        # 所有的城市
        all_cities = CityDict.objects.all()

        # 对课程机构分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, per_page=3)
        orgs = p.page(page)
        return render(request, 'org-list.html', {
            'all_orgs': orgs,
            'all_cities': all_cities,
            'org_nums': org_nums,
        })
