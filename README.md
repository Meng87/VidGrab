README.md

## Description
This tool was developed to automate the process of downloading videos and transcripts, so as to facilitate the generation of large amounts of data for machine learning.

## Dependencies and Installation Instructions

* pytube
    * `pip install git+https://github.com/rmerzouki/pytube`
* xmltodict
    * `pip install xmltodict`
* Python 3.6 and above

## Usage

### Python Script
To use VidGrab within your own Python script, you would first import the library and call the `get` function.
~~~
import vidgrab
dict_out = vidgrab.get(url, video_save_path, caption_save_path, write_caption, debug, write_if_both)
~~~
Note that `video_save_path` and `caption_save_path` take in a file path to the saved video or caption file, e.g. "./videos/video1.mp4", "./videos/caption1.json".

The last 3 arguments are optional. Their meanings and default values are detailed below in the "Argument Descriptions and Flags" section.

### Shell Script
To use this tool with the command line interface (CLI), you would use the following command:
```
python vidgrab.py -u <video url> -v <video save path> -c <caption save path>
```
### Argument Descriptions and Flags
| Flag               | Meaning     | Default Value |
| ------------------ | ----------- | ------------- |
| -u --url           | Takes in a valid link to a video  | NA, argument required |
| -v --video_path    | Takes in a file path to a .mp4 file that does not exist yet | NA, argument required |
| -c --caption_path  | Takes in a file path to a .json file that does not exist yet | NA, argument required |
| -w --write_caption | Write the output into a .json file  | False |
| -d --debug         | Turn on debuging mode  | False |
| -b --write_if_both | Only write the output into a .json file if both the video and captions are available | False |

Here is an example of using the tool with the CLI with optional flags:
```
python get.py -u <video url> -v <video save path> -c <caption save path> -w -d -b
```
This gets a video at \<video url\>, saves the video to \<video save path\> and saves relevant information to \<caption save path\> as a .json file if captions exist for the video. It also prints out useful debugging information that can help identify the sources of any errors.

## Output
The output will be a .json file containing the relevant information. If using the tool within Python script, the function also returns the relevant information as a Python dictionary.

The output follows the following format:
~~~~
{
    'video_id': <string>,
    'url': <string>,
    'video_path': <string>,
    'chunks': <list>
    'intervals': <2D list>
    'transcript_type': <string: "human" / "asr_youtube"
}
~~~~

## Failure Cases
The output in the failure cases will contain information about the error.

No English captions are available.
~~~~
{
    'video_id': <string>,
    'url': <string>,
    'video_path': <string>,
    'chunks': None,
    'intervals': None,
    'transcript_type': None
}
~~~~

Video is not found.
~~~~
{
   "error": "video_not_found"
}
~~~~

Unable to download the video.
~~~~
{
   "error": "download_failed"
}
~~~~
