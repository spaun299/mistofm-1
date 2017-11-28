
$(document).ready(function() {
    "use strict";

    $('.page-loader').delay(2300).fadeOut('slow');
    
    $(".back-to-top").on('click', '#top-svg', function(e) {
		e.preventDefault();
    	$('html, body').animate({ scrollTop: 0 }, 'slow');
    	return false;
    });

    if (addEventListener("scroll", function() {
        mr_scrollTop = window.pageYOffset
    }, !1),
    
    $(".background-image-holder").each(function() {
        var a = $(this).children("img").attr("src");
        // var a = im;
        $(this).css("background", 'url("' + a + '")'),
        $(this).children("img").hide(),
        $(this).css("background-position", "initial")
    }),
    setTimeout(function() {
        $(".background-image-holder").each(function() {
            $(this).addClass("fadeIn")
        })
    }, 200),

    $("nav").hasClass("fixed") || $("nav").hasClass("absolute") ? $("body").addClass("nav-is-overlay") : ($(".nav-container").css("min-height", $("nav").outerHeight(!0)),
    $(window).resize(function() {
        $(".nav-container").css("min-height", $("nav").outerHeight(!0))
    }),
    $(window).width() > 768 && $(".background-image-holder").css("top", -$("nav").outerHeight(!0)),
    $(window).width() > 768 && $("section.fullscreen:nth-of-type(1)").css("height", $(window).height() - $("nav").outerHeight(!0))),
    $("nav").hasClass("bg-dark") && $(".nav-container").addClass("bg-dark"),
    mr_nav = $("body .nav-container nav:first"),
    mr_navOuterHeight = $("body .nav-container nav:first").outerHeight(),
    mr_fixedAt = "undefined" != typeof mr_nav.attr("data-fixed-at") ? parseInt(mr_nav.attr("data-fixed-at").replace("px", "")) : parseInt($("section:nth-of-type(1)").outerHeight()),
    window.addEventListener("scroll", updateNav, !1),

    $(".mobile-toggle").click(function() {
        $(".nav-bar").toggleClass("nav-open"),
        $(this).toggleClass("active")
    }),
    $(".menu li").click(function(a) {
        a || (a = window.event),
        a.stopPropagation(),
        $(this).find("ul").length ? $(this).toggleClass("toggle-sub") : $(this).parents(".toggle-sub").removeClass("toggle-sub")
    }),
    $(".menu li a").click(function() {
        $(this).hasClass("inner-link") && $(this).closest(".nav-bar").removeClass("nav-open")
    }),
    $(".module.widget-handle").click(function() {
        $(this).toggleClass("toggle-widget-handle")
    }),
    $(".offscreen-toggle").length ? $("body").addClass("has-offscreen-nav") : $("body").removeClass("has-offscreen-nav"),
    $(".offscreen-toggle").click(function() {
        $(".main-container").toggleClass("reveal-nav"),
        $("nav").toggleClass("reveal-nav"),
        $(".offscreen-container").toggleClass("reveal-nav")
    }),
    $(".main-container").click(function() {
        $(this).hasClass("reveal-nav") && ($(this).removeClass("reveal-nav"),
        $(".offscreen-container").removeClass("reveal-nav"),
        $("nav").removeClass("reveal-nav"))
    }),
    $(".offscreen-container a").click(function() {
        $(".offscreen-container").removeClass("reveal-nav"),
        $(".main-container").removeClass("reveal-nav"),
        $("nav").removeClass("reveal-nav")
    }),
    
    $(".instafeed").length && (jQuery.fn.spectragram.accessData = {
        accessToken: "5465599682.6239321.6079c459536f4db1bdb0c9eed2628135",
        clientID: "5465599682"
    },
    $(".instafeed").each(function() {
        var a = $(this).attr("data-user-name");
        $(this).children("ul").spectragram("getUserFeed", {
            query: a,
            max: 3
        })
    })),
    
    $(".slider-arrow-controls").length && ($(".slider-all-controls").flexslider({
        start: function(a) {
            a.find(".slides li:first-child").length && a.find(".slides li:first-child").get(0).play()
        },
        after: function(a) {
            (a.find("li:not(.flex-active-slide)").length && a.find("li:not(.flex-active-slide)").get(0).pause(),
            a.find(".flex-active-slide").length && a.find(".flex-active-slide").get(0).play())
        }
    }),

    $(".slider-arrow-controls").flexslider({
        controlNav: !1
    }),
    $(".slider-thumb-controls .slides li").each(function() {
        var a = $(this).find("img").attr("src");
        $(this).attr("data-thumb", a)
    }),
    $(".slider-thumb-controls").flexslider({
        animation: "slide",
        controlNav: "thumbnails",
        directionNav: !0
    })),
    $(".countdown").length && $(".countdown").each(function() {
        var a = $(this).attr("data-date");
        $(this).countdown(a, function(a) {
            $(this).text(a.strftime("%D days %H:%M:%S"))
        })
    }));
});

var mr_nav, mr_fixedAt, mr_navOuterHeight, mr_navScrolled = !1, mr_navFixed = !1, mr_outOfSight = !1, mr_scrollTop = 0;

