from django import template

register = template.Library()


@register.simple_tag
def active_menu(request, url_name: str, class_name: str = "active"):
    app_name = request.resolver_match.app_name
    if app_name is None:
        url_resolve_name = request.resolver_match.app_name + ":" + request.resolver_match.url_name
    else:
        url_resolve_name = request.resolver_match.url_name
    if url_resolve_name in url_name:
        return class_name
    return ""


@register.simple_tag
def shared(request):
    menu = [
        {
            'name': 'Dashboard',
            'icon': 'fa fa-dashboard',
            'url': 'dashboard',
            'active': False
        },
        {
            'name': 'Users',
            'icon': 'fa fa-users',
            'url': 'users',
            'active': False
        },
        {
            'name': 'Roles',
            'icon': 'fa fa-user-secret',
            'url': 'roles',
            'active': False
        },
    ]

    for item in menu:
        if request.path.startswith('/' + item['url']):
            item['active'] = True

    return menu
