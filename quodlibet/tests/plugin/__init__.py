# -*- coding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation

import os

import quodlibet
from quodlibet import util
from quodlibet.util.modulescanner import ModuleScanner
from quodlibet.plugins import list_plugins, Plugin, PluginImportException
from quodlibet.compat import iteritems

from tests import TestCase, init_fake_app, destroy_fake_app


init_fake_app, destroy_fake_app

# Nasty hack to allow importing of plugins...
PLUGIN_DIRS = []

root = os.path.join(quodlibet.__path__[0], "ext")
for entry in os.listdir(root):
    if entry.startswith("_"):
        continue
    path = os.path.join(root, entry)
    if not os.path.isdir(path):
        continue
    PLUGIN_DIRS.append(path)

PLUGIN_DIRS.append(os.path.join(util.get_module_dir(), "test_plugins"))

ms = ModuleScanner(PLUGIN_DIRS)

ms.rescan()

# make sure plugins only raise expected errors
for name, err in ms.failures.items():
    exc = err.exception
    assert issubclass(type(exc), (PluginImportException, ImportError)),\
        "%s shouldn't have raised a %s, but it did (%r)."\
        % (name, type(exc), exc)

plugins = {}
modules = {}
for name, module in iteritems(ms.modules):
    for plugin in list_plugins(module.module):
        plugins[plugin.PLUGIN_ID] = Plugin(plugin)
        modules[plugin.PLUGIN_ID] = module.module


class PluginTestCase(TestCase):
    """Base class for all plugin tests"""

    plugins = plugins
    modules = modules
