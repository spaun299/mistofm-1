$('.trak-item audio').attr('data-state','pause');

var pauseIf,
    jPlayerPausePlay = 'pause';

$("#mesh-main-player").jPlayer({
    ready: function () {

        if ( $('.playlist-wrapper .jp-playlist .trak-item').length > 0 ) {

            var $this = $('.playlist-wrapper .jp-playlist .about-list').next();
                audioSrc = $this.data('audio'),
                audtioTitle = $this.find('audio').attr('title'),
                audtioThumb = $this.data('thumbnail'),
                audtioArtist = $this.data('artist');

            $('.mesh-main-player .mesh-artist').text(audtioArtist);

            $('.mesh-main-player .mesh-thumbnail img').attr('src',audtioThumb);

            $this.addClass('active');

            $this.find('audio').attr('data-state','pause');

            $('.jp-jplayer').attr({
                'data-state':'pause',
                'data-audio-src':audioSrc
            });

            $("#mesh-main-player").jPlayer("setMedia", {
                title: audtioTitle,
                m4a: audioSrc
            });

        }

    },
    swfPath: '../dist/jplayer',
    solution: 'html, flash',
    supplied: 'm4a, oga',
    preload: 'metadata',
    volume: 0.8,
    muted: false,
    backgroundColor: '#000000',
    cssSelectorAncestor: '#mesh-main-player-content',
    cssSelector: {
        play: '.mesh-play',
        pause: '.mesh-pause',
        // stop: '.jp-stop',
        seekBar: '.mesh-seek-bar',
        playBar: '.mesh-seek-bar > div',
        mute: '.mesh-mute',
        // unmute: '.mesh-unmute',
        volumeBar: '.mesh-volume-bar',
        volumeBarValue: '.mesh-volume-bar-value',
        // volumeMax: '.jp-volume-max',
        // playbackRateBar: '.jp-playback-rate-bar',
        // playbackRateBarValue: '.jp-playback-rate-bar-value',
        currentTime: '.mesh-current-time',
        duration: '.mesh-duration',
        // title: '.mesh-title',
        
        
        
        // fullScreen: '.jp-full-screen',
        // restoreScreen: '.jp-restore-screen',
        // repeat: '.jp-repeat',
        // repeatOff: '.jp-repeat-off',
        // gui: '.jp-gui',
        // noSolution: '.jp-no-solution'
    },
    errorAlerts: false,
    warningAlerts: false,
    ended: function() {

       var playingSongParent = $('.trak-item.active');

        if ( playingSongParent.next().length > 0 ) {

            var parentForFind = playingSongParent.next(),
                songTitle = parentForFind.find('audio').attr('title'),
                songSrc = parentForFind.data('audio'),
                soundThumb = parentForFind.data('thumbnail'),
                audtioArtist = parentForFind.data('artist'),
                jPlayerPausePlay = $('.jp-jplayer').attr('data-state');

            $('.mesh-main-player .mesh-artist').text(audtioArtist);

            $('.trak-item').removeClass('active playing');

            parentForFind.addClass('active playing');

            $('.mesh-thumbnail img').attr('src',soundThumb);

            $("#mesh-main-player").jPlayer("setMedia", {
                title: songTitle,
                m4a: songSrc
            }).jPlayer("play");

            parentForFind.find('audio').attr('data-state','play');

            $('.jp-jplayer').attr({
                'data-state':'play',
                'data-audio-src':songSrc
            });


        } else {

            playingSongParent.removeClass('playing');

            playingSongParent.find('audio').attr('data-state','pause');

        };

    },
    play: function() {

        $('.trak-item.active').addClass('playing');

        $('.trak-item.active').find('audio').attr('data-state','play');

        $('.jp-jplayer').attr('data-state','play');

    },
    pause: function() {

        $('.trak-item.active').removeClass('playing');

        $('.trak-item.active').find('audio').attr('data-state','pause');

        $('.jp-jplayer').attr('data-state','pause');

    }
});

