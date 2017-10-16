from django.shortcuts import render, get_object_or_404,redirect
from blog.models import Post
from .models import Comment
from  .forms import CommentForm
# Create your views here.
'''
'''

def post_comment(request, post_pk):
    #先获取被评论的文章，后面需要把评论和被评论的文章关联起来
    #函数get_object_or_404 ，当文存在时，获取（Post），否则返回404给用户
    post = get_object_or_404(Post, pk = post_pk)

    #HTTP 请求有get和post 两种， 一般通过表单提交的数据都是  post 请求
    #当请求为 Post 时，才需要处理表单数据

    if request.method == 'POST':
        #用户提交的数据存在在request.POST中，这是一个字典对象
        #我们利用这些数据构造了  CommentForm的实例， 这样django的表单就生成了
        form = CommentForm(request.POST)

        #当调用form.is_valid() 方法时， django 自动帮我们检测表单的数据是否符合格式要求
        if form.is_valid():
            #检查数据是合法的，调用表单的save方法保存数据到数据库
            #commit =False  利用表单数据生成 Comment 模型类的实例，但还不保存进评论数
            comment = form.save(commit=False)

            #将评论数和文章关联起来
            comment.post = post

            #将评论数据 保存进数据库
            comment.save()

            return redirect(post)
    else:
        '''
        检查数据不合法，重新渲染详情页面，并且渲染表单的错误
        传3个模板变量给 detail.html
        文章（Post），评论列表和表单 Form
        这里用到  post.comment_set.all() 获取post下的全部评论
        因为 Post 和 Comment 是 ForeignKey 关联的
        可使用  post.comment_set.all() 反向查询全部评论
        '''

        comment_list = post.comment_set.all()
        context = {'post':post,
                   'form':form,
                   'comment_list':comment_list}
        return render(request, 'blog/detail.html',context=context)
   #不是post请求，用户没有提交数据，重定向到文章详情页
    return redirect(post)
