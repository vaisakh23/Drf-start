from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    '''
    allow only owner of post to edit it.
    '''
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.owner
