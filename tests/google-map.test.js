"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const maps = require("../build/assets/google-map.js");

const publicPlace = {
  id: "sagrada-familia", name: "Sagrada Família", lat: 41.40363, lng: 2.17436,
  googlePlaceId: "ChIJ-test", googleMapsUrl: "", private: false,
  optional: false, type: "attraction"
};

test("place URL encodes query and Place ID", () => {
  const url = new URL(maps.buildPlaceUrl(publicPlace));
  assert.equal(url.origin, "https://www.google.com");
  assert.equal(url.searchParams.get("query"), "Sagrada Família");
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
  assert.equal(url.searchParams.get("destination"), "Sagrada Família");
  assert.equal(url.searchParams.get("travelmode"), "walking");
});

test("driving route selects public non-optional parking nodes only", () => {
  const places = {
    stay: { id: "stay", name: "Private", private: true, optional: false, type: "accommodation" },
    a: { id: "a", name: "Lot A", private: false, optional: false, type: "parking" },
    sight: { id: "sight", name: "Sight", private: false, optional: false, type: "attraction" },
    b: { id: "b", name: "Lot B", private: false, optional: false, type: "parking" },
    optional: { id: "optional", name: "Optional lot", private: false, optional: true, type: "parking" }
  };
  const day = {
    defaultMode: "driving",
    stops: ["stay", "a", "sight", "optional", "b"].map((placeId, order) => ({ placeId, order }))
  };
  assert.deepEqual(maps.selectRoutePlaces(day, places, false).map((place) => place.id), ["a", "b"]);
  const route = new URL(maps.buildMultiStopRouteUrl(day, places, false));
  assert.equal(route.searchParams.get("origin"), "Lot A");
  assert.equal(route.searchParams.get("destination"), "Lot B");
  assert.equal(route.searchParams.get("travelmode"), "driving");
});

test("walking multi-stop route preserves non-optional order", () => {
  const places = {
    a: { id: "a", name: "A", private: false, optional: false, type: "attraction" },
    b: { id: "b", name: "B & B", private: false, optional: false, type: "attraction" },
    c: { id: "c", name: "C", private: false, optional: false, type: "attraction" }
  };
  const day = { defaultMode: "walking", stops: ["a", "b", "c"].map((placeId, order) => ({ placeId, order })) };
  const route = new URL(maps.buildMultiStopRouteUrl(day, places, false));
  assert.equal(route.searchParams.get("waypoints"), "B & B");
});
