# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import View

from pure_pagination import Paginator, PageNotAnInteger

from .models import Course
from organization.models import CourseOrg
from operation.models import UserFavorite

# Create your views here.


class CourseListView(View):
    def get(self, request):
        # 全部
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = all_courses.order_by('-click_nums')[:3]

        # 课程排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')

        # 对课程列表分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, per_page=3)
        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': courses,
            'hot_courses': hot_courses,
            'sort': sort,

        })


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        course_org = CourseOrg.objects.get(id=int(course.course_org_id))

        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
            if relate_courses[0].id == course.id:
                relate_courses = Course.objects.filter(tag=tag)[1:2]
        else:
            relate_courses = []

        course_has_fav = False
        org_has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                course_has_fav = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                org_has_fav = True

        return render(request, 'course-detail.html', {
            'course': course,
            'course_org': course_org,
            'relate_courses': relate_courses,
            'course_has_fav': course_has_fav,
            'org_has_fav': org_has_fav,
        })
