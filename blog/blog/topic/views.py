from django.shortcuts import render
from django.http import JsonResponse
import json
from . import models
from common.login_check import login_check
import datetime
import html


# Create your views here.
def gettopics(request,username):
    topics = []

    # 博主自己访问自己的博客
    if username == request.user.username:
        topic_all = request.user.topic_set.all()
    else:
        topic_all = request.user.topic_set.filter()

    for topic in topic_all:
        topics.append({"id":topic.id,
                       "title": topic.title,
                       "category": topic.category,
                       "limit": topic.limit,
                       "introduce": topic.introduce,
                       "content": topic.content,
                       "created_time": topic.created_time.strftime('%Y-%m-%d %H:%M:%S'),
                       "modified_time": topic.modified_time.strftime('%Y-%m-%d %H:%M:%S'),
                       "author": request.user.nickname})
    return topics


@login_check("POST", "GET","DELETE")
def topics(request, username):
    if request.method == "GET":
        # http://127.0.0.1:5000/<username>/topics
        topics = gettopics(request,username)
        result = {"code": 200, "error": "", "data": {"topics": topics}}
        return JsonResponse(result)
    elif request.method == "POST":
        topic_str = request.body
        json_obj = json.loads(topic_str)
        content = json_obj.get("content")
        if not content:
            result = {"code": 301, "error": "内容不能为空"}
            return JsonResponse(result)

        content_text = json_obj.get("content_text")
        if not content_text:
            result = {"code": 302, "error": "内容不能为空"}
            return JsonResponse(result)

        introduce = content_text[:30]
        title = json_obj.get("title")
        if not title:
            result = {"code": 303, "error": "标题不能为空"}
            return JsonResponse(result)
        title = html.escape(title)

        limit = json_obj.get("limit")
        if limit not in ('public', 'private'):
            result = {"code": 304, "error": "文章权限不能为空"}
            return JsonResponse(result)

        category = json_obj.get("category")
        if category not in ('tec', 'no-tec'):
            result = {"code": 305, "error": "文章的分类不能为空"}
            return JsonResponse(result)

        if request.user.username != username:
            result = {"code": 306, "error": "数据异常"}
            return JsonResponse(result)

        models.Topic.objects.create(
            title=title,
            category=category,
            limit=limit,
            introduce=introduce,
            content=content,
            author=request.user
        )

    elif request.method == "DELETE":
        if username != request.user.username:
            result = {"code": 307, "error": "数据异常"}
            return JsonResponse(result)

        topic_id = request.GET.get("topic_id")
        try:
            topic = models.Topic.objects.get(id = topic_id)
            if topic.author.username != username:
                result = {"code": 309, "error": "数据异常"}
                return JsonResponse(result)
            topic.delete()
        except Exception as e:
            result = {"code": 308, "error": str(e)}
            return JsonResponse(result)
    else:
        result = {"code": 110, "error": "无效的请求"}
        return JsonResponse(result)

    result = {"code": 200, "error": ""}
    return JsonResponse(result)
