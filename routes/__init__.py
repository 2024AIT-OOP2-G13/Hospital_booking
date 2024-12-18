from .user import user_bp
from .appointment import appointment_bp
from .jibyou import jibyou_bp
from .medical_condition import medical_condition_bp
from .medical_condition_graph import medical_graph_bp

# Blueprintをリストとしてまとめる
blueprints = [
  user_bp,
  appointment_bp,
  jibyou_bp,
  medical_condition_bp,
  medical_graph_bp
]
