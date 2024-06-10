from __future__ import annotations

from vuepy.utils.common import Nil


class VueCompNamespace:
    def __init__(self, root, global_vars, local_vars=None):
        self.local_vars = local_vars or {}
        self.global_vars = global_vars
        self.root = root
        self.ns_list = [
            self.local_vars,
            self.global_vars,
        ]

    def to_py_eval_ns(self, tmp_vars=None):
        return {
            **self.global_vars,
            **self.local_vars,
            **(tmp_vars or {}),
        }

    @staticmethod
    def _getattr(obj, attr, default=Nil):
        if isinstance(obj, dict):
            return obj[attr] if default is Nil else obj.get(attr, default)
        else:
            return getattr(obj, attr) if default is Nil else getattr(obj, attr, default)

    @classmethod
    def get_by_attr_chain(cls, obj, attr_chain, default=Nil):
        for attr in attr_chain.split('.'):
            obj = cls._getattr(obj, attr, Nil)
            if obj is Nil:
                break
        else:
            return obj

        raise Exception(f"get attr {attr_chain} from ns failed")

    def get_obj_and_attr(self, attr_chain):
        obj_attr_tuple = attr_chain.rsplit('.', 1)
        for ns in self.ns_list:
            if not ns:
                continue

            if len(obj_attr_tuple) == 1:
                if attr_chain not in ns:
                    continue
                else:
                    return self.root, attr_chain

            obj_attr_chain, attr = obj_attr_tuple
            obj = self.get_by_attr_chain(ns, obj_attr_chain)
            if obj is not Nil:
                return obj, attr

        raise Exception(f"get attr {attr_chain} from ns failed")

    def getattr(self, attr_chain, default=Nil):
        return self.get_by_attr_chain(self.to_py_eval_ns(), attr_chain, default)
