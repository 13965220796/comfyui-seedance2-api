# ComfyUI 项目调研
2026-11-19 查阅的榜单数据更新于 2026-11-18，星标数量为近似值。
| 项目 | Stars | 方向 |
|---|---:|---|
| ComfyUI | 147.4k | 节点式生成平台 |
| Pixelle-Video | 30.2k | 自动短视频制作 |
| ComfyUI-Manager | 16.9k | 节点安装与管理 |
| ComfyUI-Workflows-ZHO | 8.0k | 可复用工作流 |
| ComfyUI-WanVideoWrapper | 6.8k | 视频模型节点 |

来源 https://github.com/liusida/top-100-comfyui
据此选择视频节点方向，参考 VideoHelperSuite 的模块化工具思路及 WanVideoWrapper 的视频模型接入方式。
本项目实现云端提交和任务查询两个独立节点，支持跨工作流用任务 ID 恢复查询，降低因等待超时而重复提交的机会。代码为独立实现。
