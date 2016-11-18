"""ContentHandler.py: transforms the JSON into an acceptable data format."""
import requests
import json
import shutil
import uuid
import os


class ContentHandler(object):
    """returns a string of HTML with the relevant content."""

    def __init__(self,
                 src_image_file_path=False,
                 dest_image_file_path=False,
                 reference_url=False,
                 katex_conversion_url=False,
                 create_images=True,
                 reuse_images=True):
        """Constructor for ContentHandler."""
        # Q: Should the file paths be relative?
        # A: Yes, otherwise the file src is not going to mean much.
        #    That is, only the place to store the file
        super(ContentHandler, self).__init__()
        if src_image_file_path:
            self.src_image_file_path = src_image_file_path
        else:
            raise Exception("src_image_file_path is not specified")
        if dest_image_file_path:
            self.dest_image_file_path = dest_image_file_path
        else:
            raise Exception("dest_image_file_path is not specified")
        if reference_url:
            self.reference_url = reference_url
        else:
            raise Exception("reference_url is not specified")
        if katex_conversion_url:
            self.katex_conversion_url = katex_conversion_url
        else:
            raise Exception("katex_conversion_url is not specified")
        self.create_images = create_images
        self.reuse_images = reuse_images
        self.equation_image_references = {}

    def create_katex(self, latex_string):
        """Convert string of latex into katex."""
        resp = requests.post(
            self.katex_conversion_url,
            data=json.dumps({'latex': latex_string}),
            headers={'Content-Type': 'application/json'})
        return resp.text

    def create_image(self, latex):
        """Create image from latex and return html image src."""
        if(self.reuse_images and (latex in self.equation_image_references)):
                return self.equation_image_references[latex]

        resp = requests.get(
            "http://latex.codecogs.com/gif.latex?{" + latex + "}",
            stream=True)
        # generate uuid for image
        image_uuid = str(uuid.uuid4())
        image_file_name = image_uuid + ".gif"
        image_file_path = os.path.join(self.dest_image_file_path, image_file_name)
        with open(image_file_path, 'wb') as f:
            resp.raw.decode_content = True
            shutil.copyfileobj(resp.raw, f)

        img_tag = "<img src='{0}' alt='{1}' >".format(
            # this will need to be changed to a relative file path
            # (that is relative to the file referenceing)
            self.reference_url + "/" + image_file_name,
            latex)

        if(self.reuse_images):
            self.equation_image_references[latex] = img_tag

        return img_tag

    def process_image(self, image_file_name):
        """Copy image files across to destination and optimised them."""
        # copy the image across to the ./images or static folder
        src_file = os.path.join(self.src_image_file_path, image_file_name)
        # print(src_file)
        dest_file = os.path.join(self.dest_image_file_path, image_file_name)
        # print(dest_file)
        shutil.copyfile(src_file, dest_file)

        # TODO: optimise the image

        # create the image tag and return it
        return "<img src='{0}' alt='{1}' >".format(
            # this will need to be changed to a relative file path
            # (that is relative to the file referenceing)
            (os.path.join(self.reference_url, image_file_name)),
            "Image of math content")

    def break_into_lines(self, list_of_blocks):
        """Return an array of arrays, each array denoting lines."""
        lines = []

        line = [list_of_blocks[0]]
        if len(list_of_blocks) == 1:
            lines.append(line)
            return lines
        # separate content into lines
        else:
            for block in list_of_blocks[1:]:
                if "inline" in block and block["inline"] is True:
                    # print("It's inline")
                    # print(line)
                    line.append(block)
                    # print(line)
                    # print("---------")
                else:
                    # print("It's not inline!")
                    # add line to lines
                    lines.append(line)
                    # start a new line
                    line = [block]
        # case where last line is True,
        if line != []:
            lines.append(line)

        return lines

    def get_formatted_content(self, list_of_blocks):
        """
        Convert list of block content and returns HTML.

        Converts latex to images.
        """
        if list_of_blocks == []:
            return ""
        lines = self.break_into_lines(list_of_blocks)
        content = ""

        for line in lines:
            line_of_text = ""

            for block in line:
                if 'text' in block:
                    line_of_text += block["text"]

                elif 'latex' in block:
                    if self.create_images:
                        line_of_text += self.create_image(block["latex"])
                    else:
                        line_of_text += self.create_katex(block["latex"])

                elif 'image' in block:
                    # TODO: process the image
                    # get the URL where image is stored
                    line_of_text += self.process_image(block['image'])

                else:
                    raise Exception(
                        "Block does not contain image, text or latex")
            # check if it is a simgle image and don't wrap with p tags
            content += "<p>" + line_of_text + "</p>"

        return content
