from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import serializers
from rest_framework import generics
from rest_framework.views import APIView
from core.models import *
from django.forms import widgets
from django.core.exceptions import PermissionDenied
from xos.exceptions import XOSNotFound
from api.xosapi_helpers import PlusModelSerializer, XOSViewSet, ReadOnlyField
from django.db.models import Q

class PortForwarding(Port):
    class Meta:
        proxy = True
        app_label = "core"

    def __init__(self, *args, **kwargs):
        super(PortForwarding, self).__init__(*args, **kwargs)

class PortForwardingSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    ip = serializers.CharField(read_only=True)
    ports = serializers.CharField(read_only=True, source="network.ports")
    hostname = serializers.CharField(read_only=True, source="instance.node.name")

    class Meta:
        model = PortForwarding
        fields = ('id', 'ip', 'ports', 'hostname')

class PortForwardingViewSet(XOSViewSet):
    base_name = "list"
    method_name = "portforwarding"
    method_kind = "viewset"
    serializer_class = PortForwardingSerializer

    def get_queryset(self):
        queryset = queryset=Port.objects.exclude(Q(network__isnull=True) |
                                                 Q(instance__isnull=True) |
                                                 Q(instance__node__isnull=True) |
                                                 Q(network__ports__exact='') |
                                                 Q(ip__isnull=True) | Q(ip__exact=''))

        node_name = self.request.query_params.get('node_name', None)
        if node_name is not None:
            queryset = queryset.filter(instance__node__name = node_name)

        return queryset


