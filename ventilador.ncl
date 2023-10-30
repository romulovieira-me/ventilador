<?xml version="1.0" encoding="ISO-8859-1"?>
<ncl id="AppWind">
 <head>
	<regionBase>
		<region id="rgVideo1" width="100%" height="100%" />
		<region id="rgVideo2" width="100%" height="100%" />
		<region id="rgWind" location="center:top:front" />
   	</regionBase>

	<descriptorBase>
		<descriptor id="dVideo1"  region="rgVideo1" explicitDur="39s"/> 
		<descriptor id="dVideo2"  region="rgVideo2" explicitDur="11s"/> 

		<!-- Descritor de vento -->
		<descriptor id="dWind" region="rgWind"  />
		<!--  intensityValue="1" intensityRange="[1,3]" /> -->

	</descriptorBase>
	
	<connectorBase>

		<causalConnector id="onBeginStart">
			<simpleCondition role="onBegin" />
			<simpleAction role="start" />
		</causalConnector>

		<causalConnector id="onEndStart">
			<simpleCondition role="onEnd" />
			<simpleAction role="start" max="unbounded"/>
		</causalConnector>

		<causalConnector id="onEndStop">
			<simpleCondition role="onEnd" />
			<simpleAction role="stop" />
		</causalConnector>

		<causalConnector id="onBeginSet">
            <connectorParam name="var" />
            <simpleCondition role="onBegin" />
            <simpleAction role="set" max="unbounded" value="$var" />
        </causalConnector> 

	</connectorBase>
  </head>

  <body>
  	
		<port id="pStart" component="video1" />

		<media id="video1" src="media/sea.mp4" descriptor="dVideo1" />
		<media id="video2" src="media/autumn.mp4" descriptor="dVideo2" />

		<!-- Declarando efeito de vento -->
		<effect id="windEffect" type="WindType" descriptor="dWind" />
		
		<link xconnector="onBeginStart">
			<bind role="onBegin" component="video1" />
			<bind role="start" component="windEffect" />
		</link>

		<link xconnector="onEndStart">
			<bind role="onEnd" component="video1" />
			<bind role="start" component="video2" />
		</link>

		<link xconnector="onEndStop">
			<bind role="onEnd" component="video2" />
			<bind role="stop" component="windEffect" />
		</link>

</body>
</ncl>