function getCurrentTimeInSeconds(){
    return new Date().getTime() / 1000;
}
function updateNav() {
    var a = mr_scrollTop;
    if (0 >= a)
        return mr_navFixed && (mr_navFixed = !1,
        mr_nav.removeClass("fixed")),
        mr_outOfSight && (mr_outOfSight = !1,
        mr_nav.removeClass("outOfSight")),
        void (mr_navScrolled && (mr_navScrolled = !1,
        mr_nav.removeClass("scrolled")));
    if (a > mr_navOuterHeight + mr_fixedAt) {
        if (!mr_navScrolled)
            return mr_nav.addClass("scrolled"),
            void (mr_navScrolled = !0)
    } else
        a > mr_navOuterHeight ? (mr_navFixed || (mr_nav.addClass("fixed"),
        mr_navFixed = !0),
        a > mr_navOuterHeight + 10 ? mr_outOfSight || (mr_nav.addClass("outOfSight"),
        mr_outOfSight = !0) : mr_outOfSight && (mr_outOfSight = !1,
        mr_nav.removeClass("outOfSight"))) : (mr_navFixed && (mr_navFixed = !1,
        mr_nav.removeClass("fixed")),
        mr_outOfSight && (mr_outOfSight = !1,
        mr_nav.removeClass("outOfSight"))),
        mr_navScrolled && (mr_navScrolled = !1,
        mr_nav.removeClass("scrolled"))
}

$(document).ready(function() {
    if (document.querySelector("[data-maps-api-key]") && !document.querySelector(".gMapsAPI") && $("[data-maps-api-key]").length) {
        var f = document.createElement("script")
          , g = $("[data-maps-api-key]:first").attr("data-maps-api-key");
        f.type = "text/javascript",
        f.src = "https://maps.googleapis.com/maps/api/js?key=" + g + "&callback=initializeMaps",
        f.className = "gMapsAPI",
        document.body.appendChild(f)
    }
});

window.initializeMaps = function() {
    "undefined" != typeof google && "undefined" != typeof google.maps && $(".map-canvas[data-maps-api-key]").each(function() {
        var a, b, c, d = this, e = "undefined" != typeof $(this).attr("data-map-style") ? $(this).attr("data-map-style") : !1, f = JSON.parse(e) || [{
            featureType: "landscape",
            stylers: [{
                saturation: -100
            }, {
                lightness: 65
            }, {
                visibility: "on"
            }]
        }, {
            featureType: "poi",
            stylers: [{
                saturation: -100
            }, {
                lightness: 51
            }, {
                visibility: "simplified"
            }]
        }, {
            featureType: "road.highway",
            stylers: [{
                saturation: -100
            }, {
                visibility: "simplified"
            }]
        }, {
            featureType: "road.arterial",
            stylers: [{
                saturation: -100
            }, {
                lightness: 30
            }, {
                visibility: "on"
            }]
        }, {
            featureType: "road.local",
            stylers: [{
                saturation: -100
            }, {
                lightness: 40
            }, {
                visibility: "on"
            }]
        }, {
            featureType: "transit",
            stylers: [{
                saturation: -100
            }, {
                visibility: "simplified"
            }]
        }, {
            featureType: "administrative.province",
            stylers: [{
                visibility: "off"
            }]
        }, {
            featureType: "water",
            elementType: "labels",
            stylers: [{
                visibility: "on"
            }, {
                lightness: -25
            }, {
                saturation: -100
            }]
        }, {
            featureType: "water",
            elementType: "geometry",
            stylers: [{
                hue: "#ffff00"
            }, {
                lightness: -25
            }, {
                saturation: -97
            }]
        }], g = "undefined" != typeof $(this).attr("data-map-zoom") && "" !== $(this).attr("data-map-zoom") ? 1 * $(this).attr("data-map-zoom") : 17, h = "undefined" != typeof $(this).attr("data-latlong") ? $(this).attr("data-latlong") : !1, i = h ? 1 * h.substr(0, h.indexOf(",")) : !1, j = h ? 1 * h.substr(h.indexOf(",") + 1) : !1, k = new google.maps.Geocoder, l = "undefined" != typeof $(this).attr("data-address") ? $(this).attr("data-address").split(";") : [""], m = "We Are Here", n = $(document).width() > 766 ? !0 : !1, o = {
            draggable: n,
            scrollwheel: !1,
            zoom: g,
            disableDefaultUI: !0,
            styles: f
        };
        void 0 != $(this).attr("data-marker-title") && "" != $(this).attr("data-marker-title") && (m = $(this).attr("data-marker-title")),
        void 0 != l && "" != l[0] ? k.geocode({
            address: l[0].replace("[nomarker]", "")
        }, function(a, b) {
            if (b == google.maps.GeocoderStatus.OK) {
                var e = new google.maps.Map(d,o);
                e.setCenter(a[0].geometry.location),
                l.forEach(function(a) {
                    var b;
                    if (c = {
                        url: void 0 == window.mr_variant ? "img/gmap_marker.png" : "../img/gmap_marker.png",
                        size: new google.maps.Size(50,50),
                        scaledSize: new google.maps.Size(50,50)
                    },
                    /(\-?\d+(\.\d+)?),\s*(\-?\d+(\.\d+)?)/.test(a))
                        var d = a.split(",")
                          , f = new google.maps.Marker({
                            position: {
                                lat: 1 * d[0],
                                lng: 1 * d[1]
                            },
                            map: e,
                            icon: c,
                            title: m,
                            optimised: !1
                        });
                    else
                        a.indexOf("[nomarker]") < 0 && (b = new google.maps.Geocoder,
                        b.geocode({
                            address: a.replace("[nomarker]", "")
                        }, function(a, b) {
                            b == google.maps.GeocoderStatus.OK && (f = new google.maps.Marker({
                                map: e,
                                icon: c,
                                title: m,
                                position: a[0].geometry.location,
                                optimised: !1
                            }))
                        }))
                })
            }
        }) : void 0 != i && "" != i && 0 != i && void 0 != j && "" != j && 0 != j && (o.center = {
            lat: i,
            lng: j
        },
        a = new google.maps.Map(d,o),
        b = new google.maps.Marker({
            position: {
                lat: i,
                lng: j
            },
            map: a,
            icon: c,
            title: m
        }))
    })
},
initializeMaps();

