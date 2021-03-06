import os
from django.db import models
from core.models import PlCoreBase, Controller, Deployment
from core.models.plcorebase import StrippedCharField, ModelLink
from core.models.site import ControllerLinkManager, ControllerLinkDeletionManager

class DashboardView(PlCoreBase):
    name = StrippedCharField(max_length=200, unique=True, help_text="Name of the View")
    url = StrippedCharField(max_length=1024, help_text="URL of Dashboard")
    controllers = models.ManyToManyField(Controller, blank=True, related_name="dashboardviews", through='ControllerDashboardView')
    enabled = models.BooleanField(default=True)
    icon = models.CharField(max_length=200, default="default-icon.png", help_text="Icon for Dashboard")
    icon_active = models.CharField(max_length=200, default="default-icon-active.png", help_text="Icon for active Dashboard")
    deployments = models.ManyToManyField(Deployment, blank=True, null=True, related_name="dashboardviews", help_text="Deployments that should be included in this view")


    def __unicode__(self):  return u'%s' % (self.name)

class ControllerDashboardView(PlCoreBase):
    objects = ControllerLinkManager()
    deleted_objects = ControllerLinkDeletionManager()
    controller = models.ForeignKey(Controller, related_name='controllerdashboardviews')
    dashboardView = models.ForeignKey(DashboardView, related_name='controllerdashboardviews')
    enabled = models.BooleanField(default=True)
    url = StrippedCharField(max_length=1024, help_text="URL of Dashboard")
    xos_links=[ModelLink(Controller,via='controller'),ModelLink(DashboardView,via='dashboardview')]



