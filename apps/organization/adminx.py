# -*- coding: utf-8 -*-
__author__ = 'sssssjd'
__date__ = '2018/8/22 19:10'

import xadmin
from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']
    model_icon = 'fa fa-building'


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address',
                    'city', 'add_time']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums', 'address', 'city']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums', 'address',
                   'city__name', 'add_time']
    model_icon = 'fa fa-graduation-cap'
    relfield_style = 'fk_ajax'


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points',
                    'click_nums', 'fav_nums', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points',
                     'click_nums', 'fav_nums']
    list_filter = ['org__name', 'name', 'work_years', 'work_company', 'work_position', 'points',
                   'click_nums', 'fav_nums', 'add_time']
    model_icon = 'fa fa-user-secret'


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)

