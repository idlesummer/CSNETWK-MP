def import_file(module_name, path):
    # From: https://stackoverflow.com/questions/27381264/python-3-4-how-to-import-a-module-given-the-full-path
    
    """Import a python module from a path. 3.4+ only.

    Does not call sys.modules[full_name] = path
    """
    from importlib import util

    spec = util.spec_from_file_location(module_name, path)
    module = util.module_from_spec(spec)

    spec.loader.exec_module(module)
    return module
