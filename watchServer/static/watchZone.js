// Init vars
var zones;
var rightClick;
var leftClick;

//Webpage Init
$( document ).ready(function() {
	getAreas().done(function () {
		setArea(0);
		getZones(cur_map);
		makeClickEvent();
	});
});

$( window ).resize(function() {
	$.each( zones, function( key, val ){
		scaleZone(key,val)
	});
})

function makeClickEvent() {
	$('#floorMap').mousedown(function(e) {
		var offset = $(this).offset();
		var pos = [e.pageX - offset.left , e.pageY - offset.top] 
		updateClick(e.which,pos)
	});	
}

function updateClick(click,pos) {
	roundPos = [ Math.round(pos[0] / imgLocs['ratio']),Math.round(pos[1] / imgLocs['ratio']) ]
	switch (click) {
		case 1:
			leftClick = pos
			$('#leftClick').val(roundPos);
			break;
		case 3:
			rightClick = pos
			$('#rightClick').val(roundPos);
			break;
	}
}

function getZones(MapID) {
	var r = $.Deferred();
	$.getJSON( api_url+"zone/list/"+MapID, function( data ) {
		if ( data[0] == 0 ) {
			zones = data[1];
		}
		$.each( zones, function( key, val ){
			writeZone(key,val)
		});
		r.resolve();
	})
	return r;
}

function writeZone(key,val) {
	$( "<div/>", {
		"class": "zone",
		"id": "zone-"+key,
		html: "<div class=\"zoneText\">"+val[0]+"</div>"
	}).appendTo( "#map" );
	scaleZone(key,val);
}

function scaleZone(key,val) {
	getImageInfo();
	y = imgLocs['left'] + eval(val[3])[0] * imgLocs['ratio'];
	x = imgLocs['top'] + eval(val[3])[1] * imgLocs['ratio'];
	width = ( eval(val[4])[0] - eval(val[3])[0] ) * imgLocs['ratio'] ;
	height = ( eval(val[4])[1] - eval(val[3])[1] ) * imgLocs['ratio'] ;
	$("#zone-"+key).css({"top": x+"px" , "left": y+"px", "width": width+"px", "height": height+"px"});
}
