from datetime import datetime

from django.db import models

from organization.models import CourseOrg, Teacher
# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name=u'课程机构', null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u'课程名称')
    desc = models.CharField(max_length=300, verbose_name=u'课程描述')
    detail = models.TextField(verbose_name=u'课程详情')
    teacher = models.ForeignKey(Teacher, verbose_name=u'讲师', null=True, blank=True, on_delete=models.CASCADE)
    degree = models.CharField(choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), max_length=10, verbose_name=u'课程难度')
    learn_times = models.IntegerField(default=0, verbose_name=u'学习时长（分钟数）')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数')
    image = models.ImageField(upload_to='courses/%Y/%m', verbose_name=u'封面图', max_length=100)
    is_banner = models.BooleanField(default=False, verbose_name=u'是否是首页广告')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击量')
    category = models.CharField(default=u'后端开发', max_length=50, verbose_name=u'课程类别')
    tag = models.CharField(default='', max_length=50, verbose_name=u'课程标签')
    need_know = models.CharField(default=u'', max_length=500, verbose_name=u'课程须知')
    will_learn = models.CharField(default=u'', max_length=500, verbose_name=u'将会学到')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def get_lesson_nums(self):
        # 获取课程章节数
        return self.lesson_set.all().count()

    def get_lesson_students(self):
        # 获取课程学生
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        # 获取所有课程章节
        return self.lesson_set.all()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def get_lesson_video(self):
        return self.video_set.all()

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u'视频名称')
    times = models.IntegerField(default=0, verbose_name=u'视频时长（分钟数）')
    url = models.CharField(max_length=200, default='', verbose_name=u'视频链接')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u'资源名称')
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name=u'资源文件', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
