import site
import os

now_dir = os.path.dirname(os.path.abspath(__file__))
site_packages_roots = []
for path in site.getsitepackages():
    if "packages" in path:
        site_packages_roots.append(path)
if(site_packages_roots==[]):site_packages_roots=["%s/runtime/Lib/site-packages" % now_dir]
#os.environ["OPENBLAS_NUM_THREADS"] = "4"
for site_packages_root in site_packages_roots:
    if os.path.exists(site_packages_root):
        try:
            with open("%s/ChatTTS.pth" % (site_packages_root), "w") as f:
                f.write(
                    "%s\n%s/ChatTTS\n"
                    % (now_dir,now_dir)
                )
            break
        except PermissionError:
            raise PermissionError

if os.path.isfile("%s/ChatTTS.pth" % (site_packages_root)):
    print("!!!ChatTTS path was added to " + "%s/ChatTTS.pth" % (site_packages_root) 
    + "\n if meet `No module` error,try `python main.py` again")

from huggingface_hub import snapshot_download
model_path = os.path.join(now_dir,"pretrained_models")
if not os.path.isfile(os.path.join(model_path,"asset","GPT.pt")):
    snapshot_download(repo_id="2Noise/ChatTTS",local_dir=model_path)
else:
    print("ChatTTS use cache models,make sure your 'pretrained_models' complete")


WEB_DIRECTORY = "./web"
from .nodes import PreViewAudio,ChatTTS

# Set the web directory, any .js file in that directory will be loaded by the frontend as a frontend extension
# WEB_DIRECTORY = "./somejs"

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "ChatTTS":ChatTTS,
    "PreViewAudio": PreViewAudio,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "ChatTTS":"ChatTTS Node",
    "PreViewAudio": "PreView Audio",
}
