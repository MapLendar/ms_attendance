# api/resources.py
from tastypie.resources import ModelResource
from api.models import Attendance
from tastypie.authorization import Authorization
from tastypie import http
from django.db import IntegrityError

class AttendanceResource(ModelResource):
    class Meta:
        queryset = Attendance.objects.all()
        allowed_methods = ['get', 'post', 'put']
        resource_name = 'attendance'
        authorization = Authorization()
        filtering = {
            "user_id": 'exact',
            "event_id": 'exact',
            "status": 'exact',
        }

    def custom_deserialize(self, request):
        deserialized = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        return self.build_bundle(data=dict(deserialized), request=request)

    def post_list(self, request, **kwargs):
        bundle = custom_deserialize(self, request)
        if int(bundle.data['status']) < 0 or int(bundle.data['status']) > 2:
            return http.HttpNotAcceptable("Status values can only be 0: not specified, 1: not attending, 2: attending");

        try:
            updated_bundle = self.obj_create(bundle, request=request, **self.remove_api_resource_names(kwargs))
        except IntegrityError as e:
            if e.args[0] == 1062:
                return http.HttpConflict("An attendance event already exists for the specified user_id and event_id combination")
        location = self.get_resource_uri(updated_bundle)

        return http.HttpCreated("Attendance event succesfully created")

    def put_detail(self, request, **kwargs):
        bundle = custom_deserialize(self, request)
        if int(bundle.data['status']) < 0 or int(bundle.data['status']) > 2:
            return http.HttpNotAcceptable("Status values can only be 0: not specified, 1: not attending, 2: attending");
        if 'user_id' in bundle.data or 'event_id' in bundle.data:
            return http.HttpForbidden("Not allowed to edit user_id or event_id")

            return http.HttpAccepted("Attendance event succesfully edited")
