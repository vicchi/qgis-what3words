# -*- coding: utf-8 -*-
#
# (c) 2016 Boundless, http://boundlessgeo.com
# This code is licensed under the GPL 2.0 license.
#
import os
import site

def classFactory(iface):
    from plugin import W3WTools
    return W3WTools(iface)
