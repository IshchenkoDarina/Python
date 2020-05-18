from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView, DetailView, CreateView

from core.models import Post, Tag, PostLike, PostTime


class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        sort_param = self.request.GET.get('sort', '')

        if sort_param == 'date-asc':
            order_by_field = 'core_post.date'
            order_by_order = 'asc'
        elif sort_param == 'date-desc':
            order_by_field = 'core_post.date'
            order_by_order = 'desc'
        elif sort_param == 'like-desc':
            order_by_field = 'post_likes.like_count'
            order_by_order = 'desc'
        else:
            sort_param = 'date-desc'
            order_by_field = 'core_post.date'
            order_by_order = 'desc'

        posts = Post.objects.raw(f"""
        select core_post.*, ifnull(post_likes.like_count, 0) as like_count
        from core_post
        left join (select post_id, count(id) as like_count
        from core_postlike
        group by post_id) as post_likes on post_likes.post_id = core_post.id
        order by {order_by_field} {order_by_order}
         """)

        return {
            'sort': sort_param,
            'posts': posts
        }


class PostDetail(DetailView):
    template_name = 'post_detail.html'
    model = Post

    def get_context_data(self, **kwargs):
        post_id = self.kwargs.get('pk', '')
        likes_count = len(PostLike.objects.filter(post_id=post_id))
        likes_count_by_user = len(PostLike.objects.filter(post_id=post_id, author_id=self.request.user.id))
        post = Post.objects.get(id=post_id)
        spend_time = PostTime.objects.filter(post_id=post_id).aggregate(Avg('spend_time')).get('spend_time__avg', 0)
        return {
            'post': post,
            'likes_count': likes_count,
            'is_already_liked': likes_count_by_user != 0,
            'spend_time': 0 if spend_time is None else round(spend_time)
        }


class PostDetailLike(CreateView):
    model = Post
    fields = ()
    template_name = 'post_detail.html'

    def form_valid(self, form):
        post_id = self.kwargs.get('pk', '')
        user = self.request.user
        likes_count_by_user = len(PostLike.objects.filter(post_id=post_id, author_id=user.id))

        if likes_count_by_user == 0:
            post_like = PostLike()
            post_like.author = user
            post_like.post = Post.objects.get(id=post_id)
            post_like.save()

        return redirect(f'/post/{post_id}')


class PostDetailUnlike(CreateView):
    model = Post
    fields = ()
    template_name = 'post_detail.html'

    def form_valid(self, form):
        post_id = self.kwargs.get('pk', '')
        PostLike.objects.filter(post_id=post_id, author_id=self.request.user.id).delete()
        return redirect(f'/post/{post_id}')


class CreatePostViews(CreateView):
    template_name = 'create_post_view.html'
    model = Post
    fields = ('title', 'text', 'tags')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()

        for tag in form.cleaned_data['tags']:
            post.tags.add(tag)

        post.save()
        return redirect('/')


class TagPostViews(DetailView):
    template_name = 'tag_posts.html'
    model = Tag

    def get_context_data(self, **kwargs):
        tag_id = self.kwargs.get('pk', '')
        posts = Tag.objects.get(id=tag_id).post_set.all().order_by('-date')[:20]

        return {
            'posts': posts
        }


class PostTimeCreate(CreateView):
    model = PostTime
    fields = ('post', 'spend_time')

    def form_valid(self, form):
        spend_time = form.cleaned_data.get('spend_time', 0)

        if spend_time > 0:
            form.save(commit=True)

        return HttpResponse('')


class ContactView(TemplateView):
    template_name = 'contacts.html'

