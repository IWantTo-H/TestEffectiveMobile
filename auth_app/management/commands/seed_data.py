from django.core.management.base import BaseCommand
from auth_app.models import User, Role, BusinessElement, AccessRule, UserRole


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **options):
        admin_role, _ = Role.objects.get_or_create(name='admin', defaults={'description': 'Администратор системы'})
        manager_role, _ = Role.objects.get_or_create(name='manager', defaults={'description': 'Менеджер'})
        user_role, _ = Role.objects.get_or_create(name='user', defaults={'description': 'Обычный пользователь'})

        # бизнес-элементы
        products_element, _ = BusinessElement.objects.get_or_create(
            name='Продукты',
            code='products',
            defaults={'description': 'Управление продуктами'}
        )
        orders_element, _ = BusinessElement.objects.get_or_create(
            name='Заказы',
            code='orders',
            defaults={'description': 'Управление заказами'}
        )

        # правила доступа для админа
        AccessRule.objects.get_or_create(
            role=admin_role,
            element=products_element,
            defaults={
                'read_permission': True,
                'create_permission': True,
                'update_permission': True,
                'delete_permission': True,
                'read_all_permission': True,
                'update_all_permission': True,
                'delete_all_permission': True,
            }
        )

        AccessRule.objects.get_or_create(
            role=admin_role,
            element=orders_element,
            defaults={
                'read_permission': True,
                'create_permission': True,
                'update_permission': True,
                'delete_permission': True,
                'read_all_permission': True,
                'update_all_permission': True,
                'delete_all_permission': True,
            }
        )

        # правила доступа для менеджера
        AccessRule.objects.get_or_create(
            role=manager_role,
            element=products_element,
            defaults={
                'read_permission': True,
                'create_permission': True,
                'update_permission': True,
                'delete_permission': False,
                'read_all_permission': True,
                'update_all_permission': True,
                'delete_all_permission': False,
            }
        )

        AccessRule.objects.get_or_create(
            role=manager_role,
            element=orders_element,
            defaults={
                'read_permission': True,
                'create_permission': True,
                'update_permission': True,
                'delete_permission': False,
                'read_all_permission': True,
                'update_all_permission': True,
                'delete_all_permission': False,
            }
        )

        # правила доступа для пользователя
        AccessRule.objects.get_or_create(
            role=user_role,
            element=products_element,
            defaults={
                'read_permission': True,
                'create_permission': False,
                'update_permission': False,
                'delete_permission': False,
                'read_all_permission': False,
                'update_all_permission': False,
                'delete_all_permission': False,
            }
        )

        AccessRule.objects.get_or_create(
            role=user_role,
            element=orders_element,
            defaults={
                'read_permission': True,
                'create_permission': True,
                'update_permission': True,
                'delete_permission': False,
                'read_all_permission': False,
                'update_all_permission': False,
                'delete_all_permission': False,
            }
        )

        admin_user, created = User.objects.get_or_create(
            email='admin@example.com',
            defaults={
                'first_name': 'Админ',
                'last_name': 'Системный',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            UserRole.objects.create(user=admin_user, role=admin_role)

        manager_user, created = User.objects.get_or_create(
            email='manager@example.com',
            defaults={
                'first_name': 'Менеджер',
                'last_name': 'Тестовый'
            }
        )
        if created:
            manager_user.set_password('manager123')
            manager_user.save()
            UserRole.objects.create(user=manager_user, role=manager_role)

        regular_user, created = User.objects.get_or_create(
            email='user@example.com',
            defaults={
                'first_name': 'Пользователь',
                'last_name': 'Обычный'
            }
        )
        if created:
            regular_user.set_password('user123')
            regular_user.save()
            UserRole.objects.create(user=regular_user, role=user_role)

        self.stdout.write(
            self.style.SUCCESS('Данные успешно добавлены!\n\n'
                               'Пользователи:\n'
                               'admin@example.com / admin123 (администратор)\n'
                               'manager@example.com / manager123 (менеджер)\n'
                               'user@example.com / user123 (обычный пользователь)')
        )