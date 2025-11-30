from .models import AccessRule, UserRole, BusinessElement


def has_permission(user, element_code, permission_type):
    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    try:
        element = BusinessElement.objects.get(code=element_code)
        user_roles = UserRole.objects.filter(user=user).values_list('role_id', flat=True)

        access_rules = AccessRule.objects.filter(
            role_id__in=user_roles,
            element=element
        )

        for rule in access_rules:
            if getattr(rule, f'{permission_type}_permission', False):
                return True

        return False
    except BusinessElement.DoesNotExist:
        return False