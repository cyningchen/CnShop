from django.apps import AppConfig


class UserOperationConfig(AppConfig):
    name = 'apps.user_operation'
    verbose_name = '操作管理'

    def ready(self):
        import apps.user_operation.signals