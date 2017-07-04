
var wH = $(window).height();

$('.breadcrumb-fullscreen').css('height', wH);

$('.breadcrumb:not(.breadcrumb-fullscreen)').each(function() {

    $('header.header').addClass('no-breadcrumb-fullscreen');

});

$('.breadcrumb.breadcrumb-video-content').each(function() {

    $('header.header').removeClass('no-breadcrumb-fullscreen');

});
// <!-- ================================================== -->
// <!-- =============== END BREADCRUMB JS ================ -->
// <!-- ================================================== -->

// <!-- ================================================== -->
// <!-- =============== START BREACRUMB OPTIONS ================ -->
// <!-- ================================================== -->


// SLIDER-----
$(function() {
    
    function changeBg() {
    var imgCount = 0;
    var img_array = [
        
        "http://i.imgur.com/3KD5zaV.jpg",//night city terrace
        "http://i.imgur.com/4iEFtie.jpg",//run girl
        "http://i.imgur.com/JU1LGpD.jpg",
        "http://i.imgur.com/HFw2OGy.jpg",//b&w cigar girl
        "http://i.imgur.com/iGnPBLM.png",//roof girl
        "http://i.imgur.com/vFWyl0Y.jpg",// orange girl 2
        "http://i.imgur.com/G8ELq1X.jpg",

        ],
        _nxtIndex = 0,
        _curIndex = 0,
        interval = 10000;

    function nextIndex() {
        _nxtIndex = (_nxtIndex + 1) % img_array.length;
        return _nxtIndex;
    };

    function shiftIndexes() {
        _curIndex = _nxtIndex;
        nextIndex();
    };

    function createImgTags(){
        imgCount = img_array.length;
        var html = '';
        var slider = document.getElementById('slider');
        for(var i=0; i<imgCount;i++){
            html +='<div id="background-slide'+i+'" class="background-slider"></div>';
        }
        $(slider).html(html);
    }
    function assignBackgrounds() {
        imgCount = img_array.length;  
        for (var i = 0; i < imgCount; i++) {

            $('#background-slide' + i).css('backgroundImage', function() {
                return 'url(' + img_array[nextIndex()] + ')';
            });
            if (i == 0) {
                $('#background-slide' + i).css('opacity', 1);
            } else {
                $('#background-slide' + i).css('opacity', 0);
            }
        }
    }

    function startBackgroundOpacityToggle() {
        elem = $('#background-slide' + _curIndex);
        elem.animate({
            opacity: (elem.css('opacity') == 0) ? 1 : 0
        }, {
            // duration: 5000,
            duration: 2000,
            start: finishBackgroundOpacityToggle
        });
    };

    function finishBackgroundOpacityToggle() {
        elem = $('#background-slide' + _nxtIndex);
        elem.animate({
            opacity: (elem.css('opacity') == 0) ? 1 : 0
        }, {
            // duration: 5000,
            duration: 2000,
            complete: runSlider
        });

    };

    function runSlider() {
        shiftIndexes();
        setTimeout(startBackgroundOpacityToggle, interval);
    };

    createImgTags();
    assignBackgrounds();
    runSlider();
    };
    changeBg();
// END SLIDER-----

    var breadcrumbH = $('.breadcrumb').outerHeight();

    $('.breadcrumb-fullscreen-parent').after('<div class="before-affix-breadcrumb"></div>');

    var wH = $(window).height();

    $('.deepTitle > *').each(function() {

        var fadeStart = 0
          , fadeUntil = 400
          , fading = $(this);

        $(window).bind('scroll', function() {
            var offset = $(document).scrollTop()
              , opacity = 0;
            if (offset <= fadeStart) {
                opacity = 1;
            } else if (offset <= fadeUntil) {
                opacity = 1 - offset / fadeUntil;
            }
            fading.css('opacity', opacity);
        });

    });

    function affixPhoneMenu() {

        $('header.header').addClass('phone-menu-bg');

        $('.phone-menu-bg').affix({
            offset: {
                top: 50
            }
        });

    }
    ;
    function unAffixPhoneMenu() {

        $('header.header').removeClass('phone-menu-bg');

    }
    ;
    if ($(window).width() <= 768) {
        affixPhoneMenu();
    } else {
        $(window).resize(function() {
            if ($(window).width() <= 768) {
                affixPhoneMenu();
            }
        });
    }
    ;
    if ($(window).width() >= 768) {
        unAffixPhoneMenu();
    } else {
        $(window).resize(function() {
            if ($(window).width() >= 768) {
                unAffixPhoneMenu();
            }
        });
    }
    ;
    $('.breadcrumb-fullscreen-parent').affix({
        offset: {
            top: function() {
                return ( this.top = (breadcrumbH - 75))
            }
        }
    });

    $('header.header').affix({
        offset: {
            top: function() {
                return ( this.top = (breadcrumbH - 120))
            }
        }
    });

    $('header.header').on('affix.bs.affix', function() {

        $('.project-single').addClass('affix');

    });

    $('header.header').on('affix-top.bs.affix', function() {

        $('.project-single').removeClass('affix');

    });

    function fullScreenBreadcrumb() {

        $('.breadcrumb-fullscreen-parent').on('affix-top.bs.affix', function() {

            $('.before-affix-breadcrumb').css('height', 0);

            if (navigator.userAgent.indexOf('Safari') != -1 && navigator.userAgent.indexOf('Chrome') == -1) {

                $(this).css('bottom', 0);

            }
            ;

        });

        $('.breadcrumb-fullscreen-parent').on('affix.bs.affix', function() {

            $('.before-affix-breadcrumb').css('height', breadcrumbH);

            if (navigator.userAgent.indexOf('Safari') != -1 && navigator.userAgent.indexOf('Chrome') == -1) {

                $(this).css('bottom', wH - 69);

            }
            ;

        });

    }
    ;
    function splitEqual() {

        $('.split-equal').each(function() {

            var bigImageH = $(this).find('.big-image').outerHeight();

            $('.padding-content > div').css('height', bigImageH - 160);

        });

    }
    ;
    fullScreenBreadcrumb();

    $(window).resize(function() {

        fullScreenBreadcrumb();

        splitEqual();

    });

});

