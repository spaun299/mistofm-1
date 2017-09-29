
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

var mr_firstSectionHeight, mr_nav, mr_fixedAt, mr_navOuterHeight, mr_navScrolled = !1, mr_navFixed = !1, mr_outOfSight = !1, mr_floatingProjectSections, mr_scrollTop = 0;

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

