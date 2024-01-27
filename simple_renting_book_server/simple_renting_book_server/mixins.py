from django.contrib.admin.views.main import ChangeList


# Admin
class CollapsibleInlineMixin:
    classes = ["collapse"]


class EagerLoadingChangeList(ChangeList):
    def get_queryset(self, changelist_request):
        queryset = super().get_queryset(changelist_request)
        queryset = self.model_admin.setup_eager_loading(queryset)
        return queryset


class EagerLoadingAdminChangeListMixin:
    """
    EagerLoadingAdminChangeListMixin
    ---
    Catching model queryset to display OneToOne, ManyToOne, ManyToMany related in list_display without several hit database
    ---
    """

    def setup_eager_loading(self, queryset):
        raise NotImplementedError(
            "{} is missing function setup_eager_loading.".format(
                self.__class__.__name__
            )
        )

    def get_changelist(self, request, **kwargs):
        return EagerLoadingChangeList