var playerPlayOne = {

    init: function(){

        $('.trak-item .play-pause-button').on('click',function(){
            $('.main-music-player').removeClass('hide-player');
            if ( $(this).parent().hasClass('active') ) {} else {

                $('.trak-item').removeClass('active playing');
                $('.trak-item audio').data('state','pause');
                $('.jp-jplayer').attr('data-state','pause');

            }

            var parentForFind = $(this).parent(),
                songTitle = parentForFind.find('audio').attr('title'),
                songSrc = parentForFind.data('audio'),
                soundThumb = parentForFind.data('thumbnail'),
                audtioArtist = parentForFind.data('artist'),
                findItemByTitlteClick = $('.trak-item.active[data-audio="' + songSrc + '"][data-artist="' + audtioArtist + '"][data-thumbnail="' + soundThumb + '"]'),
                jPlayerPausePlay = $(this).parent().find('audio').attr('data-state'),
                pauseIf = $('.jp-jplayer').attr('data-audio-src');

            if ( pauseIf == songSrc ) {

                if ( jPlayerPausePlay == 'play' ) {

                    if ( parentForFind.hasClass('active') ) {

                        $("#mesh-main-player").jPlayer("pause");

                        parentForFind.removeClass('playing');

                        parentForFind.find('audio').attr('data-state','pause');

                        $('.jp-jplayer').attr('data-state','pause');

                        findItemByTitlteClick.addClass('active');
                        findItemByTitlteClick.removeClass('playing');

                    } else {

                        $('.trak-item').removeClass('active playing');

                        parentForFind.addClass('active playing');

                        var audtioArtist = parentForFind.data('artist');

                        $('.mesh-main-player .mesh-artist').text(audtioArtist);

                        $("#mesh-main-player").jPlayer("setMedia", {
                            title: songTitle,
                            m4a: songSrc
                        }).jPlayer("play");

                        parentForFind.find('audio').attr('data-state','play');

                        $('.jp-jplayer').attr({
                            'data-state':'play',
                            'data-audio-src':songSrc
                        });

                        findItemByTitlteClick.addClass('active playing');

                        var playingSongParent = $('.trak-item.active'),
                            soundThumb = parentForFind.data('thumbnail');

                        $('.mesh-thumbnail img').attr('src',soundThumb);

                    }

                } else if ( jPlayerPausePlay == 'pause' ) {

                    if ( parentForFind.hasClass('active') ) {

                        $("#mesh-main-player").jPlayer("play");

                        parentForFind.addClass('playing');

                        parentForFind.find('audio').attr('data-state','play');

                        $('.jp-jplayer').attr('data-state','play');

                        findItemByTitlteClick.addClass('active playing');

                    } else {

                        $('.trak-item').removeClass('active playing');

                        parentForFind.addClass('active playing');

                        var audtioArtist = parentForFind.data('artist');

                        $('.mesh-main-player .mesh-artist').text(audtioArtist);

                        $("#mesh-main-player").jPlayer("setMedia", {
                            title: songTitle,
                            m4a: songSrc
                        }).jPlayer("play");

                        parentForFind.find('audio').attr('data-state','play');

                        $('.jp-jplayer').attr({
                            'data-state':'play',
                            'data-audio-src':songSrc
                        });

                        findItemByTitlteClick.addClass('active playing');

                        var playingSongParent = $('.trak-item.active'),
                            soundThumb = parentForFind.data('thumbnail');

                        $('.mesh-thumbnail img').attr('src',soundThumb);

                    }

                };

            } else {

                $('.trak-item').removeClass('active playing');

                parentForFind.addClass('active playing');

                var audtioArtist = parentForFind.data('artist');

                $('.mesh-main-player .mesh-artist').text(audtioArtist);

                $("#mesh-main-player").jPlayer("setMedia", {
                    title: songTitle,
                    m4a: songSrc
                }).jPlayer("play");

                parentForFind.find('audio').attr('data-state','play');

                $('.jp-jplayer').attr({
                    'data-state':'play',
                    'data-audio-src':songSrc
                });

                findItemByTitlteClick.addClass('active playing');

                var playingSongParent = $('.trak-item.active'),
                    soundThumb = parentForFind.data('thumbnail');

                $('.mesh-thumbnail img').attr('src',soundThumb);

            };

        });

    },

}

$(document).ready(function(){

    playerPlayOne.init();

    $('.hide-player-button').on('click',function(){

        $('.main-music-player').toggleClass('hide-player');

    });

    $('.trak-item audio').bind('canplay',function(){

        var seconds = $(this)[0].duration;
        var duration = moment.duration(seconds, "seconds");
        
        var time = "";
        var hours = duration.hours();
        var minutes = duration.minutes();
        var seconds = duration.seconds();
        if (hours > 0) { time = hours + ":" ; }

        if ( minutes < 10 ) {

            minutes = '0' + minutes;

        }

        if ( seconds < 10 ) {

            seconds = '0' + seconds;

        }
        
        time = time + minutes + ":" + seconds;
        $(this).parent().find('.trak-duration').text(time);

    });

    $(window).scroll(function(){

        var aS = $(window).scrollTop(),
            wH = $(window).height(),
            dH = $(document).height(),
            pM = $('.main-music-player');

        if ( aS >= ( dH - wH ) ) {

            pM.addClass('hide-player-footer');

        } else {

            pM.removeClass('hide-player-footer');

        }

    });

});

$(window).scroll(function() {    
    var scroll = $(window).scrollTop();
    if (scroll >= 100 ) {
        $(".main-music-player").addClass("active", 1000);

    }
    else{
        $(".main-music-player").removeClass("active");
    }
});


function radioTitle() {
		var url = 'http://93.75.217.95:8000/json.xsl';
		$.ajax({
			type: 'GET',
			url: url,
			acync: true,
			jsonpCallback: 'parseMusic',
			contentType: "application/json",
			dataType: 'jsonp',
			success: function (json) {
				// $('.mesh-title').text(json["/listen"].title);
				// $('.mesh-title').text(json["/listen"].title);
				// $('#listeners').text(json["/listen"].listeners);
				var listen = json["/listen"].title;
				var title = listen.split(/\-/)[1];
				var artist = listen.split(/\-/)[0];
				// var artist = listen.split(/\-/)[0] || listen.split(/\-/)[0];
				$('.mesh-listen').text(json["/listen"].title);
				$('.mesh-title').text(title);
				$('.mesh-artist').text(artist);
			},
			error: function (e) {
				// alert(e.message);
			}
		});
	}
	
	function upDate() {
		setTimeout(function() {
			radioTitle();
		}, 20000);
		setInterval(function() {
			radioTitle();
		}, 1500);
	}
	upDate();

