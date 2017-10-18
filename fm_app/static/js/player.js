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
        var name = $('#onListen').text();
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
        var name = $('#onListen').text();

        name = encodeURIComponent(name);

        var ttt = "https://soundcloud.com/search/sounds?q=";
        var link_text = ttt+name;
        
        window.open(link_text,'_blank')

    });
    
    
    // FACEBOOK-----
    $(".fb-share").on('click', function() {
        cache: false;
        var name = $('#onListen').text();
        var image = "http://127.0.0.1:5000/static/img/logo_400x400.png";

        if(name!='Misto FM') {
                           
        }

        name = encodeURIComponent(name);
        image = encodeURIComponent(image);
        if (image === 'undefined') { image = "http://127.0.0.1:5000/static/img/logo_400x400.png"; }

        var ttt = "https://www.facebook.com/dialog/feed?app_id=535111550164465&display=popup&caption="+encodeURIComponent("Misto Fm ● Lviv ● Deep ")+"&link=http://mistofm.com.ua/";
        var link_text = ttt+"&name="+"&description="+"&picture="+image;
                        
        window.open(link_text,'popup', 'width=640,height=520')
    });
    
    



	$('#np-volume').on('input propertychange', function() {
		var val = ($(this).val() - $(this).attr('min')) / ($(this).attr('max') - $(this).attr('min'));
        audio.volume = val;
	});


});

