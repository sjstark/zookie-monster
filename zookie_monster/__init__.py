"""Top-level package for Zookie Monster"""
# zookie_monster/__init__.py

__app_name__ = "Zookie Monster"
__version__ = "0.1.0"

(
	SUCCESS,
	DIR_ERROR,
	FILE_ERROR,
	JSON_ERROR
) = range(4)

ERRORS = {
	DIR_ERROR: "config directory error",
	FILE_ERROR: "config file error",

}
