var audio = document.getElementById("audio-player");

$(document).ready(function() {

    var player = $('.player');
    
    player.on('click', '.btn-player', function(e){
    	e.preventDefault();
    	if ( $(this).hasClass('play') ) {
    		$(this).removeClass('play');
    		$(this).addClass('pause');
    		audio.play();
            // audio.currentTime = 0;
    	} else {
    		$(this).removeClass('pause');
    		$(this).addClass('play');
    		
    		audio.pause();
            // audio.currentTime = 0;
    	}
    });
    
    /***********************************************************************************************/
    /* SEARCH TRACK */
    /***********************************************************************************************/
    
    // YOUTUBE-----
    $(".utube-find").on('click', function() {
        cache: false;
        var name = $('.on-listen').text();
        var image = $('#track-image img').attr('src');

        if(name!='Misto FM') {
                            
        }

        name = encodeURIComponent(name);
        image = encodeURIComponent(image);
        if (image === 'undefined') { image = 'http://reold-vovax.c9users.io/img/misto_logo.png'; }

        var ttt = "https://www.youtube.com/results?search_query=";  
        var link_text = ttt+name;
        
        window.open(link_text,'_blank')

    });
    
    // SOUNDCLOUD-----
    $(".scloud-find").on('click', function() {
        cache: false;
        var name = $('.on-listen').text();

        name = encodeURIComponent(name);

        var ttt = "https://soundcloud.com/search/sounds?q=";
        var link_text = ttt+name;
        
        window.open(link_text,'_blank')

    });
    
    
    // FACEBOOK-----
    $(".fb-share").on('click', function() {
        cache: false;
        var name = $('.on-listen').text();
        var image = "http://reold-vovax.c9users.io/img/logo-light1.png";

        if(name!='Misto FM') {
                           
        }

        name = encodeURIComponent(name);
        image = encodeURIComponent(image);
        if (image === 'undefined') { image = 'http://reold-vovax.c9users.io/img/logo-light1.png'; }

        var ttt = "https://www.facebook.com/dialog/feed?app_id=318530685222946&display=popup&caption="+encodeURIComponent("Misto Fm ● Lviv ● Deep ")+"&link=http://reold-vovax.c9users.io/";
        var ttt2 = encodeURIComponent(" - ");
        var ttt3 = encodeURIComponent("Мне нравится ");
        var ttt4 = encodeURIComponent(" на Misto FM ");
        var ttt5 = encodeURIComponent("");

        var link_text = ttt+"&name="+ttt3+name+ttt2+name+ttt4+"&description="+ttt5+"&picture="+image;
                        
        window.open(link_text,'popup', 'width=640,height=520')
    });
    
    

    var artist;
    function radioTitle() {
        if ($("body").data("title") === "deep-page") {
    		var url = 'http://94.23.66.114:8122/statistics?json=1';
    		$.ajax({
    			type: 'POST',
    			url: url,
    			acync: true,
    			jsonpCallback: 'parseMusic',
    			contentType: "application/json",
    			dataType: 'jsonp',
    			success: function (json) {
    			    artist = json.streams["0"].songtitle;
    				var mistoFm = 'Deep - for those who need music like oxygen'
    				var sonica = 'sonica';
                    if( sonica.indexOf(artist) >= 0){
                        $('.on-listen').text(mistoFm);
                        $('#audio-player').prop('title', mistoFm);
                    } else {
                        $('.on-listen').text(artist);
                        $('#audio-player').prop('title', artist);
                    }
    			},
    			error: function (e) {
    				// alert(e.message);
    			}
    		});
        } else {
            var artist;
        	var url = 'http://77.92.76.134:8032/statistics?json=1';
        	$.ajax({
    			type: 'POST',
        		url: url,
        		acync: true,
        		jsonpCallback: 'parseMusic',
    			contentType: "application/json",
    			dataType: 'jsonp',
        		success: function (json) {
        		    artist = json.streams["0"].songtitle;
    				var mistoFm = 'Deep - for those who need music like oxygen'
    				var sonica = 'sonica';
                    if( sonica.indexOf(artist) >= 0){
                        $('.on-listen').text(mistoFm);
                        $('#audio-player').prop('title', mistoFm);
                    } else {
                        $('.on-listen').text(artist);
                        $('#audio-player').prop('title', artist);
                    }
        		},
        		error: function (e) {
        			// alert(e.message);
    			}
        	});
        }
	}
	
    function upDate() {
		setTimeout(function() {
			radioTitle();
			getHtml();
		}, 20000);
		setInterval(function() {
			radioTitle();
			getHtml();
		}, 1500);
	}
	upDate();
	
	

    var html;
    var table;
    var trackName2;
    var trackName3;
    var trackName4;
	function getHtml() {
	    if ($("body").data("title") === "deep-page") {
    	    $.ajaxSetup({
                scriptCharset: "utf-8",
                contentType: "application/json; charset=utf-8"
            });
            $.getJSON('http://www.whateverorigin.org/get?url=' + encodeURIComponent('http://94.23.66.114:8122/played.html') + '&callback=?', function(data){
            	html = $(data.contents);
            	table = html["5"];

                trackName2 = table.rows["2"].cells["1"].innerHTML
                trackName3 = table.rows["3"].cells["1"].innerHTML
                trackName4 = table.rows["4"].cells["1"].innerHTML
                
                $('.played-2').text(trackName2);
                $('.played-3').text(trackName3);
                $('.played-4').text(trackName4);
                
            });
	    } else {
	        $.ajaxSetup({
                scriptCharset: "utf-8",
                contentType: "application/json; charset=utf-8"
            });
            $.getJSON('http://www.whateverorigin.org/get?url=' + encodeURIComponent('http://77.92.76.134:8032/played.html') + '&callback=?', function(data){
            	html = $(data.contents);
            	table = html["6"];
                trackName2 = table.rows["2"].cells["1"].innerHTML
                trackName3 = table.rows["3"].cells["1"].innerHTML
                trackName4 = table.rows["4"].cells["1"].innerHTML
    
                $('.played-2').text(trackName2);
                $('.played-3').text(trackName3);
                $('.played-4').text(trackName4);
                
                
            });
	    }
        
    };

	$('#np-volume').on('input propertychange', function() {
		var val = ($(this).val() - $(this).attr('min')) / ($(this).attr('max') - $(this).attr('min'));
        audio.volume = val;
	});


});

