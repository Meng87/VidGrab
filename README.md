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
dict_out = vidgrab.get(url, video_save_path, caption_save_path)
~~~

### Shell Script
To use this tool with the command line interface, you would use the following command:
```
python get.py -u <video url> -v <video save path> -c <caption save path>
```
There are also a number of optional flags you can use.
| Flag               | Meaning     |
| ------------------ | ----------- |
| -w --write_caption | Write the output into a .json file       |
| -d --debug         | Turn on debuging mode  |
| -b --write_if_both | Only write the output into a .json file if both the video and captions are available |

## Output
The output will be a .json file containing the relevant information. If using the Python module, the function also returns the relevant information as a Python dictionary.

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
