#
# Copyright(c) 2020 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause-Clear
#

import pytest
import sys
import importlib


class PluginManager:
    def __init__(self, item, config):
        if 'plugins_dir' in config:
            sys.path.append(config['plugins_dir'])
        self.plugins = {}

        self.req_plugins = config.get('req_plugins', {})
        self.opt_plugins = config.get('opt_plugins', {})

        self.req_plugins.update(dict(map(lambda mark: (mark.args[0], mark.kwargs),
                                item.iter_markers(name="require_plugin"))))

        req_plugin_mod = {}
        opt_plugin_mod = {}

        for name in self.req_plugins:
            try:
                req_plugin_mod[name] = self.__import_plugin(name)
            except ModuleNotFoundError:
                pytest.skip("Unable to find requested plugin!")

        for name in self.opt_plugins:
            try:
                opt_plugin_mod[name] = self.__import_plugin(name)
            except ModuleNotFoundError:
                continue

        for name, mod in req_plugin_mod.items():
            try:
                self.plugins[name] = mod.plugin_class(self.req_plugins[name])
            except Exception:
                pytest.skip(f"Unable to initialize plugin '{name}'")

        for name, mod in opt_plugin_mod.items():
            try:
                self.plugins[name] = mod.plugin_class(self.opt_plugins[name])
            except Exception:
                continue

    def __import_plugin(self, name):
        try:
            return importlib.import_module(f"internal_plugins.{name}")
        except ModuleNotFoundError:
            pass
        return importlib.import_module(f"external_plugins.{name}")

    def hook_pre_setup(self):
        for plugin in self.plugins.values():
            plugin.pre_setup()

    def hook_post_setup(self):
        for plugin in self.plugins.values():
            plugin.post_setup()

    def hook_teardown(self):
        for plugin in self.plugins.values():
            plugin.teardown()

    def get_plugin(self, name):
        if name not in self.plugins:
            raise KeyError("Requested plugin does not exist")
        return self.plugins[name]
