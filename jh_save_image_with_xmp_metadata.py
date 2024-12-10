from enum import Enum
import os
import re

import json
from lxml import etree
import numpy as np
from PIL import Image, ExifTags
from PIL.PngImagePlugin import PngInfo

import folder_paths


class JHSupportedImageTypes(Enum):
    PNG = "PNG"
    WEBP = "WebP"


class JHSaveImageWithXMPMetadata:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 0

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE", {"tooltip": "The images to save."}),
                "filename_prefix": ("STRING", {"default": "ComfyUI", "tooltip": "The prefix for the file to save. This may include formatting information such as %date:yyyy-MM-dd% or %Empty Latent Image.width% to include values from nodes."}),
                "image_type": ([x.value for x in JHSupportedImageTypes], {"default": JHSupportedImageTypes.PNG.value}),
                "embed_workflow": ("BOOLEAN", {"default": True}),
            },
            "optional": {
                "description": ("STRING",),
                "subject": ("STRING",),
                "title": ("STRING",),
                "instructions": ("STRING",),
                "make": ("STRING", {"default": "ComfyUI"}),
                "model": ("STRING",),
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "save_images"
    CATEGORY = "JHXMP"
    OUTPUT_NODE = True

    def string_to_list(self, string):
        return re.split(r"[;,]\s*", string)

    def generate_xmpmeta(
            self,
            description=None,
            subject=None,
            title=None,
            instructions=None,
            make=None,
            model=None,
            ):
 
        #
        # https://developer.adobe.com/xmp/docs/XMPSpecifications/
        #

        namespaces = {
            "x": "adobe:ns:meta/",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "dc": "http://purl.org/dc/elements/1.1/",
            "xml": "http://www.w3.org/XML/1998/namespace",
            "xmp": "http://ns.adobe.com/xap/1.0/",
            "photoshop": "http://ns.adobe.com/photoshop/1.0/",
            "exif": "http://ns.adobe.com/exif/1.0/",
            "tiff": "http://ns.adobe.com/tiff/1.0/",
        }

        # Create the root x:xmpmeta element
        xmpmeta = etree.Element("{adobe:ns:meta/}xmpmeta", nsmap=namespaces)

        # Set the x:xmptk attribute using the namespace URI
        xmpmeta.set("{adobe:ns:meta/}xmptk", "Adobe XMP Core 6.0-c002 79.164861, 2016/09/14-01:09:01")

        # Create the rdf:RDF container
        rdf = etree.SubElement(xmpmeta, "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}RDF")

        # Add the rdf:Description element
        rdf_description = etree.SubElement(
            rdf,
            "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Description",
            attrib={"{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about": ""}
        )

        # description → dc:description
        if description:
            dc_description_element = etree.SubElement(rdf_description, "{http://purl.org/dc/elements/1.1/}description")
            alt = etree.SubElement(dc_description_element, "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Alt")
            li = etree.SubElement(alt, "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}li", attrib={"{http://www.w3.org/XML/1998/namespace}lang": "x-default"})
            li.text = description

        # subject → dc:subject
        if subject:
            dc_subject_set = set(self.string_to_list(subject))
            dc_subject_element = etree.SubElement(rdf_description, "{http://purl.org/dc/elements/1.1/}subject")
            seq = etree.SubElement(dc_subject_element, "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Seq")
            for subject in dc_subject_set:
                li = etree.SubElement(seq, "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}li", attrib={"{http://www.w3.org/XML/1998/namespace}lang": "x-default"})
                li.text = subject

        # title → dc:title
        if title:
            dc_title_element = etree.SubElement(rdf_description, "{http://purl.org/dc/elements/1.1/}title")
            alt = etree.SubElement(dc_title_element, "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}Alt")
            li = etree.SubElement(alt, "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}li", attrib={"{http://www.w3.org/XML/1998/namespace}lang": "x-default"})
            li.text = title
        
        # instructions →photoshop:Instructions
        if instructions:
            photoshop_instructions_element = etree.SubElement(rdf_description, "{http://ns.adobe.com/photoshop/1.0/}Instructions")
            photoshop_instructions_element.text = instructions
        
        # make → tiff:Make
        if make:
            tiff_make_element = etree.SubElement(rdf_description, "{http://ns.adobe.com/tiff/1.0/}Make")
            tiff_make_element.text = make
        
        # model → tiff:Model
        if model:
            tiff_model_element = etree.SubElement(rdf_description, "{http://ns.adobe.com/tiff/1.0/}Model")
            tiff_model_element.text = model
        
        # Done!
        return xmpmeta
    
    def xmpmeta_to_string(self, xmpmeta, pretty_print=False):
        return etree.tostring(xmpmeta, pretty_print=pretty_print, encoding="UTF-8").decode("utf-8")
    
    def wrap_xmpmeta(self, xmpmeta):
        # Convert the ElementTree to a string
        xmpmeta_string = self.xmpmeta_to_string(xmpmeta)
        
        # Wrap it in xpacket tags; "\uFEFF" and "W5M0MpCehiHzreSzNTczkc9d" are magic numbers.
        xpacket_wrapped = f"""<?xpacket begin="\uFEFF" id="W5M0MpCehiHzreSzNTczkc9d"?>{xmpmeta_string}<?xpacket end="w"?>"""

        return xpacket_wrapped

    def save_images(
            self,
            images,
            filename_prefix="ComfyUI",
            image_type=JHSupportedImageTypes.PNG.value,
            embed_workflow=True,
            description=None,
            subject=None,
            title=None,
            instructions=None,
            make=None,
            model=None,
            prompt=None,
            extra_pnginfo=None
            ):
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0])
        results = list()

        match image_type:
            case JHSupportedImageTypes.PNG.value:
                filename_extension = "png"
            case JHSupportedImageTypes.WEBP.value:
                filename_extension = "webp"

        xmpmeta = self.generate_xmpmeta(
            description=description,
            subject=subject,
            title=title,
            instructions=instructions,
            make=make,
            model=model
        )
        
        for (batch_number, image) in enumerate(images):
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
            file = f"{filename_with_batch_num}_{counter:05}_.{filename_extension}"

            match image_type:
                case JHSupportedImageTypes.PNG.value:
                    pnginfo = PngInfo()
                    pnginfo.add_text("XML:com.adobe.xmp", self.wrap_xmpmeta(xmpmeta))

                    if embed_workflow:
                        if prompt is not None:
                            pnginfo.add_text("prompt", json.dumps(prompt))
                        if extra_pnginfo is not None:
                            pnginfo.add_text("workflow", json.dumps(extra_pnginfo["workflow"]))

                    img.save(os.path.join(full_output_folder, file), pnginfo=pnginfo, compress_level=self.compress_level)
 
                case JHSupportedImageTypes.WEBP.value:
                    if embed_workflow:
                        exif_dict = {}
                        if prompt is not None:
                            exif_dict["prompt"] = json.dumps(prompt)
                        if extra_pnginfo is not None:
                            exif_dict.update(extra_pnginfo)

                        exif = img.getexif()
                        exif_addr = ExifTags.Base.UserComment
                        for key in exif_dict:
                            exif[exif_addr] = "{}:{}".format(key, json.dumps(exif_dict[key]))
                            exif_addr -= 1
                    
                    img.save(os.path.join(full_output_folder, file), exif=exif, xmp=self.wrap_xmpmeta(xmpmeta), quality=100, lossless=True)
            
            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
            })
            counter += 1

        return { "result": images, "ui": { "images": results } }
