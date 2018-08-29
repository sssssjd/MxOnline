# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg, CityDict, Teacher
from operation.forms import UserAskForm
# Create your views here.


class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self, request):
        # 所有的课程机构
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by('-click_nums')[:5]
        # 所有的城市
        all_cities = CityDict.objects.all()

        # 筛选机构
        catgory = request.GET.get('ct', '')
        if catgory:
            all_orgs = all_orgs.filter(catgory=catgory)

        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')

        # 筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 获取筛选后的机构数量
        org_nums = all_orgs.count()

        # 对课程机构分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, per_page=3)
        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'all_orgs': orgs,
            'hot_orgs': hot_orgs,
            'all_cities': all_cities,
            'org_nums': org_nums,
            'city_id': city_id,
            'catgory': catgory,
            'sort': sort,
        })


class UserAskView(View):
    """
    添加用户咨询
    """
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status": "success"}', content_type='application/json')
        else:
            return HttpResponse("{'status': 'fail', 'msg':{0}}".format(userask_form.errors), content_type='json')
            # return HttpResponse('{"status":"fail", "msg":"请求失败！"}', content_type='application/json')
