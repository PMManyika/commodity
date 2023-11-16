from django.urls import resolve, reverse

from commodity.views import list_commodities


def breadcrumbs(request):
    breadcrumbs = []

    # Get the current view function and its arguments
    resolver_match = resolve(request.path_info)
    view_name = resolver_match.url_name
    args = resolver_match.args

    # Iterate through the view arguments and construct breadcrumbs
    for i, arg in enumerate(args):
        breadcrumb = {
            "text": str(arg),  # Convert the argument to a string (customize as needed)
            "url": reverse(list_commodities, args=args[: i + 1]),
        }
        breadcrumbs.append(breadcrumb)

    return {"breadcrumbs": breadcrumbs}
