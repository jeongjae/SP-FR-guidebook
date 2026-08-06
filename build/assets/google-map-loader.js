(function (global) {
  "use strict";

  var promise;

  function meta(name) {
    var node = document.querySelector('meta[name="' + name + '"]');
    return node ? node.content.trim() : "";
  }

  function load() {
    if (global.google && global.google.maps && global.google.maps.Map) {
      return Promise.resolve(global.google.maps);
    }
    if (promise) return promise;

    promise = new Promise(function (resolve, reject) {
      var key = meta("google-maps-api-key");
      if (!key) {
        reject(new Error("Google Maps API key is not configured"));
        return;
      }

      var callback = "__spfrGoogleMapsReady";
      var timeout = global.setTimeout(function () {
        cleanup();
        reject(new Error("Google Maps API load timed out"));
      }, 12000);

      function cleanup() {
        global.clearTimeout(timeout);
        try { delete global[callback]; } catch (_error) { global[callback] = undefined; }
      }

      global[callback] = function () {
        cleanup();
        if (global.google && global.google.maps) resolve(global.google.maps);
        else reject(new Error("Google Maps API loaded without maps namespace"));
      };

      var params = new URLSearchParams({
        key: key,
        callback: callback,
        loading: "async",
        libraries: "marker",
        v: "weekly"
      });
      var script = document.createElement("script");
      script.src = "https://maps.googleapis.com/maps/api/js?" + params.toString();
      script.async = true;
      script.onerror = function () {
        cleanup();
        reject(new Error("Google Maps API request failed"));
      };
      document.head.appendChild(script);
    });
    return promise;
  }

  global.SPFRGoogleMapsLoader = {
    load: load,
    mapId: function () { return meta("google-maps-map-id") || "DEMO_MAP_ID"; }
  };
}(window));
