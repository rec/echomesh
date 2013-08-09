__all__ = ['Mod1', 'Mod2']

print('SUB!')

from echomesh.util.registry import Registry as _Registry
_Registry.module_registry(__name__)
