var audio = document.getElementById("audio-player");
var metadataUrl;
var stream_url;
var currentTime;

$(document).ready(function() {

    var player = $('.player');
    currentTime = getCurrentTimeInSeconds();

    player.on('click', '.btn-player', function(e){
        e.preventDefault();
        if ( $(this).hasClass('play') ) {
                $(this).removeClass('play');
                $(this).addClass('pause');
                audio.play();
                audio.currentTime = getCurrentTimeInSeconds() - currentTime;
        } else {
                $(this).removeClass('pause');
                $(this).addClass('play');
                audio.pause();
                audio.src = "";
                audio.load();
                $("audio").remove();
                currentTime = getCurrentTimeInSeconds();
                $("audio-player-wrapper").html("<audio id='audio-player' preload='metadata' title='Misto Fm ☆ Lviv ☆ On Air'></audio>");
                audio.src = stream_url;
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
        var image = "http://mistofm.com.ua/static/img/logo_400x400.png";

        if(name!='Misto FM') {

        }

        name = encodeURIComponent(name);
        image = encodeURIComponent(image);
        if (image === 'undefined') { image = "http://mistofm.com.ua/static/img/logo_400x400.png"; }

        var ttt = "https://www.facebook.com/dialog/feed?app_id=535111550164465&display=popup&caption="+encodeURIComponent("Misto Fm ● Lviv ● Deep ")+"&link=http://mistofm.com.ua/";
        var link_text = ttt+"&name="+"&picture="+image;

        window.open(link_text,'popup', 'width=640,height=520')
    });
        $('#np-volume').on('input propertychange', function() {
                var val = ($(this).val() - $(this).attr('min')) / ($(this).attr('max') - $(this).attr('min'));
        audio.volume = val;
        });

    (function radioTitle() {

        var songContent;
        $.ajaxSetup({
            scriptCharset: "utf-8",
            contentType: "application/json; charset=utf-8",
            cache: false
        })

        $.getJSON(metadataUrl, function(data){})
        .done(function(data) {
            songContent = data;
            $("#onListen").empty();
            $(".playlist").empty();

            $($(songContent).get().reverse()).each( function(n, songJson) {
                if (n == 0) {
                    var contentPlayNow = '<span>' + songJson.name + '</span>';
                    var contentPlayList = '<li class="about-list clearfix"><span class="about-icon">' + songJson.play_from + '</span><span class="about-name on-listen">' + songJson.name + '</span></li>';
                    $(contentPlayList).appendTo(".playlist");
                    $(contentPlayNow).appendTo("#onListen");
                    $(audio).prop('title', 'Misto Fm ☆ Lviv ☆ ' + songJson.name);
                } else {
                    var contentPlayList = '<li class="about-list clearfix"><span class="about-icon">' + songJson.play_from + '</span><span class="about-name on-listen">' + songJson.name + '</span></li>';
                    $(contentPlayList).appendTo(".playlist");
               }
            });
        })
        .always(function(data) {
            var nextUpdate = data.next_update;
            if (!nextUpdate) {
                nextUpdate = 36;
            }
            setTimeout(function() {
                radioTitle();
            }, nextUpdate * 1000);
        });

    })();


});
