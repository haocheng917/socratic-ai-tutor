from io import BytesIO

from PIL import Image, UnidentifiedImageError
from fastapi import APIRouter, HTTPException, UploadFile

from ..services.oss import StorageService

router = APIRouter()


@router.post('/upload')
async def upload_image(file: UploadFile):
    content = await file.read()

    try:
        img = Image.open(BytesIO(content))

        img_format = img.format

        img.verify()

        if not img_format:
            raise ValueError("未知图片格式")

        ext_map = {"JPEG": ".jpg", "PNG": ".png",
                   "WEBP": ".webp", "GIF": ".gif"}
        real_ext = ext_map.get(img_format, ".jpg")
    except (UnidentifiedImageError, ValueError):
        raise HTTPException(400, '不支持的图片格式')
    except Exception as e:
        raise HTTPException(400, f'图片解析失败: {str(e)}')

    img_key = StorageService.upload_image(content, real_ext)
    return {'key': img_key, 'url': StorageService.get_cached_url(img_key)}