// <!-- ================================================== -->
// <!-- =============== END BREACRUMB OPTIONS ================ -->
// <!-- ================================================== -->

// <!-- ================================================== -->

$(document).ready(function() {

    // FitVides Option
    $("html").fitVids({
        customSelector: "iframe"
    });

    //Page Loader

    $('.page-loader').delay(800).fadeOut('slow');

    /***********************************************************************************************/
    /* MENU */
    /***********************************************************************************************/
    $('.open-menu').on('click', function() {

        $(this).toggleClass('active');

        $('.menu-fixed-container').toggleClass('open');

    });

    $('.x-filter').on('click', function() {

        $('.open-menu').toggleClass('active');

        $('.menu-fixed-container').toggleClass('open');

    });

    $('.menu-fixed-container > nav > ul > li > a').on('click', function() {

        $(this).parent().siblings().toggleClass('no-hovered');
        $(this).parent().toggleClass('click');
        $(this).parent().siblings().removeClass('click');
    });

    /***********************************************************************************************/
    /* END MENU */
    /***********************************************************************************************/

    $(window).load(function() {
        $(window).scroll(function() {

            if ($(document).scrollTop() > 300) {
                $('.goTop').css({
                    bottom: "50px"
                });
            } else {
                $('.goTop').css({
                    bottom: "-80px"
                });
            }
        });
        $('#overlay').fadeOut();
    });

    $('.goTop').on("click", function() {
        $('html, body').animate({
            scrollTop: 0
        }, 'slow');
        return false;
    });
    /***********************************************************************************************/
    /* INSTAGRAM */
    /***********************************************************************************************/
    var token = '5465599682.6239321.6079c459536f4db1bdb0c9eed2628135',
        userid = 5465599682,
        num_photos = 1; 
     
    $.ajax({
    	url: 'https://api.instagram.com/v1/users/' + userid + '/media/recent', // or /users/self/media/recent for Sandbox
    	dataType: 'jsonp',
    	type: 'GET',
    	data: {access_token: token, count: num_photos},
    	success: function(data){
     		console.log(data);
    		for( x in data.data ){
                // $('.instaPost').append('<img class="instaPhoto" src="'+data.data[x].images.low_resolution.url+'">');
    			$('.instaPost').append('<img class="instaPhoto" style="background-image: url('+data.data[x].images.standard_resolution.url+');">');
    			// data.data[x].images.low_resolution.url - URL of image, 306х306
    			// data.data[x].images.thumbnail.url - URL of image 150х150
    			// data.data[x].images.standard_resolution.url - URL of image 612х612
    			// data.data[x].link - Instagram post URL 
    		}
    	},
    	error: function(data){
    		console.log(data);
    	}
    });
    /***********************************************************************************************/
    /* END INSTAGRAM */
    /***********************************************************************************************/

    /***********************************************************************************************/
    /* JPLAYER */
    /***********************************************************************************************/
    $('.trak-item audio').each(function() {

        var seconds = $(this)[0].duration;
        var duration = moment.duration(seconds, "seconds");

        var time = "";
        var hours = duration.hours();
        if (hours > 0) {
            time = hours + ":";
        }

        time = time + duration.minutes() + ":" + duration.seconds();
        $(this).parent().find('.trak-duration').text(time);
    });

    $('.jplayerButton').on('click', function() {

        $(this).toggleClass('active');

        $('.playlist-wrapper').fadeToggle('open');

        $('body').toggleClass('opacityPlaylist');

    });
    
    $('.right-player-side').on('click', function() {

        $('.right-player-side').addClass('open');
        $('#search').addClass('show');
        $('.mesh-thumbnail').addClass('hide');
        $('.mesh-title').addClass('hide');
        $('.mesh-artist').addClass('hide');
        $(".topHeader,.no-mb, .mesh-main-player, .playlist-wrapper").on("click", function(e){
            if ($(e.target).closest(".right-player-side.open").length == 0) {
                $('.right-player-side').removeClass('open');
                $('#search').removeClass('show');
                $('.mesh-thumbnail').removeClass('hide');
                $('.mesh-title').removeClass('hide');
                $('.mesh-artist').removeClass('hide');
            }
        });
    });

    /***********************************************************************************************/
    /* END JPLAYER */
    /***********************************************************************************************/ 
    /***********************************************************************************************/
    /* SEARCH TRACK */
    /***********************************************************************************************/
    
    // YOUTUBE-----
    $(".utube-search").on('click', function() {
        cache: false;
        var name = $('.mesh-listen').text();
        var image = $('#track-image img').attr('src');

        if(name!='Misto FM') {
                            
        }

        name = encodeURIComponent(name);
        image = encodeURIComponent(image);
        if (image === 'undefined') { image = 'http://deep-vovax.c9users.io/img/misto_logo.png'; }

        var ttt = "https://www.youtube.com/results?search_query=";  
        var link_text = ttt+name;
        
        window.open(link_text,'_blank')

    });
    
    // SOUNDCLOUD-----
    $(".soundcloud-search").on('click', function() {
        cache: false;
        var name = $('.mesh-listen').text();

        name = encodeURIComponent(name);

        var ttt = "https://soundcloud.com/search/sounds?q=";
        var link_text = ttt+name;
        
        window.open(link_text,'_blank')

    });
    
    // VK-----
    $(".vk-search").on('click', function() {
        cache: false;
        var name = $('#track marquee').text();

        name = encodeURIComponent(name);

        var ttt = "http://vk.com/audio?q=";  
        var link_text = ttt+name;
        
        window.open(link_text,'_blank')

    });
    /***********************************************************************************************/
    /* END SEARCH TRACK */
    /***********************************************************************************************/
    
    
});

// <!-- ================================================== -->
