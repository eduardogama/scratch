from mpegdash.parser import MPEGDASHParser

# Parse from url
mpd_url = 'https://dash.akamaized.net/akamai/bbb_30fps/bbb_30fps.mpd'
mpd = MPEGDASHParser.parse(mpd_url)




print(mpd.__dict__)
print(mpd.base_urls[0].__dict__)


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
mpd = MPEGDASHParser.parse(mpd_string)

# Write to xml file
MPEGDASHParser.write(mpd, 'output.mpd')
