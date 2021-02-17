from rest_framework import renderers
from rest_framework.utils import json
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict


class JsonRendererNew(renderers.BaseRenderer):
    media_type = 'application/json'
    format = 'json'

    def render(self, data, media_type='application/json', renderer_context=None, message=None):
        stat = [200, 201, 202, 203, 204]
        response_dict = {
            'status': 1 if renderer_context['response'].status_code in stat else 0,
            'status_code': renderer_context['response'].status_code,
            'message': message,
        }
        if type(data) is ReturnList or ReturnDict:
            response_dict['data'] = data
        else:
            if type(data) is str:
                response_dict['data'] = data
            else:
                if data.get('count'):
                    response_dict['count'] = data['count']
                if data.get('next'):
                    response_dict['next'] = data['next']
                if data.get('previous'):
                    response_dict['previous'] = data['previous']
                if data.get('results'):
                    response_dict['data'] = data['results']

        return json.dumps(response_dict)
