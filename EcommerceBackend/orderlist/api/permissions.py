
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow the user who created the review to modify it.
    """

    def has_permission(self, request, view):
        """
        Check if the requesting user is authenticated.
        """
        # print("hello")
        print(request.user)
        # print(obj)
        if request.user.is_authenticated:
            return True

        else:
            raise PermissionDenied(
                "You must be authenticated to access this resource.")

    # def has_object_permission(self, request, view, obj):
    #     """
    #     Check if the requesting user is the owner of the review.
    #     """
    #     # print(obj.user == request.user)

    #     # print(obj)
    #     # print(self)
    #     if obj.user == request.user:
    #         print("sddsds")
    #         return True
    #     else:
    #         raise PermissionDenied("You are not the owner of this OrderList.")
