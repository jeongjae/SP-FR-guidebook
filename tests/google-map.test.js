"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const maps = require("../build/assets/google-map.js");

const publicPlace = {
  id: "sagrada-familia", name: "Sagrada Família", lat: 41.40363, lng: 2.17436,
  googlePlaceId: "ChIJ-test", googleMapsUrl: "", private: false,
  optional: false, type: "attraction"
};

test("place URL falls back to coordinates and keeps Place ID", () => {
  const url = new URL(maps.buildPlaceUrl(publicPlace));
  assert.equal(url.origin, "https://www.google.com");
  assert.equal(url.searchParams.get("query"), "41.40363,2.17436");
  assert.equal(url.searchParams.get("query_place_id"), "ChIJ-test");
});

test("private places never receive public place or destination URLs", () => {
  const privatePlace = { ...publicPlace, id: "stay", private: true, googlePlaceId: "", googleMapsUrl: "" };
  assert.equal(maps.buildPlaceUrl(privatePlace), null);
  assert.equal(maps.buildDirectionsUrl(publicPlace, privatePlace, "driving"), null);
});

test("a private origin becomes current location", () => {
  const privateOrigin = { ...publicPlace, id: "stay", private: true };
  const url = new URL(maps.buildDirectionsUrl(privateOrigin, publicPlace, "walking"));
  assert.equal(url.searchParams.has("origin"), false);
  assert.equal(url.searchParams.get("destination"), "41.40363,2.17436");
  assert.equal(url.searchParams.get("travelmode"), "walking");
});

test("driving route selects public non-optional parking nodes only", () => {
  const places = {
    stay: { id: "stay", name: "Private", lat: 42.164, lng: 2.914, private: true, optional: false, type: "accommodation" },
    a: { id: "a", name: "Lot A", lat: 41.7226, lng: 2.9309, private: false, optional: false, type: "parking" },
    sight: { id: "sight", name: "Sight", lat: 41.7195, lng: 2.9319, private: false, optional: false, type: "attraction" },
    b: { id: "b", name: "Lot B", lat: 41.9701, lng: 3.1526, private: false, optional: false, type: "parking" },
    optional: { id: "optional", name: "Optional lot", lat: 41.9704, lng: 3.1484, private: false, optional: true, type: "parking" }
  };
  const day = {
    defaultMode: "driving",
    stops: ["stay", "a", "sight", "optional", "b"].map((placeId, order) => ({ placeId, order }))
  };
  assert.deepEqual(maps.selectRoutePlaces(day, places, false).map((place) => place.id), ["a", "b"]);
  const route = new URL(maps.buildMultiStopRouteUrl(day, places, false));
  assert.equal(route.searchParams.get("origin"), "41.7226,2.9309");
  assert.equal(route.searchParams.get("destination"), "41.9701,3.1526");
  assert.equal(route.searchParams.get("travelmode"), "driving");
});

test("walking multi-stop route preserves non-optional order", () => {
  const places = {
    a: { id: "a", name: "A", lat: 41.1, lng: 2.1, private: false, optional: false, type: "attraction" },
    b: { id: "b", name: "B & B", lat: 41.2, lng: 2.2, private: false, optional: false, type: "attraction" },
    c: { id: "c", name: "C", lat: 41.3, lng: 2.3, private: false, optional: false, type: "attraction" }
  };
  const day = { defaultMode: "walking", stops: ["a", "b", "c"].map((placeId, order) => ({ placeId, order })) };
  const route = new URL(maps.buildMultiStopRouteUrl(day, places, false));
  assert.equal(route.searchParams.get("waypoints"), "41.2,2.2");
});
