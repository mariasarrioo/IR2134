import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/maria/Documentos/GitHub/IR2134/rmf_ws/install/project_fleet_adapter'
