import json
import os
import urllib.request

BASE_URL = "https://www.runninghub.cn/openapi/v2/"


def request(path, payload):
    key = os.environ.get("RUNNINGHUB_API_KEY", "").strip()
    if not key:
        raise ValueError("Set RUNNINGHUB_API_KEY before starting ComfyUI.")
    req = urllib.request.Request(
        BASE_URL + path,
        data=json.dumps(payload).encode(),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=90) as response:
        result = json.load(response)
    if result.get("errorMessage"):
        raise RuntimeError(result["errorMessage"])
    return result


class SeedanceSubmit:
    CATEGORY = "RunningHub/Seedance"
    FUNCTION = "submit"
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("task_id",)

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {
            "prompt": ("STRING", {"multiline": True}),
            "duration": ("INT", {"default": 5, "min": 4, "max": 15}),
            "confirm_paid_request": ("BOOLEAN", {"default": False}),
        }}

    def submit(self, prompt, duration, confirm_paid_request):
        if not confirm_paid_request:
            raise ValueError("Enable confirm_paid_request to submit a paid generation.")
        if not prompt.strip() or not 4 <= duration <= 15:
            raise ValueError("Provide a prompt and duration between 4 and 15 seconds.")
        result = request("rhart-video/sparkvideo-2.0/text-to-video", {
            "prompt": prompt, "duration": str(duration),
            "resolution": "720p", "ratio": "16:9",
        })
        task_id = result.get("taskId")
        if not task_id:
            raise RuntimeError("No taskId returned. Check RunningHub tasks before resubmitting.")
        return (str(task_id),)


class SeedanceResume:
    CATEGORY = "RunningHub/Seedance"
    FUNCTION = "query"
    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("status", "video_url", "result_json")
    OUTPUT_NODE = True

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"task_id": ("STRING", {"default": ""})}}

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("nan")

    def query(self, task_id):
        if not task_id.strip():
            raise ValueError("Enter an existing RunningHub task ID.")
        result = request("query", {"taskId": task_id.strip()})
        status = result.get("status", "UNKNOWN")
        if status == "FAILED":
            raise RuntimeError(result.get("errorMessage") or "RunningHub task failed.")
        outputs = result.get("results") or []
        url = outputs[0].get("url", "") if outputs else ""
        serialized = json.dumps(result, ensure_ascii=False, indent=2)
        return {"ui": {"text": [status, url, serialized]},
                "result": (status, url, serialized)}


NODE_CLASS_MAPPINGS = {
    "RHSeedanceSubmit": SeedanceSubmit,
    "RHSeedanceResume": SeedanceResume,
}
