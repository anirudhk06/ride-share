from django.http import HttpRequest


def get_client_ip(request: HttpRequest) -> str:
    x_forworded_for: str | None = request.META.get("HTTP_X_FORWARDED_FOR")

    if x_forworded_for:
        ip = x_forworded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")

    return ip
