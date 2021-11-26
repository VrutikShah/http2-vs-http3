# https://github.com/sangwonl/python-mpegdash


from mpegdash.parser import MPEGDASHParser



# Parse from file path
mpd_path = 'video.mp4'
mpd = MPEGDASHParser.parse(mpd_path)

# Parse from url
mpd_url = 'http://yt-dash-mse-test.commondatastorage.googleapis.com/media/motion-20120802-manifest.mpd'
# mpd = MPEGDASHParser.parse(mpd_url)

# Parse from string
mpd_string = '''
<MPD xmlns="urn:mpeg:DASH:schema:MPD:2011" mediaPresentationDuration="PT0H1M52.43S" minBufferTime="PT1.5S"
profiles="urn:mpeg:dash:profile:isoff-on-demand:2011" type="static">
  <Period duration="PT0H1M52.43S" start="PT0S">
    <AdaptationSet>
      <ContentComponent contentType="video" id="1" />
      <Representation bandwidth="4190760" codecs="avc1.640028" height="1080" id="1" mimeType="video/mp4" width="1920">
        <BaseURL>motion-20120802-89.mp4</BaseURL>
        <SegmentBase indexRange="674-981">
          <Initialization range="0-673" />
        </SegmentBase>
      </Representation>
    </AdaptationSet>
  </Period>
</MPD>
'''
# mpd = MPEGDASHParser.parse(mpd_string)

# Write to xml file
MPEGDASHParser.write(mpd, 'output_video.mpd')
