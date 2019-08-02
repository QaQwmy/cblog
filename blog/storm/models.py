from django.db import models
from django.conf import settings
from django.shortcuts import reverse


# Create your models here.


class BigCategory(models.Model):
    name = models.CharField(max_length=20, help_text='一级分类')
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=240, default=settings.SITE_DESCRIPTION,
                                   help_text='用来做SEO中的description，长度参考SEO标准')
    keywords = models.TextField('关键字', max_length=240, default=settings.SITE_KEYWORDS,
                                help_text='用来做SEO中keywords,长度参考SEO标准')

    class Meta:
        verbose_name = '一级标题'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=20, help_text='二级分类')
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=240, default=settings.SITE_DESCRIPTION,
                                   help_text='用来做SEO中的description，长度参考SEO标准')
    bigcategory = models.ForeignKey(BigCategory, verbose_name='一级标题')

    class Meta:
        verbose_name = '二级标题'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug, 'bigslug': self.bigcategory.slug})

    def get_article_list(self):
        return Article.objects.filter(category=self)


class Tag(models.Model):
    name = models.CharField(max_length=20, help_text='标签')
    slug = models.SlugField(unique=True)
    description = models.TextField(max_length=240, default=settings.SITE_DESCRIPTION,
                                   help_text='用来做SEO中的description，长度参考SEO标准')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:tag', kwargs={'tag': self.name})

    def get_article_list(self):
        """返回当前标签下所有发表的文章列表"""
        return Article.objects.filter(tags=self)


class Keyword(models.Model):
    name = models.CharField('文章关键词', max_length=20)

    class Meta:
        verbose_name = '关键词'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name


class Article(models.Model):
    IMG_LINK = ''
    title = models.CharField(max_length=150, verbose_name='文章标题')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='文章作者')
    summary = models.TextField(max_length=230, default='文章的简略描述、摘要')
    context = models.TextField(verbose_name='文章内容')
    img = models.CharField(max_length=255, default=IMG_LINK)
    pass
