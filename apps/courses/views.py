# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q

from pure_pagination import Paginator, PageNotAnInteger

from .models import Course, CourseResource
from organization.models import CourseOrg
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin

# Create your views here.


class CourseListView(View):
    def get(self, request):
        # 全部
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = all_courses.order_by('-click_nums')[:3]

        # 课程搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords) | Q(desc__contains=search_keywords)
                                             | Q(detail__icontains=search_keywords))

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


class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程ID
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取该用户学过的其他课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        # 课程资源
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {
            'course': course,
            'course_resources': all_resources,
            'relate_courses': relate_courses,
        })


class CourseCommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        course_comments = CourseComments.objects.filter(course=course)
        return render(request, 'course-comment.html', {
            'course': course,
            'course_resources': all_resources,
            'course_comments': course_comments,
        })


class AddCommentView(View):
    def post(self, request):
        # 判断用户是否登录
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"发布成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"发布失败"}', content_type='application/json')
