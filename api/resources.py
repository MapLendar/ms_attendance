# api/resources.py
from tastypie.resources import ModelResource
from api.models import Attendance
from tastypie.authorization import Authorization
from django.db import IntegrityError
from django import http
import json

class AttendanceResource(ModelResource):
    class Meta:
        queryset = Attendance.objects.all()
        allowed_methods = ['get', 'post', 'put']
        always_return_data = True
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
        bundle = self.custom_deserialize(request)
        response = dict()
        if int(bundle.data['status']) < 0 or int(bundle.data['status']) > 2:
            response = {"code":406,"response":"Status values can only be 0: not specified, 1: not attending, 2: attending"}
            return http.HttpResponse(json.dumps(response), content_type='application/json', status=response["code"])

        updated_bundle = None
        location = None
        try:
            updated_bundle = self.obj_create(bundle, request=request, **self.remove_api_resource_names(kwargs))
            location = self.get_resource_uri(updated_bundle)
        except IntegrityError as e:
            if e.args[0] == 1062:
                response = {"code":409,"response":"An attendance event already exists for the specified user_id and event_id combination"}
                return http.HttpResponse(json.dumps(response), content_type='application/json', status=response["code"])
            elif e.args[0] == 1048:
                response = {"code":406,"response":"user_id, event_id or status cannot be null or blank, please verify"}
                return http.HttpResponse(json.dumps(response), content_type='application/json', status=response["code"])

        response = {"code":201,"response":"Attendance event succesfully created","location":location}
        return http.HttpResponse(json.dumps(response), content_type='application/json', status=response["code"])

    def put_detail(self, request, **kwargs):
        bundle = self.custom_deserialize(request)
        response = dict()
        if int(bundle.data['status']) < 0 or int(bundle.data['status']) > 2:
            response = {"code":406,"response":"Status values can only be 0: not specified, 1: not attending, 2: attending"}
            return http.HttpResponse(json.dumps(response), content_type='application/json', status=response["code"])
        if 'user_id' in bundle.data or 'event_id' in bundle.data:
            response = {"code":403,"response":"Not allowed to edit user_id or event_id"}
            return http.HttpResponse(json.dumps(response), content_type='application/json', status=response["code"])
        response = {"code":200,"response":"Attendance event succesfully edited"}
        return http.HttpResponse(json.dumps(response), content_type='application/json', status=response["code"])
