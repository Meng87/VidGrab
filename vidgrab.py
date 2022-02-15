import sys, getopt, os
import pytube
import xmltodict, json

def get(url, video_path, caption_path, write_caption=False, debug=False, write_if_both=False):
   if (not os.path.isdir(video_path) or not os.path.isdir(caption_path)):
      print("Error: Invalid File Path.")
      return
   
   # Create YouTube object
   try:
      yt = pytube.YouTube(url)
   except:
      print("Error: Invalid URL.")
      return
   
   filename = pytube.extract.video_id(url)

   # Only download progressive streams
   prog = yt.streams.filter(progressive=True)
   bestVid = prog.get_highest_resolution()
   if (bestVid == None):
      if (debug): print("[DEBUG] Video not found.")
      output = {"error": "video_not_found"}
      if (write_caption):
         json_data = json.dumps(output)
         filepath = caption_path + "/" + filename
         with open(filepath + ".json", "w+") as json_file:
            json_file.write(json_data)
      return output
   else:
      try:
         bestVid.download(video_path, filename + ".mp4")
      except:
         if (debug): print("[DEBUG] Download Failed.")
         output = {"error": "download_failed"}
         if (write_caption):
            json_data = json.dumps(output)
            filepath = caption_path + "/" + filename
            with open(filepath + ".json", "w+") as json_file:
               json_file.write(json_data)
         return output

   # Get captions
   transcript_type = None
   if ('en' in yt.captions):
      transcript_type = "human"
      caption = yt.captions['en']
   elif ('a.en' in yt.captions):
      transcript_type = "asr_youtube"
      caption = yt.captions['a.en']
   else:
      if (debug): print("[DEBUG] No English captions available.")
      output = {
         'video_id': filename,
         'url': url,
         'video_path': video_path + "/" + filename + ".mp4",
         'chunks': None,
         'intervals': None,
         'transcript_type': None
      }
      if (write_caption and not write_if_both):
         json_data = json.dumps(output)
         filepath = caption_path + "/" + filename
         with open(filepath + ".json", "w+") as json_file:
            json_file.write(json_data)
      return output
      

   if (caption != None):
      filepath = caption_path + "/" + filename
      
      with open(filepath + ".xml", "w+") as caption_file:
         caption_file.write(caption.xml_captions)
         if (debug): print("[DEBUG] Saved captions as xml.")

      with open(filepath + ".xml") as xml_file:
         data_dict = xmltodict.parse(xml_file.read())
      
      # Convert to json
      json_data = json.dumps(data_dict)
      text_timings = data_dict["timedtext"]["body"]["p"]
      chunks_list = [] # list of captions
      intervals_list = [] # list of tuples of caption start, end times
      if (transcript_type == "human"):
         for d in text_timings:
            start_time = d["@t"]
            duration = d["@d"]
            chunks_list.append(d["#text"])
            intervals_list.append((start_time, str(int(start_time) + int(duration))))
      else:
         for d in text_timings:
            if ("s" in d):
               start_time = d["@t"]
               duration = d["@d"]
               chunk = []
               if (isinstance(d["s"], list)):
                  for t in d["s"]:
                     chunk.append(t["#text"])
                  chunk_str = " ".join(chunk)
               elif (isinstance(d["s"], dict)):
                  chunk_str = d["s"]["#text"]
               chunks_list.append(chunk_str)
               intervals_list.append((start_time, str(int(start_time) + int(duration))))
            else: continue
      output = {
            'video_id': filename,
            'url': url,
            'video_path': video_path + "/" + filename + ".mp4",
            'chunks': chunks_list,
            'intervals': intervals_list,
            'transcript_type': transcript_type
         }
      if (write_caption):
         json_data = json.dumps(output)
         filepath = caption_path + "/" + filename
         with open(filepath + ".json", "w+") as json_file:
            json_file.write(json_data)
            if (debug): print("[DEBUG] Saved captions as json.")
      # return output

if __name__ == "__main__":
   url, video_path, caption_path = None, None, None
   write_caption, debug, write_if_both = None, None, None
   try:
      opts, args = getopt.getopt(sys.argv[1:],
                                 "u:v:c:wdb",
                                 ["url=","video_path=","caption_path=",
                                  "write_caption=", "debug=",
                                  "write_if_both=True="])
   except getopt.GetoptError:
      print("Usage: get.py -u <video url> -v <video save path> -c <caption save path>\n")
      sys.exit(2)
   for opt, arg in opts:
      if opt in ("-u", "--url"):
         url = arg
      elif opt in ("-v", "--video_path"):
         video_path = arg
      elif opt in ("-c", "--caption_path"):
         caption_path = arg
      elif opt in ("-w", "--write_caption"):
         write_caption = True
      elif opt in ("-d", "--debug"):
         debug = True
      elif opt in ("-b", "--write_if_both"):
         write_if_both = True
   if (url == None or video_path == None or caption_path == None): # check invalid
      print("Usage: get.py -u <video url> -v <video save path> -c <caption save path>")
      sys.exit(2)
   get(url, video_path, caption_path, write_caption, debug, write_if_both)
