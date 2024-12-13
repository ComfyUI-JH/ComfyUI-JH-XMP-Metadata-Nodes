# The following block of code is copyright pythongosssss and licensed
# under the MIT License.
# https://github.com/pythongosssss/ComfyUI-Custom-Scripts

class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False
