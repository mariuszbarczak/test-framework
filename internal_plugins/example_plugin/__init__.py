#
# Copyright(c) 2020 Intel Corporation
# SPDX-License-Identifier: BSD-3-Clause-Clear
#


class ExamplePlugin:
    def __init__(self, params):
        self.params = params
        print(f"Example plugin initialized with params {self.params}")

    def pre_setup(self):
        print("Example plugin pre setup")

    def post_setup(self):
        print("Example plugin post setup")

    def teardown(self):
        print("Example plugin teardown")


plugin_class = ExamplePlugin
