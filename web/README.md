---
# 详细文档见https://modelscope.cn/docs/%E5%88%9B%E7%A9%BA%E9%97%B4%E5%8D%A1%E7%89%87
domain: #领域：cv/nlp/audio/multi-modal/AutoML
# - cv
tags: #自定义标签
-
datasets: #关联数据集
  evaluation:
  #- iic/ICDAR13_HCTR_Dataset
  test:
  #- iic/MTWI
  train:
  #- iic/SIBR
models: #关联模型
#- iic/ofa_ocr-recognition_general_base_zh

## 启动文件(若SDK为Gradio/Streamlit，默认为app.py, 若为Static HTML, 默认为index.html)
# deployspec:
#   entry_file: app.py
license: Apache License 2.0
---
#### Clone with HTTP
```bash
 git clone https://www.modelscope.cn/studios/Kumono/materials-candidate-triage.git
```

# Materials Candidate Triage

纯前端、无上传的材料组成证据工具。支持括号、非整数化学计量和水合物，输出质量/原子分数、组成熵、供应风险与安全复核标志，并按电池、催化、低供应风险三种透明目标排序。所有分数均为 `composition-only` 初筛，不代表真实性能。
