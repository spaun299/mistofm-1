
// ------ Google Map -------


!function(a) {
    "use strict";
    var t = {
        cntClass: "map",
        mapClass: "map_model",
        locationsClass: "map_locations",
        marker: {
            basic: "img/gmap_marker.png",
            active: "img/gmap_marker_active.png"
        },
        styles: [],
        onInit: !1
    }
      , o = {
        map: {
            x: -73.9924068,
            y: 40.646197,
            zoom: 14
        },
        locations: []
    }
      , n = function(t, o) {
        var n = t.parent().find("." + o.locationsClass).find("li")
          , e = [];
        return n.length > 0 && n.each(function(t) {
            var n = a(this);
            n.data("x") && n.data("y") && (e[t] = {
                x: n.data("x"),
                y: n.data("y"),
                basic: n.data("basic") ? n.data("basic") : o.marker.basic,
                active: n.data("active") ? n.data("active") : o.marker.active
            },
            a.trim(n.html()) ? e[t].content = '<div class="iw-content">' + n.html() + "</div>" : e[t].content = !1)
        }),
        e
    };
    a.fn.googleMap = function(e) {
        e = a.extend(!0, {}, t, e),
        a(this).each(function() {
            var t = a(this)
              , s = a.extend(!0, {}, o, {
                map: {
                    x: t.data("x"),
                    y: t.data("y"),
                    zoom: t.data("zoom")
                },
                locations: n(t, e)
            })
              , i = new google.maps.Map(this,{
                center: new google.maps.LatLng(parseFloat(s.map.y),parseFloat(s.map.x)),
                styles: e.styles,
                zoom: s.map.zoom,
                scrollwheel: !1
            });
            e.onInit && e.onInit.call(this, i);
            var c = new google.maps.InfoWindow
              , l = [];
            for (var r in s.locations)
                l[r] = new google.maps.Marker({
                    position: new google.maps.LatLng(parseFloat(s.locations[r].y),parseFloat(s.locations[r].x)),
                    map: i,
                    icon: s.locations[r].basic,
                    index: r
                }),
                s.locations[r].content && (google.maps.event.addListener(l[r], "click", function() {
                    for (var t in l)
                        l[t].setIcon(s.locations[t].basic);
                    c.setContent(s.locations[this.index].content),
                    c.open(i, this),
                    a(".gm-style-iw").parent().parent().addClass("gm-wrapper"),
                    this.setIcon(s.locations[this.index].active)
                }),
                google.maps.event.addListener(c, "closeclick", function() {
                    for (var a in l)
                        l[a].setIcon(s.locations[a].basic)
                }));
            google.maps.event.addDomListener(window, "resize", function() {
                i.setCenter(new google.maps.LatLng(parseFloat(s.map.y),parseFloat(s.map.x)))
            })
        })
    }
}(jQuery);

