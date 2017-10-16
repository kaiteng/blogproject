from django.db import models
from django.contrib.auth.models import User
from django.utils.six import python_2_unicode_compatible
from django.urls import reverse

# Create your models here.
@python_2_unicode_compatible
class Category(models.Model):
    '''
    Django 要求模型必须继承 models.Model 类
    Category 只需要一个简单的分类名name就可以
    CharField 指定了分类名 name 的数据类型，CharField是字符型
    charField 的 max_length 参数指定其最大长度
    '''
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Tag(models.Model):
    '''
    标签tag 和 Category一样
    '''
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Post(models.Model):
    '''
    文章数据表，结构复杂一点，主要是涉及的字段比较多
    '''
    #文章标题
    title = models.CharField(max_length=70)
    #文章正文，用 TextField
    body = models.TextField()
    #创建时间和修改时间，用DATATimeField
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()

    #文章摘要，指定 CharField的 blank为 True ，可以允许空值了
    excerpt = models.CharField(max_length=100, blank=True)

    #分类与标签
    #把文章对应的数据表和分类，标签对应的数据表关联起来
    #一片文章只能对应一个分类，一个分类下可以有多篇文章，所以用外键，一对多
    #对于标签，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以用多对多的关系
    #定义的文章也可以没有标签，所以指定了  blank为空
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    #文章作者，这里 User 是从 django.contrib.auth.models导入的
    #django.contrib.auth 是 Django 内置应用， 专门用于处理网站的用户注册，登录，等路程，User是 dajngo为我们写好的用户模型
    #通过外键把文章和User关联了 起来
    #一个作者可以写多篇文章，所以 一对多的关系
    author = models.ForeignKey(User)

    def __str__(self):
        return self.title

    #自定义 get_absolute_url 方法
    #从 django.urls 中导入 reverse 函数
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-created_time']