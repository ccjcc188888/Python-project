r"""百度 OCR 客户端

依赖: pip install python-dotenv requests

用法:
    from src.ocr_client import OCRClient
    ocr = OCRClient()
    text = ocr.recognize("错题图片.png")
    print(text)
"""

import base64
import requests
import os
from dotenv import load_dotenv

load_dotenv()


class OCRClient:
    """百度通用文字识别（标准版）"""

    TOKEN_URL = "https://aip.baidubce.com/oauth/2.0/token"
    OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"

    def __init__(self):
        self.api_key = os.getenv("BAIDU_OCR_API_KEY")
        self.secret_key = os.getenv("BAIDU_OCR_SECRET_KEY")
        self._token = None

    def _get_token(self):
        if self._token:
            return self._token
        resp = requests.post(
            self.TOKEN_URL,
            params={
                "grant_type": "client_credentials",
                "client_id": self.api_key,
                "client_secret": self.secret_key,
            },
        ).json()
        self._token = resp["access_token"]
        return self._token

    def recognize(self, image_path=None, image_bytes=None, image_url=None):
        """识别图片中的文字，返回纯文本"""
        token = self._get_token()

        if image_path:
            with open(image_path, "rb") as f:
                img_data = base64.b64encode(f.read())
            params = {"image": img_data}
        elif image_bytes:
            params = {"image": base64.b64encode(image_bytes)}
        elif image_url:
            params = {"url": image_url}
        else:
            raise ValueError("请提供 image_path / image_bytes / image_url 其中之一")

        resp = requests.post(
            self.OCR_URL + "?access_token=" + token,
            data=params,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        ).json()

        if "error_code" in resp:
            raise RuntimeError(f"OCR 错误: {resp['error_msg']}")

        lines = [item["words"] for item in resp.get("words_result", [])]
        return "\n".join(lines)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("用法: python src/ocr_client.py 图片路径")
        sys.exit(1)
    ocr = OCRClient()
    result = ocr.recognize(sys.argv[1])
    print(result)
