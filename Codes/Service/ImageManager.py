import weakref
import os
from Codes.config import AppConfig
from PySide6.QtGui import QPixmap


class ImageManager:
    """
        Efficient image memory management through caching
    """
    _cache = weakref.WeakValueDictionary()

    @classmethod
    def get_image(cls, category, data_key):
        """
            Get Image from ImageManager Cache
        """

        if isinstance(data_key, list):
            data_key = tuple(data_key)

        cache_key = (category, data_key)
        path = AppConfig.get_main_image(category, data_key)
        
        # print(cache_key)

        if cache_key not in cls._cache:
            ### Caching
            pixmap = QPixmap(path)

            if pixmap.isNull():
                return ImageManager.get_image('UI', 'NoImage')

            cls._cache[cache_key] = pixmap
            # print(f"Log: Loaded {category} / {data_key} from disk")
        
        return cls._cache[cache_key]
    
    @classmethod
    def update_image(cls, category, data_key):
        """
            Update Image to ImageManager Cache
        """

        if isinstance(data_key, list):
            data_key = tuple(data_key)

        cache_key = (category, data_key)
        path = AppConfig.get_main_image(category, data_key)

        pixmap = QPixmap(path)
        cls._cache[cache_key] = pixmap
        print(f"Log: Updated {category} / {data_key}")