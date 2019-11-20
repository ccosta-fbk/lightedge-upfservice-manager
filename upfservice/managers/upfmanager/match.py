#!/usr/bin/env python3
#
# Copyright (c) 2019 Roberto Riggio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.

"""Match Class."""

import socket

from pymodm import MongoModel, fields
from upfservice.core.serialize import serializable_dict


@serializable_dict
class Match(MongoModel):
    """An user account on this controller."""

    index = fields.IntegerField(primary_key=True,
                                min_value=0,
                                required=True)
    desc = fields.CharField(required=True)
    ip_proto_num = fields.IntegerField(min_value=0,
                                       required=True)
    dst_ip = fields.CharField(required=True)
    dst_port = fields.IntegerField(min_value=0,
                                   max_value=65535,
                                   required=True)
    netmask = fields.IntegerField(min_value=0,
                                  max_value=32,
                                  required=True)
    new_dst_ip = fields.CharField(blank=True,
                                  required=True)
    new_dst_port = fields.IntegerField(min_value=0,
                                       max_value=65535,
                                       required=True)

    def from_dict(self, index, data):

        super().__init__()

        self.index = index
        self.desc = data["desc"]
        self.ip_proto_num = int(data["ip_proto_num"])
        self.dst_port = int(data["dst_port"])
        self.netmask = int(data["netmask"])
        self.new_dst_port = int(data["new_dst_port"])

        # return an ip address for both ip and hostname
        try:
            self.dst_ip = socket.gethostbyname(data["dst_ip"])
            if data["new_dst_ip"]:
                self.new_dst_ip = socket.gethostbyname(data["new_dst_ip"])
            else:
                self.new_dst_ip = None
        except Exception as ex:
            raise KeyError(ex)

    def to_dict(self):
        """Return JSON-serializable representation of the object."""

        return {
            "index": self.index,
            "desc": self.desc,
            "ip_proto_num": self.ip_proto_num,
            "dst_ip": self.dst_ip,
            "dst_port": self.dst_port,
            "netmask": self.netmask,
            "new_dst_ip": self.new_dst_ip,
            "new_dst_port": self.new_dst_port,
        }

    def to_str(self):
        """Return an ASCII representation of the object."""

        out = "%s/%u (%u): -> %s/%u" % (self.dst_port, self.netmask,
                                        self.ip_proto_num, self.new_dst_ip,
                                        self.new_dst_port)

        return out

    def __str__(self):
        return self.to_str()

    def __hash__(self):
        return hash(self.to_str())

    def __eq__(self, other):
        if isinstance(other, Match):
            return self.to_str() == other.to_str()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.__class__.__name__ + "('" + self.to_str() + "')"
