import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/maria/Documentos/GitHub/IR2134/rmf_ws/install/rmf_demos_fleet_adapter'
