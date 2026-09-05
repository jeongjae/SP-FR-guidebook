"""Tests for Paris Museum Reservation interactive execution state and UI."""
import json
import unittest
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"


class ParisMuseumReservationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (SITE / "prepare" / "paris-museums.html").exists():
            import site as build_site
            build_site.main()

    def test_paris_museum_default_status_uses_canonical(self):
        """Default state includes the two user-confirmed museum bookings."""
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto((SITE / "prepare" / "paris-museums.html").as_uri())

            # Clear any leftover localStorage
            page.evaluate("() => localStorage.removeItem('spfr_paris_museum_booking_state')")
            page.evaluate("() => window.__renderParisMuseumUI && window.__renderParisMuseumUI()")

            cards = page.query_selector_all(".paris-museum-card")
            self.assertEqual(15, len(cards))

            count_book_now = page.query_selector("#count-book-now").inner_text()
            count_check_sale = page.query_selector("#count-check-sale").inner_text()
            count_book_later = page.query_selector("#count-book-later").inner_text()
            count_recheck = page.query_selector("#count-recheck").inner_text()
            count_booked = page.query_selector("#count-booked").inner_text()
            count_no_res = page.query_selector("#count-no-reservation").inner_text()

            self.assertEqual("6", count_book_now)
            self.assertEqual("1", count_check_sale)
            self.assertEqual("5", count_book_later)
            self.assertEqual("0", count_recheck)
            self.assertEqual("2", count_booked)
            self.assertEqual("1", count_no_res)

            browser.close()

    def test_paris_museum_mark_booked(self):
        """Scenario A: Click [✓ 예약 완료] on Louvre -> BOOKED, counts update, persists reload."""
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto((SITE / "prepare" / "paris-museums.html").as_uri())

            page.evaluate("() => localStorage.removeItem('spfr_paris_museum_booking_state')")
            page.evaluate("() => window.__renderParisMuseumUI && window.__renderParisMuseumUI()")

            louvre_card = page.query_selector('.paris-museum-card[data-museum-id="musee-du-louvre|2026-10-02|14:00"]')
            self.assertIsNotNone(louvre_card)
            self.assertEqual("book-now", louvre_card.get_attribute("data-effective-status"))

            # Click book
            book_btn = louvre_card.query_selector('.btn-museum-book-toggle')
            book_btn.click()

            # Effective status is now booked
            self.assertEqual("booked", louvre_card.get_attribute("data-effective-status"))
            self.assertIn("is-booked", louvre_card.get_attribute("class"))
            self.assertIn("✓ 예약 완료", louvre_card.query_selector(".status-badge-container").inner_text())

            # Counts update
            self.assertEqual("5", page.query_selector("#count-book-now").inner_text())
            self.assertEqual("3", page.query_selector("#count-booked").inner_text())

            # Reload persists
            page.reload()
            louvre_card_reload = page.query_selector('.paris-museum-card[data-museum-id="musee-du-louvre|2026-10-02|14:00"]')
            self.assertEqual("booked", louvre_card_reload.get_attribute("data-effective-status"))
            self.assertEqual("5", page.query_selector("#count-book-now").inner_text())
            self.assertEqual("3", page.query_selector("#count-booked").inner_text())

            browser.close()

    def test_paris_museum_unbook_restores_status(self):
        """Scenario B: Unbooking restores canonical status and counts."""
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto((SITE / "prepare" / "paris-museums.html").as_uri())

            # Seed booked state for Versailles
            page.evaluate("""() => {
                localStorage.setItem('spfr_paris_museum_booking_state', JSON.stringify({
                    'versailles|2026-10-01|morning': 'booked'
                }));
            }""")
            page.reload()

            v_card = page.query_selector('.paris-museum-card[data-museum-id="versailles|2026-10-01|morning"]')
            self.assertEqual("booked", v_card.get_attribute("data-effective-status"))
            self.assertEqual("3", page.query_selector("#count-booked").inner_text())

            # Click unbook
            unbook_btn = v_card.query_selector('.btn-museum-book-toggle')
            self.assertEqual("완료 취소", unbook_btn.inner_text())
            unbook_btn.click()

            # Status restored to book-now
            self.assertEqual("book-now", v_card.get_attribute("data-effective-status"))
            self.assertNotIn("is-booked", v_card.get_attribute("class"))
            self.assertEqual("6", page.query_selector("#count-book-now").inner_text())
            self.assertEqual("2", page.query_selector("#count-booked").inner_text())

            browser.close()

    def test_paris_museum_recheck_state(self):
        """Scenario C: Marking recheck sets state to recheck, updates counts, persists reload."""
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto((SITE / "prepare" / "paris-museums.html").as_uri())

            page.evaluate("() => localStorage.removeItem('spfr_paris_museum_booking_state')")
            page.evaluate("() => window.__renderParisMuseumUI && window.__renderParisMuseumUI()")

            luxembourg_card = page.query_selector('.paris-museum-card[data-museum-id="musee-du-luxembourg|2026-09-26|special"]')
            recheck_btn = luxembourg_card.query_selector('.btn-museum-recheck-toggle')
            self.assertEqual("재확인", recheck_btn.inner_text())
            recheck_btn.click()

            self.assertEqual("recheck", luxembourg_card.get_attribute("data-effective-status"))
            self.assertIn("is-recheck", luxembourg_card.get_attribute("class"))
            self.assertEqual("1", page.query_selector("#count-recheck").inner_text())
            self.assertEqual("5", page.query_selector("#count-book-now").inner_text())

            page.reload()
            luxembourg_card_reload = page.query_selector('.paris-museum-card[data-museum-id="musee-du-luxembourg|2026-09-26|special"]')
            self.assertEqual("recheck", luxembourg_card_reload.get_attribute("data-effective-status"))

            browser.close()

    def test_paris_museum_duplicate_visit_state_independent(self):
        """Scenario D: Orsay 9/29 and Orsay 10/6 have independent local states."""
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto((SITE / "prepare" / "paris-museums.html").as_uri())

            page.evaluate("() => localStorage.removeItem('spfr_paris_museum_booking_state')")
            page.evaluate("() => window.__renderParisMuseumUI && window.__renderParisMuseumUI()")

            orsay_perm = page.query_selector('.paris-museum-card[data-museum-id="musee-d-orsay|2026-09-29|09:30"]')
            orsay_spec = page.query_selector('.paris-museum-card[data-museum-id="musee-d-orsay|2026-10-06|special"]')

            self.assertIsNotNone(orsay_perm)
            self.assertIsNotNone(orsay_spec)

            # Book Orsay 9/29 only
            orsay_perm.query_selector('.btn-museum-book-toggle').click()

            self.assertEqual("booked", orsay_perm.get_attribute("data-effective-status"))
            self.assertEqual("book-now", orsay_spec.get_attribute("data-effective-status"))

            browser.close()

    def test_paris_museum_clear_local_state(self):
        """Verify that reset button clears localStorage and restores canonical counts."""
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto((SITE / "prepare" / "paris-museums.html").as_uri())

            # Seed state with multiple booked/recheck items
            page.evaluate("""() => {
                localStorage.setItem('spfr_paris_museum_booking_state', JSON.stringify({
                    'versailles|2026-10-01|morning': 'booked',
                    'musee-du-louvre|2026-10-02|14:00': 'booked',
                    'grand-palais|2026-09-25|special': 'recheck'
                }));
            }""")
            page.reload()

            self.assertEqual("3", page.query_selector("#count-booked").inner_text())
            self.assertEqual("1", page.query_selector("#count-recheck").inner_text())

            # Auto-accept confirm dialog and click reset
            page.on("dialog", lambda dialog: dialog.accept())
            page.query_selector("#btn-reset-museum-state").click()

            self.assertEqual("2", page.query_selector("#count-booked").inner_text())
            self.assertEqual("0", page.query_selector("#count-recheck").inner_text())
            self.assertEqual("6", page.query_selector("#count-book-now").inner_text())

            browser.close()

    def test_paris_museum_filter_chips(self):
        """Verify that filter chips filter visible cards."""
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto((SITE / "prepare" / "paris-museums.html").as_uri())

            page.evaluate("() => localStorage.removeItem('spfr_paris_museum_booking_state')")
            page.evaluate("() => window.__renderParisMuseumUI && window.__renderParisMuseumUI()")

            # Click BOOK NOW filter
            page.query_selector('.paris-filter-chip[data-filter="book-now"]').click()
            visible_cards = [c for c in page.query_selector_all(".paris-museum-card") if c.is_visible()]
            self.assertEqual(6, len(visible_cards))

            # Click CHECK SALE filter
            page.query_selector('.paris-filter-chip[data-filter="check-sale"]').click()
            visible_cards = [c for c in page.query_selector_all(".paris-museum-card") if c.is_visible()]
            self.assertEqual(1, len(visible_cards))

            # Click all filter
            page.query_selector('.paris-filter-chip[data-filter="all"]').click()
            visible_cards = [c for c in page.query_selector_all(".paris-museum-card") if c.is_visible()]
            self.assertEqual(15, len(visible_cards))

            browser.close()

    def test_paris_museum_mobile_touch_targets_and_overflow(self):
        """Verify 360, 390, 430 viewports have 0 overflow and >=44px touch targets."""
        viewports = [
            {"width": 360, "height": 740},
            {"width": 390, "height": 844},
            {"width": 430, "height": 932},
        ]
        with sync_playwright() as p:
            browser = p.chromium.launch()
            for vp in viewports:
                page = browser.new_page(viewport=vp)
                page.goto((SITE / "prepare" / "paris-museums.html").as_uri())

                scroll_w = page.evaluate("() => document.documentElement.scrollWidth")
                client_w = page.evaluate("() => document.documentElement.clientWidth")
                self.assertLessEqual(scroll_w, client_w, f"Horizontal overflow at {vp['width']}x{vp['height']}")

                # Check visible action buttons on an unbooked card. Confirmed cards
                # intentionally hide their recheck action.
                card = page.query_selector(
                    '.paris-museum-card[data-museum-id="musee-du-luxembourg|2026-09-26|special"]'
                )
                btns = [btn for btn in card.query_selector_all(".btn") if btn.is_visible()]
                self.assertTrue(btns)
                for btn in btns:
                    box = btn.bounding_box()
                    self.assertIsNotNone(box)
                    self.assertGreaterEqual(box["height"], 40.0, f"Button height {box['height']} too small at {vp}")
                page.close()
            browser.close()


if __name__ == "__main__":
    unittest.main()
