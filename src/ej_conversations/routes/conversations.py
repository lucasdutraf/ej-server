from logging import getLogger

from boogie import rules
from django.http import HttpResponseServerError, Http404
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from hyperpython import a

from ej_conversations.models import Vote
from . import urlpatterns, conversation_url
from ..forms import CommentForm
from ..models import Conversation, Comment
from ..rules import max_comments_per_conversation

log = getLogger('ej')


@urlpatterns.route('', name='list')
def conversation_list(request):
    show_welcome_window = 'show_welcome_window' in request.COOKIES.keys()
    ctx = {
        'conversations': Conversation.objects.filter(is_promoted=True, is_hidden=False),
        'can_add_conversation': request.user.has_perm('ej.can_add_promoted_conversation'),
        'create_url': reverse('conversation:create'),
        'topic': _('A space for adolescents to discuss actions that promote, guarantee and defend their rights'),
        'title': _('Public conversations'),
        'subtitle': _('Participate of conversations and give your opinion with comments and votes!'),
        'description': _('Participate of conversations and give your opinion with comments and votes!'),
        'show_welcome_window': show_welcome_window,
    }
    response = render(request, 'ej_conversations/list.jinja2', ctx)
    if (show_welcome_window):
        response.delete_cookie('show_welcome_window')
    return response


@urlpatterns.route(conversation_url)
def detail(request, conversation):
    if not conversation.is_promoted:
        raise Http404
    return get_conversation_detail_context(request, conversation)


#
# Auxiliary and re-usable functions
#
def get_conversation_detail_context(request, conversation):
    """
    Common implementation used by both /conversations/<slug> and inside boards
    in /<board>/conversations/<slug>/
    """
    user = request.user
    is_favorite = user.is_authenticated and conversation.followers.filter(user=user).exists()
    comment_form = CommentForm(None, conversation=conversation)
    voted = False
    if user.is_authenticated:
        voted = Vote.objects.filter(author=user).exists()

    # User is voting in the current comment. We still need to choose a random
    # comment to display next.
    if request.POST.get('action') == 'vote':
        vote = request.POST['vote']
        comment_id = request.POST['comment_id']
        Comment.objects.get(id=comment_id).vote(user, vote)
        log.info(f'user {user.id} voted {vote} on comment {comment_id}')

    # User is posting a new comment. We need to validate the form and try to
    # keep the same comment that was displayed before.
    elif request.POST.get('action') == 'comment':
        comment_form = CommentForm(request.POST, conversation=conversation)
        if comment_form.is_valid():
            new_comment = comment_form.cleaned_data['content']
            new_comment = conversation.create_comment(user, new_comment)
            comment_form = CommentForm(conversation=conversation)
            log.info(f'user {user.id} posted comment {new_comment.id} on {conversation.id}')

    # User toggled the favorite status of conversation.
    elif request.POST.get('action') == 'favorite':
        conversation.toggle_favorite(user)
        log.info(f'user {user.id} toggled favorite status of conversation {conversation.id}')

    # User to pass modalities
    elif request.POST.get('modalities') == 'pass':
        voted = True

    # User is probably trying to something nasty ;)
    elif request.method == 'POST':
        log.warning(f'user {user.id} se nt invalid POST request: {request.POST}')
        return HttpResponseServerError('invalid action')

    n_comments_under_moderation = rules.compute('ej_conversations.comments_under_moderation', conversation, user)
    comments_made = rules.compute('ej_conversations.comments_made', conversation, user)

    return {
        # Objects
        'conversation': conversation,
        'comment': conversation.next_comment(user, None),
        'login_link': login_link(_('login'), conversation),
        'comment_form': comment_form,

        # Permissions and predicates
        'is_favorite': is_favorite,
        'can_comment': user.is_authenticated,
        'can_edit': user.has_perm('ej.can_edit_conversation', conversation),
        'cannot_comment_reason': '',
        'comments_under_moderation': n_comments_under_moderation,
        'comments_made': comments_made,
        'max_comments': max_comments_per_conversation(),
        'user_is_owner': conversation.author == user,
        'voted': voted,
    }


def login_link(content, obj):
    path = obj.get_absolute_url()
    return a(content, href=reverse('auth:login') + f'?next={path}')
