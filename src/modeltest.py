cat > ~/modeltest.py << 'EOF'
import torch
torch.backends.mkldnn.enabled = False
import numpy as np
from ultralytics import YOLO

m = YOLO('best.pt')
m(np.zeros((720, 1280, 3), dtype='uint8'))
print('ok')
EOF