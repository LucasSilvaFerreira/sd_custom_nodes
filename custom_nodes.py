
from PIL import Image, ImageSequence
import torch


class Example:
    """
    A example node

    Class methods
    -------------
    INPUT_TYPES (dict): 
        Tell the main program input parameters of nodes.

    Attributes
    ----------
    RETURN_TYPES (`tuple`): 
        The type of each element in the output tulple.
    RETURN_NAMES (`tuple`):
        Optional: The name of each output in the output tulple.
    FUNCTION (`str`):
        The name of the entry-point method. For example, if `FUNCTION = "execute"` then it will run Example().execute()
    OUTPUT_NODE ([`bool`]):
        If this node is an output node that outputs a result/image from the graph. The SaveImage node is an example.
        The backend iterates on these output nodes and tries to execute all their parents if their parent graph is properly connected.
        Assumed to be False if not present.
    CATEGORY (`str`):
        The category the node should appear in the UI.
    execute(s) -> tuple || None:
        The entry point method. The name of this method must be the same as the value of property `FUNCTION`.
        For example, if `FUNCTION = "execute"` then this method's name must be `execute`, if `FUNCTION = "foo"` then it must be `foo`.
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        """
            Return a dictionary which contains config for all input fields.
            Some types (string): "MODEL", "VAE", "CLIP", "CONDITIONING", "LATENT", "IMAGE", "INT", "STRING", "FLOAT".
            Input types "INT", "STRING" or "FLOAT" are special values for fields on the node.
            The type can be a list for selection.

            Returns: `dict`:
                - Key input_fields_group (`string`): Can be either required, hidden or optional. A node class must have property `required`
                - Value input_fields (`dict`): Contains input fields config:
                    * Key field_name (`string`): Name of a entry-point method's argument
                    * Value field_config (`tuple`):
                        + First value is a string indicate the type of field or a list for selection.
                        + Secound value is a config for type "INT", "STRING" or "FLOAT".
        """
        return {
            "required": {
                "image": ("IMAGE",),
                "int_field": ("INT", {
                    "default": 0, 
                    "min": 0, #Minimum value
                    "max": 4096, #Maximum value
                    "step": 64, #Slider's step
                    "display": "number" # Cosmetic only: display as "number" or "slider"
                }),
                "float_field": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.01, "display": "number"}),
                "print_to_screen": (["enable", "disable"],),
                "string_field": ("STRING", {
                    "multiline": False, #True if you want the field to look like the one on the ClipTextEncode node
                    "default": "Hello World!"
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    #RETURN_NAMES = ("image_output_name",)

    FUNCTION = "test"

    #OUTPUT_NODE = False

    CATEGORY = "Example"

    def test(self, image, string_field, int_field, float_field, print_to_screen):
        if print_to_screen == "enable":
            print(f"""Your input contains:
                string_field aka input text: {string_field}
                int_field: {int_field}
                float_field: {float_field}
            """)
        #do some processing on the image, in this example I just invert it
        image = 1.0 - image
        return (image,)




class Lucas:
    def __init__(self):
      pass
    @classmethod
    def INPUT_TYPES(s):
      return {
            "required": {
                "image": ("IMAGE",),
                "columns": ("INT", {
                    "default": 1, 
                    "min": 1, #Minimum value
                    "step": 1, #Slider's step
                    "display": "number" # Cosmetic only: display as "number" or "slider"
                }),
                  "rows": ("INT", {
                    "default": 1, 
                    "min": 1, #Minimum value
                    "step": 1, #Slider's step
                    "display": "number" # Cosmetic only: display as "number" or "slider"
                }),
                    "video_speed": ("INT", {
                    "default": 200, 
                    "min": 1, #Minimum value
                    "max": 1000, #Minimum value
                    "step": 1, #Slider's step
                    "display": "slider" # Cosmetic only: display as "number" or "slider"
                }),

            },
        }


    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "to_gif"
    CATEGORY = "gif"


    def to_gif(self, image, columns, rows, video_speed):
      #print (image)
      print (columns, rows)
      print (image.shape)
      tensor_to_gif(image, rows, columns, 'output.gif', video_speed)

      return (image,)
      




def tensor_to_gif(tensor, rows, columns, gif_filename, video_speed):
    """
    Convert a tensor of shape (1, H, W, 3) to a gif.
    
    Parameters:
    tensor: The input tensor (should have shape [1, H, W, 3]).
    rows: Number of rows to split the image.
    columns: Number of columns to split the image.
    gif_filename: The output filename for the gif.
    """
    


    tensor = (tensor * 255).byte()
    
    # Step 1: Convert tensor to numpy and then to PIL Image
    numpy_image = tensor.squeeze(0).numpy()  # Remove the batch dimension
    pil_image = Image.fromarray(numpy_image, 'RGB')
    
    # Step 2: Split the image using rows and columns to create a sequence
    width, height = pil_image.size
    frame_width = width // columns
    frame_height = height // rows
    frames = []
    
    for i in range(rows):
        for j in range(columns):
            left = j * frame_width
            upper = i * frame_height
            right = left + frame_width
            lower = upper + frame_height
            frame = pil_image.crop((left, upper, right, lower))
            frames.append(frame)
    
    # Step 3: Create GIF using the sequence
    frames[0].save(gif_filename, save_all=True, append_images=frames[1:], duration=video_speed, loop=0)






# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "Example": Example, "Lucas": Lucas
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "Example": "Example Node",
    "Lucas": "Lucas Node"
}
